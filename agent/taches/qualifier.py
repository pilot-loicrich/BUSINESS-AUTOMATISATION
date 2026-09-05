"""Qualifie les prospects : lance l'audit GEO et calcule un score de priorite.

Tourne tous les matins. Zero intervention humaine.
"""

from __future__ import annotations

from datetime import date

from geo_audit import lancer  # depuis outils/geo-audit, cf. agent/config

from ..config import CONFIG, secteur_interdit
from ..etat import ecrire_prospects, journaliser, lire_prospects


def _score(cite: bool, nb_concurrents: int, a_email: bool) -> int:
    """Priorite de 0 a 100. Plus c'est haut, plus le prospect est chaud.

    Le meilleur prospect est celui qui est absent alors que ses concurrents
    sont bien identifies : la douleur est demontrable en une capture d'ecran.
    """
    score = 0
    if not cite:
        score += 50           # absent = argumentaire immediat
    if nb_concurrents >= 3:
        score += 30           # concurrents visibles = comparaison qui pique
    elif nb_concurrents >= 1:
        score += 15
    if a_email:
        score += 20           # joignable sans passer par le telephone
    return min(score, 100)


def executer(limite: int | None = None) -> dict:
    """Audite les prospects en statut `a_qualifier`."""
    limite = limite or CONFIG.audits_par_jour
    prospects = lire_prospects()
    resume = {"audites": 0, "exclus": 0, "erreurs": 0}

    a_traiter = [p for p in prospects if p.get("statut", "a_qualifier") == "a_qualifier"]

    for prospect in a_traiter[:limite]:
        nom = prospect["entreprise"]

        interdit = secteur_interdit(nom, prospect.get("secteur", ""), prospect.get("notes", ""))
        if interdit:
            prospect["statut"] = "exclu"
            prospect["notes"] = f"Exclu automatiquement (mot-cle « {interdit} »). " + prospect.get("notes", "")
            resume["exclus"] += 1
            journaliser("qualifier", nom, "exclu", f"secteur interdit : {interdit}")
            continue

        try:
            resultat = lancer(
                ville=prospect.get("ville") or CONFIG.ville,
                metier=prospect["secteur"],
                entreprise=nom,
                nb_requetes=CONFIG.requetes_par_audit,
                modele=CONFIG.modele,
            )
        except Exception as exc:  # une panne d'audit ne doit pas arreter le lot
            resume["erreurs"] += 1
            journaliser("qualifier", nom, "erreur", str(exc)[:200])
            continue

        cite = resultat.citations_cible > 0
        concurrents = [
            resultat.affichage.get(cle, cle)
            for cle, _ in resultat.classement[:3]
        ]
        prospect["cite_par_ia"] = "oui" if cite else "non"
        prospect["concurrents_cites"] = " | ".join(concurrents)
        prospect["score"] = str(_score(cite, len(concurrents), bool(prospect.get("email"))))
        prospect["date_qualification"] = date.today().isoformat()
        prospect["statut"] = "qualifie"
        resume["audites"] += 1
        journaliser(
            "qualifier", nom, "audite",
            f"cite={prospect['cite_par_ia']} score={prospect['score']}",
        )

    # Les plus chauds remontent : le brouillon du lendemain part sur eux.
    prospects.sort(key=lambda p: int(p.get("score") or 0), reverse=True)
    ecrire_prospects(prospects)
    return resume
