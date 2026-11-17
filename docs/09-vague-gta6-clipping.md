# 09 — Vague GTA 6 : le tuto clipping de A à Z

> GTA 6 sort le **jeudi 19 novembre 2026** (PS5 et Xbox, pas de PC). Ce document est le mode d'emploi complet pour en tirer un revenu **sans console, sans visage et sans budget** : tu découpes les meilleurs moments de streamers qui jouent, dans le cadre de campagnes qui te paient aux vues.
> C'est la mise en pratique de la fiche `07-clipping.md`, calée sur le calendrier de la sortie.

---

## 0. Le calcul, une fois pour toutes

Une campagne paie un **taux pour 1 000 vues**, avec un **minimum** par clip (en dessous, rien) et un **plafond** par clip (au-dessus, rien de plus).

| Repère (novembre 2026) | Valeur |
|---|---|
| Taux médian observé sur les campagnes ouvertes | ~1,09 $ pour 1 000 vues |
| Fourchette courante | 0,50 à 1,50 $ |
| Commission de la plateforme sur tes paiements | ~10 % |

Donc, à 1 $ les 1 000 vues :

```
100 000 vues validées  ->  ~90 $ nets
300 $ nets             ->  ~330 000 vues validées
```

La distribution est très inégale : la plupart des clips font quelques centaines de vues, un sur plusieurs dizaines décolle. Ton levier est le **volume régulier pendant le pic**, pas le clip parfait.

> La configuration détaillée de la chaîne YouTube est dans **`10-chaine-youtube-configuration.md`** et celle de TikTok dans **`11-compte-tiktok-configuration.md`**.

---

## 1. Aujourd'hui — mise en place (2 h)

### 1.1 Le compte de paiement

1. Crée ton compte sur **Whop**, puis ouvre **Content Rewards** (la place de marché des campagnes de clipping).
2. Fais **tout de suite** la vérification d'identité et renseigne ton moyen de retrait : c'est l'étape qui prend du délai, et tu ne veux pas la découvrir le jour où tu demandes ton premier paiement.

### 1.2 Les comptes de publication

Crée **deux comptes dédiés** : TikTok et YouTube (pour les Shorts). Ajoute Instagram seulement si une campagne retenue l'exige.

- Une adresse mail **neuve**, sans lien avec ton nom ni avec ton employeur.
- Un nom de niche clair, du type « clips GTA 6 FR ». **Pas** de logo Rockstar, pas de « officiel », pas le nom d'un streamer : c'est un motif de suppression.
- Photo, bio d'une ligne, et c'est tout.

### 1.3 Les outils (gratuits)

| Besoin | Outil |
|---|---|
| Montage, recadrage vertical, sous-titres | CapCut |
| Repérage automatique des moments forts sur une longue vidéo | Opus Clip (offre gratuite limitée) |
| Suivi de tes clips et de tes gains | `outils/clipping/suivi_clips.py` |

```bash
python outils/clipping/suivi_clips.py --init    # crée donnees/clips.csv
```

### 1.4 Le statut

Ces revenus sont **imposables**. Si ta micro-entreprise n'est pas encore déclarée, fais-le maintenant (`00-cadre-legal.md` §4) : c'est elle qui te permet de les encaisser proprement.

---

## 2. Samedi et dimanche — choisir 2 ou 3 campagnes

Dans Content Rewards, cherche les campagnes de **streamers et créateurs gaming** qui joueront à GTA 6 dès la sortie. Lis la page de règles de chacune : **c'est elle qui fait foi**, et elle peut changer en cours de campagne.

### La grille de choix

| Critère | Ce que tu veux |
|---|---|
| Taux pour 1 000 vues | ≥ 1 $ |
| Minimum par clip | Bas. À 1 $ de taux, un minimum de 2 $ exige déjà 2 000 vues par clip |
| Plafond par clip | Le plus haut possible |
| Budget restant | Plus de la moitié. Une campagne presque vide s'arrête avant ton paiement |
| Plateformes acceptées | TikTok et/ou Shorts |
| **Origine des vues exigée** | Vérifie : certaines campagnes ne comptent que les vues d'un pays donné. Un compte français publie surtout vers la France — privilégie les **streamers francophones** ou les campagnes sans restriction |
| Source imposée | Les VOD et lives du streamer, ou un dossier fourni |
| Mentions obligatoires | Hashtag, identification du streamer, texte en légende : note-les |

Prends **2 ou 3 campagnes**, jamais une seule : si l'une ferme ou rejette tes clips, les autres continuent.

---

## 3. Du samedi 14 au mercredi 18 — roder les comptes

Un compte qui publie pour la première fois le jour J part de zéro. Usage courant : lui donner quelques jours d'activité normale avant.

- **2 clips par jour** sur chaque compte, tirés des campagnes déjà ouvertes (réactions aux bandes-annonces, attentes sur le jeu).
- 10 minutes par jour à regarder et aimer du contenu GTA depuis ces comptes, pour que la plateforme les classe dans la bonne niche.
- Pas d'abonnements en masse, pas d'achat d'abonnés ni de vues : c'est le **bannissement définitif** de la campagne et la perte des gains en attente.

**Lundi 16, 20 h : prospection GEO + setter, comme d'habitude.** Ce créneau ne bouge pas.

---

## 4. La fabrication d'un clip — 15 minutes

### 4.1 Trouver le moment (5 min)

