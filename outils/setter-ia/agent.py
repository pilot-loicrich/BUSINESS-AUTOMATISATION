"""Squelette d'agent setter : repond a un prospect et propose un creneau.

Sert de base de livraison client pour le business n°1. La partie RAG est
volontairement laissee sous forme d'interface (`BaseConnaissance`) : branche-la
sur le ChromaDB de ton projet `chatbot-rag`.

Regle de conception centrale : l'agent ne doit JAMAIS inventer un prix, un
delai ou un engagement. Quand il ne sait pas, il passe la main. Un agent qui
improvise un devis coute un client au professionnel — et te coute le contrat.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

import anthropic

MODELE = "claude-haiku-4-5"  # suffisant ici, et ~5x moins cher qu'Opus

SYSTEME = """\
Tu reponds aux messages WhatsApp recus par {entreprise}, {activite} a {ville}.

Ton role : accueillir le prospect, comprendre son besoin, et proposer un
rendez-vous. Tu ecris comme un humain de l'entreprise : phrases courtes,
tutoiement ou vouvoiement selon le message recu, jamais de jargon, jamais
d'emoji en rafale.

REGLES ABSOLUES
1. Tu ne donnes QUE des informations presentes dans le contexte fourni.
2. Tu n'inventes JAMAIS un prix, un delai, une disponibilite ou un engagement.
3. Si l'information manque, tu reponds : « Je transmets a {referent}, il vous
   rappelle rapidement pour vous confirmer ca. » puis tu appelles l'outil
   `escalader`.
4. Si le message evoque une urgence (fuite, panne de chauffage, degat des eaux,
   douleur, danger), tu appelles `escalader` IMMEDIATEMENT avec urgence=true,
   avant toute autre chose.
5. Tu ne discutes ni de politique, ni de religion, ni des concurrents.
6. Quand tu as le besoin et une preference d'horaire, tu appelles `proposer_rdv`.

CONTEXTE DISPONIBLE
{contexte}
"""

OUTILS = [
    {
        "name": "proposer_rdv",
        "description": (
            "Propose un rendez-vous au prospect une fois le besoin compris et "
            "une preference d'horaire exprimee."
        ),
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "nom_prospect": {"type": "string"},
                "besoin": {"type": "string", "description": "Le besoin, en une phrase."},
                "creneau_souhaite": {"type": "string"},
                "telephone": {"type": "string"},
            },
            "required": ["nom_prospect", "besoin", "creneau_souhaite", "telephone"],
            "additionalProperties": False,
        },
    },
    {
        "name": "escalader",
        "description": (
            "Transmet la conversation a un humain. A utiliser des qu'une "
            "information manque ou qu'une urgence est detectee."
        ),
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "motif": {"type": "string"},
                "urgence": {"type": "boolean"},
                "resume": {"type": "string"},
            },
            "required": ["motif", "urgence", "resume"],
            "additionalProperties": False,
        },
    },
]


class BaseConnaissance(Protocol):
    """Interface RAG. Branche ici le ChromaDB de `chatbot-rag`."""

    def rechercher(self, question: str, k: int = 4) -> list[str]:
        """Retourne les k extraits les plus pertinents du corpus client."""


@dataclass
class ConfigClient:
    entreprise: str
    activite: str
    ville: str
    referent: str


class AgentSetter:
    def __init__(
        self,
        config: ConfigClient,
        connaissance: BaseConnaissance,
        client: anthropic.Anthropic | None = None,
    ) -> None:
        self.config = config
        self.connaissance = connaissance
        self.client = client or anthropic.Anthropic()

    def _systeme(self, question: str) -> str:
        extraits = self.connaissance.rechercher(question)
        contexte = "\n\n".join(f"- {e}" for e in extraits) or "(aucun extrait pertinent)"
        return SYSTEME.format(
            entreprise=self.config.entreprise,
            activite=self.config.activite,
            ville=self.config.ville,
            referent=self.config.referent,
            contexte=contexte,
        )

    def repondre(self, historique: list[dict]) -> dict:
        """Traite un tour de conversation.

        `historique` est la liste des messages au format Messages API.
        Retourne {"texte": str, "actions": [ {nom, arguments}, ... ]}.
        Les actions sont a executer par l'appelant (agenda, notification SMS).
        """
        derniere_question = next(
            (m["content"] for m in reversed(historique) if m["role"] == "user"), ""
        )

        try:
            reponse = self.client.messages.create(
                model=MODELE,
                max_tokens=1024,
                system=self._systeme(str(derniere_question)),
                messages=historique,
                tools=OUTILS,
            )
        except anthropic.RateLimitError:
            return {"texte": "", "actions": [{"nom": "escalader", "arguments": {
                "motif": "limite de debit", "urgence": False,
                "resume": "Agent indisponible, reprise humaine necessaire."}}]}
        except anthropic.APIStatusError as exc:
            return {"texte": "", "actions": [{"nom": "escalader", "arguments": {
                "motif": f"erreur API {exc.status_code}", "urgence": False,
                "resume": "Agent indisponible, reprise humaine necessaire."}}]}

        texte = "".join(b.text for b in reponse.content if b.type == "text")
        actions = [
            {"nom": b.name, "arguments": b.input}
            for b in reponse.content
            if b.type == "tool_use"
        ]
        return {"texte": texte.strip(), "actions": actions}


if __name__ == "__main__":
    # Demonstration hors ligne : base de connaissance factice.
    class FausseBase:
        def rechercher(self, question: str, k: int = 4) -> list[str]:
            return [
                "Depannage 7j/7 de 7h a 21h sur Orleans et 20 km alentour.",
                "Deplacement 45 EUR, deduits si intervention.",
                "Devis gratuit sous 24h pour les travaux de renovation.",
            ]

    client = anthropic.Anthropic()
    if not (client.api_key or client.auth_token):
        raise SystemExit(
            "Aucune credential Anthropic trouvee.\n"
            '  export ANTHROPIC_API_KEY="sk-ant-..."   ou   ant auth login'
        )

    agent = AgentSetter(
        ConfigClient("Plomberie Durand", "plombier-chauffagiste", "Orleans", "Marc"),
        FausseBase(),
        client=client,
    )
    resultat = agent.repondre(
        [{"role": "user", "content": "Bonjour, j'ai une fuite sous l'evier, vous passez quand ?"}]
    )
    print(json.dumps(resultat, ensure_ascii=False, indent=2))
