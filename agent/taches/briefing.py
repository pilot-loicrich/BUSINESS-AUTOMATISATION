"""Briefing hebdomadaire : ce qu'il reste a faire humainement.

Publie le lundi en fin d'apres-midi, avant le creneau de prospection de 20h.
L'agent a deja tout prepare : le briefing dit quoi faire de ce qu'il a produit.
"""

from __future__ import annotations

from datetime import date, timedelta

from ..config import SORTIES
from ..etat import lire_clients, lire_journal, lire_prospects, metriques

DOSSIER = SORTIES / "briefings"


def _barre(valeur: float, objectif: float, largeur: int = 24) -> str:
    pleins = round(min(valeur / objectif, 1.0) * largeur) if objectif else 0
    return "`[" + "#" * pleins + "." * (largeur - pleins) + "]`"


def construire() -> str:
    m = metriques()
    prospects = lire_prospects()
    clients = lire_clients()
    depuis = date.today() - timedelta(days=7)
    journal = lire_journal(depuis)

    lignes: list[str] = []
    a = lignes.append

    a(f"# Briefing — semaine du {date.today().strftime('%d/%m/%Y')}")
    a("")

    # --- Revenu
    a("## Ou tu en es")
    a("")
    a(f"- **MRR : {m.mrr:.0f} EUR/mois** {_barre(m.mrr, 1000)} {m.mrr / 1000:.0%} de l'objectif")
    a(f"- Clients actifs : {m.clients_actifs}")
    if m.manque_objectif > 0:
        panier = m.mrr / m.clients_actifs if m.clients_actifs else 240
        a(f"- Reste a signer : **{m.manque_objectif / panier:.1f} client(s)** au panier actuel ({panier:.0f} EUR)")
    else:
        a("- **Objectif atteint.** Prochain palier : augmenter les tarifs de 15 % pour les nouveaux.")
    a("")

    # --- Ce que l'agent a fait
    a("## Ce que l'agent a fait cette semaine")
    a("")
    compte: dict[str, int] = {}
    for ligne in journal:
        compte[ligne["action"]] = compte.get(ligne["action"], 0) + 1
    if compte:
        for action, nombre in sorted(compte.items(), key=lambda x: -x[1]):
            a(f"- {action} : {nombre}")
    else:
        a("- Rien. Verifie que les workflows GitHub Actions tournent.")
    a("")

    # --- Ce qui t'attend
    brouillons = sorted(
        (p for p in prospects if p.get("statut") == "brouillon"),
        key=lambda p: int(p.get("score") or 0),
        reverse=True,
    )
    a("## Ce qui t'attend ce soir a 20h")
    a("")
    if brouillons:
        a(f"**{len(brouillons)} brouillons prets** dans `sorties/brouillons/`. "
          "Relis, corrige la premiere phrase si elle sonne faux, envoie.")
        a("")
        a("| Priorite | Entreprise | Secteur | Cite par l'IA | Score |")
        a("|----------|------------|---------|---------------|-------|")
        for p in brouillons[:12]:
            a(f"| {p.get('score', '')} | {p['entreprise']} | {p.get('secteur', '')} "
              f"| {p.get('cite_par_ia', '?')} | {p.get('score', '')} |")
        a("")
        a("Les premiers de la liste sont ceux qui sont absents des reponses IA "
          "alors que leurs concurrents y sont : la douleur se demontre en une "
          "capture d'ecran.")
    else:
        a("Aucun brouillon en attente.")
        a("")
        restants = m.par_statut.get("a_qualifier", 0)
        if restants == 0:
            a("**Ton fichier de prospects est vide.** C'est le seul vrai blocage : "
              "l'agent ne peut pas inventer des entreprises. Bloque 2 h ce week-end "
              "pour ajouter 40 lignes dans `donnees/prospects.csv` "
              "(Google Maps + PagesJaunes).")
        else:
            a(f"{restants} prospects attendent d'etre qualifies — l'agent les "
              "traitera dans les prochains jours.")
    a("")

    # --- RDV et suites
    rdv = [p for p in prospects if p.get("statut") == "rdv"]
    if rdv:
        a("## Rendez-vous a honorer")
        a("")
        for p in rdv:
            a(f"- **{p['entreprise']}** — {p.get('contact', '')} — {p.get('telephone', '')} "
              f"— {p.get('notes', '')}")
        a("")

    # --- Alertes
    alertes: list[str] = []
    if m.contacts_7j < 20:
        alertes.append(
            f"**{m.contacts_7j} contacts emis cette semaine, cible : 20.** "
            "C'est le seul indicateur que tu controles a 100 %, et celui qui "
            "produit le MRR avec 4 a 6 semaines de decalage."
        )
    sans_rapport = [
        c for c in clients
        if c.get("statut") == "actif" and "geo" in c.get("offre", "").lower()
        and (c.get("dernier_rapport") or "")[:7] != date.today().strftime("%Y-%m")
    ]
    if sans_rapport:
        alertes.append(
            f"{len(sans_rapport)} client(s) sans rapport ce mois-ci : "
            + ", ".join(c["entreprise"] for c in sans_rapport)
        )
    erreurs = [l for l in journal if l["action"] == "erreur"]
    if erreurs:
        alertes.append(f"{len(erreurs)} erreur(s) dans le journal — voir `donnees/journal.csv`.")

    if alertes:
        a("## Alertes")
        a("")
        for alerte in alertes:
            a(f"- {alerte}")
        a("")

    a("---")
    a("")
    a("*Genere automatiquement. L'agent prepare ; toi tu envoies, tu appelles "
      "et tu signes — ces trois-la ne s'automatisent pas.*")

    return "\n".join(lignes) + "\n"


def executer() -> dict:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    contenu = construire()
    fichier = DOSSIER / f"{date.today().isoformat()}.md"
    fichier.write_text(contenu, encoding="utf-8")
    # Le workflow lit ce fichier pour en faire le corps d'une issue GitHub.
    (SORTIES / "briefing-courant.md").write_text(contenu, encoding="utf-8")
    return {"briefing": fichier.name}
