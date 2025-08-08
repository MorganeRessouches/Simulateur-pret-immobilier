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

tab1, tab2, tab3 = st.tabs([
        "⚙️ Configuration",
        "📊 Comparatif des Prêts", 
        "⏩ Remboursement Anticipé"
    ])

with tab1:
    
    montant_bien = st.number_input(
        "Quel est le montant du bien immobilier ?",
        min_value=50000,
        value=None,
        step=10000,
        help="Indiquez le prix de vente du bien que vous visez."
    )

    # Utilisation d'un expander pour alléger l'interface
    with st.expander("👤 Renseignez votre situation financière", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Personne A**")
            salaire_a = st.number_input("Salaire net", min_value=0, key='salaire_a')
            epargne_a = st.number_input("Épargne disponible", min_value=0, key='epargne_a')
            epargne_m_a = st.number_input("Épargne mensuelle", min_value=0, key='epargne_m_a')
        with col_b:
            st.write("**Personne B (facultatif)**")
            salaire_b = st.number_input("Salaire net", min_value=0, key='salaire_b')
            epargne_b = st.number_input("Épargne disponible", min_value=0, key='epargne_b')
            epargne_m_b = st.number_input("Épargne mensuelle", min_value=0, key='epargne_m_b')


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
        apport_validé = epargne_totale>=apport_objectif 

        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Coût total du projet", value=formater_nombre(cout_total_projet))
                st.caption(f"Dont {formater_nombre(frais_notaire_valeur)} de frais de notaire")
            with col2:
                # On affiche clairement l'apport qui a été utilisé dans le calcul (l'objectif)
                st.metric(label="Apport considéré (Objectif)", value=formater_nombre(apport_objectif))
                epargne_pct = (epargne_totale/montant_bien)*100
                st.caption(f"Votre épargne disponible est de {formater_nombre(epargne_totale)}.")
            if epargne_pct>20:
                st.success(f"Félicitation ! Votre épargne représente {epargne_pct:.0f}% du projet, ce qui est largement suffisant.")
            elif epargne_pct>10:
                st.success(f"Félicitation ! Votre épargne représente {epargne_pct:.0f}% du projet, ce qui est souvent suffisant.")
            else:
                st.warning(f"Votre épargne représente {epargne_pct:.0f}% du projet, ce qui n'est généralement pas suffisant.")
            if apport_validé:
                st.success(f"De plus, votre épargne couvre l'apport souhaité de {apport_souhaite_pct}%.")
            else:
                st.write(f"Il vous manque {formater_nombre(apport_objectif-epargne_totale)} d'apport pour atteindre l'objectif.")
            apport = st.number_input(
                    "Quel est votre apport personnel pour ce projet ?",
                    min_value=0,
                    max_value=montant_bien,
                    value=int(max(apport_objectif, epargne_totale)), 
                    step=1000
                )

            # 3. Le montant à emprunter est calculé sur la base de cet apport objectif.
            montant_a_emprunter = cout_total_projet - apport
            
            emprunt = montant_a_emprunter>epargne_totale

            st.markdown("---")

            if emprunt:
                st.metric(label="Montant à emprunter", value=formater_nombre(montant_a_emprunter))
                st.caption(f"Calcul : {formater_nombre(cout_total_projet)} (Coût total) - {formater_nombre(apport)} (Apport)")
            else:
                st.success("Félicitations ! Votre apport couvre la totalité du coût du projet.")
    else:
        st.warning("Veuillez entrer un montant pour le bien immobilier.")

    st.markdown("---")
    st.subheader("💰 Récapitulatif de votre situation")
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Salaire net mensuel total", formater_nombre(salaire_total))
    col_s2.metric("Capacité d'épargne mensuelle", formater_nombre(epargne_mensuelle_totale))

    if emprunt and not apport_validé and epargne_mensuelle_totale!=0:
        nombre_mois = (apport_objectif -  epargne_totale) / epargne_mensuelle_totale
        date_actuelle = date.today()
        date_objectif = date_actuelle + relativedelta(months=int(nombre_mois))
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        # Formatage de la date en "Mois Année"
        date_objectif_str = date_objectif.strftime("%B %Y")
        durée_str = formater_duree(nombre_mois)
        st.info(f"Il vous faut encore {durée_str}, soit jusqu'en {date_objectif_str} pour compléter votre apport de {formater_nombre(apport)}.")


with tab2:

    if emprunt:
        st.header("🔍 Analyse des options de prêt")

        # Dictionnaire pour lier les durées et les taux saisis dans la sidebar
        durees_taux = {
            15: taux_15_ans,
            20: taux_20_ans,
            25: taux_25_ans,
        }

        df_prets, df_display = generer_tableau_comparatif(montant_a_emprunter, durees_taux, taux_assurance_pct, salaire_total)

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
    else:
        st.warning("Veuillez d'abord compléter l'onglet configuration.")

with tab3:
    if emprunt:
        st.header("⏩ Scénario de remboursement anticipé")

        col_ra1, col_ra2 = st.columns(2)
        with col_ra1:
            montant_remboursement_anticipe = st.number_input(
                "Montant du remboursement anticipé (€)",
                min_value=0,
                step=500,
                help="Combien souhaitez-vous rembourser en une seule fois ?"
            )
        with col_ra2:
            annee_remboursement = st.slider(
                "Année du remboursement",
                min_value=1,
                max_value=25, 
                value=5,
                help="Au bout de combien d'années prévoyez-vous de faire ce remboursement ?",
                disabled=(montant_remboursement_anticipe == 0)
            )

            resultats_ra_list = []
        
        if montant_remboursement_anticipe>0:

            choix_impact = st.radio(
                "Quel est l'objectif de ce remboursement ?",
                options=["Réduire la durée du prêt", "Réduire les mensualités"],
                horizontal=True,
                index=0 # Par défaut, on cherche à réduire la durée
            )

            # On itère sur df_prets
            for index, pret_initial in df_prets.iterrows():
                
                # On ne fait le calcul que si l'année du RA est inférieure à la durée du prêt
                if annee_remboursement < pret_initial['duree_annees']:
                    
                    sim_ra = calculer_remboursement_anticipe(
                        choix_impact=choix_impact,
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

                    resultat = {
                        "Durée Initiale": f"{pret_initial['duree_annees']} ans",
                        "Gain Total Estimé": formater_nombre(gain_total)
                    }
                    
                    if choix_impact == "Réduire la durée du prêt":
                        resultat["Nouvelle Durée"] = formater_duree(sim_ra['nouvelle_duree_totale_ans'] * 12)
                        resultat["Temps Économisé"] = formater_duree(sim_ra['duree_reduite_mois'])
                    else: # "Réduire les mensualités"
                        mensualite_initale = pret_initial['mensualite_avec_assurance']
                        # On ajoute le coût de l'assurance à la nouvelle mensualité de crédit
                        nouvelle_mensualite_avec_assurance = sim_ra['nouvelle_mensualite'] + (mensualite_initale - pret_initial['mensualite_hors_assurance'])
                        
                        resultat["Ancienne Mensualité"] = formater_nombre(mensualite_initale)
                        resultat["Nouvelle Mensualité"] = formater_nombre(nouvelle_mensualite_avec_assurance)
                        resultat["Baisse par mois"] = formater_nombre(sim_ra['reduction_mensualite'])

                    resultats_ra_list.append(resultat)


            # On vérifie si on a des résultats à afficher
            if resultats_ra_list:
                df_ra = pd.DataFrame(resultats_ra_list)

                if choix_impact == "Réduire la durée du prêt":
                    colonnes_ordonnees = ["Durée Initiale", "Nouvelle Durée", "Temps Économisé", "Gain Total Estimé"]
                else:
                    colonnes_ordonnees = ["Durée Initiale", "Ancienne Mensualité", "Nouvelle Mensualité", "Baisse par mois", "Gain Total Estimé"]
                
                # On filtre le DataFrame pour n'avoir que les colonnes pertinentes et dans l'ordre
                df_ra = df_ra[colonnes_ordonnees]
                
                st.dataframe(
                    df_ra,
                    hide_index=True,
                    use_container_width=True
                )

                with st.expander("🤔 Comment est calculé le gain ?"):
                    if choix_impact == "Réduire la durée du prêt":
                        st.info(
                            """
                            Pourquoi le temps économisé est-il si important ?

                            **Ce n'est pas une simple division !**

                            Un remboursement anticipé ne supprime pas simplement les "dernières" mensualités. Il s'attaque directement au **capital restant dû**.

                            **Voici l'effet "boule de neige" :**
                            1.  Votre capital à rembourser diminue instantanément.
                            2.  Dès le mois suivant, les **intérêts sont calculés sur un capital plus faible**, et sont donc moins élevés.
                            3.  Comme votre mensualité reste la même, une **plus grande partie sert à rembourser le capital**, ce qui accélère encore plus le processus.

                            Vous économisez donc non seulement le montant remboursé, mais surtout **tous les intérêts que ce montant aurait générés jusqu'à la fin du prêt.**
                            """
                        )
                    else: # "Réduire les mensualités"
                        st.info(
                            """
                            A quoi ça sert ?

                            **Plus de souplesse pour votre budget.**

                            **Voici l'effet "Respiration Financière" :**
                            1.  Votre capital à rembourser (**capital restant dû**) diminue instantanément.
                            2.  La banque **recalcule une nouvelle mensualité** pour la même durée restante, mais sur ce capital réduit.
                            3.  Puisque vous devez moins d'argent au total, votre nouvelle mensualité est mathématiquement plus faible, vous donnant **plus de pouvoir d'achat chaque mois**.

                            Le "Gain Total Estimé" représente **l'économie totale d'intérêts** que vous réaliserez sur toute la durée restante du prêt grâce à ce capital réduit.
                            """
                        )
            else:
                st.warning("L'année de remboursement choisie est supérieure ou égale aux durées des prêts. Aucune simulation n'est possible.")
    else:
        st.warning("Veuillez d'abord compléter l'onglet configuration.")