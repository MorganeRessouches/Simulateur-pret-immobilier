import streamlit as st
from dateutil.relativedelta import relativedelta
from datetime import date
import locale
import pandas as pd

from utils import *

# --- Configuration de la page ---
st.set_page_config(
    page_title="Simulateur de Projet Immobilier",
    page_icon="🏡",
    layout="wide"
)

# --- Barre Latérale pour les taux et paramètres globaux ---
st.sidebar.header("Réglage des taux et paramètres")

frais_notaire_pct = st.sidebar.slider(
    "Estimation frais de notaire (%)",
    min_value=0.0,
    max_value=15.0,
    value=7.5,
    step=0.1,
    key='frais_notaire'
)

apport_souhaite_pct = st.sidebar.slider(
    "Apport personnel souhaité (%) du prix du bien",
    min_value=0,
    max_value=100,
    value=20,
    key='apport_souhaite',
    help="C'est le pourcentage du prix du bien que la banque demande généralement comme apport minimum."
)

taux_assurance_pct = st.sidebar.slider(
    "Taux annuel effectif d'assurance (%)",
    min_value=0.0,
    max_value=2.0,
    value=0.34,
    step=0.01,
    key='taux_assurance'
)

st.sidebar.markdown("---")
st.sidebar.subheader("Taux d'intérêts (hors assurance)")
taux_15_ans = st.sidebar.number_input("sur 15 ans (%)", value=3.09, step=0.01, format="%.2f")
taux_20_ans = st.sidebar.number_input("sur 20 ans (%)", value=3.16, step=0.01, format="%.2f")
taux_25_ans = st.sidebar.number_input("sur 25 ans (%)", value=3.28, step=0.01, format="%.2f")


# --- Page principale ---
st.title("🏡 Simulateur de projet immobilier")

montant_bien = st.number_input(
    "Quel est le montant du bien immobilier ?",
    min_value=50000,
    value=None,
    step=10000,
    help="Indiquez le prix de vente du bien que vous visez."
)

