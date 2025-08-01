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