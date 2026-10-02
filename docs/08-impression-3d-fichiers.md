# 08 — Impression 3D : vendre les fichiers, pas les objets

> Issue de la **2ᵉ vidéo de Yomi Denzel** (7 machines physiques), business n°2 — l'imprimante 3D.
> Rôle dans le portefeuille : **actif de fond du dimanche**, en remplacement du clipping (fiche `07`).
> ⚠️ Ce n'est **pas** une priorité. Lis la section 9 avant de commander quoi que ce soit.

---

## 1. Pourquoi celle-ci, et aucune des six autres

La vidéo note les machines sur le coût, la simplicité et le potentiel. Ces notes ne te servent à rien : elles ignorent ta contrainte réelle — **35 h au CNPF, des nuits au Novotel, 5 à 10 h par semaine, pas de capital, pas de week-ends.**

Le seul critère qui compte dans ton cas : **est-ce que la machine produit pendant que je ne suis pas là ?**

| Machine | Produit sans toi ? | Ce qui la disqualifie chez toi |
|---|---|---|
| **2. Imprimante 3D** | **Oui, 4 h seule** | — |
| 3. Brodeuse numérique | Oui, mais montage manuel par pièce | 450 € + stock de vêtements à avancer |
| 1. Pistolet à tufting | Non, 100 % manuel | 3 tapis/semaine = la totalité de tes 10 h |
| 5. Presse DTF | Non | Son argument de vente est « je livre demain » — tu ne peux pas |
| 4. Machine à bougie | Non | Le canal, ce sont les marchés le week-end — tu travailles |
| 6. Graveur laser | Non | Fumées et extraction d'air en appartement |
| 7. *(absente de la retranscription)* | ? | Non évaluée |

Les six autres partagent le même défaut structurel : **le temps consommé est proportionnel au chiffre d'affaires.** Deux fois plus de ventes = deux fois plus d'heures. Tu n'as pas ces heures, et tu ne les auras pas avant août 2028.

---

## 2. Les trois choses à ne pas confondre

C'est le point que tout le monde rate sur ce business.

| | Ce que tu vends | Verdict |
|---|---|---|
| **Objets imprimés** | Ton **temps** : impression, emballage, poste | ❌ 1 000 €/mois ≈ 70 colis/mois. C'est un emploi. |
| **Fichiers** | Ton **cerveau** : le design paramétrique | ✅ Conçu une fois, vendu N fois. |
| **L'imprimante** | Rien — c'est un **outil** | ✅ 200 € une fois. Indispensable. |

### L'imprimante n'est pas optionnelle, même pour vendre des fichiers

Quatre raisons concrètes :

1. **Valider.** Un modèle a des porte-à-faux, des tolérances, des retraits. Un fichier qui ne s'imprime pas chez l'acheteur = avis 1 étoile et remboursement. Impossible à savoir sans l'avoir imprimé.
2. **Les photos de la pièce réelle *sont* l'argument de vente.** Une fiche avec des photos de l'objet vend ; une fiche avec un rendu 3D ne vend pas.
3. **Le canal d'acquisition, c'est la vidéo de l'impression en cours.** Sans machine, pas de contenu, pas de trafic. C'est exactement ce que fait le lycéen de la vidéo.
4. **Les plateformes récompensent la preuve.** Makerworld et Printables ont des programmes de primes liés à l'usage réel des modèles.

Donc : **200 € d'investissement, oui.** Mais la machine ne gagne pas d'argent en imprimant — elle en gagne en te permettant de concevoir et de prouver.

---

## 3. Ton avantage déloyal : le paramétrique en Python

C'est la seule des 7 machines où ton M1 IA & Data compte.

Le design 3D paramétrique s'écrit en code. **`CadQuery` et `build123d` sont des bibliothèques Python.** Tu écris une fonction, tu passes des paramètres, et une boucle `for` sort la famille entière.

Ce n'est pas théorique — c'est livré dans `outils/modeles-3d/` et testé :

```
$ python generateur.py --catalogue
129 variante(s) a produire
...
129 reference(s) produites, 0 echec(s).
```

**129 références prêtes à publier**, chacune avec son STL validé, son estimation de filament et son texte d'annonce rédigé. En une commande.

Ton concurrent sur Makerworld modélise à la main dans Fusion 360 : il en sort une par soirée.

### Pourquoi un bac de rangement, et pas un accessoire de Crocs

Le modèle livré est un bac de rangement modulaire. Ce choix est raisonné :

- **Le paramétrage EST la valeur.** Tous les tiroirs font une taille différente. 129 variantes répondent à 129 besoins réels ; un modèle figé n'en sert qu'un. Un accessoire de Crocs, au contraire, n'a qu'une taille utile — le paramétrique n'y apporte rien.
- **Demande permanente**, pas une mode. Les accessoires de Crocs cités dans la vidéo sont déjà saturés : l'exemple date, et le créneau s'est refermé.
- **Imprimable sans support**, donc aucun avis négatif sur la difficulté d'impression.
- **Aucune propriété intellectuelle de tiers** — voir le piège n°1 ci-dessous.

---

## 4. Le modèle économique : où ça devient vraiment récurrent

La vente de fichiers à l'unité reste du one-shot. La structure qui correspond à ton objectif, c'est **l'abonnement à une bibliothèque de modèles** :

```
200 abonnés × 5 €/mois = 1 000 €/mois
```

Tu publies 4 à 6 nouveaux modèles par mois — ce que la génération paramétrique te permet de faire en quelques heures le dimanche — et les abonnés paient pour l'accès continu.

C'est exactement le business n°8 de la première vidéo (communauté à abonnement), mais avec un produit tangible au lieu d'un cours. Et c'est là que ton avantage technique paie deux fois : tu alimentes la bibliothèque plus vite que quiconque.

