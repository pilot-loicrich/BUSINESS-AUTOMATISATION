# BUSINESS-AUTOMATISATION — Plan 1 000 €/mois récurrent

**Loïc Nanzo Tonlieu** — Alternant Data & IA @ CNPF (Orléans) + Night Auditor @ Novotel
**Objectif :** 1 000 € / mois de revenu récurrent, en 5–10 h/semaine, avec ≤ 100 €/mois de coûts.
**Horizon :** 90 jours (J0 = jour où tu lis ça).

---

## 1. La correction la plus importante avant de commencer

Tu as demandé **« 1 000 € en automatique »** et une **« implémentation instantanée »**. Il faut être direct :

- **Aucun** des 25 business de la vidéo ne produit 1 000 €/mois automatiques sans une phase de travail manuel préalable. L'automatisation vient **après** l'acquisition, jamais avant.
- Ce qui *peut* être instantané, c'est le **lancement** : statut, offre, outils, premiers messages de prospection. C'est exactement ce que contient ce dépôt — prêt à l'emploi.
- Le raccourci réel dans ton cas n'est pas de choisir un business « facile ». C'est d'**arrêter de te vendre comme débutant**. Tu as un RAG en production sur AWS EC2, du FastAPI, du LangChain, du Docker/CI-CD. Un artisan qui paie 300 €/mois pour un agent IA n'achète pas un débutant — il achète exactement ton profil.

**Traduction chiffrée :** un « business débutant » de la vidéo demande 200 h pour atteindre 1 000 €/mois. Une offre B2B adossée à tes compétences réelles demande **4 clients**. C'est tout. Le calcul est en `docs/planning-90-jours.md`.

---

## 2. Les 7 business retenus (et pourquoi ceux-là)

Sur les 25 idées de la vidéo, j'en ai gardé 7 filtrées sur **tes** contraintes : ≤ 100 €/mois, 5–10 h/semaine, compatibles avec un employeur public, et adossées à ta stack.

| # | Business | Idée vidéo | Rôle dans le portefeuille | Récurrent ? | Ticket |
|---|----------|-----------|---------------------------|-------------|--------|
| 1 | [Setter IA WhatsApp](docs/01-setter-ia-whatsapp.md) | n°21 | **Moteur principal** | Oui | 490 € + 290 €/mois |
| 2 | [Agence GEO](docs/02-agence-geo.md) | n°6 | **Moteur secondaire** (même prospect) | Oui | 350 € + 190 €/mois |
| 3 | [Agence de témoignages vidéo](docs/03-agence-temoignages.md) | n°7 | Upsell gros ticket | Non | 690 € / mission |
| 4 | [Agence UGC IA](docs/04-agence-ugc-ia.md) | n°4 | Upsell volume | Oui | 390–690 €/mois |
| 5 | [Micro-SaaS IA de niche](docs/05-micro-saas-ia.md) | n°19/20/22 | Actif long terme | Oui | 9–29 €/mois × N |
| 6 | [Annuaire IA francophone](docs/06-annuaire-ia.md) | n°23 | Actif SEO/GEO | Oui | Listing + affiliation |
| 7 | [Clipping](docs/07-clipping.md) | n°2 | Tampon 0 € (nuits Novotel) | Non | ~1–2 $/1000 vues |

### L'insight qui change tout

**Les business 1, 2, 3 et 4 partagent le même fichier de prospects et le même geste commercial.**

Ce ne sont pas quatre business. C'est **une agence avec quatre offres**. Tu démarches une fois un dentiste orléanais ; tu peux lui vendre un setter IA, un audit GEO, des témoignages vidéo et de l'UGC. C'est précisément ce qui rend l'objectif atteignable en 5–10 h/semaine — sinon il ne l'est pas.

Les business 5 et 6 se construisent **en fond**, le dimanche, sans prospection. Le 7 se fait **pendant tes gardes de nuit**, sur les temps morts.

### Les 18 idées écartées — et pourquoi

