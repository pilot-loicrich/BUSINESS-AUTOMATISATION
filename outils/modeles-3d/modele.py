"""Bac de rangement modulaire parametrique.

Le choix du modele n'est pas anodin : pour un bac de rangement, le
parametrage EST la valeur. Tous les tiroirs font une taille differente, donc
une famille de 200 variantes repond a 200 besoins reels, la ou un modele fige
n'en sert qu'un. C'est exactement le genre de produit qu'un concurrent qui
modelise a la main dans Fusion 360 ne peut pas sortir en volume.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import cadquery as cq

# Masse volumique du PLA, pour l'estimation de filament.
DENSITE_PLA = 1.24e-3  # g/mm3


@dataclass(frozen=True)
class Parametres:
    largeur: float = 100.0        # X, en mm
    profondeur: float = 80.0      # Y
    hauteur: float = 50.0         # Z
    epaisseur: float = 2.0        # parois et fond
    rayon: float = 4.0            # conge des angles verticaux
    colonnes: int = 1             # compartiments selon X
    rangees: int = 1              # compartiments selon Y
    prise: float = 0.0            # chanfrein de prehension sur l'arete avant haute
    empilable: bool = True        # feuillure en dessous pour empiler

    def valider(self) -> None:
        if min(self.largeur, self.profondeur, self.hauteur) <= 0:
            raise ValueError("Les dimensions doivent etre positives.")
        if self.epaisseur <= 0:
            raise ValueError("L'epaisseur doit etre positive.")
        # Il faut de la matiere ET du volume utile : deux parois plus un
        # minimum de vide interieur.
        if self.largeur <= 2 * self.epaisseur + 4:
            raise ValueError("Largeur trop faible pour l'epaisseur demandee.")
        if self.profondeur <= 2 * self.epaisseur + 4:
            raise ValueError("Profondeur trop faible pour l'epaisseur demandee.")
        if self.hauteur <= self.epaisseur + 2:
            raise ValueError("Hauteur trop faible pour l'epaisseur demandee.")
        # Un conge ne peut pas exceder la demi-cote, sinon la geometrie casse.
        if self.rayon >= min(self.largeur, self.profondeur) / 2:
            raise ValueError("Rayon de conge trop grand pour ces dimensions.")
        if self.colonnes < 1 or self.rangees < 1:
            raise ValueError("Il faut au moins une colonne et une rangee.")
        if self.prise < 0 or self.prise >= self.hauteur / 2:
            raise ValueError("Chanfrein de prehension hors limites.")

    @property
    def reference(self) -> str:
        """Reference lisible, utilisee comme nom de fichier."""
        base = f"bac-{self.largeur:g}x{self.profondeur:g}x{self.hauteur:g}"
        if self.colonnes > 1 or self.rangees > 1:
            base += f"-{self.colonnes}x{self.rangees}"
        return base


def construire(p: Parametres) -> cq.Workplane:
    """Retourne le solide du bac."""
    p.valider()
    ep = p.epaisseur

    corps = (
        cq.Workplane("XY")
        .box(p.largeur, p.profondeur, p.hauteur, centered=(True, True, False))
        .edges("|Z")
        .fillet(p.rayon)
    )

    # La cavite depasse volontairement en hauteur : c'est ce qui ouvre le bac.
    rayon_interieur = max(p.rayon - ep, 0.5)
    cavite = (
        cq.Workplane("XY")
        .workplane(offset=ep)
        .box(
            p.largeur - 2 * ep,
            p.profondeur - 2 * ep,
            p.hauteur,
            centered=(True, True, False),
        )
        .edges("|Z")
        .fillet(rayon_interieur)
    )
    bac = corps.cut(cavite)

    # Cloisons internes. Elles montent jusqu'a 2 mm sous le bord, pour que le
    # bord reste continu : plus solide, et plus propre a l'impression.
    hauteur_cloison = p.hauteur - ep - 2
    if hauteur_cloison > 0:
        for i in range(1, p.colonnes):
            x = -p.largeur / 2 + i * p.largeur / p.colonnes
            bac = bac.union(
                cq.Workplane("XY")
                .workplane(offset=ep)
                .box(ep, p.profondeur - 2 * ep, hauteur_cloison, centered=(True, True, False))
                .translate((x, 0, 0))
            )
        for j in range(1, p.rangees):
            y = -p.profondeur / 2 + j * p.profondeur / p.rangees
            bac = bac.union(
                cq.Workplane("XY")
                .workplane(offset=ep)
                .box(p.largeur - 2 * ep, ep, hauteur_cloison, centered=(True, True, False))
                .translate((0, y, 0))
            )

    # Feuillure inferieure : le bac vient se poser dans le bord de celui du
    # dessous. Profondeur volontairement faible (1,2 mm) pour rester imprimable
    # sans support.
    if p.empilable:
        jeu = 0.4
        bac = bac.cut(
            cq.Workplane("XY")
            .box(
                p.largeur - 2 * ep - jeu,
                p.profondeur - 2 * ep - jeu,
                2.4,  # centre sur Z=0 : 1,2 mm reellement retires
                centered=(True, True, True),
            )
        )

    # Chanfrein de prehension sur l'arete avant haute (Y minimum, Z maximum).
    if p.prise > 0:
        try:
            bac = bac.edges(">Z and <Y").chamfer(p.prise)
        except Exception:
            # Selon les cotes, l'arete peut etre introuvable ou le chanfrein
            # impossible : le bac reste valide sans, on ne casse pas le lot.
            pass

    return bac


def volume_mm3(solide: cq.Workplane) -> float:
    return solide.val().Volume()


def masse_grammes(solide: cq.Workplane, remplissage: float = 0.15) -> float:
    """Estimation de filament.

    Approximation volontairement grossiere : les parois d'un bac fin sont
    quasi pleines, l'infill ne joue que sur le fond. Suffisant pour afficher
    un ordre de grandeur dans la fiche produit.
    """
    return volume_mm3(solide) * DENSITE_PLA * (0.55 + remplissage)


def en_dict(p: Parametres) -> dict:
    return asdict(p)
