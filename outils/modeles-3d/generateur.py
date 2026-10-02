"""Genere une famille de modeles 3D et leurs fiches produit, en une commande.

C'est le coeur de l'avantage : une boucle produit 60 references pretes a
publier, chacune avec son STL, son estimation de filament et son texte
d'annonce. Un concurrent qui modelise a la main en sort une par soiree.

    python generateur.py --catalogue
    python generateur.py --largeur 120 --profondeur 90 --hauteur 60 --colonnes 3
"""

from __future__ import annotations

import argparse
import csv
import itertools
from pathlib import Path

import cadquery as cq

from modele import Parametres, construire, masse_grammes, volume_mm3

SORTIE = Path(__file__).parent / "sortie"

# Famille par defaut. Les cotes sont choisies pour couvrir les tiroirs et
# etageres courants ; c'est la grille qu'on fait varier.
LARGEURS = [50, 75, 100, 125, 150]
PROFONDEURS = [50, 75, 100]
HAUTEURS = [30, 50, 70]
COMPARTIMENTS = [(1, 1), (2, 1), (3, 1), (2, 2)]

FICHE = """\
# Bac de rangement modulaire {largeur:g} x {profondeur:g} x {hauteur:g} mm{suffixe_titre}

Bac de rangement empilable, concu pour les tiroirs, etablis, tiroirs de bureau
et rangements d'atelier. {phrase_compartiments}

## Dimensions

| | mm |
|---|---|
| Largeur | {largeur:g} |
| Profondeur | {profondeur:g} |
| Hauteur | {hauteur:g} |
| Epaisseur des parois | {epaisseur:g} |

{phrase_empilable}

## Impression

| Reglage | Valeur conseillee |
|---|---|
| Matiere | PLA ou PETG |
| Hauteur de couche | 0,2 mm |
| Parois | 3 |
| Remplissage | 15 % |
| Supports | **aucun** — la piece est concue pour s'imprimer a plat |
| Filament estime | ~{masse:.0f} g |
| Volume de matiere | {volume:.0f} mm3 |

Aucun support n'est necessaire : toutes les surfaces en surplomb ont ete
evitees a la conception, y compris la feuillure d'empilement.

## Fichiers

- `{reference}.stl` — pret a trancher

## Licence

{licence}

---

*Modele genere parametriquement. Besoin d'une cote sur mesure ? Les dimensions
exactes peuvent etre produites a la demande.*
"""

LICENCE_DEFAUT = (
    "Usage personnel autorise. **Revente de l'objet imprime ou "
    "redistribution du fichier interdites sans accord.** Pour une licence "
    "commerciale, contactez-moi."
)


def _fiche(p: Parametres, solide: cq.Workplane, licence: str) -> str:
    compartiments = p.colonnes * p.rangees
    if compartiments > 1:
        suffixe_titre = f" — {p.colonnes} x {p.rangees} compartiments"
        phrase = (
            f"Il comporte {compartiments} compartiments separes "
            f"({p.colonnes} en largeur, {p.rangees} en profondeur), pour trier "
            "visserie, composants ou petit outillage."
        )
    else:
        suffixe_titre = ""
        phrase = "Volume unique, sans cloison."

    empilable = (
        "Les bacs **s'empilent** : une feuillure sous le fond vient se loger "
        "dans le bord du bac inferieur, avec 0,4 mm de jeu."
        if p.empilable
        else "Modele a poser, sans empilement."
    )

    return FICHE.format(
        largeur=p.largeur,
        profondeur=p.profondeur,
        hauteur=p.hauteur,
        epaisseur=p.epaisseur,
        suffixe_titre=suffixe_titre,
        phrase_compartiments=phrase,
        phrase_empilable=empilable,
        masse=masse_grammes(solide),
        volume=volume_mm3(solide),
        reference=p.reference,
        licence=licence,
    )