### Où publier, et comment chaque canal paie

| Canal | Mécanisme | Rôle |
|---|---|---|
| **Makerworld** (Bambu Lab) | Programme de points/primes lié à l'usage des modèles | Acquisition — le plus gros trafic |
| **Printables** (Prusa) | Programme de récompenses similaire | Acquisition, audience complémentaire |
| **Cults3D** | Tu fixes ton prix, la plateforme prend une commission | Revenu direct à l'unité |
| **Abonnement (Patreon ou équivalent)** | Abonnement mensuel à la bibliothèque | **Le revenu récurrent** |
| **TikTok / Instagram** | Vidéos d'impression | Le moteur de trafic vers tout le reste |

Les conditions et taux de ces programmes changent souvent : **vérifie-les sur chaque plateforme avant de bâtir dessus.** Le gratuit (Makerworld, Printables) sert à se faire connaître ; le payant (Cults3D, abonnement) encaisse.

---

## 5. Les trois pièges que la vidéo ne mentionne pas

### Piège 1 — Les licences des modèles existants

Les modèles gratuits de Printables et Makerworld sont très majoritairement sous licence **Creative Commons non commerciale**. Imprimer les « dragons articulés » cités dans la vidéo pour les revendre **viole la licence de leur auteur**.

C'est une raison de plus de ne publier que tes propres modèles : le générateur livré produit du code que tu as écrit, donc des fichiers dont tu es l'auteur. Aucune ambiguïté.

Inversement, **choisis explicitement la licence de ce que tu publies.** Le générateur écrit une mention de licence dans chaque fiche ; adapte-la via `--licence`.

### Piège 2 — Ton statut

| Tu vends | Catégorie | Conséquence |
|---|---|---|
| Des **objets** imprimés | BIC — vente de marchandises | Seuil de CA et taux de cotisations différents ; activité à déclarer en plus |
| Des **fichiers** | Prestation / cession de droits | Même case que ton activité de services actuelle |

Vendre des fichiers, c'est donc aussi un tracas administratif en moins. Vérifie les seuils et taux applicables sur `urssaf.fr` et `impots.gouv.fr` — ils évoluent.

### Piège 3 — Les chiffres de la vidéo

Le lycéen à 17–20 k$/mois et la créatrice au million d'euros sont des **cas extrêmes, portés par une percée virale**. Ce sont des exemples réels, mais ce ne sont pas des médianes. La médiane sur ces plateformes est très basse, et la majorité des boutiques ne dépassent jamais quelques dizaines d'euros par mois.

Ce qui est solide dans ce business, ce n'est pas le plafond : c'est le **plancher**. 200 € de risque, et un actif qui ne se déprécie pas.

---

## 6. Le déroulé réaliste

| Phase | Quoi | Revenu attendu |
|---|---|---|
| **Mois 1–2** | Achat imprimante (~200 €, A1 mini ou Ender). Prise en main. Tu imprimes et **tu vends quelques objets** — pour la trésorerie, les photos et comprendre la demande. | 100–300 € au total |
| **Mois 3–5** | Bascule : tes modèles paramétriques publiés sur Makerworld + Cults3D. Comptes TikTok/Instagram des impressions. | 100–400 €/mois |
| **Mois 6–12** | Ouverture de l'abonnement bibliothèque. Les objets ne sont plus qu'un support marketing. | montée vers 1 000 €/mois |

Oui, tu vends des objets **au début** — mais comme un moyen, pas comme le modèle final.

**Budget total engagé : ~250 €** (imprimante + 2 bobines), une seule fois. Aucun coût mensuel.

---

## 7. Le créneau horaire

**Dimanche 18 h–20 h, 2 h.** Le même créneau que celui prévu pour l'annuaire IA dans `planning-90-jours.md`.

Tu ne touches **ni** au lundi soir (prospection, le seul créneau qui produit du chiffre d'affaires), **ni** au samedi matin (livraison client).

L'impression tourne pendant que tu es au CNPF ou en garde de nuit. C'est tout l'intérêt.

---

## 8. L'outil livré

`outils/modeles-3d/` — générateur paramétrique testé, voir son `README.md`.

```bash
pip install cadquery
cd outils/modeles-3d
python generateur.py --catalogue          # 129 références : STL + fiche + index
python generateur.py --largeur 120 --hauteur 60 --colonnes 3
```

Produit pour chaque variante : le `.stl` (binaire, validé), une fiche `.md` prête à coller dans l'annonce (dimensions, réglages d'impression, filament estimé, licence), et un `index.csv` de l'ensemble.

---

## 9. Notes — et la priorité

| Critère | Note | Commentaire |
|---|---|---|
| Coût | 5/5 | ~250 € une fois, zéro mensuel |
| Rapidité | **2/5** | **6 à 12 mois avant un revenu stable** |
| Simplicité technique | 5/5 | C'est du Python. Ton terrain. |
| Simplicité commerciale | 2/5 | Il faut construire une audience |
| Fit avec ton profil | 5/5 | La seule des 7 machines où ton code compte |
| Potentiel à 12 mois | 4/5 | 1 000 €/mois crédible via l'abonnement |

### L'avertissement qui compte

Ce business met **6 à 12 mois** avant un revenu stable. Le plan GEO + setter IA met **6 à 8 semaines** pour les mêmes 1 000 €, avec 4 clients, et il est déjà outillé et automatisé sur ce dépôt.

> **Si tu transfères tes 10 h/semaine de la prospection du lundi soir vers l'imprimante, tu repousses tes 1 000 € de six mois.**

Celui-ci est la **8ᵉ ligne du portefeuille**. Deux heures le dimanche, pas une de plus, et seulement après que le créneau du lundi soir est tenu depuis un mois.
