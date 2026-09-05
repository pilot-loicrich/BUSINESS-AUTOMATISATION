"""Genere le rapport d'audit vendable a partir d'un Resultat."""

from __future__ import annotations

from datetime import date

from .audit import Resultat, _normaliser

PLAN_ACTION = """\
## 5. Plan d'action

Par ordre d'impact decroissant. Les trois premiers points expliquent la
majorite de l'ecart constate.

| # | Action | Impact | Delai |
|---|--------|--------|-------|
| 1 | Fiche Google Business Profile complete : categorie principale exacte, description, horaires, zone d'intervention, photos recentes | Fort | 1 semaine |
| 2 | Campagne d'avis clients : viser un volume et une fraicheur comparables aux entreprises citees ci-dessus | Fort | 1 a 3 mois |
| 3 | Presence coherente dans les annuaires et plateformes du secteur (nom, adresse, telephone identiques partout) | Fort | 2 semaines |
| 4 | Page « a propos » redigee en langage naturel, repondant explicitement aux questions que les gens posent aux IA | Moyen | 1 semaine |
| 5 | Donnees structurees Schema.org `LocalBusiness` sur le site | Moyen | 2 jours |
| 6 | Mentions dans la presse locale, les blogs et les associations professionnelles | Fort mais lent | 3 a 6 mois |

## 6. Ce qui est mesure chaque mois

La position sur les moteurs IA n'est pas garantie et personne ne peut la
garantir : ces systemes evoluent en permanence. Ce qui est garanti, c'est la
mesure. Chaque mois, la meme serie de requetes est rejouee a l'identique et le
resultat est compare a celui d'aujourd'hui. Vous voyez la courbe.

## 7. Methode

Le modele a ete interroge avec plusieurs formulations differentes de la meme
question, puis les entreprises citees ont ete comptees. Une entreprise citee
sur une seule formulation n'a pas la meme visibilite qu'une entreprise citee
sur toutes. C'est ce taux de presence qui est mesure ici.

Ce rapport reflete les connaissances du modele interroge a la date indiquee.
Il ne prejuge pas des reponses d'autres moteurs ni de leurs evolutions.
"""


def _barre(n: int, total: int, largeur: int = 20) -> str:
    if total == 0:
        return ""
    pleins = round(n / total * largeur)
    return "#" * pleins + "." * (largeur - pleins)


