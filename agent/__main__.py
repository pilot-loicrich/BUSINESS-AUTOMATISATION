"""CLI de l'agent : python -m agent <tache>"""

from __future__ import annotations

import argparse
import sys
import traceback

from .etat import journaliser

TACHES = {
    "qualifier": "Audite les prospects en attente et calcule leur priorite",
    "rediger": "Redige les brouillons de premier contact",
    "relancer": "Prepare les relances dues (J+3, J+10)",
    "rapport-client": "Rapport mensuel de suivi pour chaque client GEO",
    "facturer": "Emet les factures d'abonnement du mois",
    "briefing": "Construit le briefing hebdomadaire",
    "quotidien": "qualifier + rediger + relancer",
    "mensuel": "rapport-client + facturer",
}


def _executer(nom: str) -> dict:
    if nom == "qualifier":
        from .taches import qualifier
        return qualifier.executer()
    if nom == "rediger":
        from .taches import rediger
        return rediger.executer()
    if nom == "relancer":
        from .taches import relancer
        return relancer.executer()
    if nom == "rapport-client":
        from .taches import rapport_client
        return rapport_client.executer()
    if nom == "facturer":
        from .taches import facturer
        return facturer.executer()
    if nom == "briefing":
        from .taches import briefing
        return briefing.executer()
    raise ValueError(nom)


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(
        prog="agent",
        description="Agent d'automatisation.\n\nTaches :\n"
        + "\n".join(f"  {n:<16} {d}" for n, d in TACHES.items()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parseur.add_argument("tache", choices=list(TACHES))
    args = parseur.parse_args(argv)

    groupes = {
        "quotidien": ["qualifier", "rediger", "relancer"],
        "mensuel": ["rapport-client", "facturer"],
    }
    a_faire = groupes.get(args.tache, [args.tache])

    code = 0
    for nom in a_faire:
        print(f"\n--- {nom} ---")
        try:
            resume = _executer(nom)
            print("  " + ", ".join(f"{k}={v}" for k, v in resume.items()))
        except Exception as exc:
            # Une tache qui echoue ne doit pas empecher les suivantes : le lot
            # quotidien doit produire ce qu'il peut.
            code = 1
            print(f"  ECHEC : {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            journaliser(nom, "-", "erreur", str(exc)[:200])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
