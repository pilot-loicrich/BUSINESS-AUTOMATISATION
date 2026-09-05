"""Rapport mensuel des clients GEO : re-mesure, comparaison, livrable.

C'est LA tache qui rend l'abonnement a 190 EUR/mois reellement recurrent.
Sans elle, quatre clients = quatre rapports a rediger a la main chaque mois,
soit l'equivalent d'une soiree perdue. Avec elle, c'est zero.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from geo_audit import generer, lancer

from ..config import CONFIG, DONNEES, SORTIES
from ..etat import ecrire_clients, journaliser, lire_clients

DOSSIER = SORTIES / "rapports-clients"
HISTORIQUE = DONNEES / "historique-geo.json"

SYSTEME_SYNTHESE = """\
Tu rediges la synthese d'ouverture d'un rapport mensuel de suivi GEO, adressee \
au dirigeant d'une TPE qui n'est pas technique.

Contraintes :
- 4 a 6 phrases, pas plus.
- Tu dis ce qui a bouge depuis le mois dernier, en clair et sans jargon.
- Si la position s'ameliore, tu le dis sobrement, sans triomphalisme.
- Si elle stagne ou recule, tu le dis franchement et tu expliques ce qui est \
engage pour le mois suivant. Ne maquille jamais un recul : un client qui \
decouvre qu'on lui a cache une baisse resilie.
- Tu ne promets aucune position future.
- Tu ne t'adresses jamais au lecteur par son prenom, tu ne signes pas."""


def _historique() -> dict:
    if HISTORIQUE.exists():
        return json.loads(HISTORIQUE.read_text(encoding="utf-8"))
    return {}


def _sauver_historique(donnees: dict) -> None:
    HISTORIQUE.parent.mkdir(parents=True, exist_ok=True)
    HISTORIQUE.write_text(
        json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _synthese(client: dict, actuel: int, total: int, precedent: int | None) -> str:
    from ..llm import LLMIndisponible, texte

    if precedent is None:
        contexte = (
            f"Premier releve pour {client['entreprise']} : cite sur {actuel} "
            f"requetes sur {total}. Pas de point de comparaison ce mois-ci."
        )
    else:
        sens = "progression" if actuel > precedent else "recul" if actuel < precedent else "stabilite"
        contexte = (
            f"{client['entreprise']} : cite sur {actuel} requetes sur {total} "
            f"ce mois-ci, contre {precedent} le mois dernier. C'est une {sens}."
        )
    try:
        return texte(SYSTEME_SYNTHESE, contexte, max_tokens=600)
    except LLMIndisponible:
        # Degradation propre : le rapport reste livrable sans la synthese redigee.
        return contexte


def executer(entreprise: str | None = None) -> dict:
    clients = lire_clients()
    resume = {"rapports": 0, "erreurs": 0}
    DOSSIER.mkdir(parents=True, exist_ok=True)
    historique = _historique()

    cibles = [
        c for c in clients
        if c.get("statut") == "actif"
        and "geo" in c.get("offre", "").lower()
        and (entreprise is None or c["entreprise"] == entreprise)
    ]

    for client in cibles:
        nom = client["entreprise"]
        try:
            resultat = lancer(
                ville=client.get("ville") or CONFIG.ville,
                metier=client["secteur"],
                entreprise=nom,
                nb_requetes=CONFIG.requetes_par_audit * 2,  # suivi = mesure fine
                modele=CONFIG.modele,
            )
        except Exception as exc:
            resume["erreurs"] += 1
            journaliser("rapport_client", nom, "erreur", str(exc)[:200])
            continue

        releves = historique.setdefault(nom, [])
        precedent = releves[-1]["citations"] if releves else None

        corps = generer(resultat)
        synthese = _synthese(client, resultat.citations_cible, resultat.nb_requetes, precedent)

        # Evolution mois par mois : c'est la courbe que le client a achetee.
        tableau = ["| Mois | Citations | Presence |", "|------|-----------|----------|"]
        for releve in releves[-5:]:
            taux = releve["citations"] / releve["total"] if releve["total"] else 0
            tableau.append(f"| {releve['mois']} | {releve['citations']}/{releve['total']} | {taux:.0%} |")
        taux_actuel = resultat.citations_cible / resultat.nb_requetes if resultat.nb_requetes else 0
        tableau.append(
            f"| **{date.today().strftime('%m/%Y')}** | "
            f"**{resultat.citations_cible}/{resultat.nb_requetes}** | **{taux_actuel:.0%}** |"
        )

        entete = (
            f"# Suivi GEO — {nom}\n\n"
            f"**Periode :** {date.today().strftime('%B %Y')}\n\n"
            f"## Ce qui a change ce mois-ci\n\n{synthese}\n\n"
            f"## Evolution\n\n" + "\n".join(tableau) + "\n\n---\n\n"
        )

        fichier = DOSSIER / f"{client['id']}-{date.today().strftime('%Y-%m')}.md"
        fichier.write_text(entete + corps, encoding="utf-8")

        releves.append({
            "mois": date.today().strftime("%m/%Y"),
            "citations": resultat.citations_cible,
            "total": resultat.nb_requetes,
        })
        client["dernier_rapport"] = date.today().isoformat()
        resume["rapports"] += 1
        journaliser(
            "rapport_client", nom, "rapport",
            f"{resultat.citations_cible}/{resultat.nb_requetes} (precedent : {precedent})",
        )

    _sauver_historique(historique)
    ecrire_clients(clients)
    return resume
