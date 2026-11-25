# Plan et décisions — service « réponses aux avis Google » (copie du doc du Project claude.ai, mise à jour 23/11/2026, expurgée des identifiants)

Activité ArtiLien/ArtisanVoisin (réseau d'artisans) ARRÊTÉE et supprimée par Stan le 22/11/2026.

## Objectif
- 1er client payant en 10 jours ; 1 000 € de CA en 40-60 jours (30 jours possible mais peu probable : estimation Claude).
- Budget d'outils jusqu'à 50 €/mois (surtout Apify).
- Depuis le 23/11 : pilote automatique, sans intervention de Stan.
- Premier envoi réel 23/11 8h36 : 19 mails, 1 rebond, 0 réponse, ≈2,95 $ Apify ; ~11-14 % des lieux trouvés ont un e-mail publié.

## Offres
- Mission initiale : réponses personnalisées aux avis sans réponse, livrées en 48 h, le commerçant relit et publie lui-même. Prix 90 € (clients 1-3), 120 € (4-6), 150 € ensuite. Remboursement si pas satisfait avant publication.
- Règle des 60 avis : une commande couvre au plus les 60 avis récents sans réponse ; au-delà « À CHIFFRER » dans le Journal. Variante de mail « plus de 60 avis » (Paramètres B99).
- Abonnement 49 €/mois sans engagement : réponses hebdo aux nouveaux avis + rapport mensuel, proposé dans le mail de livraison.
- Cibles (Paramètres B105) : restaurants, cafés/bars, boulangeries, coiffeurs, barbiers, instituts/onglerie, hôtels/gîtes, garages, fleuristes, caves/épiceries fines, salles de sport/yoga, auto-écoles, magasins indépendants. Exclus : santé/bien-être médical, chaînes/franchises, professions réglementées, adultes, jeux d'argent.
- Preuve dans le 1er mail : une réponse gratuite à un vrai avis récent sans réponse.

## Fonctionnement
3 agents planifiés (voir CLAUDE.md). Prospection jusqu'à 25 mails/session, 100/jour max. Mode hybride (25/11) : recherche des commerces et e-mails SANS Apify (WebSearch/WebFetch), un seul run Apify d'avis par session sur les finalistes. Garde-fous : pause auto si >5 % rebonds/50 envois, plainte spam, menace juridique. Alertes (ALERTE / ALERTE JURIDIQUE) par push. Risque connu : 100 mails/jour depuis un Gmail récent peut dégrader la délivrabilité.

## Statistiques CRM
Stats quotidiennes (mails/€ Apify, dépense/client, ROI), Runs Apify (une ligne par run), Stats secteurs, Stats avancées (rendement, bandes de score, jour d'envoi, santé d'envoi, seuil de rentabilité). Colonne « Secteur » normalisée (liste dans B105). Lire avec prudence avant 50 envois.

## Facturation
Une facture par paiement (mission et chaque mois d'abonnement), numéro FA-AAAA-NNN continu sans trou, envoyée par mail + archivée en Google Doc dans Drive > Factures > Recettes. Mentions : EI de Stan, « TVA non applicable, art. 293 B du CGI », acquittée par carte (Stripe), pénalités de retard et indemnité 40 €. Règles dans Paramètres lignes 111-113. (SIREN/SIRET : voir Paramètres.)

## Style des mails (validé le 23/11)
HTML léger + version texte ; gras sur 5 arguments max ; avis cité en retrait ; réponse d'exemple en encadré ; ni image, ni bouton, ni lien, ni pièce jointe en prospection. Accroche = fait vérifiable (« En [mois], [prénom] a écrit… Personne ne lui a répondu depuis N mois »). Objet <50 car. : A « [PRÉNOM] vous a laissé [N] étoiles, sans réponse » (si 4-5 étoiles), B « Votre réponse à l'avis de [PRÉNOM] est déjà écrite ». ~100 mots, un seul appel à l'action « OK », fin « Belle journée, », signature 3 lignes, ligne légale. Une seule relance (prudence CNIL).

## Règles légales
Mail B2B sur adresse publiée, lié à l'activité ; identité + source + STOP ; désinscrits jamais recontactés ; une relance ; aucune réponse publiée sans validation du commerçant. Détail : Note juridique (Drive).

## À la charge de Stan (au 23/11)
1. Vérifier que les liens Stripe sont en mode LIVE et que les confirmations arrivent sur artilien.contact@gmail.com.
2. Changer le nom d'affichage de l'expéditeur Gmail (« ArtiLien » alors que les mails sont signés Stanislas Roux).
3. Activité déclarée = apport d'affaires (APE 8299Z) : vérifier au guichet unique/URSSAF avant la 1re facture ; déclaration URSSAF mensuelle même à 0 € ; ACRE avant le 15/01/2027.
4. Régime BNC/BIC et facturation électronique à vérifier.
5. Supprimer les 2 anciens Google Forms (puis Claude supprime les 4 onglets masqués).
6. Remboursements et résiliations dans Stripe quand signalés.
7. Adapter plus tard les tarifs au-delà de 60 avis.
