# Générateur de maquettes de sites (activité « Sites web pour commerçants »)

Génère un site statique de 5 pages (accueil, présentation, contact + formulaire, mentions légales, politique de confidentialité) à partir d'un fichier JSON. 4 thèmes métiers : `batiment`, `beaute`, `bouche`, `auto` (3 palettes chacun, voir `THEMES` dans `build.py`).

## Utilisation (agents)
1. Créer `clients/<slug>.json` (copier un exemple `demo-*.json` du bon secteur). Le dossier `clients/` du dépôt ne contient QUE des démos fictives : ne jamais y commiter un vrai prospect (dépôt public).
2. `python3 build.py clients/<slug>.json` → site dans `dist/<slug>/` (ignoré par git).
3. Publier `dist/<slug>/` dans le dépôt PRIVÉ `stanroux16/artilien-maquettes`, dossier `m/<slug>/` (commit + push sur main ; Hostinger déploie automatiquement sur `https://<DOMAINE>/m/<slug>/` en ≈ 1 min). JAMAIS de commit de maquette dans ce dépôt public. Vérifier l'URL avec WebFetch (le shell ne joint pas le domaine).
4. Noter slug, URL et date dans l'onglet « Maquettes » du CRM.

## Champs du JSON
`slug` (ascii, minuscules, tirets : `ville-metier-nom`), `secteur` (batiment|beaute|bouche|auto), `nom`, `metier`, `ville`, `zone` (facultatif), `tel`, `email`, `adresse`, `titre` ([ligne 1, ligne 2 du titre]), `slogan`, `accroche`, `presentation` ([paragraphe 1, paragraphe 2]), `dirigeant`, `fonction`, `icone_logo` (voir `ICONS`), `cta`, `palette` (facultatif), `agence` (nom dans le bandeau), `services` (facultatif : liste de `{icone, titre, texte}`), `horaires` (facultatif), `legal` (facultatif : forme, siret, tva, directeur, reglemente, mediateur), `maquette` (true par défaut : bandeau + noindex + robots.txt).
Choix du client (brochure) : `palette` (clé du secteur : A/B/C = ordre dans `THEMES`), `police` (absent = police du secteur ; `classique` ; `moderne`), `logo` (`icone` par défaut, `capitales`, `souligne`, `deux-lignes`, `point`, `encadre`, `serif` ; numéros 1 à 7 dans cet ordre), `ton` (A convivial, B sérieux, C haut de gamme : à appliquer en réécrivant `accroche` et `presentation`), `prix_install` / `prix_abo` (facultatifs, affichés dans la brochure), `contact_agence` (adresse de réponse, défaut artilien.contact@gmail.com).

## Règles de contenu (maquettes de prospects)
- Utiliser uniquement des informations PUBLIQUES du commerce (nom, ville, adresse, téléphone, e-mail publié, horaires publiés, services visibles sur Google Maps / annuaires / Facebook).
- N'inventer AUCUN fait : pas d'ancienneté, de chiffre, de certification, d'assurance, de distinction, de nombre d'avis, de prénom. Texte neutre et honnête ; les photos restent des cadres « à fournir ».
- Les mentions légales gardent leurs champs surlignés « à compléter » : ne rien inventer (SIRET etc.).
- Une maquette sans réponse est supprimée après 30 jours.

## Fiche de choix client
`FICHE_CLIENT.md` : envoyée par mail après le « OK » du commerçant. Les réponses sont recopiées dans `Clients sites` du CRM puis appliquées dans le JSON.

## Brochure de personnalisation
Chaque build produit aussi `personnalisation.html` (page non listée, noindex) et `personnalisation.pdf` (rendu par Chrome sans interface, A4, ≈ 5 pages) : couleurs (A/B/C), polices (A/B/C), 7 logos texte sur fond clair et foncé, tons (A/B/C), photos (A/B/C), sections en plus, informations à envoyer, ce qui est inclus. Elle est envoyée au client APRÈS son « OK » (lien `https://<DOMAINE>/m/<slug>/personnalisation.html` + PDF en pièce jointe), le client répond par codes (« Couleurs B – Police A – Logo 3 – Ton C – Photos A »).

## Polices
Polices locales (`fonts/`, licence OFL, copiées dans chaque `dist/<slug>/fonts/`) : aucune requête vers Google (RGPD, rendu identique partout, PDF fidèle). Pour en ajouter : fichier `.woff2` `latin` de `@fontsource/<police>` + entrée dans `FONT_WEIGHTS`.