def produire(p: Parametres, dossier: Path, licence: str) -> dict:
    """Construit, exporte le STL et ecrit la fiche. Retourne la ligne d'index."""
    solide = construire(p)
    dossier.mkdir(parents=True, exist_ok=True)

    chemin_stl = dossier / f"{p.reference}.stl"
    cq.exporters.export(solide, str(chemin_stl))
    (dossier / f"{p.reference}.md").write_text(
        _fiche(p, solide, licence), encoding="utf-8"
    )

    return {
        "reference": p.reference,
        "largeur": p.largeur,
        "profondeur": p.profondeur,
        "hauteur": p.hauteur,
        "colonnes": p.colonnes,
        "rangees": p.rangees,
        "masse_g": round(masse_grammes(solide), 1),
        "volume_mm3": round(volume_mm3(solide)),
        "octets_stl": chemin_stl.stat().st_size,
    }


def catalogue(maximum: int | None = None) -> list[Parametres]:
    """Produit la grille de variantes, en ecartant les combinaisons absurdes."""
    variantes: list[Parametres] = []
    for largeur, profondeur, hauteur, (colonnes, rangees) in itertools.product(
        LARGEURS, PROFONDEURS, HAUTEURS, COMPARTIMENTS
    ):
        # Un compartiment doit rester utilisable : au moins 20 mm de large.
        if largeur / colonnes < 20 or profondeur / rangees < 20:
            continue
        # Les cloisons ne concernent que les bacs peu profonds, sinon on
        # multiplie des references que personne ne cherche.
        if hauteur > 50 and colonnes * rangees > 1:
            continue
        variantes.append(
            Parametres(
                largeur=largeur,
                profondeur=profondeur,
                hauteur=hauteur,
                colonnes=colonnes,
                rangees=rangees,
                prise=6 if hauteur >= 50 else 0,
            )
        )
        if maximum and len(variantes) >= maximum:
            break
    return variantes


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(
        description="Genere des bacs de rangement parametriques (STL + fiche)."
    )
    parseur.add_argument("--catalogue", action="store_true", help="Genere la famille complete.")
    parseur.add_argument("--max", type=int, help="Plafonne le nombre de variantes.")
    parseur.add_argument("--sortie", type=Path, default=SORTIE)
    parseur.add_argument("--licence", default=LICENCE_DEFAUT)
    for nom, defaut in [
        ("largeur", 100.0), ("profondeur", 80.0), ("hauteur", 50.0),
        ("epaisseur", 2.0), ("rayon", 4.0), ("prise", 0.0),
    ]:
        parseur.add_argument(f"--{nom}", type=float, default=defaut)
    parseur.add_argument("--colonnes", type=int, default=1)
    parseur.add_argument("--rangees", type=int, default=1)
    parseur.add_argument("--sans-empilement", action="store_true")
    args = parseur.parse_args(argv)

    if args.catalogue:
        variantes = catalogue(args.max)
    else:
        variantes = [
            Parametres(
                largeur=args.largeur, profondeur=args.profondeur, hauteur=args.hauteur,
                epaisseur=args.epaisseur, rayon=args.rayon, prise=args.prise,
                colonnes=args.colonnes, rangees=args.rangees,
                empilable=not args.sans_empilement,
            )
        ]

    print(f"{len(variantes)} variante(s) a produire vers {args.sortie}/")
    index: list[dict] = []
    echecs = 0
    for i, p in enumerate(variantes, start=1):
        try:
            index.append(produire(p, args.sortie, args.licence))
            print(f"  [{i}/{len(variantes)}] {p.reference}")
        except Exception as exc:
            # Une cote impossible ne doit pas interrompre le lot.
            echecs += 1
            print(f"  [{i}/{len(variantes)}] {p.reference} — ECHEC : {exc}")

    if index:
        chemin = args.sortie / "index.csv"
        with chemin.open("w", encoding="utf-8", newline="") as f:
            redacteur = csv.DictWriter(f, fieldnames=list(index[0]))
            redacteur.writeheader()
            redacteur.writerows(index)
        total = sum(l["masse_g"] for l in index)
        print(f"\n{len(index)} reference(s) produites, {echecs} echec(s).")
        print(f"Index : {chemin}")
        # Sous 10 g, l'arrondi a l'entier afficherait « ~0 g » et ferait
        # croire a un solide vide.
        print(f"Filament pour imprimer une fois chaque modele : ~{total:.1f} g"
              if total < 10 else
              f"Filament pour imprimer une fois chaque modele : ~{total:.0f} g")
    return 1 if echecs and not index else 0


if __name__ == "__main__":
    raise SystemExit(main())
