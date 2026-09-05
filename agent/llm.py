"""Acces au modele, avec gestion d'erreur uniforme.

Toutes les taches passent par ici : une seule politique de repli, un seul
endroit ou le modele est nomme.
"""

from __future__ import annotations

import json

import anthropic

from .config import CONFIG


class LLMIndisponible(RuntimeError):
    """Le modele n'a pas pu repondre. L'appelant doit degrader, pas planter."""


_client: anthropic.Anthropic | None = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        c = anthropic.Anthropic()
        if not (c.api_key or c.auth_token):
            raise LLMIndisponible(
                "Aucune credential Anthropic. Definis ANTHROPIC_API_KEY "
                "(secret GitHub) ou lance `ant auth login` en local."
            )
        _client = c
    return _client


def texte(systeme: str, invite: str, max_tokens: int = 2000) -> str:
    """Une reponse en texte libre."""
    try:
        reponse = client().messages.create(
            model=CONFIG.modele,
            max_tokens=max_tokens,
            system=systeme,
            messages=[{"role": "user", "content": invite}],
        )
    except anthropic.RateLimitError as exc:
        raise LLMIndisponible(f"Limite de debit atteinte : {exc}") from exc
    except anthropic.APIStatusError as exc:
        raise LLMIndisponible(f"Erreur API {exc.status_code} : {exc}") from exc
    except anthropic.APIConnectionError as exc:
        raise LLMIndisponible(f"Connexion impossible : {exc}") from exc

    if reponse.stop_reason == "refusal":
        raise LLMIndisponible("Requete declinee par le modele.")
    return "".join(b.text for b in reponse.content if b.type == "text").strip()


def structure(systeme: str, invite: str, schema: dict, max_tokens: int = 2000) -> dict:
    """Une reponse JSON conforme au schema fourni."""
    try:
        reponse = client().messages.create(
            model=CONFIG.modele,
            max_tokens=max_tokens,
            system=systeme,
            messages=[{"role": "user", "content": invite}],
            output_config={"format": {"type": "json_schema", "schema": schema}},
        )
    except anthropic.RateLimitError as exc:
        raise LLMIndisponible(f"Limite de debit atteinte : {exc}") from exc
    except anthropic.APIStatusError as exc:
        raise LLMIndisponible(f"Erreur API {exc.status_code} : {exc}") from exc
    except anthropic.APIConnectionError as exc:
        raise LLMIndisponible(f"Connexion impossible : {exc}") from exc

    if reponse.stop_reason == "refusal":
        raise LLMIndisponible("Requete declinee par le modele.")
    brut = next(b.text for b in reponse.content if b.type == "text")
    return json.loads(brut)
