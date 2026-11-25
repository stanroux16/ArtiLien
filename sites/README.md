# Générateur de maquettes de sites (activité « Sites web pour commerçants »)

Génère un site statique de 5 pages (accueil, présentation, contact + formulaire, mentions légales, politique de confidentialité) à partir d'un fichier JSON. 4 thèmes métiers : `batiment`, `beaute`, `bouche`, `auto` (3 palettes chacun, voir `THEMES` dans `build.py`).

## Utilisation (agents)
1. Créer `clients/<slug>.json` (copier un exemple `demo-*.json` du bon secteur). Le dossier `clients/` du dépôt ne contient QUE des démos fictives : ne jamais y commiter un vrai prospect (dépôt public).
2. `python3 build.py clients/<slug>.json` → site dans `dist/<slug>/` (ignoré par git).
3. Publier `dist/<slug>/` sur Hostinger sous `https://<DOMAINE>/m/<slug>/` (skill `hostinger:deploy-to-hosting`, envoi de fichiers via le connecteur Hostinger, JAMAIS par commit dans ce dépôt public). Vérifier que l'URL répond (200).
4. Noter slug, URL et date dans l'onglet « Maquettes » du CRM.

## Champs du JSON
`slug` (ascii, minuscules, tirets : `ville-metier-nom`), `secteur` (batiment|beaute|bouche|auto), `nom`, `metier`, `ville`, `zone` (facultatif), `tel`, `email`, `adresse`, `titre` ([ligne 1, ligne 2 du titre]), `slogan`, `accroche`, `presentation` ([paragraphe 1, paragraphe 2]), `dirigeant`, `fonction`, `icone_logo` (voir `ICONS`), `cta`, `palette` (facultatif), `agence` (nom dans le bandeau), `services` (facultatif : liste de `{icone, titre, texte}`), `horaires` (facultatif), `legal` (facultatif : forme, siret, tva, directeur, reglemente, mediateur), `maquette` (true par défaut : bandeau + noindex + robots.txt).

## Règles de contenu (maquettes de prospects)
- Utiliser uniquement des informations PUBLIQUES du commerce (nom, ville, adresse, téléphone, e-mail publié, horaires publiés, services visibles sur Google Maps / annuaires / Facebook).
- N'inventer AUCUN fait : pas d'ancienneté, de chiffre, de certification, d'assurance, de distinction, de nombre d'avis, de prénom. Texte neutre et honnête ; les photos restent des cadres « à fournir ».
- Les mentions légales gardent leurs champs surlignés « à compléter » : ne rien inventer (SIRET etc.).
- Une maquette sans réponse est supprimée après 30 jours.

## Fiche de choix client
`FICHE_CLIENT.md` : envoyée par mail après le « OK » du commerçant. Les réponses sont recopiées dans `Clients sites` du CRM puis appliquées dans le JSON.
