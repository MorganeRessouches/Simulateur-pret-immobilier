import plotly.graph_objects as go
import pandas as pd
from math import log, ceil
import streamlit as st

# --- Fonctions Utilitaires ---

def formater_nombre(nombre: float) -> str:
    """Formate un nombre en chaîne de caractères avec un espace comme séparateur de milliers."""
    return f"{nombre:,.0f} €".replace(",", " ")

def formater_duree(nombre_mois: float) -> str:
    """Convertit un nombre de mois en une chaîne de caractères "X an(s) et Y mois"."""
    nombre_mois = int(nombre_mois)
    
    if nombre_mois < 1:
        return "moins d'un mois"

    annees = nombre_mois // 12
    mois_restants = nombre_mois % 12
    
    parts = []
    if annees > 0:
        s_an = "s" if annees > 1 else ""
        parts.append(f"{annees} an{s_an}")
    
    if mois_restants > 0:
        parts.append(f"{mois_restants} mois")
        
    return " et ".join(parts)

# --- Fonctions de Calcul Financier ---

def calculer_details_pret(montant_emprunte: float, taux_annuel_nominal_pct: float, duree_annees: int, taux_annuel_assurance_pct: float) -> dict:
    """
    Calcule les détails d'un prêt immobilier pour une durée et un taux donnés.

    Args:
        montant_emprunte (float): Le montant total du prêt.
        taux_annuel_nominal_pct (float): Le taux d'intérêt annuel du crédit (hors assurance), en pourcentage.
        duree_annees (int): La durée du prêt en années.
        taux_annuel_assurance_pct (float): Le taux d'assurance annuel, en pourcentage.

    Returns:
        dict: Un dictionnaire contenant les détails calculés du prêt.
    """
    # --- Conversion des pourcentages et des durées ---
    taux_annuel_nominal = taux_annuel_nominal_pct / 100
    taux_mensuel_nominal = taux_annuel_nominal / 12
    nombre_mensualites = duree_annees * 12
    taux_annuel_assurance = taux_annuel_assurance_pct / 100

    # --- Calcul de la mensualité du crédit (hors assurance) ---
    if taux_mensuel_nominal > 0:
        mensualite_hors_assurance = (montant_emprunte * taux_mensuel_nominal) / (1 - (1 + taux_mensuel_nominal)**-nombre_mensualites)
    else:
        mensualite_hors_assurance = montant_emprunte / nombre_mensualites

    # --- Calcul de la mensualité de l'assurance ---
    mensualite_assurance = (montant_emprunte * taux_annuel_assurance) / 12

    # --- Totaux ---
    mensualite_avec_assurance = mensualite_hors_assurance + mensualite_assurance
    cout_total_credit = (mensualite_avec_assurance * nombre_mensualites) - montant_emprunte

    # --- Calcul du salaire net mensuel minimum requis ---
    salaire_minimum = mensualite_avec_assurance / 0.35

    return {
        "duree_annees": duree_annees,
        "taux_nominal_pct": taux_annuel_nominal_pct,
        "mensualite_avec_assurance": mensualite_avec_assurance,
        "mensualite_hors_assurance": mensualite_hors_assurance,
        "cout_total_credit": cout_total_credit,
        "salaire_mensuel_minimum": salaire_minimum,
    }

