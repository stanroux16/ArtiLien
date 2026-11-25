# ArtiLien — service « réponses aux avis Google » (Stan)

Dépôt de contexte pour Claude Code. Ce n'est PAS du code applicatif : le système tourne via des **tâches planifiées cloud** (agents Claude) + un **CRM Google Sheets**. Ce dépôt garde ce que les connecteurs ne donnent pas : décisions de Stan, règles, historique, mode d'emploi.

## Langue et style
- Français, réponses courtes et ciblées (Stan déteste le blabla et les réponses à côté).
- Si la demande est floue : poser des questions de clarification avant de produire.
- Contredire Stan quand son raisonnement ou son plan est faible. Pas de promesses « argent facile », pas de contenu IA générique.

## Ce qui est actif
Service B2B : réponses personnalisées aux avis Google sans réponse, vendues par mail de prospection à des commerces (restaurants, cafés, coiffeurs, etc.). Détail : `docs/plan-avis-google.md`.
**L'ancien « réseau d'artisans » (ArtiLien/ArtisanVoisin) est ARRÊTÉ depuis le 22/11/2026** : ignorer, sauf `docs/archive-reseau-artisans.md` (leçons). Le nom « ArtiLien » est resté (adresse d'envoi artilien.contact@gmail.com, noms des agents).

## Architecture (tout est accessible par connecteurs)
- **3 tâches planifiées** (outil `list_triggers` / `update_trigger` du connecteur Claude_Code_Remote) ; leur prompt complet = la spécification de chaque agent. Les lire avant toute modification :
  - `Avis Google – Prospection` (trig_01TJUL6A2KMTAp4aBSxqda69) : 8h36, 11h36, 14h36, 17h36, lun-ven, modèle Opus
  - `Avis Google – Abonnés` (trig_01AZ66VR1QxqhoFCUDSzZRX6) : 9h47, 12h47, 15h47, 18h47, lun-ven
  - `Avis Google – Suivi et analyse` (trig_0151vvVr4vm2A6LAQQJfmuDZ) : 19h23 lun-ven, expériences A/B + bilan hebdo le lundi
  - Fuseau Europe/Paris ; il peut exister d'autres tâches (liste paginée).
- **CRM** = Google Sheet « Avis Google – CRM » (Drive, dossier « Avis Google »). Onglets : Prospects commerces, Paiements, Abonnés, Journal, Paramètres, Expériences, Suivi hebdo avis, Runs Apify, Dépenses, Compta, Stats quotidiennes/secteurs/avancées. Les agents sont pilotés par des cellules de « Paramètres » (B88 mode d'envoi/pause, B98-B101 modèles de mails, B105 consignes, B106 garde-fous, B116 latitude d'expérimentation + limites fixes, B117 tests en cours). **Retrouver les IDs Drive/Sheets par recherche Drive** (non stockés ici, dépôt public).
- Autres docs Drive : Playbook commercial, Note juridique, dossier Factures (Recettes / Dépenses).
- Outils : Gmail (artilien.contact@gmail.com), Stripe (liens de paiement créés par Stan), Apify (lecture des avis uniquement, plafond 45 $/mois), WebSearch/WebFetch pour trouver commerces et e-mails.

## Limites fixes (ne jamais contourner)
- Mail B2B uniquement, sur adresse **publiée** par le commerce ; identité + source + « répondez STOP » ; désinscrits jamais recontactés ; 1 relance max (2 si test validé).
- Jamais de réponse publiée à la place du commerçant ; aucune promesse de résultat, faux chiffre ou fausse urgence.
- Budget outils 50 €/mois total ; aucun nouvel outil/abonnement payant sans accord de Stan.
- Les agents ne remboursent ni ne paient ni ne résilient (Stripe) : ils lèvent une ALERTE dans le Journal + notification push.
- Pause automatique (Paramètres B88/B106) : >5 % rebonds sur 50 envois, plainte spam ou menace juridique.
- Adresse de test de Stan : jamais traitée comme prospect.
- Ne pas stocker de secrets (clés Stripe/Apify, mots de passe) ici. Ne jamais les demander en clair.

## Comment travailler ici
1. Lire `docs/decisions.md` (chronologie des décisions de Stan) puis `docs/plan-avis-google.md`.
2. Pour changer un comportement d'agent : lire son prompt (`list_triggers`), modifier via `update_trigger`, noter la décision dans `docs/decisions.md` (date + raison). Les consignes dynamiques passent plutôt par les cellules Paramètres.
3. Diagnostiquer avant d'agir : lire Journal, Runs Apify, Stats quotidiennes ; chiffres recalculés, jamais estimés de tête.
4. Proposer d'abord les nouvelles pistes d'optimisation à Stan (demande du 25/11), appliquer ensuite ; Stan veut que Claude applique lui-même les corrections de rendement.
5. Tâches à la charge de Stan (Claude ne peut pas) : liens Stripe, remboursements/résiliations Stripe, démarches URSSAF/impôts, dépôt de ses factures de dépenses dans Drive > Factures > Dépenses.
