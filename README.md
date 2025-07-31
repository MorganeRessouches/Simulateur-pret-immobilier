# Simulateur de Prêt Immobilier

Ce projet est une application web construite avec Python et Streamlit pour simuler les mensualités et le coût d'un prêt immobilier.

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