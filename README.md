# Simulateur de Prêt Immobilier

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47%2B-ff69b4.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transformez votre projet d'achat immobilier en un plan financier solide et visuel.** Cette application web, développée avec Python et Streamlit, va au-delà d'un simple calcul de mensualités. Elle vous offre une vision à 360° de votre projet, de la constitution de l'apport à l'impact d'un remboursement anticipé.

[**Lien vers l'application**](https://simulateur-pret-immobilier.streamlit.app)

![Aperçu de l'application](https://github.com/MorganeRessouches/Simulateur-pret-immobilier/blob/1666755354024ed0fbf6374612d3ff8d905a2c64/assets/demo.gif)

## ✨ Fonctionnalités

Cette application permet de passer d'une simple idée à un plan financier complet.

*   **💰 Calcul du financement :** Calcule le coût total du projet (prix du bien + frais de notaire) et le montant à emprunter en fonction de l'apport.
*   **📊 Analyse de l'endettement :** Compare votre salaire aux mensualités requises pour différentes durées de prêt (15, 20, 25 ans) et affiche votre taux d'endettement.
*   **⏳ Analyse de l'apport :** Si votre apport est insuffisant, l'application estime le temps nécessaire pour atteindre votre objectif en fonction de votre capacité d'épargne.
*   **📈 Graphiques interactifs :** Visualisez l'impact de la durée du prêt sur vos mensualités et sur le coût total des intérêts.
*   **⏩ Scenario de remboursement anticipé :** Simulez l'impact d'un remboursement anticipé sur la durée et le coût total de votre crédit.

## Contexte et Point de Départ

Ce projet est né d'un besoin personnel : disposer d'un outil complet pour simuler un prêt immobilier, incluant non seulement le calcul des mensualités mais aussi l'analyse de l'apport, du taux d'endettement et des scénarios de remboursement anticipé.

La première version de cet outil a été un tableur Excel complet.

➡️ **[Vous pouvez consulter le fichier Excel original ici](./source_excel/Simulation_prêt.xlsx)**

Bien que fonctionnel, le format Excel présentait plusieurs limites :
-   Moins interactif et visuel qu'une application web.
-   Difficile à partager et à utiliser sur mobile.

L'objectif de ce projet est donc de migrer ce simulateur vers une application Python/Streamlit afin de le rendre plus accessible, plus maintenable et plus agréable à utiliser.

## Installation

1.  Clonez le dépôt :
    ```bash
    git clone git@github.com:MorganeRessouches/Simulateur-pret-immobilier.git
    cd simulateur-pret-immobilier
    ```

2.  Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```

3.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Lancement de l'application

Pour lancer le simulateur, exécutez la commande suivante à la racine du projet :

```bash
streamlit run app.py
```

## 📈 Pistes d'Amélioration

Ce projet est fonctionnel et complet, mais voici quelques idées pour aller encore plus loin :

*   [ ] **Génération d'un PDF :** Ajouter un bouton pour télécharger le résumé de la simulation au format PDF.
*   [ ] **Tableau d'amortissement détaillé :** Afficher le tableau d'amortissement complet selon la durée du prêt.