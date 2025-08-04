import plotly.graph_objects as go
import pandas as pd

def formater_duree(nombre_mois):
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
        "cout_total_credit": cout_total_credit,
        "salaire_mensuel_minimum": salaire_minimum,
    }

def creation_graph(df_prets: pd.DataFrame, salaire_total: float) -> go.Figure:
    """
    Crée un graphique Plotly combiné (barres et ligne) pour visualiser
    le compromis entre la durée du prêt, le coût total et la mensualité.

    Args:
        df_prets (pd.DataFrame): DataFrame contenant les résultats des simulations de prêt.
                                 Doit contenir les colonnes 'duree_annees', 'cout_total_credit',
                                 et 'salaire_mensuel_minimum'.
        salaire_total (float): Le revenu mensuel total de l'emprunteur pour calculer
                               le seuil d'endettement.

    Returns:
        go.Figure: Une figure Plotly prête à être affichée avec st.plotly_chart.
    """
    
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
        name=f'Salaire actuel : {salaire_total:,.0f} €'.replace(',', ' '),
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