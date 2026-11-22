# ArtiLien – consignes pour Claude Code

## Le projet
ArtiLien met en relation des **particuliers** (petits chantiers, ≤ 500 m²) et des **artisans du bâtiment** à Montpellier (34), Strasbourg (67) et Lyon (69). Gratuit pour les particuliers ; l'artisan paie une mise en relation acceptée (1er client 10 €, puis paliers 49/99/199/399 € selon le lot, plafond 1 000 €). Fondateur : Stanislas Roux (EI, SIREN 133060277, SIRET 13306027700018). Contact : artilien.contact@gmail.com. Langue de tout le produit : **français**.

Le cahier des charges complet (pages, formulaires, légal, design, e-mails, critères d'acceptation) est dans le fichier `docs/cahier-des-charges.md` (à y copier depuis le doc Claude : https://claude.ai/artifact/2qib8dwX7RBheNBEMXNNmh). En cas de doute, il fait foi ; en cas de contradiction avec ce fichier, demande.

## Contraintes de Stan (à respecter toujours)
- Moins d'1 h/semaine de son temps ; budget outils ≤ 50 €/mois → services gratuits ou très peu chers, aucune maintenance manuelle.
- Le site tourne en permanence sur le cloud (hébergeur géré, aucun serveur à administrer).
- Stan n'est pas développeur : explique en français simple, une étape à la fois, dis exactement ce qu'il doit cliquer ou créer.
- Ne jamais écrire de secret dans le code ni dans git. Tout passe par les variables d'environnement (`.env.example`).

## Architecture (monorepo pnpm)
- `packages/shared` : schémas Zod, constantes (zones, types de travaux, prix), design tokens. **Source unique** pour le web et le mobile.
- `apps/web` : Next.js (App Router) + TypeScript + Tailwind. Formulaires en actions serveur.
- `apps/mobile` : Expo (React Native) + expo-router, pour particuliers et artisans.
- Base : PostgreSQL géré en UE (Supabase, région Paris/Francfort). Connexion unique, rôle `particulier` ou `artisan`.
- CRM : Google Sheet `1EnXTRxewvqUGFKJQ79TjkCUnmk0XY_BWFuss8nJ5RDI` (les agents IA le lisent). Le site écrit dans les onglets « Réponses au formulaire 1 », « Inscriptions artisans », « Retours refus », en respectant l'ordre des colonnes existantes (demande à Stan ou lis les en-têtes via l'API avant d'écrire).
- Mails : depuis artilien.contact@gmail.com (nodemailer + mot de passe d'application) tant qu'il n'y a pas de nom de domaine ; ensuite Resend/Brevo avec SPF/DKIM/DMARC.

## Règles métier et légales
- Trois consentements distincts et non précochés dans le formulaire particulier ; conserver la preuve (date, version du texte, IP tronquée). Les textes exacts viennent de Stan/du Conseiller juridique : ne jamais les inventer, laisser `[Texte à valider]`.
- On ne donne **jamais** les coordonnées d'un artisan au particulier (seulement une fiche sans contact). Le contact du particulier n'est transmis à l'artisan qu'après paiement.
- RGPD : minimisation, hébergement UE, désinscription en un clic (STOP), durée de conservation définie, pas de revente de données, cookies strictement nécessaires par défaut.
- Aucune prospection automatisée par téléphone/SMS/réseaux sociaux sur la rénovation énergétique ou l'adaptation du logement.
- Mentions légales : « ArtiLien – Stanislas Roux, EI – SIREN 133060277 ».

## Design (direction C : moderne, façon application)
Fond sombre #0E1730, surfaces #16224A, bordures #2C3C66, texte #E8ECF5, secondaire #B8C2D9, accent orange #F28C28, marine #1B2A49. Titres Space Grotesk, texte Inter. Boutons pill (rayon 999), hauteur ≥ 48 px, cartes rayon 24. Logo : monogramme « A » dont la barre est un maillon orange (piste C) ; maquettes : https://claude.ai/artifact/6UddRyqAbUefBbFHSi9VaM. Les couleurs viennent de `packages/shared/src/tokens.ts`, jamais codées en dur.
Accessibilité : visée WCAG 2.2 AA (contraste, focus visible, labels, erreurs annoncées, `prefers-reduced-motion`).

## Conventions de code
- TypeScript strict, aucune erreur `pnpm typecheck` avant de conclure une tâche.
- Toute entrée utilisateur est validée côté serveur avec les schémas Zod de `packages/shared` ; texte échappé dans les mails ; valeurs envoyées au Sheet neutralisées (pas de formule).
- Pas de dépendance ajoutée sans raison ; préférer l'offre gratuite d'un service.
- Messages d'erreur et textes d'interface en français, ton direct et rassurant.
- Commits courts, en français, un sujet par commit. Ne pas pousser sur `main` sans que `pnpm typecheck` et `pnpm build:web` passent.

## Commandes
`pnpm install` · `pnpm dev:web` (http://localhost:3000) · `pnpm dev:mobile` (Expo) · `pnpm typecheck` · `pnpm build:web`
Après `pnpm install` côté mobile, exécute `npx expo install --fix` dans `apps/mobile` pour aligner les versions Expo.

## Points ouverts (ne pas décider seul)
Nom de domaine ; textes des 3 consentements ; questions du formulaire de refus ; délai de rappel ; présentation publique de l'équipe d'agents IA et photo de Stan ; fond sombre sur tout le site ou seulement accueil + app ; logo C à confirmer.
