"""Suivi des clips et decision a J+14.

Un clip rapporte : vues / 1000 x taux, plafonne au maximum par clip, et rien
du tout sous le minimum de paiement de la campagne. Ce script applique cette
regle a chaque ligne de donnees/clips.csv, retire la commission de la
plateforme, et rapporte le gain a l'heure passee : c'est ce chiffre qui decide
si le clipping continue ou s'arrete.

    python outils/clipping/suivi_clips.py --init     # cree donnees/clips.csv
    python outils/clipping/suivi_clips.py            # bilan
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

FICHIER = Path(__file__).resolve().parent.parent.parent / "donnees" / "clips.csv"

COLONNES = [
    "date", "campagne", "plateforme", "url", "vues",
    "taux_pour_1000", "minimum", "plafond", "statut", "minutes",
]

# Statuts : poste -> soumis -> approuve -> paye, ou rejete.
STATUTS_PERDUS = {"rejete"}
STATUTS_ACQUIS = {"approuve", "paye"}

COMMISSION = 0.10       # prelevee par la plateforme sur chaque paiement
SEUIL_HORAIRE = 8.0     # en dessous, l'heure vaut plus en prospection


def _nombre(valeur: str) -> float:
    try:
        return float((valeur or "0").replace(",", ".").replace(" ", ""))
    except ValueError:
        return 0.0


def gain_brut(vues: float, taux: float, minimum: float, plafond: float) -> float:
    """Gain d'un clip avant commission, selon les regles de la campagne."""
    brut = vues / 1000 * taux
    if brut < minimum:
        return 0.0          # sous le minimum, la campagne ne paie rien
    if plafond > 0:
        brut = min(brut, plafond)
    return brut


def lire() -> list[dict]:
    if not FICHIER.exists():
        return []
    with FICHIER.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def initialiser() -> None:
    if FICHIER.exists():
        print(f"{FICHIER} existe deja, non ecrase.")
        return
    FICHIER.parent.mkdir(parents=True, exist_ok=True)
    with FICHIER.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(COLONNES)
    print(f"{FICHIER} cree. Une ligne par clip poste.")


def bilan(commission: float, seuil: float) -> None:
    lignes = lire()
    if not lignes:
        print("Aucun clip enregistre. Lance --init, puis ajoute une ligne par clip.")
        return

    par_campagne: dict[str, dict] = defaultdict(
        lambda: {"clips": 0, "vues": 0.0, "acquis": 0.0, "attendu": 0.0, "sous_min": 0}
    )
    minutes = 0.0
    for l in lignes:
        c = par_campagne[l.get("campagne") or "?"]
        vues = _nombre(l.get("vues", ""))
        statut = (l.get("statut") or "").strip().lower()
        minutes += _nombre(l.get("minutes", ""))
        c["clips"] += 1
        c["vues"] += vues
        if statut in STATUTS_PERDUS:
            continue
        net = gain_brut(
            vues, _nombre(l.get("taux_pour_1000", "")),
            _nombre(l.get("minimum", "")), _nombre(l.get("plafond", "")),
        ) * (1 - commission)
        if net == 0:
            c["sous_min"] += 1
        if statut in STATUTS_ACQUIS:
            c["acquis"] += net
        else:
            c["attendu"] += net

    print(f"\n{'Campagne':<24}{'Clips':>6}{'Vues':>10}{'Sous min.':>10}{'Acquis':>9}{'Attendu':>9}")
    for nom, c in sorted(par_campagne.items(), key=lambda x: -(x[1]["acquis"] + x[1]["attendu"])):
        print(f"{nom[:23]:<24}{c['clips']:>6}{c['vues']:>10.0f}{c['sous_min']:>10}"
              f"{c['acquis']:>9.2f}{c['attendu']:>9.2f}")

    acquis = sum(c["acquis"] for c in par_campagne.values())
    attendu = sum(c["attendu"] for c in par_campagne.values())
    heures = minutes / 60
    print(f"\nAcquis (approuve ou paye) : {acquis:.2f}")
    print(f"Attendu (pas encore approuve) : {attendu:.2f}")
    print(f"Temps passe : {heures:.1f} h")
    if heures > 0:
        horaire = acquis / heures
        print(f"Gain horaire sur l'acquis : {horaire:.2f} / h  (seuil : {seuil:.2f})")
        if horaire >= seuil:
            print("=> Au-dessus du seuil : continue, sur les campagnes du haut du tableau.")
        elif attendu > acquis:
            print("=> Sous le seuil, mais l'essentiel attend encore l'approbation : re-mesure dans 7 jours.")
        else:
            print("=> Sous le seuil : arrete, et remets ces heures sur la prospection.")
    print("\nMontants dans la devise des campagnes, commission deduite.")


def main() -> int:
    p = argparse.ArgumentParser(description="Suivi des clips et decision a J+14.")
    p.add_argument("--init", action="store_true", help="Cree le CSV s'il n'existe pas.")
    p.add_argument("--commission", type=float, default=COMMISSION)
    p.add_argument("--seuil", type=float, default=SEUIL_HORAIRE, help="Gain horaire minimal.")
    a = p.parse_args()
    if a.init:
        initialiser()
    else:
        bilan(a.commission, a.seuil)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
