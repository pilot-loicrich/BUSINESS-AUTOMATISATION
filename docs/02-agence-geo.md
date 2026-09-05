# 02 — Agence GEO (référencement sur les IA)  ⭐ MOTEUR SECONDAIRE

> Idée n°6 de la vidéo. Se vend **au même prospect, dans le même rendez-vous** que le setter IA. C'est ce cumul qui rend l'objectif atteignable en 5–10 h/semaine.

## Le principe

Des centaines de millions de personnes demandent chaque semaine à ChatGPT, Claude ou Gemini « quel est le meilleur dentiste à Orléans ». Les modèles citent trois ou quatre noms. **Tous les autres n'existent pas.**

Le GEO (*Generative Engine Optimization*) consiste à travailler la présence d'une entreprise dans ces réponses. C'est le SEO d'il y a vingt ans : quasi personne ne s'en occupe encore en France, et le marché va se refermer.

## Pourquoi c'est parfait en complément du n°1

- **Même fichier de prospects.** Zéro coût d'acquisition marginal.
- **Même rendez-vous.** Tu vends deux offres en un déplacement.
- **La vente se fait toute seule** : tu montres un écran où ses trois concurrents sont cités et lui non. Le choc fait le travail à ta place.
- **Coût : 0 €**, hors quelques centimes d'API.

## L'offre

| Ligne | Prix |
|-------|------|
| Audit GEO initial (rapport 8–12 pages + plan d'action) | **350 €** (une fois) |
| Suivi mensuel : mise en œuvre, re-mesure, rapport de position | **190 €/mois** |

L'audit se vend **seul**, sans engagement. C'est ta porte d'entrée : le client teste ton sérieux à 350 €, puis prend le suivi. Taux de conversion audit → suivi observé sur ce type d'offre : élevé, parce que le rapport crée l'inquiétude et propose le remède dans le même document.

## L'outil que je t'ai livré

`outils/geo-audit/` génère le rapport en une commande :

```bash
python -m geo_audit --ville "Orléans" --metier "plombier" --entreprise "Plomberie Durand"
```

Il interroge le modèle sur plusieurs formulations de la question, compte qui est cité et à quelle fréquence, situe l'entreprise cible, et produit un rapport Markdown vendable. Détails dans `outils/geo-audit/README.md`.

**Ce script est ton produit d'appel.** Tu peux lancer un audit gratuit sur un prospect *avant* de le contacter, et attaquer ton mail par le résultat. C'est ce qui fait la différence entre un mail ignoré et un rendez-vous.

## Ce que contient concrètement la prestation

Le GEO n'est pas magique, et il ne faut rien promettre qu'on ne puisse tenir. Ce qui marche réellement :

1. **Fiche Google Business Profile** complète, catégorisée, à jour — c'est la source la plus citée par les moteurs pour le local.
2. **Cohérence NAP** (nom, adresse, téléphone) identique partout : annuaires, réseaux, site.
3. **Présence dans les annuaires et comparateurs** que les modèles ingèrent (PagesJaunes, annuaires sectoriels, plateformes d'avis).
4. **Page « à propos » structurée** en langage naturel, répondant explicitement aux questions posées aux IA (« qui intervient en urgence à Orléans le dimanche ? »).
5. **Données structurées Schema.org** (`LocalBusiness`) sur le site.
6. **Volume et fraîcheur d'avis** — les modèles s'appuient massivement dessus.
7. **Mentions dans la presse locale et les blogs** — le levier le plus lourd, et le plus durable.

## Honnêteté commerciale (ça te protège)

Ne garantis **jamais** une position. Tu ne contrôles pas les modèles, et ils changent. Vends une **obligation de moyens mesurée** :

> « Je ne peux pas vous garantir que ChatGPT vous citera. Personne ne le peut. Ce que je garantis, c'est qu'on mesure votre position aujourd'hui, qu'on met en place tout ce qui influence cette position, et qu'on la re-mesure chaque mois. Vous verrez la courbe. »

Cette phrase te distingue immédiatement des vendeurs de vent — qui sont déjà nombreux sur ce créneau.

## Notes

| Critère | Note |
|---------|------|
| Coût | 5/5 (~2 €/mois d'API) |
| Rapidité | 4/5 — un audit peut se vendre dès la 2ᵉ semaine |
| Simplicité | 4/5 — l'outil fait le gros du travail |
| Fit avec ton profil | 4/5 |

## Ce que tu fais ce soir

Lance l'audit sur **3 entreprises réelles d'Orléans** dans 3 secteurs différents. Tu obtiens 3 rapports. Ce sont à la fois ton portfolio et tes 3 premiers prospects — tu les contactes avec leur propre rapport en pièce jointe.
