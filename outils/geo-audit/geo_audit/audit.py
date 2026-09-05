"""Interroge le modele et agrege les entreprises citees."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

import anthropic

from .queries import construire

MODELE_DEFAUT = "claude-opus-5"

# Le schema force le modele a repondre en JSON exploitable, sans post-traitement
# fragile a base d'expressions regulieres.
SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "entreprises": {
                "type": "array",
                "description": "Les entreprises citees, dans l'ordre de la reponse.",
                "items": {
                    "type": "object",
                    "properties": {
                        "nom": {"type": "string"},
                        "raison": {
                            "type": "string",
                            "description": "En une phrase, pourquoi celle-ci est citee.",
                        },
                    },
                    "required": ["nom", "raison"],
                    "additionalProperties": False,
                },
            },
            "aucune_connaissance": {
                "type": "boolean",
                "description": "Vrai si le modele n'a aucune connaissance fiable du secteur local.",
            },
        },
        "required": ["entreprises", "aucune_connaissance"],
        "additionalProperties": False,
    },
}

SYSTEME = (
    "Tu reponds comme un assistant grand public a qui l'on demande une "
    "recommandation locale. Cite uniquement des entreprises dont tu as "
    "reellement connaissance : n'invente aucun nom. Si tu ne connais pas le "
    "tissu local, mets aucune_connaissance a vrai et renvoie une liste vide."
)


def _normaliser(nom: str) -> str:
    """Cle de comparaison : sans accents, sans casse, sans ponctuation."""
    sans_accent = "".join(
        c for c in unicodedata.normalize("NFD", nom) if unicodedata.category(c) != "Mn"
    )
    return "".join(c for c in sans_accent.lower() if c.isalnum() or c.isspace()).strip()


@dataclass
class Resultat:
    """Resultat agrege d'un audit."""

    ville: str
    metier: str
    entreprise: str | None
    nb_requetes: int
    modele: str
    citations: Counter = field(default_factory=Counter)
    raisons: dict[str, list[str]] = field(default_factory=dict)
    affichage: dict[str, str] = field(default_factory=dict)
    requetes_sans_reponse: int = 0
    erreurs: list[str] = field(default_factory=list)

    @property
    def classement(self) -> list[tuple[str, int]]:
        return self.citations.most_common()

    @property
    def citations_cible(self) -> int:
        if not self.entreprise:
            return 0
        return self.citations.get(_normaliser(self.entreprise), 0)

    @property
    def taux_cible(self) -> float:
        if not self.entreprise or self.nb_requetes == 0:
            return 0.0
        return self.citations_cible / self.nb_requetes


def _interroger(client: anthropic.Anthropic, modele: str, question: str) -> dict:
    reponse = client.messages.create(
        model=modele,
        max_tokens=4000,
        system=SYSTEME,
        messages=[{"role": "user", "content": question}],
        output_config={"format": SCHEMA},
    )
    texte = next(b.text for b in reponse.content if b.type == "text")
    return json.loads(texte)


def lancer(
    ville: str,
    metier: str,
    entreprise: str | None = None,
    nb_requetes: int = 8,
    modele: str = MODELE_DEFAUT,
    client: anthropic.Anthropic | None = None,
) -> Resultat:
    """Pose `nb_requetes` variantes de la question et agrege les citations."""
    client = client or anthropic.Anthropic()
    questions = construire(metier, ville, nb_requetes)
    resultat = Resultat(
        ville=ville,
        metier=metier,
        entreprise=entreprise,
        nb_requetes=nb_requetes,
        modele=modele,
    )

    def _travail(question: str):
        try:
            return _interroger(client, modele, question)
        except anthropic.RateLimitError as exc:
            return {"_erreur": f"Limite de debit atteinte : {exc}"}
        except anthropic.APIStatusError as exc:
            return {"_erreur": f"Erreur API ({exc.status_code}) : {exc}"}
        except anthropic.APIConnectionError as exc:
            return {"_erreur": f"Connexion impossible : {exc}"}

    with ThreadPoolExecutor(max_workers=4) as pool:
        reponses = list(pool.map(_travail, questions))

    for donnees in reponses:
        if "_erreur" in donnees:
            resultat.erreurs.append(donnees["_erreur"])
            continue
        if donnees.get("aucune_connaissance") or not donnees["entreprises"]:
            resultat.requetes_sans_reponse += 1
            continue
        # Une entreprise citee deux fois dans la meme reponse ne compte qu'une
        # fois : on mesure la presence par requete, pas la verbosite du modele.
        vues: set[str] = set()
        for item in donnees["entreprises"]:
            cle = _normaliser(item["nom"])
            if not cle or cle in vues:
                continue
            vues.add(cle)
            resultat.citations[cle] += 1
            resultat.affichage.setdefault(cle, item["nom"])
            resultat.raisons.setdefault(cle, []).append(item["raison"])

    return resultat
