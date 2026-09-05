"""Redige les brouillons de premier contact, personnalises par l'audit GEO.

C'est la tache ou le modele apporte le plus : transformer un resultat d'audit
en un message court, factuel et non generique.
"""

from __future__ import annotations

from datetime import date

from ..config import CONFIG, SORTIES
from ..etat import ecrire_prospects, journaliser, lire_prospects

DOSSIER = SORTIES / "brouillons"

SYSTEME = """\
Tu rediges des courriels de premier contact B2B pour un prestataire independant \
francais qui vend deux services aux TPE : un audit de visibilite sur les moteurs \
de recherche IA (GEO) et un assistant WhatsApp qui repond aux prospects.

Regles de redaction, strictes :
- Moins de 120 mots. Un artisan lit sur son telephone, entre deux chantiers.
- Vouvoiement. Ton direct, jamais commercial, jamais flatteur.
- Aucune formule creuse : pas de « je me permets de vous contacter », pas de \
« solution innovante », pas de « revolutionner ».
- La premiere phrase doit contenir un fait verifiable et specifique a CETTE \
entreprise. C'est elle qui decide si le reste est lu.
- Tu ne promets aucun resultat, aucune position, aucun chiffre d'affaires.
- Tu ne demandes pas d'acheter : tu proposes d'envoyer le rapport, gratuitement.
- Termine par une question simple, fermee.
- Signature : prenom et nom seuls, sans titre ronflant.

Tu produis un objet et un corps. Rien d'autre : pas de commentaire, pas de \
variantes, pas de meta-explication."""

SCHEMA = {
    "type": "object",
    "properties": {
        "objet": {"type": "string", "description": "Moins de 60 caracteres."},
        "corps": {"type": "string"},
    },
    "required": ["objet", "corps"],
    "additionalProperties": False,
}


def _invite(prospect: dict) -> str:
    concurrents = prospect.get("concurrents_cites", "").split(" | ")
    concurrents = [c for c in concurrents if c]
    cite = prospect.get("cite_par_ia") == "oui"

    lignes = [
        f"Entreprise : {prospect['entreprise']}",
        f"Secteur : {prospect['secteur']}",
        f"Ville : {prospect.get('ville') or CONFIG.ville}",
        f"Interlocuteur : {prospect.get('contact') or 'inconnu'}",
        "",
        "Resultat de l'audit qui vient d'etre realise :",
    ]
    if cite:
        lignes.append(
            "- L'entreprise EST citee par le modele, mais pas systematiquement. "
            "Angle : sa position est fragile et ses concurrents travaillent le sujet."
        )
    else:
        lignes.append(
            "- L'entreprise n'est citee sur AUCUNE des requetes testees. "
            "Angle : elle n'existe pas pour qui cherche via une IA."
        )
    if concurrents:
        lignes.append(f"- Concurrents cites a sa place : {', '.join(concurrents)}.")
        lignes.append(
            "  Cite un ou deux de ces noms dans le courriel : c'est verifiable "
            "en trente secondes par le destinataire, et c'est ce qui rend le "
            "message credible."
        )
    else:
        lignes.append(
            "- Aucun concurrent clairement identifie : le secteur entier est "
            "absent. Angle : le terrain est libre, le premier qui s'en occupe "
            "prend la place."
        )
    lignes += [
        "",
        f"Signature : {CONFIG.exploitant}",
        "",
        "Redige le courriel.",
    ]
    return "\n".join(lignes)


def executer(limite: int | None = None) -> dict:
    from ..llm import LLMIndisponible, structure

    limite = limite or CONFIG.brouillons_par_jour
    prospects = lire_prospects()
    resume = {"rediges": 0, "erreurs": 0}
    DOSSIER.mkdir(parents=True, exist_ok=True)

    candidats = [p for p in prospects if p.get("statut") == "qualifie"]
    candidats.sort(key=lambda p: int(p.get("score") or 0), reverse=True)

    for prospect in candidats[:limite]:
        nom = prospect["entreprise"]
        try:
            resultat = structure(SYSTEME, _invite(prospect), SCHEMA, max_tokens=1200)
        except LLMIndisponible as exc:
            resume["erreurs"] += 1
            journaliser("rediger", nom, "erreur", str(exc)[:200])
            continue

        fichier = DOSSIER / f"{prospect['id']}-{date.today().isoformat()}.md"
        fichier.write_text(
            f"---\n"
            f"prospect_id: {prospect['id']}\n"
            f"entreprise: {nom}\n"
            f"email: {prospect.get('email', '')}\n"
            f"score: {prospect.get('score', '')}\n"
            f"statut: a_valider\n"
            f"---\n\n"
            f"**Objet :** {resultat['objet']}\n\n"
            f"{resultat['corps']}\n",
            encoding="utf-8",
        )
        prospect["statut"] = "brouillon"
        resume["rediges"] += 1
        journaliser("rediger", nom, "brouillon", fichier.name)

    ecrire_prospects(prospects)
    return resume
