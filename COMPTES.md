# Comptes à créer (par Stan) et ce qu'il faut garder

| Service | Pourquoi | Coût | Ce que tu récupères |
|---|---|---|---|
| GitHub | héberger le code | gratuit | un dépôt privé « artilien » |
| Vercel | mettre le site en ligne | gratuit (offre Hobby) ; passer en Pro si usage commercial exigé par leurs conditions | projet relié à GitHub |
| Supabase | base de données UE + connexion | gratuit | URL de la base (`DATABASE_URL`) |
| Mot de passe d'application Gmail | envoyer les mails depuis artilien.contact@gmail.com | gratuit | `GMAIL_APP_PASSWORD` (nécessite la validation en 2 étapes) |
| Compte de service Google | écrire dans le CRM | gratuit | e-mail + clé privée ; partager le Sheet CRM avec cet e-mail en « Éditeur » |
| Cloudflare Turnstile | anti-spam | gratuit | clé de site + clé secrète |
| Nom de domaine | adresse du site, mail pro | ~10 €/an | à choisir |
| Sentry / UptimeRobot | surveillance | gratuit | alertes par mail |

Ne jamais envoyer ces clés dans un message ou dans git : elles vont uniquement dans `apps/web/.env.local` et dans les variables d'environnement Vercel.
