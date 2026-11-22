# Plan de construction : étapes et consignes à donner à Claude Code

Chaque étape : colle la consigne dans Claude Code, laisse-le travailler, puis vérifie le « critère » avant de passer à la suivante. Le squelette actuel contient déjà : monorepo, schémas Zod partagés, design tokens, accueil, page demande (formulaire + écriture au CRM + mail de confirmation), page artisans (tarifs), accueil de l'app mobile.

## Étape 0 – Mise en place (Stan, ~30 min) : voir COMPTES.md
Créer GitHub, Vercel, Supabase, mot de passe d'application Gmail, compte de service Google, Cloudflare Turnstile. Copier `.env.example` en `apps/web/.env.local`.

## Étape 1 – Vérifier le squelette
Consigne : « Lis CLAUDE.md et PLAN.md. Lance `pnpm install`, `pnpm typecheck`, `pnpm build:web`, puis `pnpm dev:web` et dis-moi ce qui marche. Corrige les erreurs sans changer l'architecture. »
Critère : site visible sur localhost:3000.

## Étape 2 – Branchement du CRM et du mail (réel)
Consigne : « Lis l'onglet « Réponses au formulaire 1 » du Sheet (en-têtes) via l'API Google et aligne l'ordre des colonnes écrites dans `lib/actions.ts`. Ajoute la colonne « Référence site ». Teste l'envoi d'une demande de bout en bout : ligne dans le Sheet + mail reçu. »
Critère : une demande test apparaît dans le Sheet et le mail arrive (pas en spam).

## Étape 3 – Pages du site
Consigne : « Construis les pages décrites dans docs/cahier-des-charges.md section 4 (accueil complète, pour les particuliers, pour les artisans, comment ça marche, tarifs, ce qu'on vérifie, à propos, FAQ, contact, zones, mentions légales, confidentialité, CGV, cookies, 404) avec la direction de design C. Ajoute Cloudflare Turnstile sur tous les formulaires. »
Critère : toutes les pages de la section 3 du cahier existent, Lighthouse ≥ 90.

## Étape 4 – Base de données et fiabilité
Consigne : « Ajoute Supabase (PostgreSQL UE) : table `soumissions`, `consentements`, `artisans`. Les formulaires enregistrent d'abord en base, puis une tâche synchronise vers le Sheet avec 5 reprises (1, 5, 15 min, 1 h, 6 h) et alerte Stan par mail en cas d'échec. Ajoute la synchronisation inverse des statuts Désinscrit/Refus/Opposition toutes les 15 minutes (cron Vercel). »
Critère : couper l'accès au Sheet ne perd aucune soumission.

## Étape 5 – Formulaire artisan
Consigne : « Construis le formulaire d'inscription artisan en 5 étapes (section 5.2) : vérification du SIRET via l'API recherche-entreprises.api.gouv.fr (entreprise active), CGV à accepter, écriture dans l'onglet « Inscriptions artisans », mail de confirmation. »
Critère : un SIRET invalide ou radié est refusé avec un message clair.

## Étape 6 – Formulaires restants et mails
Consigne : « Construis : retour après refus, contact, désinscription STOP (lien signé HMAC avec TOKEN_SECRET), liste d'attente, et les 8 e-mails transactionnels de la section 10 (HTML sobre + version texte). »
Critère : chaque formulaire écrit au bon endroit, chaque mail est reçu.

## Étape 7 – App mobile
Consigne : « Dans apps/mobile, construis : connexion (Supabase Auth, e-mail + lien magique), rôle particulier ou artisan. Particulier : nouvelle demande (mêmes schémas Zod), suivi du statut. Artisan : liste des demandes reçues, accepter/refuser, notifications push. Utilise les design tokens partagés. »
Critère : l'app tourne dans Expo Go sur un téléphone, les deux rôles fonctionnent.

## Étape 8 – Sécurité et mise en ligne
Consigne : « Fais la revue de sécurité de la section 9.5 (en-têtes, limitation de débit, validation, secrets), configure Sentry et UptimeRobot, branche le nom de domaine, passe les mails sur le domaine (SPF/DKIM/DMARC), déploie sur Vercel (région Paris/Francfort). »
Critère : site en ligne en HTTPS, alerte reçue si le site tombe.

## Étape 9 – Publication de l'app
Compte Apple Developer (99 €/an) et Google Play (25 € une fois) : hors budget mensuel, à décider avec Stan avant. Build avec EAS (offre gratuite).
