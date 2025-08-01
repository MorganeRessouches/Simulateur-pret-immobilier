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

    return {
        "duree_annees": duree_annees,
        "taux_nominal_pct": taux_annuel_nominal_pct,
        "mensualite_avec_assurance": mensualite_avec_assurance,
        "cout_total_credit": cout_total_credit,
    }