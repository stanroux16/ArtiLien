# Activité 2 : sites web pour commerçants/artisans sans site (créée le 25/11/2026)

## Idée
Repérer des commerçants et artisans SANS site web (Google Maps via recherche web, annuaires, Facebook) avec e-mail publié, leur envoyer une maquette de site en ligne (lien), puis vendre : installation 190 € (une fois) + 29 €/mois (hébergement, domaine, sécurité, 1 modification/mois), sans engagement. Prix de départ bas, à relever selon la conversion (étude de marché du 25/11 : Wix/Squarespace 11-17 €/mois, éditeurs clé en main 10-80 €/mois, Obat ~599 €/an, freelance 800-3 000 €).

## Objectifs de Stan
1er client sous 3 jours, 1 000 € en 30 jours (estimation Claude : ~5 clients ; il faut ~150 à 200 contacts par client signé ; risque réel de ne pas être atteint). Tout est fait par des agents IA.

## Architecture
- Générateur : `sites/build.py` (voir `sites/README.md`).
- Hébergement : plan Hostinger existant ; un seul domaine (gratuit du compte, nom à choisir par Stan) ; maquettes sous `https://DOMAINE/m/SLUG/`, supprimées après 30 jours sans réponse.
- CRM (mêmes classeur et Journal que les avis) : onglets `Prospects sites`, `Clients sites`, `Maquettes`, `Paramètres sites` (mode d'envoi B2 = PAUSE tant que le domaine n'est pas branché).
- Agents (tâches planifiées) : `Sites – Prospection` et `Sites – Clients et suivi`. Ils réutilisent Gmail (artilien.contact@gmail.com), Journal, Paiements, règles de facturation (Paramètres lignes 111-113), règles légales, garde-fous de l'activité avis.
- Pas d'Apify pour chercher (décision du 25/11) ; recherche web + annuaires. Phase 2 (SMS) seulement si moins de 10 % des commerces examinés ont un e-mail : nouvel outil payant, accord de Stan requis.

## À la charge de Stan
1. Choisir/enregistrer le nom de domaine gratuit Hostinger (puis renseigner `Paramètres sites` B3 et passer B2 à « Envoi automatique … »).
2. Créer les liens Stripe : installation 190 € (paiement unique) et abonnement 29 €/mois ; les coller en B8 et B9 de `Paramètres sites`.
3. Vérifier le régime fiscal/activité : « création de sites » est une prestation différente de l'apport d'affaires (APE 8299Z) et des réponses aux avis.
