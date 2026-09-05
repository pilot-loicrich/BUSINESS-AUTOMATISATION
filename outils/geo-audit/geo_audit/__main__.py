"""Point d'entree CLI : python -m geo_audit --ville ... --metier ..."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import anthropic

from .audit import MODELE_DEFAUT, lancer
from .report import generer


def _slug(texte: str) -> str:
    sans_accent = "".join(
        c for c in unicodedata.normalize("NFD", texte) if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"[^a-z0-9]+", "-", sans_accent.lower()).strip("-")


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(
        prog="geo_audit",
        description="Genere un rapport d'audit GEO vendable pour une entreprise.",
    )
    parseur.add_argument("--ville", required=True, help="Ex. : Orleans")
    parseur.add_argument("--metier", required=True, help="Ex. : plombier")
    parseur.add_argument(
        "--entreprise",
        help="Nom de l'entreprise auditee. Omis : cartographie du secteur seul.",
    )
    parseur.add_argument(
        "--requetes", type=int, default=8, help="Nombre de requetes (defaut : 8)"
    )
    parseur.add_argument("--modele", default=MODELE_DEFAUT)
    parseur.add_argument(
        "--sortie", type=Path, help="Fichier de sortie (defaut : rapports/<slug>.md)"
    )
    args = parseur.parse_args(argv)

    client = anthropic.Anthropic()
    # Le client se construit sans credentials : l'absence ne se manifeste qu'a
    # la premiere requete, par une TypeError peu lisible. On la devance.
    if not (client.api_key or client.auth_token):
        print(
            "Aucune credential Anthropic trouvee.\n"
            "  export ANTHROPIC_API_KEY=\"sk-ant-...\"   ou   ant auth login",
            file=sys.stderr,
        )
        return 2

    cible = args.entreprise or f"{args.metier}-{args.ville}"
    print(f"Audit en cours : {cible} ({args.requetes} requetes)...", file=sys.stderr)

    resultat = lancer(
        ville=args.ville,
        metier=args.metier,
        entreprise=args.entreprise,
        nb_requetes=args.requetes,
        modele=args.modele,
        client=client,
    )

    if len(resultat.erreurs) == resultat.nb_requetes:
        print("Toutes les requetes ont echoue :", file=sys.stderr)
        for erreur in resultat.erreurs:
            print(f"  - {erreur}", file=sys.stderr)
        return 1

    sortie = args.sortie or Path("rapports") / f"{_slug(cible)}.md"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(generer(resultat), encoding="utf-8")

    print(f"\nRapport ecrit : {sortie}", file=sys.stderr)
    if args.entreprise:
        print(
            f"{args.entreprise} : {resultat.citations_cible}/{resultat.nb_requetes} "
            f"citations ({resultat.taux_cible:.0%})",
            file=sys.stderr,
        )
    for rang, (cle, nombre) in enumerate(resultat.classement[:5], start=1):
        print(
            f"  {rang}. {resultat.affichage.get(cle, cle)} — {nombre}/{resultat.nb_requetes}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
