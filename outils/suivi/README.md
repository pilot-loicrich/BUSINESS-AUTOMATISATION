# suivi — tableau de bord

```bash
python outils/suivi/suivi.py --init   # une seule fois
python outils/suivi/suivi.py          # chaque lundi soir, 30 secondes
```

Affiche : MRR et progression vers 1 000 €, état du pipeline, taux de conversion réels, relances en retard.

## Les deux seuls chiffres qui comptent

1. **Contacts émis cette semaine** — le seul que tu contrôles à 100 %
2. **MRR** — le seul qui compte à l'arrivée

Le premier produit le second avec 4 à 6 semaines de décalage. C'est pour ça qu'il faut suivre le premier : sinon, pendant six semaines, tu as l'impression que rien ne marche alors que tout se met en place.

## Statuts

`a_contacter` → `contacte` → `relance` → `rdv` → `client` (ou `perdu`)

Un prospect `perdu` se recontacte à 3 mois. Ne supprime jamais de ligne.

## ⚠️ Données personnelles

`prospects.csv` et `clients.csv` contiennent des données personnelles (noms, téléphones professionnels) et sont **exclus du dépôt Git** par `.gitignore`. Ne les commite jamais, ne les publie nulle part.

Tes obligations RGPD en prospection B2B, en bref :
- **Base légale :** intérêt légitime, à condition que le message soit en rapport avec la fonction professionnelle de la personne — c'est le cas ici.
- **Information :** chaque mail doit permettre de s'opposer (une phrase suffit : « dites-le-moi et je n'insisterai pas » — elle est déjà dans les scripts de relance).
- **Opposition :** si quelqu'un demande à ne plus être contacté, supprime-le et ne le recontacte jamais.
- **Durée :** ne conserve pas indéfiniment un prospect jamais converti (3 ans après le dernier contact est l'usage courant).

Ces règles sont peu contraignantes et te coûtent deux lignes dans tes scripts. Les ignorer t'expose inutilement.
