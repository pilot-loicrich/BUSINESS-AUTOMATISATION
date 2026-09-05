# Agent d'automatisation

> Tu as demandé que les actions se fassent **sans ton intervention**. Voici ce qui est réellement automatisé, ce qui ne l'est pas, et pourquoi.

---

## 1. La ligne de partage

Il faut être précis, sinon tu attends de l'agent quelque chose qu'il ne fera pas.

### ✅ Ce qui tourne sans toi, tous les jours

| Tâche | Fréquence | Ce qu'elle fait |
|-------|-----------|-----------------|
| `qualifier` | quotidien | Audite chaque nouveau prospect (GEO), calcule un score de priorité, exclut automatiquement les secteurs interdits |
| `rediger` | quotidien | Écrit un courriel de premier contact personnalisé à partir du résultat d'audit |
| `relancer` | quotidien | Détecte les relances dues (J+3, J+10) et prépare les messages |
| `rapport-client` | **mensuel** | Re-mesure la position de chaque client, compare au mois précédent, rédige le rapport livrable |
| `facturer` | mensuel | Émet les factures d'abonnement, numérotation continue garantie |
| `briefing` | lundi | Fait le point et te dit quoi faire le soir même |

### ❌ Ce qui ne s'automatise pas

| Action | Pourquoi |
|--------|----------|
| **Trouver des prospects** | L'agent ne peut pas inventer des entreprises. Tu remplis `donnees/prospects.csv` — 2 h une fois, puis 20 min par mois. **C'est le seul vrai goulot d'étranglement.** |
| **Envoyer les courriels** | Désactivé par défaut, et c'est délibéré — voir §4. |
| **Passer les appels, tenir les RDV, signer** | C'est le métier. Personne n'achète 290 €/mois à un robot qui l'a démarché. |
| **Livrer un setter IA chez un nouveau client** | Il faut collecter ses tarifs, ses horaires, ses règles. 4 h humaines par client. |

### Le vrai gain, chiffré

L'agent ne remplace pas tes 5–10 h/semaine. Il en supprime la partie administrative :

| | Sans agent | Avec agent |
|---|---|---|
| Audits GEO de prospection | 3 h/semaine | 0 |
| Rédaction des messages | 2 h/semaine | 20 min de relecture |
| Suivi des relances | 1 h/semaine (et tu en oublies) | 0 |
| **Rapports clients mensuels** | **2 h/mois × 4 clients** | **20 min de relecture** |
| Facturation | 1 h/mois | 0 |

**La ligne qui compte est celle des rapports clients.** C'est elle qui décide si tes 190 €/mois sont un revenu récurrent ou un deuxième emploi. Sans automatisation, 4 clients = 4 rapports à écrire chaque mois, indéfiniment. Avec, c'est zéro.

---

## 2. Où ça tourne

**GitHub Actions.** C'est le seul substrat qui répond vraiment à « sans mon intervention » :

- gratuit dans les quotas d'un dépôt privé ;
- tourne **même quand ton PC est éteint** — c'est tout l'intérêt quand tu es en poste de nuit ;
- ton code y est déjà ;
- les secrets y sont gérés proprement.

| Workflow | Cadence | Contenu |
|----------|---------|---------|
| `agent-quotidien.yml` | lun–ven, 06:00 UTC | qualifier + rediger + relancer |
| `agent-hebdo.yml` | lundi, 16:00 UTC | briefing + ouverture d'une issue GitHub |
| `agent-mensuel.yml` | le 1ᵉʳ, 06:00 UTC | rapports clients + factures |

Les crons GitHub sont en **UTC** : compte +2 h en été, +1 h en hiver pour l'heure de Paris. Les cadences sont volontairement larges (une fois par jour) pour que le décalage saisonnier n'ait aucun effet.

**Comment tu reçois le briefing :** l'agent ouvre une **issue GitHub**, ce qui déclenche la notification par courriel de GitHub. Aucun SMTP à configurer.

---

## 3. Mise en service (15 minutes, une seule fois)

### ⚠️ Étape 0 — Passer le dépôt en privé

`donnees/prospects.csv` contient des noms, des courriels et des téléphones professionnels : ce sont des **données personnelles**.

> Settings → General → Danger Zone → **Change repository visibility → Private**

**Les trois workflows refusent de s'exécuter si le dépôt est public.** C'est un garde-fou volontaire, pas un bug : si un workflow échoue avec `Depot PUBLIC`, c'est qu'il fait son travail.

