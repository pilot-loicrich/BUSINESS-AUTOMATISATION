"""Configuration centrale de l'agent."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DONNEES = RACINE / "donnees"
SORTIES = RACINE / "sorties"

# geo_audit vit dans outils/geo-audit (tiret dans le nom du dossier, donc pas
# importable tel quel) : on l'ajoute au chemin plutot que de le dupliquer.
_GEO = RACINE / "outils" / "geo-audit"
if str(_GEO) not in sys.path:
    sys.path.insert(0, str(_GEO))


@dataclass(frozen=True)
class Config:
    """Parametres d'exploitation, surchargeables par variables d'environnement."""

    ville: str = os.environ.get("AGENT_VILLE", "Orleans")
    exploitant: str = os.environ.get("AGENT_EXPLOITANT", "Loic Nanzo Tonlieu")

    # Volumes
    audits_par_jour: int = int(os.environ.get("AGENT_AUDITS_PAR_JOUR", "8"))
    brouillons_par_jour: int = int(os.environ.get("AGENT_BROUILLONS_PAR_JOUR", "10"))
    requetes_par_audit: int = int(os.environ.get("AGENT_REQUETES_PAR_AUDIT", "8"))

    # Cadence de relance, en jours apres le contact initial
    delai_relance_1: int = 3
    delai_relance_2: int = 10

    # Envoi automatique des courriels de prospection.
    # PAR DEFAUT DESACTIVE — voir agent/README.md, section « Pourquoi l'envoi
    # n'est pas automatique par defaut ».
    envoi_auto: bool = os.environ.get("AGENT_ENVOI_AUTO", "").lower() == "true"
    envois_max_par_jour: int = int(os.environ.get("AGENT_ENVOIS_MAX_PAR_JOUR", "15"))

    # Secteurs interdits : conflit d'interets CNPF (foret-bois) et Accor
    # (hotellerie orleanaise). Voir docs/00-cadre-legal.md.
    secteurs_interdits: tuple[str, ...] = (
        "foret", "forestier", "forestiere", "bois", "scierie", "sylviculture",
        "pepinieriste", "elagage", "abattage", "cnpf",
        "hotel", "hotellerie", "hebergement", "auberge", "residence hoteliere",
    )

    @property
    def modele(self) -> str:
        return os.environ.get("AGENT_MODELE", "claude-opus-5")


CONFIG = Config()


def secteur_interdit(*champs: str) -> str | None:
    """Retourne le mot-cle interdit trouve, ou None.

    Filet de securite : si un prospect interdit se glisse dans le fichier,
    l'agent doit refuser de le traiter plutot que de compter sur la vigilance
    humaine a la saisie.
    """
    texte = " ".join(c.lower() for c in champs if c)
    for mot in CONFIG.secteurs_interdits:
        if mot in texte:
            return mot
    return None