def generer(resultat: Resultat) -> str:
    r = resultat
    lignes: list[str] = []
    a = lignes.append

    titre_cible = r.entreprise or f"{r.metier}s a {r.ville}"
    a(f"# Audit de visibilite sur les moteurs IA — {titre_cible}")
    a("")
    a(f"**Ville :** {r.ville}  ")
    a(f"**Secteur :** {r.metier}  ")
    a(f"**Date :** {date.today().strftime('%d/%m/%Y')}  ")
    a(f"**Methode :** {r.nb_requetes} requetes, modele `{r.modele}`")
    a("")
    a("---")
    a("")

    # 1. Le constat
    a("## 1. Le constat")
    a("")
    if r.entreprise:
        if r.citations_cible == 0:
            a(
                f"**{r.entreprise} n'a ete cite sur aucune des {r.nb_requetes} "
                f"requetes testees.**"
            )
            a("")
            a(
                "Autrement dit : pour toute personne qui cherche un "
                f"{r.metier} a {r.ville} en passant par une IA "
                "conversationnelle, votre entreprise n'existe pas. Elle ne "
                "figure pas dans la liste des options envisagees."
            )
        else:
            a(
                f"**{r.entreprise} a ete cite sur {r.citations_cible} des "
                f"{r.nb_requetes} requetes testees "
                f"({r.taux_cible:.0%} de presence).**"
            )
            a("")
            if r.taux_cible < 0.5:
                a(
                    "Votre entreprise est connue du modele, mais elle n'est pas "
                    "un reflexe. Sur la majorite des formulations, ce sont vos "
                    "concurrents qui sortent. L'ecart est rattrapable."
                )
            else:
                a(
                    "Votre position est solide. L'enjeu devient de la tenir : "
                    "vos concurrents travaillent le sujet, et ces classements "
                    "bougent."
                )
    else:
        a(
            f"Cartographie des {r.metier}s cites a {r.ville} par les moteurs IA."
        )
    a("")

    # 2. Le classement
    a("## 2. Qui est recommande a votre place")
    a("")
    if not r.classement:
        a(
            "Aucune entreprise n'a ete citee de maniere fiable. Le modele n'a "
            "pas de connaissance etablie de ce secteur sur cette ville."
        )
        a("")
        a(
            "**C'est une opportunite rare :** le terrain est vide. La premiere "
            "entreprise du secteur a travailler sa presence prendra la place, "
            "et il est beaucoup plus facile d'occuper un espace libre que d'en "
            "deloger un concurrent installe."
        )
    else:
        a("| Rang | Entreprise | Citations | Presence | |")
        a("|------|------------|-----------|----------|---|")
        cle_cible = _normaliser(r.entreprise) if r.entreprise else None
        for rang, (cle, nombre) in enumerate(r.classement[:12], start=1):
            nom = r.affichage.get(cle, cle)
            marque = " **← vous**" if cle == cle_cible else ""
            taux = nombre / r.nb_requetes
            a(
                f"| {rang} | {nom}{marque} | {nombre}/{r.nb_requetes} | "
                f"{taux:.0%} | `{_barre(nombre, r.nb_requetes)}` |"
            )
        if cle_cible and cle_cible not in r.citations:
            a(f"| — | **{r.entreprise}** | **0/{r.nb_requetes}** | **0 %** | `{'.' * 20}` |")
    a("")

    # 3. Pourquoi eux
    a("## 3. Pourquoi ce sont eux qui sortent")
    a("")
    if r.classement:
        a(
            "Les raisons avancees par le modele pour ses trois premieres "
            "recommandations :"
        )
        a("")
        for cle, _ in r.classement[:3]:
            nom = r.affichage.get(cle, cle)
            raison = r.raisons.get(cle, [""])[0]
            a(f"- **{nom}** — {raison}")
        a("")
        a(
            "Ces motifs ne sont pas aleatoires. Ils refletent ce que le modele "
            "a pu lire : fiches d'etablissement completes, avis nombreux et "
            "recents, mentions dans des annuaires et des articles. C'est "
            "exactement ce sur quoi porte le plan d'action en section 5."
        )
    else:
        a("Sans citation, il n'y a pas de motif a analyser.")
    a("")

    # 4. Ce que ca coute
    a("## 4. Ce que cela represente")
    a("")
    a(
        "Une part croissante des recherches de prestataire passe desormais par "
        "des assistants conversationnels plutot que par un moteur de recherche "
        "classique. Ces assistants ne renvoient pas dix liens : ils citent "
        "trois ou quatre noms. Il n'y a pas de deuxieme page."
    )
    a("")
    a(
        "Pour estimer l'enjeu chez vous, deux chiffres suffisent : le nombre de "
        "nouveaux clients que vous recevez chaque mois, et ce que vous rapporte "
        "un client en moyenne. Le calcul se fait en deux minutes lors de notre "
        "echange."
    )
    a("")

    a(PLAN_ACTION)

    if r.requetes_sans_reponse or r.erreurs:
        a("")
        a("---")
        a("")
        a("### Notes techniques")
        a("")
        if r.requetes_sans_reponse:
            a(
                f"- {r.requetes_sans_reponse} requete(s) sur {r.nb_requetes} "
                "sans connaissance locale exploitable."
            )
        for erreur in r.erreurs:
            a(f"- Requete en echec : {erreur}")

    return "\n".join(lignes) + "\n"
