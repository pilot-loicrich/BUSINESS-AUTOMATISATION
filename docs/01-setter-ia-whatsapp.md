# 01 — Setter IA WhatsApp  ⭐ MOTEUR PRINCIPAL

> Idée n°21 de la vidéo. **C'est celui-là qui te fait tes 1 000 €.** Si tu ne dois en lancer qu'un, c'est lui.

## Pourquoi c'est LE bon pour toi

Yomi Denzel présente ce business comme accessible à un débutant avec des outils no-code. Sauf que toi, tu as déjà **construit et déployé exactement ça** : `chatbot-rag` — FastAPI + LangChain + ChromaDB + Docker + CI/CD sur AWS EC2, réponse < 2 s.

Ton projet GitHub **est** le produit. Tu n'as pas à apprendre le métier : tu as à l'emballer et à le vendre.

C'est un avantage décisif :
- un concurrent no-code livre un chatbot générique qui hallucine ;
- toi tu livres un agent **RAG** ancré sur les vraies données du client (tarifs, zone d'intervention, horaires, FAQ), donc qui ne raconte pas n'importe quoi ;
- et tu peux l'héberger toi-même, donc ta marge est proche de 100 %.

## Le problème que tu vends

Un prospect écrit sur WhatsApp à un plombier un dimanche à 22 h. Personne ne répond avant lundi 9 h. Le prospect a déjà appelé trois concurrents entre-temps.

## L'offre

**« Vous ne perdez plus un seul client parce que vous répondez trop tard. »**

| Ligne | Prix |
|-------|------|
| Installation + paramétrage + entraînement sur les données du client | **490 €** (une fois) |
| Abonnement mensuel : hébergement, maintenance, ajustements, rapport mensuel | **290 €/mois** |

Engagement 3 mois puis mensuel. Premier mois **satisfait ou remboursé** — ça lève 80 % de l'objection et tu ne rembourseras quasiment jamais.

## L'argumentaire de vente (le calcul qui ferme)

Devant le patron, sors ton téléphone et fais **son** calcul, à voix haute :

> — Combien de demandes vous recevez par semaine sur WhatsApp ?
> — Une vingtaine.
> — Vous en ratez combien, honnêtement, faute de répondre à temps ?
> — Je sais pas… deux ou trois.
> — Et un client, il vous rapporte combien en moyenne ?
> — 400 €.
> — Donc vous perdez entre 3 200 et 4 800 € par mois. Mon service coûte 290 €.

Tu ne vends pas de la technologie. Tu vends **un écart chiffré**. C'est pour ça que ce business a un coût d'acquisition très bas.

## Cibles (Orléans + Loiret)

Plombiers · chauffagistes · électriciens · garagistes · dentistes · kinés · agences immobilières · instituts de beauté · salles de sport · auto-écoles · wedding planners · serruriers.

🚫 **Exclusions absolues** (voir `00-cadre-legal.md`) : filière forêt-bois, hôtellerie orléanaise.

**Critère de sélection :** un numéro WhatsApp Business affiché publiquement + des avis Google mentionnant la réactivité (bonne ou mauvaise). Ce sont tes meilleurs prospects.

## Livraison — 4 h par client

1. **Collecte (30 min, en visio)** — tarifs, zone d'intervention, horaires, prestations, 15 questions fréquentes, règles d'escalade vers l'humain.
2. **Ingestion RAG (1 h)** — les réponses du client deviennent le corpus. `outils/setter-ia/` contient le squelette.
3. **Connexion WhatsApp (1 h)** — WhatsApp Business Platform (API Cloud, gratuit jusqu'à un volume important) ou un intégrateur type Twilio.
4. **Prise de RDV (1 h)** — l'agent écrit dans le Google Calendar du client.
5. **Recette (30 min)** — 20 messages de test, dont 5 pièges. Tu montres au client que l'agent passe la main quand il ne sait pas.

**Règle d'or de livraison :** l'agent doit **toujours** savoir dire « je transmets à [prénom], il vous rappelle ». Un agent qui invente un devis coûte un client. Cadre-le dans le prompt système et teste-le.

## Automatisation (ce qui rend le récurrent réellement récurrent)

Une fois livré, un client te coûte **~20 min/mois** : lire les logs, corriger 2–3 réponses, envoyer le rapport. Le rapport mensuel est généré automatiquement (nombre de conversations, RDV pris, temps de réponse moyen) — c'est ce qui justifie l'abonnement aux yeux du client, et c'est du Python que tu écris une fois.

**C'est ça, ton « automatique ».** Pas 1 000 € qui tombent du ciel : 1 000 € qui demandent 1 h/mois une fois la vente faite.

## Coûts

| Poste | Coût |
|-------|------|
| VPS mutualisé (Hetzner/Scaleway) pour tous les clients | ~5 €/mois |
| API LLM (Claude Haiku 4.5 suffit largement) | ~2–5 €/mois/client |
| WhatsApp Business Platform | Gratuit à ton volume |
| **Total à 4 clients** | **~25 €/mois** |

Marge nette : **> 90 %**.

## Notes

| Critère | Note | Commentaire |
|---------|------|-------------|
| Coût | 5/5 | ~25 €/mois pour 4 clients |
| Rapidité | 4/5 | 3–6 semaines jusqu'au 1ᵉʳ client |
| Simplicité | 4/5 | Trivial pour toi techniquement. Le seul obstacle : oser démarcher. |
| Fit avec ton profil | **5/5** | Tu as déjà construit le produit |

## Ce que tu fais ce soir

1. Ouvre `github.com/pilot-loicrich/chatbot-rag`.
2. Fork-le en `setter-ia`.
3. Remplace le corpus par les données d'un plombier fictif d'Orléans (invente-les, 30 min).
4. Enregistre une **démo écran de 90 secondes** : tu envoies un message WhatsApp, l'agent répond en 2 s et pose un RDV.

Cette vidéo de 90 secondes est ton unique outil de vente. Elle vaut plus que n'importe quel site web.
