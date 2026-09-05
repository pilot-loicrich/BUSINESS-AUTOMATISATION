# setter-ia — squelette d'agent WhatsApp

Base de livraison du **business n°1**. Ce n'est pas un produit fini : c'est la charpente sur laquelle tu greffes le RAG de ton projet `chatbot-rag`.

## Ce qui est déjà là

- Prompt système durci contre l'invention de prix, de délais et d'engagements
- Deux outils : `proposer_rdv` et `escalader`, en `strict: true` (arguments toujours valides)
- Détection d'urgence avec escalade immédiate
- Repli sur escalade humaine si l'API est indisponible — **l'agent ne laisse jamais un prospect sans réponse**
- Interface `BaseConnaissance` à brancher sur ton ChromaDB

## Ce qu'il te reste à faire (≈ 4 h par client)

1. Brancher `BaseConnaissance` sur ChromaDB — tu l'as déjà écrit dans `chatbot-rag`
2. Exposer `repondre()` derrière un webhook FastAPI
3. Connecter WhatsApp Business Platform (API Cloud) ou un intégrateur
4. Implémenter les deux actions : écriture Google Calendar, notification SMS au référent
5. Recette : 20 messages de test, dont 5 pièges

## Essai hors ligne

```bash
pip install anthropic
python outils/setter-ia/agent.py
```

Affiche la réponse et les actions déclenchées pour un message de fuite d'eau — l'agent doit escalader en urgence.

## Choix du modèle

`claude-haiku-4-5` par défaut : la tâche est simple et cadrée par le RAG, et le coût par client tombe à quelques euros par mois. Passe à `claude-sonnet-5` si un client a un catalogue complexe où la qualité de compréhension devient critique.

## Le point qui fait la différence en rendez-vous

Montre au prospect l'agent **en train d'escalader**, pas seulement en train de bien répondre.

Tous tes concurrents montrent un chatbot qui répond. Aucun ne montre un chatbot qui dit « je ne sais pas, je transmets ». C'est pourtant exactement la peur du professionnel : qu'un robot raconte n'importe quoi à sa place, à ses clients. Lever cette peur ferme la vente.
