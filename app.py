import streamlit as st
from dateutil.relativedelta import relativedelta
from datetime import date
import locale

from utils import *

# --- Configuration de la page ---
st.set_page_config(
    page_title="Simulateur de Projet Immobilier",
    page_icon="🏡",
    layout="centered"
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