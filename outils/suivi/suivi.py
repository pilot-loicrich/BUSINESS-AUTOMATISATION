"""Tableau de bord : pipeline de prospection et revenu recurrent.

Deux fichiers CSV, tenus a la main (5 min le lundi soir) :
  - prospects.csv : une ligne par entreprise contactee
  - clients.csv   : une ligne par contrat signe

Usage :
    python outils/suivi/suivi.py            # tableau de bord
    python outils/suivi/suivi.py --init     # cree les CSV si absents
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

# Source unique de verite : donnees/, alimente et tenu a jour par l'agent.
RACINE = Path(__file__).resolve().parent.parent.parent / "donnees"
PROSPECTS = RACINE / "prospects.csv"
CLIENTS = RACINE / "clients.csv"

OBJECTIF_MRR = 1000

COLONNES_PROSPECTS = [
    "entreprise", "secteur", "ville", "contact", "telephone",
    "date_contact", "date_relance_1", "date_relance_2", "statut", "notes",
]
COLONNES_CLIENTS = [
    "entreprise", "offre", "date_signature", "setup_eur", "mrr_eur", "statut",
]

STATUTS = ["a_contacter", "contacte", "relance", "rdv", "client", "perdu"]

EXEMPLE_PROSPECTS = [
    ["Plomberie Durand", "plombier", "Orleans", "M. Durand", "0238000000",
     "2026-09-08", "2026-09-11", "", "contacte", "Absent de l'audit GEO"],
    ["Cabinet Dentaire Sud", "dentiste", "Orleans", "Dr Bernard", "0238000001",
     "2026-09-08", "", "", "rdv", "RDV jeudi 14h"],
]
EXEMPLE_CLIENTS = [
    ["Cabinet Dentaire Sud", "geo", "2026-09-22", "350", "190", "actif"],
]


def _lire(chemin: Path) -> list[dict]:
    if not chemin.exists():
        return []
    with chemin.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _ecrire(chemin: Path, colonnes: list[str], lignes: list[list[str]]) -> None:
    with chemin.open("w", encoding="utf-8", newline="") as f:
        redacteur = csv.writer(f)
        redacteur.writerow(colonnes)
        redacteur.writerows(lignes)


def initialiser() -> None:
    for chemin, colonnes, exemple in (
        (PROSPECTS, COLONNES_PROSPECTS, EXEMPLE_PROSPECTS),
        (CLIENTS, COLONNES_CLIENTS, EXEMPLE_CLIENTS),
    ):
        if chemin.exists():
            print(f"{chemin.name} existe deja, non ecrase.")
            continue
        _ecrire(chemin, colonnes, exemple)
        print(f"{chemin.name} cree.")


def _barre(valeur: float, objectif: float, largeur: int = 30) -> str:
    part = min(valeur / objectif, 1.0) if objectif else 0.0
    pleins = round(part * largeur)
    return "[" + "#" * pleins + "." * (largeur - pleins) + "]"


def tableau_de_bord() -> None:
    prospects = _lire(PROSPECTS)
    clients = _lire(CLIENTS)

    if not prospects and not clients:
        print(
            "donnees/prospects.csv est vide.\n"
            "L'agent ne peut pas inventer des entreprises : ajoute des lignes\n"
            "(format dans donnees/exemple-prospects.csv), et il fera le reste."
        )
        return

    print(f"\n=== TABLEAU DE BORD — {date.today().strftime('%d/%m/%Y')} ===\n")

    # --- Revenu
    actifs = [c for c in clients if c.get("statut") == "actif"]
    mrr = sum(float(c["mrr_eur"] or 0) for c in actifs)
    setup = sum(float(c["setup_eur"] or 0) for c in clients)

    print("REVENU")
    print(f"  MRR (recurrent)     {mrr:>8.0f} EUR/mois")
    print(f"  One-shot cumule     {setup:>8.0f} EUR")
    print(f"  Clients actifs      {len(actifs):>8}")
    print()
    print(f"  Objectif 1 000 EUR  {_barre(mrr, OBJECTIF_MRR)} {mrr / OBJECTIF_MRR:.0%}")
    if mrr < OBJECTIF_MRR:
        # Panier moyen observe, ou hypothese du plan a defaut d'historique.
        panier = mrr / len(actifs) if actifs else 240
        manque = OBJECTIF_MRR - mrr
        print(f"  Reste a signer      {manque / panier:.1f} client(s) au panier actuel ({panier:.0f} EUR)")
    else:
        print("  Objectif atteint.")
    print()

    # --- Pipeline
    print("PIPELINE")
    compte = {s: 0 for s in STATUTS}
    for p in prospects:
        statut = p.get("statut", "").strip()
        compte[statut] = compte.get(statut, 0) + 1
    for statut in STATUTS:
        if compte.get(statut):
            print(f"  {statut:<14} {compte[statut]:>4}")
    print(f"  {'TOTAL':<14} {len(prospects):>4}")
    print()

    # --- Taux de conversion
    contactes = sum(compte.get(s, 0) for s in ("contacte", "relance", "rdv", "client", "perdu"))
    rdv = compte.get("rdv", 0) + compte.get("client", 0)
    gagnes = compte.get("client", 0)
    if contactes:
        print("CONVERSION")
        print(f"  contact -> RDV      {rdv / contactes:>7.0%}   ({rdv}/{contactes})")
        if rdv:
            print(f"  RDV -> client       {gagnes / rdv:>7.0%}   ({gagnes}/{rdv})")
        print(f"  contact -> client   {gagnes / contactes:>7.0%}   ({gagnes}/{contactes})")
        print()
        # Reference du plan : 20 contacts -> 1 client.
        if gagnes:
            print(f"  Il te faut environ {contactes / gagnes:.0f} contacts par client signe.")
            print(f"  Pour 4 clients : {contactes / gagnes * 4:.0f} contacts au total.")
        else:
            print("  Aucun client encore signe. Reference du plan : ~20 contacts par client.")
        print()

    # --- Relances dues
    dus = [
        p for p in prospects
        if p.get("statut") == "contacte" and not p.get("date_relance_1")
    ]
    if dus:
        print(f"RELANCES A FAIRE ({len(dus)})")
        for p in dus[:10]:
            print(f"  - {p['entreprise']} ({p.get('contact', '')}) — contacte le {p.get('date_contact', '?')}")
        print()
        print("  60 % des reponses arrivent apres la premiere relance. Ne les laisse pas dormir.")
        print()


def main() -> int:
    parseur = argparse.ArgumentParser(description="Tableau de bord prospection et revenu.")
    parseur.add_argument("--init", action="store_true", help="Cree les CSV d'exemple.")
    args = parseur.parse_args()
    if args.init:
        initialiser()
    else:
        tableau_de_bord()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
