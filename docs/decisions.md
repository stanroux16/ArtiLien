# Décisions de Stan — service avis Google (chronologie)

- 22/11 : arrêt total du réseau d'artisans ; bascule vers réponses aux avis Google (restaurants/cafés, coiffeurs/instituts ; santé exclue), toute la France, prospection par mail écrit ; offre 90/120/150 € ; objectif 1 000 € en 40-60 jours ; réutilise CRM, Stripe, Apify, Gmail, micro-entreprise ; budget outils ≤ 50 €/mois.
- 22/11 : pilote automatique dès le 23/11, Stan n'intervient plus ; envoi automatique direct ; garde artilien.contact@gmail.com comme adresse d'envoi ; liens Stripe créés par Stan ; test complet avec une adresse de test perso (jugé concluant).
- 22/11 : ajout de l'abonnement 49 €/mois (sans engagement, annulable par mail).
- 23/11 : 25 mails par session « pour l'instant » (bilan le soir) ; diversifier les secteurs ; mails HTML léger plus visuel (test validé).
- 23/11 : objectif = optimiser les chiffres suivis par jour dans le CRM (mails/€ Apify, dépense/client gagné, ROI).
- 23/11 : on propose aussi aux commerces à beaucoup d'avis sans réponse ; 60 avis max par commande pour le prix du palier.
- 24/11 : objectif ≥ 30 mails envoyés par € Apify d'ici une semaine ; Claude diagnostique puis applique directement (filtrer les lieux sans e-mail avant de payer, meilleurs secteurs/villes, réglage de l'actor) ; Stan dépose lui-même ses factures de dépenses dans Drive > Factures > Dépenses.
- 25/11 : arrêt d'Apify pour chercher les commerces → mode hybride (recherche web sans Apify ; Apify seulement pour lire les avis des finalistes).
- 25/11 : grande marge d'expérimentation pour les agents (prix et paliers, offre/garantie, mails/timing, nouvelles cibles) pour maximiser le bénéfice net puis le CA ; canal supplémentaire autorisé : formulaire de contact du site (pas de DM ni courrier) ; limites fixes : règles légales, 50 €/mois, jamais de publication à la place du client, pas de nouvel abonnement payant ; compte rendu = bilan hebdo dans le CRM + push le lundi, sans validation.
- 25/11 : constat 0 retour client après 5 jours ; les mails de prospection ne partent plus directement mais sont programmés au jour/heure où le commerçant est le plus susceptible de répondre ; Stan veut qu'on lui présente d'autres pistes d'optimisation avant de les appliquer.
- 25/11 (activité 2, sites web) : lancement en parallèle d'une activité de création de sites pour commerçants/artisans sans site (repérés par recherche web/annuaires, contact par e-mail, SMS plus tard si l'e-mail est trop rare) ; maquette en ligne + fiche de choix + ~10 noms de domaine ; prix de départ bas (installation 190 € + 29 €/mois, remplace l'idée à 100 €/mois) ; pages : accueil/présentation, contact, mentions légales, politique de confidentialité (pas de CGV) ; domaine gratuit Hostinger pour les maquettes ; objectifs 1er client sous 3 jours et 1 000 € en 30 jours ; Claude configure le CRM et les agents en réutilisant l'existant. Détail : `docs/plan-sites-web.md`.
- 25/11 (sites) : domaine des maquettes = artilien.com (acheté par Stan) ; publication par dépôt GitHub PRIVÉ `artilien-maquettes` déployé automatiquement par Hostinger (le shell des agents ne joint pas le serveur de fichiers) ; mails de prospection en HTML (très visuel, simple, direct) ; 20 mails par session dès le départ (décision de Stan, sans montée progressive), garde-fous inchangés.
- 26/11 (sites) : brochure de personnalisation par maquette (page web + PDF), envoyée après le « OK » : couleurs, polices, 7 logos texte (clair/foncé), tons, photos, sections en plus ; polices locales à la place de Google Fonts. Logos limités au texte seul (pas de dessin inventé) ; autres types (monogramme, emblème) possibles plus tard.

## 26/11/2026 — Formulaire + paiement intégré + mails HTML clair/sombre
- Demande de Stan : mails HTML très visuels lisibles en thème clair ET sombre ; formulaire sur le site (il n'envoie que le lien) ; paiement Stripe sans quitter le site.
- Modèles : `sites/mails/` (prospection, relance, apres-ok, chip) ; B26 (prospection) dans « Paramètres sites », B27/B29 pointent vers le dépôt public.
- Pages `commande.html` (choix + domaines `?d=` + ref `?r=`) et `merci.html` ; API PHP `sites/api/` (choix, checkout Stripe Embedded, statut) déployée dans le dépôt privé `api/`.
- Clé Stripe côté serveur uniquement (`artilien-config.php` hors web), créée par Stan. Tests en mode test d'abord ; prospection relancée seulement après validation de Stan (B2 = PAUSE).
- Blocage connu : agents planifiés sans accès au dépôt privé `artilien-maquettes`.

## 26/11/2026 (soir) — Offre, CGV, facture
- Offre : 190 € une fois + 29 €/mois **à partir du 2e mois** (1er mois offert = essai Stripe de 30 jours). Appliqué : checkout.php, page commande, brochure, mails.
- CGV rédigées (`sites/legal/cgv.html`, publiées sur artilien.com/cgv.html) ; case « j'accepte les CGV » obligatoire avant le bouton de paiement. À faire relire par Stan (pas un avis juridique ; clients professionnels uniquement ; adresse du prestataire sur les factures).
- Factures : envoyées automatiquement par Stripe au client (réglage Dashboard : e-mails de factures/reçus). TVA non applicable art. 293 B.
- Paiement intégré validé en mode test ; passage en live = nouvelle clé dans artilien-config.php (jamais dans le dépôt).
