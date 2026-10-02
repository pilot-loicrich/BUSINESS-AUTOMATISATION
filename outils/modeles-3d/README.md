# modeles-3d — générateur de modèles paramétriques

Génère une famille de modèles 3D imprimables **et leurs fiches produit**, en une commande. Support du business n°8 (`docs/08-impression-3d-fichiers.md`).

## Installation

```bash
pip install cadquery       # ~500 Mo, compte 2-3 min
```

## Utilisation

```bash
cd outils/modeles-3d

# La famille complète : 129 références
python generateur.py --catalogue

# Un essai rapide
python generateur.py --catalogue --max 10

# Une cote sur mesure (commande client)
python generateur.py --largeur 120 --profondeur 90 --hauteur 60 --colonnes 3

# Ta propre licence sur les fiches
python generateur.py --catalogue --licence "CC BY-NC 4.0"
```

### Options

| Option | Défaut | Rôle |
|---|---|---|
| `--catalogue` | — | Génère la famille entière au lieu d'un seul modèle |
| `--max N` | — | Plafonne le nombre de variantes |
| `--largeur/--profondeur/--hauteur` | 100/80/50 | Dimensions en mm |
| `--colonnes/--rangees` | 1/1 | Compartiments en X et en Y |
| `--epaisseur` | 2.0 | Parois et fond |
| `--rayon` | 4.0 | Congé des angles verticaux |
| `--prise` | 0 | Chanfrein de préhension sur l'arête avant haute |
| `--sans-empilement` | — | Retire la feuillure d'empilement |
| `--sortie` | `sortie/` | Dossier de destination |
| `--licence` | usage personnel | Mention portée dans chaque fiche |

## Ce qui est produit par variante

| Fichier | Contenu |
|---|---|
| `<réf>.stl` | Le solide, STL binaire, prêt à trancher |
| `<réf>.md` | **La fiche d'annonce** : dimensions, réglages d'impression, filament estimé, licence |
| `index.csv` | Récapitulatif de toutes les références (masse, volume, taille de fichier) |

La génération de la fiche est le vrai gain de temps : publier 129 modèles demande 129 descriptions. Ici elles sortent avec les STL.

## Le modèle livré

Un **bac de rangement modulaire empilable**. Choix raisonné, détaillé dans `docs/08-impression-3d-fichiers.md` §3 : le paramétrage *est* la valeur (tous les tiroirs font une taille différente), la demande est permanente et non soumise à une mode, la pièce s'imprime sans support, et il n'y a aucune propriété intellectuelle de tiers.

Caractéristiques géométriques :
- angles verticaux adoucis, intérieur congé
- cloisons montant à 2 mm sous le bord (bord continu = pièce plus solide et impression plus propre)
- feuillure inférieure de 1,2 mm avec 0,4 mm de jeu, pour empiler
- chanfrein de préhension optionnel
- **aucune surface en surplomb** : imprimable sans support

## Validation

Chaque variante est vérifiée à la construction (`isValid()`), et les cotes incohérentes sont rejetées explicitement par `Parametres.valider()` plutôt que de produire un solide cassé. Une variante en échec n'interrompt pas le lot.

Les STL produits ont été contrôlés : en-tête binaire conforme, nombre de triangles cohérent avec la taille du fichier.

## Étendre à d'autres modèles

`modele.py` ne contient que la géométrie, `generateur.py` l'orchestration. Pour un nouveau produit, écris un nouveau `modele_xxx.py` exposant `Parametres` et `construire()`, et réutilise le générateur tel quel.

C'est là que se trouve l'effet cumulatif : **le second modèle te coûte un dixième du premier**, parce que l'export, les fiches, l'index et la validation sont déjà écrits.
