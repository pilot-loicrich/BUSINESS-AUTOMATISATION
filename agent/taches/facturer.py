"""Emet les factures mensuelles d'abonnement.

La numerotation doit etre continue et sans trou : un numero manquant est une
irregularite comptable. Le compteur est donc derive des factures deja emises,
jamais d'un compteur en memoire.
"""

from __future__ import annotations

import os
import re
from datetime import date

from ..config import CONFIG, SORTIES
from ..etat import ecrire_clients, journaliser, lire_clients

DOSSIER = SORTIES / "factures"

MODELE = """\
# FACTURE N° {numero}

**Date d'emission :** {aujourdhui}
**Periode facturee :** {periode}

## Prestataire

**{exploitant}**
Entrepreneur individuel — micro-entreprise
SIRET : {siret}

## Client

{entreprise}
{email}

---

| Designation | Qte | P.U. | Total |
|-------------|-----|------|-------|
| {designation} | 1 | {montant} EUR | {montant} EUR |

**TOTAL A PAYER : {montant} EUR**

---

**TVA non applicable, article 293 B du CGI**

Paiement a 30 jours a compter de la date d'emission.
En cas de retard : penalite au taux de trois fois le taux d'interet legal,
exigible sans rappel prealable, et indemnite forfaitaire de recouvrement de
40 EUR (art. L441-10 et D441-5 du Code de commerce).
Pas d'escompte pour paiement anticipe.
"""

DESIGNATIONS = {
    "geo": "Suivi mensuel de visibilite sur les moteurs de recherche IA (GEO)",
    "setter": "Abonnement mensuel — assistant conversationnel WhatsApp",
    "ugc": "Abonnement mensuel — production de videos UGC",
}


def _siret() -> str:
    return os.environ.get("AGENT_SIRET", "[SIRET a renseigner]")


def _prochain_numero() -> str:
    """Deduit le numero suivant des fichiers deja emis. Continu par construction."""
    annee = date.today().year
    DOSSIER.mkdir(parents=True, exist_ok=True)
    existants = [
        int(m.group(1))
        for f in DOSSIER.glob(f"{annee}-*.md")
        if (m := re.match(rf"{annee}-(\d+)", f.stem))
    ]
    return f"{annee}-{max(existants, default=0) + 1:03d}"


def executer() -> dict:
    clients = lire_clients()
    resume = {"factures": 0, "montant": 0.0}
    mois_courant = date.today().strftime("%Y-%m")
    siret = _siret()

    for client in clients:
        if client.get("statut") != "actif":
            continue
        # Idempotence : deux executions le meme mois ne facturent qu'une fois.
        if (client.get("derniere_facture") or "")[:7] == mois_courant:
            continue
        montant = float(client.get("mrr_eur") or 0)
        if montant <= 0:
            continue

        offre = client.get("offre", "").lower()
        designation = next(
            (v for k, v in DESIGNATIONS.items() if k in offre),
            "Prestation de services",
        )
        numero = _prochain_numero()
        (DOSSIER / f"{numero}.md").write_text(
            MODELE.format(
                numero=numero,
                aujourdhui=date.today().strftime("%d/%m/%Y"),
                periode=date.today().strftime("%m/%Y"),
                exploitant=CONFIG.exploitant,
                siret=siret,
                entreprise=client["entreprise"],
                email=client.get("email", ""),
                designation=designation,
                montant=f"{montant:.2f}",
            ),
            encoding="utf-8",
        )
        client["derniere_facture"] = date.today().isoformat()
        resume["factures"] += 1
        resume["montant"] += montant
        journaliser("facturer", client["entreprise"], "facture", f"{numero} — {montant:.2f} EUR")

    ecrire_clients(clients)
    return resume