| Idée | Motif d'exclusion |
|------|-------------------|
| 1 Revente de dons | Déplacements + stockage. Incompatible avec 35 h + nuits. |
| 3 Live selling | Stock + créneaux fixes le soir = conflit direct avec le Novotel. |
| 8 Communauté payante | Exige une audience préexistante. Tu n'en as pas encore. |
| 9 Dropshipping IA | Budget pub > 100 €/mois. Exclu par ta contrainte. |
| 10 Affiliation TikTok Shop | 500 abonnés requis + visage + exposition publique commerciale (voir `docs/00-cadre-legal.md`). |
| 11 Influenceuse IA | 6–12 mois avant le premier euro. Hors horizon. |
| 12 Photobooth 360 | 300–500 € de matériel **et** prestations le week-end — tu bosses au Novotel le week-end. |
| 13 App photos mariage | Dev long + démarchage terrain le week-end. Même conflit. |
| 14 Cookie dough | Local commercial, autorisations sanitaires, présence physique. |
| 15 Bonbons lyophilisés | ~4 000 € de machine. Hors budget. |
| 16 Compléments animaux | Plusieurs milliers d'€ de stock marque blanche. Hors budget. |
| 17 E-commerce caritatif | Stock physique + logistique. |
| 18 Ghost writer relations | Faisable techniquement, mais marché saturé d'apps clones ; le n°5 couvre mieux ce créneau. |
| 19/20/22 Apps IA | **Fusionnées dans le business n°5** — c'est le même geste : une app IA de niche. |
| 24 Collecteur d'argent | Cadre juridique lourd (démarchage successoral, RGPD, quasi-intermédiation). Trop risqué à côté d'un employeur public. |
| 25 E-commerce féminin | Stock + design produit + sourcing. Hors budget et hors compétences. |

---

## 3. Le chemin vers 1 000 €/mois

```
2 clients Setter IA      2 × 290 €  =  580 €/mois
2 clients GEO            2 × 190 €  =  380 €/mois
                                      ─────────────
                          RÉCURRENT =  960 €/mois

+ 1 mission témoignage tous les 2 mois  ≈ +345 €/mois lissé
                                      ─────────────
                              TOTAL  ≈ 1 305 €/mois
```

**4 clients.** Voilà le vrai chiffre. Pas 100 000 vues, pas 500 abonnés, pas un stock.

Le setup (490 € + 350 €) rapporte en plus **1 680 € de one-shot** pendant la phase d'acquisition, ce qui finance largement tes 100 €/mois d'outils.

---

## 4. Ordre de lecture

1. **`docs/00-cadre-legal.md`** — à lire **avant tout le reste**. Tu as répondu que tu ne savais pas ce que tu as le droit de faire. Ce document répond, et contient le mail à envoyer à ton employeur.
2. **`docs/planning-90-jours.md`** — le calendrier semaine par semaine, calé sur ton emploi du temps réel.
3. **`docs/01-...` à `07-...`** — une fiche par business : offre, prix, script de vente, livraison.
4. **`docs/scripts-prospection.md`** — mails, DM LinkedIn et script téléphonique prêts à copier.
5. **`outils/`** — le code qui tourne dès maintenant.

## 5. L'agent d'automatisation

`agent/` tourne sur **GitHub Actions** — donc sans toi, et même quand ton PC est éteint (utile en poste de nuit).

| Il fait seul | Il ne fait pas |
|--------------|----------------|
| Auditer les prospects (GEO) et les prioriser | **Trouver** les prospects — tu remplis le CSV |
| Rédiger les courriels de premier contact | Les envoyer (relecture de 20 s, délibérément) |
| Détecter et préparer les relances J+3 / J+10 | Passer les appels, tenir les RDV, signer |
| **Produire les rapports clients mensuels** | Livrer un setter IA chez un nouveau client |
| Émettre les factures | |
| Te briefer le lundi avant le créneau de 20 h | |

La ligne qui compte est celle des **rapports clients** : c'est elle qui décide si tes 190 €/mois sont un revenu récurrent ou un deuxième emploi. Sans elle, 4 clients = 4 rapports à écrire chaque mois, indéfiniment.

Coût : **~7 €/mois** d'API, pour supprimer ~5 h de travail hebdomadaire.

**Mise en service et garde-fous : `agent/README.md`.**
⚠️ Le dépôt doit être **privé** — les workflows refusent de tourner sinon.

## 6. Outils livrés

| Outil | Ce qu'il fait |
|-------|---------------|
| `agent/` | L'automatisation complète (voir ci-dessus) |
| `outils/geo-audit/` | Génère un rapport d'audit GEO vendable (350 €) pour une entreprise, en une commande. C'est ton argument de vente n°1. |
| `outils/setter-ia/` | Squelette FastAPI d'agent WhatsApp : qualification, réponse, prise de RDV. Ta base de livraison client. |
| `outils/suivi/` | Tableau de bord local (revenus, pipeline), branché sur l'état de l'agent. |
| `templates/` | Devis et facture conformes micro-entreprise. |
| `donnees/` | L'état de l'agent entre deux exécutions. **Données personnelles — dépôt privé obligatoire.** |

---

## 7. Avertissement

Ce dépôt est un plan d'affaires, pas un conseil juridique, fiscal ou comptable. Les seuils et taux cités dans `docs/00-cadre-legal.md` sont indicatifs et évoluent chaque année : **vérifie-les sur `urssaf.fr`, `entreprendre.service-public.fr` et `impots.gouv.fr` avant de t'engager**, et fais valider ton cumul d'activité par le service RH du CNPF.
