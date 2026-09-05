"""Calcule les relances dues et prepare les messages correspondants.

60 % des reponses arrivent apres la premiere relance. C'est la tache la plus
rentable de l'agent, et celle qu'un humain oublie systematiquement.
"""

from __future__ import annotations

from datetime import date

from ..config import CONFIG, SORTIES
from ..etat import ecrire_prospects, journaliser, lire_prospects

DOSSIER = SORTIES / "relances"

RELANCE_1 = """\
Bonjour {contact},

Je me permets de revenir vers vous — je sais que le message a pu passer au
milieu du reste.

Le rapport sur {entreprise} est pret, je vous l'envoie si vous le voulez.
Sinon, dites-le-moi simplement, je n'insisterai pas.

{exploitant}
"""

# La seconde relance convertit mieux que la premiere : elle retire la pression
# et donne quand meme la valeur promise.
RELANCE_2 = """\
Bonjour {contact},

Je clos le sujet de mon cote. Je vous laisse quand meme le rapport en piece
jointe — il est a vous, que l'on travaille ensemble ou non.

Bonne continuation,
{exploitant}
"""


def _jours(valeur: str) -> int | None:
    if not valeur:
        return None
    try:
        return (date.today() - date.fromisoformat(valeur[:10])).days
    except ValueError:
        return None


def executer() -> dict:
    prospects = lire_prospects()
    resume = {"relance_1": 0, "relance_2": 0}
    DOSSIER.mkdir(parents=True, exist_ok=True)

    for prospect in prospects:
        statut = prospect.get("statut", "")
        if statut not in ("contacte", "relance_1"):
            continue
        if prospect.get("date_reponse"):
            continue  # a repondu : plus de relance automatique

        ecoule = _jours(prospect.get("date_contact", ""))
        if ecoule is None:
            continue

        if statut == "contacte" and ecoule >= CONFIG.delai_relance_1:
            modele, rang = RELANCE_1, 1
        elif statut == "relance_1" and ecoule >= CONFIG.delai_relance_2:
            modele, rang = RELANCE_2, 2
        else:
            continue

        texte = modele.format(
            contact=prospect.get("contact") or "",
            entreprise=prospect["entreprise"],
            exploitant=CONFIG.exploitant,
        )
        fichier = DOSSIER / f"{prospect['id']}-relance{rang}-{date.today().isoformat()}.md"
        fichier.write_text(
            f"---\nprospect_id: {prospect['id']}\nentreprise: {prospect['entreprise']}\n"
            f"email: {prospect.get('email', '')}\nrelance: {rang}\nstatut: a_valider\n---\n\n"
            f"**Objet :** Re: {prospect['entreprise']}\n\n{texte}",
            encoding="utf-8",
        )
        prospect["statut"] = f"relance_{rang}"
        prospect[f"date_relance_{rang}"] = date.today().isoformat()
        resume[f"relance_{rang}"] += 1
        journaliser("relancer", prospect["entreprise"], f"relance_{rang}", f"J+{ecoule}")

    ecrire_prospects(prospects)
    return resume
