"""Formulations de la question posée au modèle.

On interroge plusieurs fois avec des tournures differentes : une entreprise
cite une fois sur huit formulations n'a pas la meme visibilite qu'une
entreprise citee huit fois sur huit. C'est cet ecart que l'audit mesure.
"""

VARIANTES = [
    "Quels sont les meilleurs {metier}s a {ville} ?",
    "Je cherche un bon {metier} a {ville}, lequel me conseilles-tu ?",
    "Peux-tu me recommander un {metier} fiable a {ville} ?",
    "Quel {metier} choisir a {ville} ? Donne-moi les references du secteur.",
    "Top 5 des {metier}s a {ville}",
    "J'ai besoin d'un {metier} en urgence a {ville}, qui appeler ?",
    "Quelle est la meilleure entreprise de {metier} a {ville} et pourquoi ?",
    "Si tu devais choisir un seul {metier} a {ville}, lequel ?",
]


def construire(metier: str, ville: str, n: int) -> list[str]:
    """Retourne les `n` premieres variantes, formatees."""
    if n < 1:
        raise ValueError("Il faut au moins une requete.")
    variantes = [v.format(metier=metier, ville=ville) for v in VARIANTES]
    # Au-dela du nombre de variantes disponibles, on boucle : reposer la meme
    # question revele aussi la stabilite de la reponse du modele.
    return [variantes[i % len(variantes)] for i in range(n)]
