# Simulateur de Prêt Immobilier

Ce projet est une application web construite avec Python et Streamlit pour simuler les mensualités et le coût d'un prêt immobilier.

## ✨ Fonctionnalités

Cette application permet de passer d'une simple idée à un plan financier complet.

*   **💰 Calcul du financement :** Calcule le coût total du projet (prix du bien + frais de notaire) et le montant à emprunter en fonction de l'apport.
*   **📊 Analyse de l'endettement :** Compare votre salaire aux mensualités requises pour différentes durées de prêt (15, 20, 25 ans) et affiche votre taux d'endettement.
*   **⏳ Analyse de l'apport :** Si votre apport est insuffisant, l'application estime le temps nécessaire pour atteindre votre objectif en fonction de votre capacité d'épargne.
*   **📈 Graphiques interactifs :** Visualisez l'impact de la durée du prêt sur vos mensualités et sur le coût total des intérêts.
*   **Scenario de remboursement anticipé :** Simulez l'impact d'un remboursement anticipé sur la durée et le coût total de votre crédit.

## Contexte et Point de Départ

Ce projet est né d'un besoin personnel : disposer d'un outil complet pour simuler un prêt immobilier, incluant non seulement le calcul des mensualités mais aussi l'analyse de l'apport, du taux d'endettement et des scénarios de remboursement anticipé.

La première version de cet outil a été un tableur Excel complet.

➡️ **[Vous pouvez consulter le fichier Excel original ici](./source_excel/Simulation_prêt.xlsx)**

Bien que fonctionnel, le format Excel présentait plusieurs limites :
-   Moins interactif et visuel qu'une application web.
-   Difficile à partager et à utiliser sur mobile.

L'objectif de ce projet est donc de migrer ce simulateur vers une application Python/Streamlit afin de le rendre plus accessible, plus maintenable et plus agréable à utiliser.

## 🛠️ Feuille de route du projet (Roadmap)

Voici les étapes de développement, de la migration de l'existant à l'ajout de nouvelles fonctionnalités.

-   [x] **Phase 1 : Socle de l'application**
    -   [x] Initialisation du projet Streamlit
    -   [x] Mise en place des champs de saisie principaux (montant du bien, salaires, épargne)
    -   [x] Calculs de base : coût du projet, apport, montant à emprunter

-   [x] **Phase 2 : Logique de simulation**
    -   [x] Affichage du temps nécessaire pour compléter l'apport
    -   [x] Calcul des mensualités (assurance incluse) selon la durée du prêt (15, 20, 25 ans)
    -   [x] Calcul du coût total des intérêts
    -   [x] Calcul du taux d'endettement et affichage conditionnel (alerte si dépassement)

-   [x] **Phase 3 : Fonctionnalités avancées**
    -   [x] Création du graphique interactif (coûts vs salaires)
    -   [x] Module de simulation de remboursement anticipé

-   [ ] **Phase 4 : Finalisation et Déploiement**
    -   [ ] Optimisation du code
    -   [ ] Rédaction de la documentation finale
    -   [ ] **Déploiement sur Streamlit Community Cloud**

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