@st.cache_data
def generer_tableau_comparatif(montant_a_emprunter: float, durees_taux: dict, taux_assurance_pct: float, salaire_total: float) -> pd.DataFrame:
    """
    Génère un DataFrame Pandas comparant plusieurs scénarios de prêt et le dayaframe adapté pour l'affichage associé.
    """
    resultats_prets = []
    for duree, taux in durees_taux.items():
        details_pret = calculer_details_pret(
            montant_a_emprunter,
            taux,
            duree,
            taux_assurance_pct
        )
        details_pret['taux_endettement_pct'] = (details_pret['mensualite_avec_assurance'] / salaire_total) * 100 if salaire_total > 0 else 0
        resultats_prets.append(details_pret)
    
    df = pd.DataFrame(resultats_prets)

    def get_verdict(x):
        if x['taux_endettement_pct'] > 35:
            salaire_manquant = x['salaire_mensuel_minimum'] - salaire_total
            return f"❌ Élevé : il manque {formater_nombre(salaire_manquant)}"
        elif x['taux_endettement_pct'] > 33:
            return "⚠️ Prudent"
        else:
            return "✅ Faisable"

    df['Verdict'] = df.apply(get_verdict, axis=1)

    # --- Préparation du DataFrame pour l'affichage ---
    df_display = df.copy()

    # 1. Formatage des devises en chaînes de caractères avec séparateur d'espace
    df_display['mensualite_avec_assurance'] = df_display['mensualite_avec_assurance'].apply(
        lambda x: formater_nombre(x)
    )
    df_display['cout_total_credit'] = df_display['cout_total_credit'].apply(
        lambda x: formater_nombre(x)
    )
    df_display['salaire_mensuel_minimum'] = df_display['salaire_mensuel_minimum'].apply(
        lambda x: formater_nombre(x)
    )

    # 2. Renommage des colonnes pour un affichage plus clair
    df_display = df_display.rename(columns={
        'duree_annees': 'Durée (ans)',
        'taux_nominal_pct': 'Taux nominal (%)',
        'mensualite_avec_assurance': 'Mensualité',
        'cout_total_credit': 'Coût total du crédit',
        'salaire_mensuel_minimum': 'Salaire mensuel minimum',
        'taux_endettement_pct': "Taux d'endettement (%)"
    })

    # 3. Sélection et réorganisation de l'ordre final des colonnes
    df_display = df_display[[
        'Durée (ans)',
        'Taux nominal (%)',
        'Mensualité',
        'Coût total du crédit',
        'Salaire mensuel minimum',
        "Taux d'endettement (%)",
        'Verdict'
    ]]

    return df, df_display


def calculer_remboursement_anticipe(
    choix_impact: str,
    mensualite_hors_assurance: float,
    duree_initiale_mois: int,
    taux_mensuel_nominal: float,
    annee_remboursement: int,
    montant_remboursement_anticipe: float
) -> dict:
    """
    Simule l'impact d'un remboursement anticipé sur un prêt, en permettant
    soit de réduire la durée, soit de réduire les mensualités.

    Returns:
        Un dictionnaire avec les résultats : 
        - capital_restant_du_avant: Le capital qu'il restait à payer juste avant le remboursement.
        - interets_economises: Le montant total des intérêts économisés grâce au remboursement.
        - nouvelle_duree_restante_mois: La nouvelle durée restante du prêt en mois.
        - etc.
    """
    # --- ÉTAPE 1: Calculer le capital restant dû au moment du remboursement ---
    mois_remboursement = annee_remboursement * 12
    capital_restant_du = mensualite_hors_assurance * ((1 - (1+taux_mensuel_nominal)**-(duree_initiale_mois-mois_remboursement)) / taux_mensuel_nominal)
    duree_initiale_restante_mois = duree_initiale_mois - mois_remboursement

    # Si le remboursement est supérieur au capital restant, on ajuste
    montant_remboursement_anticipe = min(montant_remboursement_anticipe, capital_restant_du)
    
    # --- ÉTAPE 2: Appliquer le remboursement anticipé ---
    nouveau_capital_a_rembourser = capital_restant_du - montant_remboursement_anticipe

    # --- ÉTAPE 3: Calculer le nouveau plan en fonction du choix de l'utilisateur ---
    if nouveau_capital_a_rembourser <= 0:
        # Le prêt est entièrement remboursé
        nouvelle_duree_restante_mois = 0
        nouvelle_mensualite_hors_assurance = 0
    elif choix_impact == "Réduire la durée du prêt":
        nouvelle_duree_restante_mois = -log(1 - (nouveau_capital_a_rembourser * taux_mensuel_nominal / mensualite_hors_assurance)) / log(1 + taux_mensuel_nominal)
        nouvelle_duree_restante_mois = ceil(nouvelle_duree_restante_mois)
        nouvelle_mensualite_hors_assurance = mensualite_hors_assurance
    else: # "Réduire les mensualités"
        nouvelle_duree_restante_mois = duree_initiale_restante_mois
        part_1 = nouveau_capital_a_rembourser * taux_mensuel_nominal * (1 + taux_mensuel_nominal)**nouvelle_duree_restante_mois
        part_2 = (1 + taux_mensuel_nominal)**nouvelle_duree_restante_mois - 1
        nouvelle_mensualite_hors_assurance = part_1 / part_2

    # --- ÉTAPE 4: Calculer les gains ---
    cout_interets_restants_avant = (mensualite_hors_assurance * (duree_initiale_mois - mois_remboursement)) - capital_restant_du 
    cout_interets_restants_apres = (nouvelle_mensualite_hors_assurance * nouvelle_duree_restante_mois) - nouveau_capital_a_rembourser
    gain_interets = cout_interets_restants_avant - cout_interets_restants_apres
    
    # --- ÉTAPE 5: Retourner les résultats ---
    nouvelle_duree_totale_mois = mois_remboursement + nouvelle_duree_restante_mois

    resultats = {
        "gain_interets": gain_interets,
        "nouvelle_duree_totale_ans": nouvelle_duree_totale_mois / 12,
        "duree_reduite_mois": duree_initiale_restante_mois - nouvelle_duree_restante_mois,
        "ancienne_mensualite": mensualite_hors_assurance,
        "nouvelle_mensualite": nouvelle_mensualite_hors_assurance,
        "reduction_mensualite": mensualite_hors_assurance - nouvelle_mensualite_hors_assurance,
    }
    return resultats

