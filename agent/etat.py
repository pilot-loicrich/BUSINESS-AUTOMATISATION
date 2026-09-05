"""Lecture et ecriture de l'etat : prospects, clients, journal.

L'etat tient dans des CSV versionnes sous donnees/. C'est volontaire : lisible
a l'oeil, editable a la main dans un tableur, et l'historique Git donne
gratuitement la tracabilite de ce que l'agent a fait.

/!\\ Ces fichiers contiennent des donnees personnelles : le depot DOIT etre
prive. Les workflows refusent de s'executer sur un depot public.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from .config import DONNEES

PROSPECTS = DONNEES / "prospects.csv"
CLIENTS = DONNEES / "clients.csv"
JOURNAL = DONNEES / "journal.csv"

COLONNES_PROSPECTS = [
    "id", "entreprise", "secteur", "ville", "contact", "email", "telephone",
    "statut", "score", "cite_par_ia", "concurrents_cites",
    "date_qualification", "date_contact", "date_relance_1", "date_relance_2",
    "date_reponse", "notes",
]

COLONNES_CLIENTS = [
    "id", "entreprise", "secteur", "ville", "email", "offre",
    "date_signature", "setup_eur", "mrr_eur", "statut", "jour_facturation",
    "dernier_rapport", "derniere_facture", "notes",
]

COLONNES_JOURNAL = ["horodatage", "tache", "cible", "action", "detail"]

# Cycle de vie d'un prospect.
STATUTS = [
    "a_qualifier",   # dans le fichier, pas encore audite
    "qualifie",      # audite, brouillon a produire
    "brouillon",     # brouillon pret, en attente d'envoi
    "contacte",      # premier message parti
    "relance_1",
    "relance_2",
    "rdv",
    "client",
    "perdu",
    "exclu",         # secteur interdit
]


def _lire(chemin: Path, colonnes: list[str]) -> list[dict]:
    if not chemin.exists():
        return []
    with chemin.open(encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    # Tolere un fichier edite a la main auquel il manque une colonne recente.
    for ligne in lignes:
        for col in colonnes:
            ligne.setdefault(col, "")
    return lignes


def _ecrire(chemin: Path, colonnes: list[str], lignes: list[dict]) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline="") as f:
        redacteur = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        redacteur.writeheader()
        redacteur.writerows(lignes)


def lire_prospects() -> list[dict]:
    return _lire(PROSPECTS, COLONNES_PROSPECTS)


def ecrire_prospects(lignes: list[dict]) -> None:
    _ecrire(PROSPECTS, COLONNES_PROSPECTS, lignes)


def lire_clients() -> list[dict]:
    return _lire(CLIENTS, COLONNES_CLIENTS)


def ecrire_clients(lignes: list[dict]) -> None:
    _ecrire(CLIENTS, COLONNES_CLIENTS, lignes)


def journaliser(tache: str, cible: str, action: str, detail: str = "") -> None:
    """Ajoute une ligne au journal. Toute action de l'agent doit y passer."""
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    nouveau = not JOURNAL.exists()
    with JOURNAL.open("a", encoding="utf-8", newline="") as f:
        redacteur = csv.writer(f)
        if nouveau:
            redacteur.writerow(COLONNES_JOURNAL)
        redacteur.writerow(
            [datetime.now().isoformat(timespec="seconds"), tache, cible, action, detail]
        )


def lire_journal(depuis: date | None = None) -> list[dict]:
    lignes = _lire(JOURNAL, COLONNES_JOURNAL)
    if depuis is None:
        return lignes
    return [
        l for l in lignes
        if l["horodatage"][:10] >= depuis.isoformat()
    ]


def _jours_depuis(valeur: str) -> int | None:
    if not valeur:
        return None
    try:
        return (date.today() - date.fromisoformat(valeur[:10])).days
    except ValueError:
        return None


@dataclass
class Metriques:
    mrr: float = 0.0
    clients_actifs: int = 0
    par_statut: dict[str, int] = field(default_factory=dict)
    contacts_7j: int = 0

    @property
    def manque_objectif(self) -> float:
        return max(0.0, 1000.0 - self.mrr)


def metriques() -> Metriques:
    prospects = lire_prospects()
    clients = lire_clients()
    actifs = [c for c in clients if c.get("statut") == "actif"]

    m = Metriques(
        mrr=sum(float(c.get("mrr_eur") or 0) for c in actifs),
        clients_actifs=len(actifs),
    )
    for p in prospects:
        statut = p.get("statut", "").strip() or "a_qualifier"
        m.par_statut[statut] = m.par_statut.get(statut, 0) + 1
    m.contacts_7j = sum(
        1 for p in prospects
        if (j := _jours_depuis(p.get("date_contact", ""))) is not None and j <= 7
    )
    return m


def prochain_id(lignes: list[dict], prefixe: str) -> str:
    numeros = []
    for l in lignes:
        ident = l.get("id", "")
        if ident.startswith(prefixe):
            try:
                numeros.append(int(ident[len(prefixe):]))
            except ValueError:
                continue
    return f"{prefixe}{max(numeros, default=0) + 1:04d}"