# Utilisation d'un expander pour alléger l'interface
with st.expander("👤 Renseignez votre situation financière"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Personne A**")
        salaire_a = st.number_input("Salaire net", min_value=0, value=2000, key='salaire_a')
        epargne_a = st.number_input("Épargne disponible", min_value=0, value=15000, key='epargne_a')
        epargne_m_a = st.number_input("Épargne mensuelle", min_value=0, value=700, key='epargne_m_a')
    with col_b:
        st.write("**Personne B**")
        salaire_b = st.number_input("Salaire net", min_value=0, value=2000, key='salaire_b')
        epargne_b = st.number_input("Épargne disponible", min_value=0, value=20000, key='epargne_b')
        epargne_m_b = st.number_input("Épargne mensuelle", min_value=0, value=800, key='epargne_m_b')


# --- CALCULS AUTOMATIQUES ---

epargne_totale = epargne_a + epargne_b
salaire_total = salaire_a + salaire_b
epargne_mensuelle_totale = epargne_m_a + epargne_m_b

emprunt = False

# --- AFFICHAGE DES RÉSULTATS ---
st.markdown("---")
st.header("📊 Synthèse du financement")

if montant_bien is not None:
    # 1. Calcul du coût total
    frais_notaire_valeur = montant_bien * (frais_notaire_pct / 100)
    cout_total_projet = montant_bien + frais_notaire_valeur

    # 2. L'apport utilisé pour le calcul est le maximum entre l'apport souhaité (objectif) et l'épargne actuelle.
    apport_objectif = montant_bien * (apport_souhaite_pct / 100)
    apport = max(apport_objectif, epargne_totale)

    # 3. Le montant à emprunter est calculé sur la base de cet apport objectif.
    montant_a_emprunter = cout_total_projet - apport
    
    apport_validé = epargne_totale>=apport_objectif
    emprunt = montant_a_emprunter>epargne_totale

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Coût total du projet", value=f"{cout_total_projet:,.0f} €".replace(",", " "))
            st.caption(f"Dont {frais_notaire_valeur:,.0f} € de frais de notaire".replace(",", " "))
        with col2:
            # On affiche clairement l'apport qui a été utilisé dans le calcul (l'objectif)
            st.metric(label="Apport considéré (Objectif)", value=f"{apport_objectif:,.0f} €".replace(",", " "))
            epargne_pct = (epargne_totale/montant_bien)*100
            st.caption(f"Votre épargne disponible est de {epargne_totale:,.0f} €.".replace(",", " "))
        if epargne_pct>20:
            st.success(f"Félicitation ! Votre épargne représente {epargne_pct:.0f}% du projet, ce qui est largement suffisant.")
        elif epargne_pct>10:
            st.success(f"Félicitation ! Votre épargne représente {epargne_pct:.0f}% du projet, ce qui est souvent suffisant.")
        else:
            st.warning(f"Votre épargne représente {epargne_pct:.0f}% du projet, ce qui n'est généralement pas suffisant.")
        if apport_validé:
            st.success(f"De plus, votre épargne couvre l'apport souhaité de {apport_souhaite_pct}%.")
            st.write(f"On considère donc désormais un apport de {epargne_totale:,.0f} €".replace(",", " "))
        else:
            st.write(f"Il vous manque {apport_objectif-epargne_totale:,.0f} € d'apport pour atteindre l'objectif.".replace(",", " "))

        st.markdown("---")

        if emprunt:
            st.metric(label="Montant à emprunter", value=f"{montant_a_emprunter:,.0f} €".replace(",", " "))
            st.caption(f"Calcul : {cout_total_projet:,.0f} € (Coût total) - {apport:,.0f} € (Apport)".replace(",", " "))
        else:
            st.success("Félicitations ! Votre apport couvre la totalité du coût du projet.")
else:
    st.warning("Veuillez entrer un montant pour le bien immobilier.")

st.markdown("---")
st.subheader("💰 Récapitulatif de votre situation")
col_s1, col_s2 = st.columns(2)
col_s1.metric("Salaire net mensuel total", f"{salaire_total:,.0f} €".replace(",", " "))
col_s2.metric("Capacité d'épargne mensuelle", f"{epargne_mensuelle_totale:,.0f} €".replace(",", " "))

if emprunt and not apport_validé:
    nombre_mois = (apport_objectif -  epargne_totale) / epargne_mensuelle_totale
    date_actuelle = date.today()
    date_objectif = date_actuelle + relativedelta(months=int(nombre_mois))
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    # Formatage de la date en "Mois Année"
    date_objectif_str = date_objectif.strftime("%B %Y").encode('latin-1').decode('utf-8')
    durée_str = formater_duree(nombre_mois)
    st.info(f"Il vous faut encore {durée_str}, soit jusqu'en {date_objectif_str} pour compléter votre apport de {apport:,.0f} €.".replace(",", " "))

if emprunt:
    st.markdown("---")
    st.header("🔍 Analyse des options de prêt")

    # Dictionnaire pour lier les durées et les taux saisis dans la sidebar
    durees_taux = {
        15: taux_15_ans,
        20: taux_20_ans,
        25: taux_25_ans,
    }

    # On prépare une liste pour stocker les résultats de chaque simulation
    resultats_prets = []
    for duree, taux in durees_taux.items():
        details_pret = calculer_details_pret(
            montant_a_emprunter,
            taux,
            duree,
            taux_assurance_pct
        )
        
        # On ajoute le taux d'endettement, qui dépend du salaire total
        details_pret['taux_endettement_pct'] = (details_pret['mensualite_avec_assurance'] / salaire_total) * 100 if salaire_total > 0 else 0
        
        resultats_prets.append(details_pret)

    # On transforme notre liste de résultats en DataFrame Pandas pour un affichage facile
    df_prets = pd.DataFrame(resultats_prets)
    
    # --- Création de la colonne "Verdict" ---
    def get_verdict(x):
        if x['taux_endettement_pct'] > 35:
            salaire_manquant = x['salaire_mensuel_minimum'] - salaire_total
            return f"❌ Élevé : il vous manque {salaire_manquant:,.0f} €.".replace(",", " ")
        elif x['taux_endettement_pct'] > 33:
            return "⚠️ Prudent"
        else:
            return "✅ Faisable"

    df_prets['Verdict'] = df_prets.apply(get_verdict, axis = 1)

    # --- Préparation du DataFrame pour l'affichage ---
    df_display = df_prets.copy()

    # 1. Formatage des devises en chaînes de caractères avec séparateur d'espace
    df_display['mensualite_avec_assurance'] = df_display['mensualite_avec_assurance'].apply(
        lambda x: f"{x:,.0f}".replace(",", " ") + " €"
    )
    df_display['cout_total_credit'] = df_display['cout_total_credit'].apply(
        lambda x: f"{x:,.0f}".replace(",", " ") + " €"
    )
    df_display['salaire_mensuel_minimum'] = df_display['salaire_mensuel_minimum'].apply(
        lambda x: f"{x:,.0f}".replace(",", " ") + " €"
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

    # --- Affichage du DataFrame ---
    st.dataframe(
        df_display,
        column_config={
            "Durée (ans)": st.column_config.NumberColumn(format="%d ans"),
            "Taux nominal (%)": st.column_config.NumberColumn(format="%.2f %%"),
            "Taux d'endettement (%)": st.column_config.ProgressColumn(
                format="%.1f %%",
                min_value=0,
                max_value=50,
            ),
            "Verdict": st.column_config.Column(width="medium")
        },
        hide_index=True,
        use_container_width=True
    )

    # --- GRAPHIQUE DU COMPROMIS DURÉE / COÛT / MENSUALITÉ ---
    
    fig = creation_graph(df_prets, salaire_total)
    st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")
    st.header("⏩ Scénario de remboursement anticipé")

    col_ra1, col_ra2 = st.columns(2)
    with col_ra1:
        montant_remboursement_anticipe = st.number_input(
            "Montant du remboursement anticipé (€)",
            min_value=0,
            value=10000,
            step=500,
            help="Combien souhaitez-vous rembourser en une seule fois ?"
        )
    with col_ra2:
        annee_remboursement = st.slider(
            "Année du remboursement",
            min_value=1,
            max_value=25, 
            value=5,
            help="Au bout de combien d'années prévoyez-vous de faire ce remboursement ?"
        )

        resultats_ra_list = []
    
    # On itère sur df_prets
    for index, pret_initial in df_prets.iterrows():
        
        # On ne fait le calcul que si l'année du RA est inférieure à la durée du prêt
        if annee_remboursement < pret_initial['duree_annees']:
            
            sim_ra = calculer_remboursement_anticipe(
                mensualite_hors_assurance=pret_initial['mensualite_hors_assurance'],
                duree_initiale_mois=pret_initial['duree_annees']*12,
                taux_mensuel_nominal=pret_initial['taux_nominal_pct']/1200,
                annee_remboursement=annee_remboursement,
                montant_remboursement_anticipe=montant_remboursement_anticipe
            )
            
            # On calcule le gain sur l'assurance
            gain_assurance = (pret_initial['mensualite_avec_assurance'] - pret_initial['mensualite_hors_assurance']) * sim_ra['duree_reduite_mois']
            gain_total = sim_ra['gain_interets'] + gain_assurance
            
            # On stocke les résultats de cette simulation dans un dictionnaire
            resultats_ra_list.append({
                "Durée Initiale": f"{pret_initial['duree_annees']} ans",
                "Nouvelle Durée": f"{sim_ra['nouvelle_duree_totale_ans']:.1f} ans",
                "Temps Économisé": formater_duree(sim_ra['duree_reduite_mois']),
                "Gain Total Estimé": f"{gain_total:,.0f} €".replace(",", " ")
            })

    # On vérifie si on a des résultats à afficher
    if resultats_ra_list:
        df_ra = pd.DataFrame(resultats_ra_list)
        
        st.dataframe(
            df_ra,
            hide_index=True,
            use_container_width=True
        )

        with st.expander("🤔 Pourquoi le temps économisé est-il si important ?"):
            st.info(
                """
                **Ce n'est pas une simple division !**

                Un remboursement anticipé ne supprime pas simplement les "dernières" mensualités. Il s'attaque directement au **capital restant dû**.

                **Voici l'effet "boule de neige" :**
                1.  Votre capital à rembourser diminue instantanément.
                2.  Dès le mois suivant, les **intérêts sont calculés sur un capital plus faible**, et sont donc moins élevés.
                3.  Comme votre mensualité reste la même, une **plus grande partie sert à rembourser le capital**, ce qui accélère encore plus le processus.

                Vous économisez donc non seulement le montant remboursé, mais surtout **tous les intérêts que ce montant aurait générés jusqu'à la fin du prêt.**
                """
            )
    else:
        st.warning("L'année de remboursement choisie est supérieure ou égale aux durées des prêts. Aucune simulation n'est possible.")