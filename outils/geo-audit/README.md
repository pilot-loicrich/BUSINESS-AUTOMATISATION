# geo-audit — générateur de rapport d'audit GEO

Interroge un modèle avec plusieurs formulations de « quel est le meilleur *[métier]* à *[ville]* ? », compte qui est cité, situe l'entreprise auditée, et produit un rapport Markdown vendable **350 €**.

## Installation

```bash
cd outils/geo-audit
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."     # ou : ant auth login
```

## Utilisation

```bash
# Audit d'une entreprise précise
python -m geo_audit --ville "Orléans" --metier "plombier" --entreprise "Plomberie Durand"

# Cartographie d'un secteur (pour repérer des prospects)
python -m geo_audit --ville "Orléans" --metier "dentiste"

# Audit approfondi
python -m geo_audit --ville "Orléans" --metier "garagiste" \
    --entreprise "Garage Dupont" --requetes 16 --sortie rapports/dupont.md
```

| Option | Défaut | Rôle |
|--------|--------|------|
| `--ville` | requis | La ville visée |
| `--metier` | requis | Le métier au singulier (`plombier`, pas `plomberie`) |
| `--entreprise` | — | Omis : cartographie du secteur seul, sans cible |
| `--requetes` | 8 | Nombre de formulations testées |
| `--modele` | `claude-opus-5` | Modèle interrogé |
| `--sortie` | `rapports/<slug>.md` | Fichier de sortie |

## Coût

Environ **2 à 5 centimes par audit** (8 requêtes courtes). Tu peux en lancer cent pour le prix d'un café.

## Les deux usages, dans cet ordre

**1. Prospection (avant le contact).** Lance la version sans `--entreprise` sur un métier. Tu obtiens la liste de ceux que l'IA cite. **Tes meilleurs prospects sont ceux qui n'y sont pas** — tu les trouves sur Google Maps, et tu les contactes avec le mail 1 de `docs/scripts-prospection.md`.

**2. Livraison (après la vente).** Lance la version avec `--entreprise` et `--requetes 16`. C'est le livrable à 350 €. Relis-le, ajoute deux captures d'écran de conversations réelles, exporte en PDF.

## Ce que le rapport contient

1. Le constat — cité combien de fois sur combien
2. Le classement des concurrents, avec barres de présence
3. Les raisons avancées par le modèle
4. La mise en perspective économique
5. Le plan d'action en 6 points, par impact décroissant
6. Ce qui est mesuré chaque mois (justifie l'abonnement à 190 €)
7. La méthode et ses limites

## Honnêteté du livrable

Le rapport contient explicitement, en section 6, la phrase qui te protège :

> « La position sur les moteurs IA n'est pas garantie et personne ne peut la garantir. Ce qui est garanti, c'est la mesure. »

Ne la retire pas. C'est elle qui te distingue des vendeurs de vent sur ce créneau — et c'est aussi elle qui t'évite un litige.

## Limites connues

- Un modèle peut se tromper ou méconnaître un tissu local. Quand c'est le cas, le rapport le dit (`aucune_connaissance`) plutôt que d'inventer.
- L'audit reflète **un** modèle à **une** date. C'est précisément pourquoi la prestation est mensuelle et non ponctuelle.
- Ne présente jamais ce rapport comme une mesure de « ce que fait ChatGPT » si tu as interrogé un autre modèle. Nomme le modèle — il est déjà écrit dans l'en-tête du rapport.