# --- Fonctions de Création de Visuels ---
@st.cache_data
def creation_graph(df_prets: pd.DataFrame, salaire_total: float) -> go.Figure:
    """
    Crée un graphique Plotly combiné pour visualiser le compromis du prêt.
    (le code de la fonction reste le même)
    """
    # ... (code de la fonction inchangé) ...
    fig = go.Figure()

    # 1. Ajout des barres pour le salaire requis (Axe Y gauche)
    fig.add_trace(go.Bar(
        x=df_prets['duree_annees'],
        y=df_prets['salaire_mensuel_minimum'],
        name='Salaire requis',
        marker_color='darkorange',
        text=df_prets['salaire_mensuel_minimum'].apply(lambda x: f'{x:,.0f} €'.replace(',', ' ')),
        textposition='inside', 
        hoverinfo='x+name+text'
    ))

    # 2. Ajout de la ligne pour le coût total du crédit (Axe Y droit)
    fig.add_trace(go.Scatter(
        x=df_prets['duree_annees'],
        y=df_prets['cout_total_credit'],
        name='Coût total du crédit',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='royalblue', width=3),
        text=df_prets['cout_total_credit'].apply(lambda x: f'{x:,.0f} €'.replace(',', ' ')),
        textposition='bottom center',
        hoverinfo='x+name+text'
    ))

    # 3. Ajout de la ligne de seuil (salaire actuel)
    fig.add_trace(go.Scatter(
        x=[10, 30],
        y=[salaire_total, salaire_total],
        name=f'Salaire actuel : {formater_nombre(salaire_total)}',
        mode='lines',
        line=dict(color='firebrick', width=2, dash='dash'),
        hoverinfo='skip'
    ))

    fig.update_layout(
        title_text="Le compromis : Mensualité vs. Coût du Crédit",
        xaxis_title="Durée du prêt (en années)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        yaxis=dict(
            title="Salaire requis (€)",
            tickfont=dict(color="darkorange"),
            showgrid=False
        ),
        yaxis2=dict(
            title="Coût total du crédit (€)",
            tickfont=dict(color="royalblue"),
            showgrid=False,
            anchor="x",
            overlaying="y",
            side="right"
        ),
        template="plotly_white",
        hovermode="x unified"
    )
    return fig