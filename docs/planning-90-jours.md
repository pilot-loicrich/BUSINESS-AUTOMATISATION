# Planning 90 jours

**Contrainte :** 5–10 h/semaine, en plus de 35 h au CNPF et des gardes au Novotel.
**Objectif :** 960 €/mois récurrent + one-shots à J+90.

---

## Ta semaine type (7 h)

| Créneau | Durée | Activité | Pourquoi ce créneau |
|---------|-------|----------|---------------------|
| **Lundi 20 h–21 h 30** | 1 h 30 | **Prospection** — 20 contacts, toujours le même geste | Le lundi, les artisans traitent leur semaine. Meilleur taux de réponse. |
| **Mercredi 20 h–21 h 30** | 1 h 30 | Relances + rendez-vous téléphoniques | Un prospect se relance à J+3, pas à J+10 |
| **Samedi 9 h–12 h** | 3 h | **Livraison client** (bloc profond) | Seul créneau long et non fragmenté de ta semaine |
| **Dimanche 18 h–19 h** | 1 h | Actif de fond (annuaire ou micro-SaaS) | Petit, mais tenu chaque semaine |
| Gardes de nuit | variable | Clipping, sur temps morts uniquement | Temps déjà perdu (voir réserves dans `07-clipping.md`) |

**La règle qui décide de tout :** le créneau du **lundi soir est non négociable**. Si tu ne prospectes qu'une seule fois par semaine, c'est celui-là. Tous les autres peuvent sauter ; celui-là jamais. C'est le seul qui produit du chiffre d'affaires.

---

## Phase 1 — Semaines 1 à 2 : armer

Objectif : être **prêt à vendre**, pas encore vendre.

| Sem. | Tâches |
|------|--------|
| **S1** | ☐ Lire `00-cadre-legal.md` en entier<br>☐ Relire les contrats CNPF **et** Novotel (clause d'exclusivité)<br>☐ Envoyer le mail d'information aux RH du CNPF<br>☐ Déclarer la micro-entreprise sur `formalites.entreprises.gouv.fr`<br>☐ Forker `chatbot-rag` → `setter-ia`, corpus plombier fictif<br>☐ **Enregistrer la démo de 90 secondes** |
| **S2** | ☐ Lancer `geo-audit` sur 3 entreprises réelles d'Orléans → 3 rapports<br>☐ Construire le fichier de **60 prospects** (voir ci-dessous)<br>☐ Préparer les modèles de devis et facture (`templates/`)<br>☐ Ouvrir le compte bancaire dédié<br>☐ Démarrer le clipping (2 campagnes) |

### Constituer le fichier de 60 prospects

Une seule séance de 2 h. Colonnes : entreprise · secteur · contact · téléphone · WhatsApp affiché ? · nb d'avis Google · cité par l'IA ? · statut.

Sources : Google Maps (recherche par métier + Orléans), PagesJaunes, annuaires de fédérations professionnelles, groupes Facebook locaux d'artisans.

**Filtre de qualification :** garde en priorité ceux qui affichent un WhatsApp Business **et** qui ne sortent pas dans ton audit GEO. Ce sont des prospects à double douleur — tu leur vends deux offres.

🚫 Rappel : aucune entreprise de la filière forêt-bois, aucun hôtel orléanais.

---

## Phase 2 — Semaines 3 à 6 : vendre

Objectif : **2 clients signés**.

| Sem. | Objectif | Indicateur |
|------|----------|------------|
| **S3** | 20 premiers contacts (mail + relance) | 3–5 réponses |
| **S4** | 20 contacts + 2 rendez-vous tenus | 1 audit GEO vendu (350 €) |
| **S5** | 20 contacts + livraison du 1ᵉʳ audit | **1ᵉʳ setter IA signé** (490 € + 290 €/mois) |
| **S6** | Livraison du setter + relance des tièdes | **2ᵉ client signé** |

**Chiffres à connaître avant de commencer** — ils t'évitent d'abandonner à tort :

- 20 contacts → ~4 réponses → ~2 rendez-vous → ~1 vente.
- Il te faut donc **environ 80 contacts pour 4 clients**. À 20/semaine, c'est **4 semaines**.
- **19 personnes sur 20 ne répondront pas. C'est normal, ce n'est pas un signal d'échec.** C'est le point exact où la plupart des gens arrêtent — et c'est la seule vraie raison pour laquelle ce plan échoue quand il échoue.

---

## Phase 3 — Semaines 7 à 10 : consolider

| Sem. | Objectif |
|------|----------|
| **S7** | 3ᵉ client. Automatiser le rapport mensuel du setter IA. |
| **S8** | 4ᵉ client. **Palier 960 €/mois récurrent atteint.** |
| **S9** | 1ʳᵉ mission témoignage **gratuite** chez un client existant → portfolio |
| **S10** | 1ʳᵉ mission témoignage **facturée** (690 €). Activer l'UGC IA si la trésorerie suit. |

---

## Phase 4 — Semaines 11 à 13 : bâtir l'après

Le récurrent tourne et te coûte ~2 h/mois. Tu réinvestis le temps libéré dans les actifs.

| Sem. | Objectif |
|------|----------|
| **S11** | Choisir la niche du micro-SaaS · page d'atterrissage en ligne |
| **S12** | 20 messages de validation dans les communautés · **seuil : 20 inscrits** |
| **S13** | Bilan trimestriel · augmenter les tarifs de 15 % pour les **nouveaux** clients |

---

## Jalons de contrôle

| Date | Jalon | Si non atteint |
|------|-------|----------------|
| J+14 | Micro-entreprise déclarée, démo enregistrée, 60 prospects listés | Tu n'as pas commencé. Bloque un samedi entier. |
| J+30 | 40 contacts émis, 2 rendez-vous tenus | Problème de **volume**, pas de message. Passe à 30 contacts/semaine. |
| J+45 | 1ᵉʳ euro encaissé | Problème de **message ou de cible**. Change de secteur, pas de business. |
| J+60 | 2 clients récurrents (580 €/mois) | Tiens bon. C'est la phase où la courbe est plate avant de monter. |
| J+90 | 4 clients (960 €/mois) + 1 one-shot | **Objectif atteint.** |

---

## Le tableau de bord

Tiens `outils/suivi/` à jour **chaque lundi soir**, en 5 minutes. Deux indicateurs seulement comptent au début :

1. **Nombre de contacts émis cette semaine** — le seul que tu contrôles à 100 %
2. **MRR** (revenu mensuel récurrent) — le seul qui compte à l'arrivée

Le premier produit le second, avec 4 à 6 semaines de décalage. Ce décalage est la raison pour laquelle il faut suivre le premier : sinon, pendant six semaines, tu as l'impression que rien ne marche.