### Étape 1 — Le secret d'API

> Settings → Secrets and variables → Actions → New repository secret

| Nom | Valeur |
|-----|--------|
| `ANTHROPIC_API_KEY` | ta clé `sk-ant-...` |
| `AGENT_SIRET` | ton SIRET (dès que tu l'as) |

### Étape 2 — Les variables

Même écran, onglet **Variables** :

| Nom | Valeur suggérée |
|-----|-----------------|
| `AGENT_VILLE` | `Orleans` |
| `AGENT_EXPLOITANT` | `Loic Nanzo Tonlieu` |
| `AGENT_AUDITS_PAR_JOUR` | `8` |

### Étape 3 — Remplir le fichier de prospects

Copie le format depuis `donnees/exemple-prospects.csv`. Seules **quatre colonnes** sont indispensables au démarrage :

```csv
id,entreprise,secteur,ville,contact,email,telephone,statut,...
P0001,Plomberie Durand,plombier,Orleans,M. Durand,contact@...,0238...,a_qualifier,
```

Laisse `statut` à `a_qualifier` : l'agent remplit tout le reste.

### Étape 4 — Premier essai

> Actions → **Agent — quotidien** → Run workflow

Regarde le journal. Si ça passe, tu n'as plus rien à faire : la suite est automatique.

---

## 4. Pourquoi l'envoi n'est pas automatique par défaut

C'est la décision de conception la plus importante de cet agent, et elle est délibérée.

**La raison technique :** un envoi massif et non relu depuis un domaine neuf détruit sa réputation en quelques jours. Tes messages finissent en spam — y compris ceux adressés à tes vrais clients. Tu grilles l'actif avant de l'avoir construit.

**La raison commerciale :** ton avantage sur ce marché est précisément que tes messages ne ressemblent pas à du publipostage. Un courriel qui cite trois concurrents réels d'une entreprise convertit parce qu'il est vrai et vérifiable. Envoyé sans relecture, il devient exactement ce que tout le monde envoie.

**La raison juridique :** en prospection B2B, tu dois pouvoir répondre de chaque message envoyé en ton nom. Une relecture de 20 secondes te garantit ça.

Le calcul est simple : l'agent te fait gagner ~5 h/semaine. La relecture t'en coûte 20 minutes. **Garder ces 20 minutes est ce qui donne de la valeur aux 5 heures.**

Si tu veux quand même activer l'envoi automatique une fois ton domaine chauffé, passe la variable `AGENT_ENVOI_AUTO` à `true` et implémente le transport SMTP — l'ossature (plafond quotidien, journalisation) est déjà là dans `config.py`.

---

## 5. Utilisation en local

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."

python -m agent quotidien        # qualifier + rediger + relancer
python -m agent briefing         # point de situation immédiat
python -m agent mensuel          # rapports clients + factures
python -m agent --help
```

## 6. Garde-fous intégrés

| Garde-fou | Effet |
|-----------|-------|
| Dépôt public | Les trois workflows refusent de démarrer |
| Secteur interdit | Tout prospect contenant `foret`, `bois`, `scierie`, `hotel`… passe en `exclu` **avant** tout appel API — conflit d'intérêts CNPF et Accor |
| Idempotence | Deux exécutions le même mois ne produisent pas deux factures ; une relance déjà émise ne repart pas |
| Numérotation | Le numéro de facture se déduit des fichiers existants — continu par construction, jamais de trou |
| Panne d'API | Une tâche qui échoue est journalisée, les autres continuent ; le rapport client reste livrable sans sa synthèse rédigée |
| Traçabilité | Toute action est écrite dans `donnees/journal.csv`, et l'historique Git donne le reste |

Le filtre secteur mérite une note : il tourne **avant** l'appel API, donc un prospect interdit n'est jamais audité ni démarché, même si tu l'as saisi par inadvertance. C'est ta protection contre le seul risque sérieux de ce plan — un conflit d'intérêts avec ton employeur.

## 7. Coût

| Poste | Coût mensuel |
|-------|--------------|
| GitHub Actions | 0 € (quotas dépôt privé) |
| API : ~8 audits/jour ouvré | ~4 € |
| API : rédaction des brouillons | ~2 € |
| API : rapports clients mensuels | ~1 € |
| **Total** | **~7 €/mois** |

Soit **7 % de ton budget de 100 €/mois**, pour supprimer environ 5 h de travail hebdomadaire.