La méthode la plus rapide : sur la chaîne Twitch du streamer, onglet **Clips**, tri sur **24 dernières heures**. Les spectateurs ont déjà repéré les meilleurs moments pour toi. Tu retrouves ensuite le passage dans la VOD pour le recouper proprement.

Ce qui marche sur un lancement :
- la **première fois** (première mission, première poursuite, première mort absurde) ;
- la **réaction** forte du streamer — rire, cri, silence ;
- le **bug** ou la situation improbable ;
- le **détail** que personne n'avait vu.

### 4.2 Monter (8 min)

1. Coupe entre **20 et 45 secondes**. Commence une seconde avant l'action, pas dix.
2. Recadre en **vertical 9:16** : le jeu en grand, la caméra du streamer en bandeau.
3. Pose un **texte d'accroche** visible dès la première seconde.
4. Ajoute les **sous-titres** automatiques et corrige les fautes.
5. Ajoute les mentions exigées par la campagne.

Accroches qui fonctionnent, à adapter :

- « Il n'aurait jamais dû ouvrir cette porte »
- « 3 heures de jeu et il découvre ça »
- « La police de GTA 6 ne pardonne rien »
- « Personne n'avait remarqué ce détail »
- « Sa réaction quand il comprend »

### 4.3 Publier, soumettre, noter (2 min)

1. Publie sur le compte prévu par la campagne.
2. **Soumets le lien** du clip dans la campagne. Un clip non soumis n'est jamais payé.
3. Ajoute une ligne dans `donnees/clips.csv`, avec les minutes passées.

---

## 5. Du jeudi 19 au jeudi 3 décembre — le rythme

Je table sur deux semaines de pic d'audience. Ton budget : **45 minutes par jour**, sur des temps morts.

| Moment | Action | Durée |
|---|---|---|
| Matin | Repérage : clips Twitch des dernières 24 h de tes 2-3 streamers | 10 min |
| Midi | 1 clip monté et publié | 15 min |
| Soir | 1 ou 2 clips, publiés entre 18 h et 21 h | 20 min |

**Objectif : 3 clips par jour, soit ~45 clips en deux semaines.**

Le jeudi 19 et le vendredi 20 comptent double : les premiers lives produisent les moments les plus partagés, et beaucoup de streamers joueront dès le déblocage du jeu. Le repérage du **vendredi matin** est le plus important de toute l'opération.

Chaque dimanche, 15 minutes : lance le bilan, regarde quels formats et quelle campagne ont payé, et **ne refais que ça** la semaine suivante.

---

## 6. Se faire payer

1. Après approbation du clip et vérification des vues, **demande le paiement** dans la campagne.
2. La commission (~10 %) est retirée à ce moment-là.
3. Retire ensuite ton solde vers ton compte.

Tu perds le gain d'un clip si : il est rejeté, il n'atteint pas le minimum, des vues sont jugées artificielles, ou ton compte est banni. Donc : **ne supprime jamais un clip soumis**, et ne touche à aucun service de « boost » de vues.

Des litiges de détection de fausses vues arrivent même à des clippers honnêtes : garde tes captures d'écran de statistiques.

---

## 7. Jeudi 3 décembre — la décision

```bash
python outils/clipping/suivi_clips.py
```

Le script applique à chaque clip la règle de sa campagne (minimum, plafond, commission) et rapporte ton **gain acquis par heure passée**.

| Résultat | Décision |
|---|---|
| Au-dessus de 8 par heure | Continue, uniquement sur les campagnes du haut du tableau |
| En dessous, mais l'essentiel attend l'approbation | Re-mesure 7 jours plus tard |
| En dessous, et tout est réglé | Arrête. Ces heures rapportent plus en prospection |

Le seuil se change avec `--seuil`. Il est volontairement modeste : c'est le niveau en dessous duquel une heure de clipping vaut moins qu'une heure à chercher ton prochain client à 290 €/mois.

---

## 8. Les règles qui te protègent

- **Uniquement dans le cadre d'une campagne** qui t'autorise à utiliser le contenu du streamer. Hors campagne, découper le contenu de quelqu'un t'expose à une réclamation.
- **Aucune image du jeu avant le 19** : les séquences issues de copies fuitées sont retirées.
- **Pas de cinématiques isolées** : Rockstar fait retirer les vidéos qui ne montrent que les scènes d'histoire. Clippe du jeu et des réactions.
- **La politique de Rockstar vise l'usage non commercial** des images de ses jeux : un clip payé aux vues est une zone grise, et l'accord d'un streamer ne couvre pas les images de l'éditeur. Une réclamation peut te faire perdre un clip ; détail et parades dans `10-chaine-youtube-configuration.md` §5 bis.
- **Apporte quelque chose** : accroche, cadrage, sous-titres. Un extrait brut republié est classé « contenu non original » et peu diffusé.
- **Pendant tes gardes au Novotel**, seulement si ton poste le permet réellement (`00-cadre-legal.md` §2).
- **Comptes sans lien** avec ton identité professionnelle.

---

## 9. Après la vague

Deux comptes rodés avec quelques milliers d'abonnés restent un actif : tu peux enchaîner sur d'autres campagnes sans repartir de zéro, et ce que tu auras appris sur les accroches sert directement à l'offre UGC (`04-agence-ugc-ia.md`).

Si les comptes n'ont pas pris, tu arrêtes sans avoir dépensé un euro.

---

*Chiffres et règles relevés mi-novembre 2026. Les taux, la commission et les conditions de chaque campagne changent : la page de la campagne fait foi.*
