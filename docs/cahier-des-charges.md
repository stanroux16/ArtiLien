# ArtiLien – Cahier des charges du site web

Nov 21, 2026 · @Stan

## 1. Contexte, objectifs et périmètre

Le site doit présenter ArtiLien en moins d'une minute de lecture et remplacer les Google Forms par des formulaires maison, intégrés à la marque, qui alimentent directement le CRM et les agents IA.

**Le projet.** ArtiLien est un réseau d'artisans du bâtiment, exploité par Stanislas Roux, entrepreneur individuel (SIREN 133060277, SIRET 13306027700018, APE 8299Z), avec une équipe d'agents IA. ArtiLien met en relation des particuliers propriétaires qui ont un petit chantier avec des artisans membres. L'entrée dans le réseau est gratuite pour l'artisan : il paie une mise en relation seulement quand il l'accepte (10 € pour le premier client, puis 49 / 99 / 199 / 399 € selon le budget estimé du lot, plafond 1 000 €). Le service est gratuit pour le particulier.

**Objectifs du site, par ordre de priorité**

1. Collecter des demandes de particuliers (chantiers de 500 m² maximum, tous métiers) avec un consentement conforme et exploitable.
2. Recruter des artisans : formulaire d'inscription complet, avec acceptation des CGV et collecte des informations de la « fiche artisan ».
3. Inspirer confiance : présenter qui est derrière ArtiLien, comment ça marche, ce qui est vérifié et ce qui est seulement déclaré.
4. Remplacer tous les Google Forms (particuliers, inscription des artisans, retour après un refus) et héberger la page de désinscription (STOP).
5. Servir de page de destination pour les mails, les réponses publiques sous les posts de groupes et les futurs courriers (QR code).

**Hors périmètre de la version 1.** Paiement en ligne sur le site (les liens Stripe restent créés à part), espace client connecté pour les particuliers, application mobile, annuaire public d'artisans, avis clients, chat en direct. Ces sujets sont listés en section 12 pour la version 2.

**Zones affichées.** Hérault (Montpellier), Bas-Rhin (Strasbourg), Rhône (Lyon). Le site doit rester utile hors de ces zones : un particulier ou un artisan d'une autre zone s'inscrit sur une liste d'attente (voir les formulaires).

**Indicateurs de réussite à 90 jours.** Taux de conversion visiteur vers formulaire envoyé au moins 8 % sur le trafic des messages ciblés ; formulaire particulier terminé par au moins 60 % de ceux qui le commencent ; formulaire artisan terminé par au moins 40 % ; zéro mention légale manquante ; score Lighthouse mobile d'au moins 90.

## 2. Cibles, parcours utilisateurs et ton éditorial

Deux publics, deux parcours courts : le particulier doit pouvoir déposer sa demande en moins de 3 minutes sur téléphone, l'artisan doit comprendre le modèle économique avant de s'inscrire.

| Public | Qui | Ce qu'il cherche | Ce qui le freine | Action attendue |
| --- | --- | --- | --- | --- |
| Particulier propriétaire | Propriétaire d'une maison ou d'un appartement, petit chantier (jusqu'à 500 m²), arrive depuis un groupe Facebook, un mail ou un QR code, surtout sur mobile | Un artisan fiable, vite, sans avoir à en chercher dix | Peur du démarchage, du spam, des artisans qui rappellent sans fin, du mauvais prix | Remplir le formulaire de demande |
| Artisan indépendant ou petite entreprise | Plombier, électricien, peintre, carreleur, maçon, couvreur, etc., 1 à 10 salariés | Des chantiers qualifiés sans payer d'abonnement ni de commission sur chantier non signé | Méfiance envers les plateformes, peur de payer pour rien | Lire le modèle, puis s'inscrire |
| Visiteur curieux ou partenaire | Presse, institution, futur partenaire, artisan qui vérifie le sérieux de la société | Savoir qui est derrière ArtiLien | Absence d'informations légales | Lire « À propos » et les mentions légales, ou écrire |

**Parcours particulier (cible du trafic des signaux d'achat).** Arrivée sur la page d'accueil ou sur une page de destination dédiée à son métier, lecture de la promesse (gratuit, sans engagement, des artisans vérifiés), clic sur « Demander un artisan », formulaire en 3 étapes avec les 3 consentements, page de confirmation qui explique la suite (je suis rappelé sous quel délai, par qui, comment me désinscrire), mail de confirmation.

**Parcours artisan.** Arrivée depuis un mail de recrutement ou une recherche, page « Artisans » (modèle, tarifs, garanties, ce qu'ArtiLien vérifie), formulaire d'inscription en plusieurs étapes avec acceptation obligatoire des CGV, page de confirmation, mail de bienvenue, puis questions de la fiche artisan si non remplies.

**Ton éditorial.** Direct, sobre, honnête, vouvoiement. Des faits, pas de slogans : pas de promesse de délai ni de prix, pas de superlatifs, pas de faux compteurs ni de faux avis. Chaque affirmation du site doit être vraie le jour de la mise en ligne (par exemple on n'affiche pas « 500 artisans vérifiés » si ce n'est pas le cas). Ce qu'ArtiLien vérifie (SIRET actif, absence de procédure collective publiée) est séparé de ce que l'artisan déclare (décennale, attestation URSSAF, labels, expérience).

## 3. Arborescence et plan du site

Le site compte 21 pages en version 1 (pages publiques, formulaires, pages légales et pages d'erreur), un back-office privé, et 2 pages prévues pour la version 2. Toutes les URL sont en français, en minuscules, sans accent, avec des tirets.

| URL | Page | Rôle | Priorité |
| --- | --- | --- | --- |
| / | Accueil | Présenter le projet et orienter vers particulier ou artisan | V1 |
| /particuliers | Pour les particuliers | Expliquer le service, rassurer, renvoyer vers le formulaire | V1 |
| /particuliers/demande | Formulaire de demande d'artisan | Collecter la demande et les 3 consentements | V1 |
| /particuliers/demande/merci | Confirmation de demande | Expliquer la suite | V1 |
| /artisans | Pour les artisans | Modèle, tarifs, garanties, vérifications | V1 |
| /artisans/inscription | Formulaire d'inscription artisan | Collecter l'inscription, les infos de la fiche et l'acceptation des CGV | V1 |
| /artisans/inscription/merci | Confirmation d'inscription | Expliquer la suite | V1 |
| /comment-ca-marche | Comment ça marche | Les étapes côté particulier et côté artisan | V1 |
| /tarifs | Tarifs et garanties | Grille de prix des mises en relation, garantie contact réel, exemples chiffrés | V1 |
| /verifications | Ce qu'ArtiLien vérifie | Séparer vérifié et déclaré | V1 |
| /a-propos | À propos | Qui est derrière ArtiLien, mission, zones | V1 |
| /faq | Questions fréquentes | Réponses aux objections, deux sections (particuliers, artisans) | V1 |
| /contact | Contact | Formulaire de contact court et adresse mail | V1 |
| /zones | Zones couvertes | Liste des zones, liste d'attente pour les autres | V1 |
| /retour-apres-refus | Retour après un refus | Remplace le formulaire de retour d'un artisan qui refuse une mise en relation | V1 |
| /desinscription | Désinscription (STOP) | Opposition et suppression des données en un clic | V1 |
| /mentions-legales | Mentions légales | Identité de l'éditeur, hébergeur | V1 |
| /confidentialite | Politique de confidentialité | RGPD détaillé | V1 |
| /cgv-artisans | Conditions générales des artisans | Texte complet des CGV, version datée | V1 |
| /conditions-particuliers | Conditions d'utilisation pour les particuliers | Gratuité, rôle d'intermédiaire | V1 |
| /cookies | Gestion des cookies | Paramètres du consentement | V1 |
| /404, /500 | Pages d'erreur | Rester dans la marque, proposer les liens utiles | V1 |
| /admin (non indexé) | Back-office | Consulter les demandes et inscriptions, exporter, supprimer | V1 |
| /blog | Conseils travaux | Contenu pour le référencement | V2 |
| /espace-artisan | Espace artisan connecté | Fiche, demandes reçues, paiements | V2 |

**Navigation.** En-tête : logo, Particuliers, Artisans, Comment ça marche, FAQ, et un bouton orange « Demander un artisan » (en mobile : menu hamburger, le bouton reste visible en permanence). Pied de page : liens légaux, contact, zones, mention « ArtiLien – Stanislas Roux EI – SIREN 133060277 ».

## 4. Spécification page par page

Chaque page a un titre unique (balise title de 50 à 60 caractères), une meta description de 140 à 160 caractères, un seul h1 et des composants listés dans l'ordre d'affichage. Les textes entre guillemets sont des propositions à reprendre telles quelles ou à ajuster ; tout chiffre doit être vérifié avant la mise en ligne.

### 4.1 Accueil (/)

- **H1** : « Des artisans pour vos travaux, gratuitement pour vous ». Sous-titre : « ArtiLien met en relation les propriétaires et des artisans du bâtiment de Montpellier, Strasbourg et Lyon. »
- **Deux boutons** côte à côte : « Je cherche un artisan » (orange, vers /particuliers/demande) et « Je suis artisan » (contour marine, vers /artisans).
- **Bandeau de 3 preuves** (icônes simples) : « Gratuit pour les particuliers », « Artisans dont le SIRET est vérifié », « Vos coordonnées ne sont jamais revendues ».
- **Comment ça marche** en 3 étapes (résumé de la page dédiée) : vous décrivez votre chantier ; nous cherchons un artisan membre adapté ; il vous contacte directement s'il accepte votre projet.
- **Section artisans** : « Entrée gratuite, vous payez seulement les mises en relation que vous acceptez » avec lien vers /artisans et /tarifs.
- **Zones couvertes** : trois cartes (Hérault, Bas-Rhin, Rhône) avec lien vers /zones.
- **Bloc confiance** : « Qui est derrière ArtiLien », deux phrases, un lien vers /a-propos. Pas de photo de stock de faux clients.
- **Aperçu de la FAQ** : 4 questions, lien vers /faq.
- **Bandeau final** : bouton « Demander un artisan ».

### 4.2 Pour les particuliers (/particuliers)

H1 « Votre chantier mérite le bon artisan ». Contenu : les cas d'usage (salle de bain, électricité, peinture, toiture, extension, etc., jusqu'à 500 m²), le déroulé en 4 étapes, ce que le particulier doit préparer (adresse du chantier, type de travaux, calendrier souhaité, budget indicatif facultatif), ce qu'il n'a pas à faire (pas de paiement, pas d'engagement), la protection des données en trois phrases, et le bouton vers le formulaire en haut et en bas de page. Une note honnête : ArtiLien met en relation, ne réalise pas les travaux et n'est pas partie au contrat avec l'artisan. Pas de page dédiée à la rénovation énergétique ni à l'adaptation du logement tant que le Conseiller juridique n'a pas validé ces usages.

### 4.3 Pour les artisans (/artisans)

H1 « Recevez des demandes de chantier, payez seulement ce que vous acceptez ». Contenu : le modèle en 4 étapes (inscription gratuite, fiche de présentation sans coordonnées, proposition de mise en relation avec le prix annoncé d'avance, paiement par carte avant la transmission des coordonnées du client), la grille de prix, la garantie contact réel (remboursement si le contact est injoignable ou faux, selon la règle de remboursement du Playbook), le récap mensuel gratuit des chantiers pros autorisés autour de chez soi pour les membres, ce qu'ArtiLien vérifie, un exemple chiffré (par exemple lot estimé à 8 000 €, palier 1, 49 €, hors premier client à 10 €), le bouton « S'inscrire gratuitement » en haut et en bas.

### 4.4 Comment ça marche (/comment-ca-marche)

Deux colonnes (particulier / artisan) avec les mêmes 4 étapes, plus un schéma du flux : demande, sélection, fiche anonyme, choix, accord de l'artisan, paiement, mise en contact. Mention explicite : le particulier ne reçoit jamais les coordonnées de l'artisan par ArtiLien ; c'est l'artisan qui contacte le particulier après avoir accepté et payé.

### 4.5 Tarifs et garanties (/tarifs)

Tableau des paliers lu depuis une source unique de paramètres (pas de valeur codée en dur dans les pages) : 1er client 10 € ; lot estimé à moins de 10 000 € : 49 € ; de 10 000 à 50 000 € : 99 € ; de 50 000 à 150 000 € : 199 € ; plus de 150 000 € : 399 €. Mention du statut de TVA (« TVA non applicable, art. 293 B du CGI » tant que la franchise s'applique, à confirmer). Texte sur la garantie contact réel et sur la facture envoyée après chaque paiement. Aucun pourcentage, aucun abonnement.

### 4.6 Ce qu'ArtiLien vérifie (/verifications)

Deux blocs côte à côte : « Vérifié par ArtiLien » (SIRET actif, absence de procédure collective publiée, avec la date de vérification) et « Déclaré par l'artisan » (assurance décennale, attestation URSSAF, labels, expérience, effectif). Un exemple de fiche anonyme (carte précise) en illustration : référence du type A070, lots couverts, capacité, ancienneté, sans nom ni coordonnées.

### 4.7 À propos (/a-propos)

Qui est Stan, pourquoi ArtiLien, comment l'équipe d'agents IA aide (transparence : une partie du suivi est automatisée, les décisions sont humaines), l'éditeur (EI, SIREN), l'adresse de contact. Pas de photo ni de prénom d'un tiers sans accord. Le dispositif humain à afficher est à valider avec Stan (voir section 12).

### 4.8 FAQ (/faq)

Accordéon en deux sections avec balisage FAQPage (schema.org). Particuliers : c'est gratuit ? qui me contacte ? sous quel délai ? mes données sont-elles revendues ? comment me désinscrire ? ArtiLien intervient-il sur le prix ? Artisans : combien ça coûte ? que se passe-t-il si le client ne répond pas (remboursement) ? qui voit mes coordonnées ? comment sont calculés les paliers ? puis-je quitter le réseau ? Les réponses reprennent mot pour mot celles du Playbook, section 5, quand elles existent.

### 4.9 Contact (/contact)

Formulaire court (nom, e-mail, sujet à choisir, message, case de consentement au traitement de la demande) et l'adresse artilien.contact@gmail.com tant que l'adresse du domaine n'existe pas. Un délai de réponse n'est pas promis.

### 4.10 Zones (/zones)

Les trois zones actives (Hérault, Bas-Rhin, Rhône) avec les villes principales, et une liste d'attente pour les autres départements (formulaire d'une ligne : e-mail, code postal, particulier ou artisan, consentement).

### 4.11 Pages de confirmation

/particuliers/demande/merci et /artisans/inscription/merci : récapitulatif de ce qui a été envoyé (sans afficher de données sensibles), prochaine étape en deux phrases, lien de désinscription, rappel du numéro de référence de la demande. Ces pages ne doivent pas être indexées, et un accès direct sans envoi redirige vers le formulaire.

### 4.12 Pages légales

Mentions légales, confidentialité, CGV artisans, conditions particuliers, cookies : voir section 7 pour le contenu obligatoire. Les textes sont fournis par le Conseiller juridique (le dev ne les rédige pas) et affichés avec leur date de version.

### 4.13 Pages d'erreur

404 : titre « Cette page n'existe pas », champ de recherche des liens utiles, deux boutons. 500 : message sobre et lien vers /contact. Aucune trace technique affichée.

## 5. Formulaires

Six formulaires remplacent les Google Forms. Chacun est un composant du site, validé côté navigateur et côté serveur, qui enregistre sa soumission en base (section 6) et déclenche un mail de confirmation (section 10).

### 5.0 Règles communes

- **Mobile d'abord.** Un champ par ligne, étapes courtes, boutons de 48 px de haut au moins, bon type de clavier (e-mail, téléphone, nombre), pas de défilement horizontal.
- **Progression.** Formulaires à étapes avec une barre « Étape 2 sur 3 », bouton Retour, sauvegarde automatique des réponses dans le navigateur (sessionStorage) pour ne rien perdre en cas de rafraîchissement. Rien n'est envoyé au serveur avant le clic final, sauf pour le formulaire artisan où le numéro SIRET est vérifié à l'étape 1.
- **Validation.** En ligne, au moment de quitter le champ ; messages d'erreur en français, près du champ, relués par les lecteurs d'écran (aria-live, aria-describedby) ; le message dit comment corriger (« Entrez un numéro à 10 chiffres, par exemple 06 12 34 56 78 »). Les champs obligatoires sont marqués dans l'étiquette (« obligatoire »), pas seulement par une étoile.
- **Anti-spam.** Cloudflare Turnstile (ou équivalent respectueux de la vie privée), champ piège invisible (honeypot), délai minimal de 3 secondes entre l'affichage et l'envoi, limite de 5 envois par heure et par adresse IP, rejet des soumissions dont l'adresse e-mail est jetable.
- **Preuve du consentement.** Pour chaque case de consentement : horodatage UTC, version du texte affiché, texte exact, URL de la page, empreinte de l'adresse IP (hachée avec un sel secret, pas l'IP en clair), agent utilisateur. Les cases ne sont jamais précochées et ne sont pas groupées en une seule case.
- **Numéro de référence.** Chaque soumission reçoit un identifiant lisible (D-2026-000123 pour une demande, I-2026-000045 pour une inscription) affiché à l'utilisateur, utilisé dans les mails et dans le CRM.
- **Double confirmation.** Après l'envoi, le particulier reçoit un mail avec un bouton « Confirmer ma demande » (lien signé, valable 7 jours). Tant qu'il n'est pas cliqué, la demande a le statut « À confirmer » et n'est pas transmise aux agents ni aux artisans. Même principe pour l'inscription artisan (confirmation de l'e-mail professionnel).
- **Accessibilité.** Conformité visée WCAG 2.1 niveau AA : étiquettes liées aux champs, focus visible, navigation au clavier, contraste d'au moins 4,5 pour 1.
- **Données minimales.** Ne demander que ce qui sert à la mise en relation ; aucune donnée sensible (santé, situation familiale, revenus).

### 5.1 Demande de particulier (/particuliers/demande)

Trois étapes. Les champs de l'étape 1 décrivent le chantier, ceux de l'étape 2 le lieu, ceux de l'étape 3 la personne et les consentements.

| Étape | Champ | Type | Obligatoire | Règle de validation et notes |
| --- | --- | --- | --- | --- |
| 1 | Type de travaux | Cases à cocher (liste des lots : plomberie, électricité, peinture, carrelage, plaquiste, menuiserie, maçonnerie, toiture, chauffage, façade, sol, salle de bain complète, cuisine, extension, autre) | Oui | Au moins un choix ; « autre » ouvre un champ texte |
| 1 | Description du besoin | Zone de texte | Oui | 20 à 1 500 caractères, compteur visible, texte d'aide avec un exemple |
| 1 | Surface concernée | Nombre en m² | Non | 1 à 500 ; au-delà de 500, message qui explique que le service vise les petits chantiers et propose de laisser un message via /contact |
| 1 | Avancement | Choix unique : j'y réfléchis / je compare des devis / prêt à démarrer | Oui |  |
| 1 | Délai souhaité | Choix unique : dès que possible / sous 1 mois / 1 à 3 mois / plus tard / flexible | Oui |  |
| 1 | Budget indicatif | Fourchette (moins de 1 000 €, 1 000 à 5 000, 5 000 à 15 000, 15 000 à 50 000, plus de 50 000, je ne sais pas) | Non | Texte : « Facultatif, utile pour trouver un artisan adapté » |
| 1 | Photos ou plans | Envoi de fichiers | Non | 5 fichiers au maximum, images (jpg, png, webp) ou pdf, 5 Mo chacun, analyse antivirus, noms de fichiers réécrits côté serveur |
| 2 | Adresse du chantier | Saisie avec suggestions (API Adresse de data.gouv.fr) | Oui | Commune, code postal et coordonnées remplis automatiquement ; saisie manuelle possible |
| 2 | Type de bien | Maison / appartement / local / autre | Oui |  |
| 2 | Votre situation | Propriétaire occupant / propriétaire bailleur / locataire avec accord du propriétaire / autre | Oui | Si « autre » : message qui demande l'accord du propriétaire |
| 2 | Contrôle de zone | Automatique | n/a | Si le département n'est pas 34, 67 ou 69 : message « Nous ne couvrons pas encore votre zone » et propose la liste d'attente (5.6) au lieu de continuer |
| 3 | Prénom, nom | Texte | Oui | 2 à 60 caractères |
| 3 | E-mail | E-mail | Oui | Syntaxe + domaine existant (enregistrement MX) |
| 3 | Téléphone | Téléphone | Oui | Numéro français (06, 07, 01 à 05, 09), normalisé au format E.164 ; espaces et points tolérés |
| 3 | Meilleur moment pour être contacté | Matin / midi / après-midi / soir / peu importe | Non |  |
| 3 | Canal préféré | Téléphone / e-mail / indifférent | Non |  |
| 3 | Consentement 1 | Case à cocher | Oui | Traitement des données pour chercher un artisan ; libellé exact à reprendre du formulaire actuel, validé par le Conseiller juridique |
| 3 | Consentement 2 | Case à cocher | Oui | Transmission de la demande et des coordonnées à un ou plusieurs artisans membres choisis par ArtiLien |
| 3 | Consentement 3 | Case à cocher | Oui | Autorisation d'être contacté par téléphone ou e-mail pour ce projet, par ArtiLien et par les artisans concernés |

Les trois cases portent exactement les trois consentements du Google Form actuel (le texte vient de Stan et du Conseiller juridique, le développeur ne le rédige pas). Le lien vers la politique de confidentialité est visible à côté du bouton d'envoi. À la soumission : création de la demande (D-2026-xxxxxx), mail de confirmation à valider, écriture dans le CRM.

### 5.2 Inscription d'un artisan (/artisans/inscription)

Cinq étapes. Le lien peut être personnalisé (« /artisans/inscription?ref=A070 ») : un jeton signé préremplit entreprise, SIRET, métier et e-mail depuis le CRM, sans afficher ces données avant que l'utilisateur confirme son e-mail.

| Étape | Champ | Type | Obligatoire | Règle de validation et notes |
| --- | --- | --- | --- | --- |
| 1 | SIRET | Texte, 14 chiffres | Oui | Contrôle de la clé (algorithme de Luhn) puis appel à l'API recherche-entreprises.api.gouv.fr ; remplit raison sociale, forme juridique, code NAF, adresse, date de création ; refuse un établissement fermé ; avertit si le code NAF n'est pas du bâtiment mais n'empêche pas l'envoi |
| 1 | Raison sociale ou nom commercial | Texte | Oui | Prérempli, modifiable |
| 1 | Doublon | Automatique | n/a | Si le SIRET existe déjà dans la base : message « Cette entreprise est déjà inscrite, cherchez le mail de bienvenue ou écrivez-nous » |
| 2 | Prénom et nom du contact | Texte | Oui |  |
| 2 | Fonction | Liste : gérant, artisan, conducteur de travaux, autre | Oui |  |
| 2 | E-mail professionnel | E-mail | Oui | Validé par un mail de confirmation ; adresse unique par entreprise |
| 2 | Téléphone | Téléphone | Oui | Format E.164 |
| 3 | Lots réalisés | Cases à cocher (même liste que 5.1) | Oui | Au moins un ; seuls les lots déclarés apparaissent sur la fiche |
| 3 | Commune de base | Saisie avec suggestions | Oui |  |
| 3 | Rayon d'intervention | Curseur de 5 à 100 km | Oui | 100 km maximum (paramètre du réseau) ; carte de prévisualisation |
| 4 | Présentation courte | Zone de texte | Non | 300 caractères au maximum ; interdit de saisir nom, téléphone, mail, site ou adresse (contrôle automatique par motifs, car la fiche est anonyme) |
| 4 | Années d'expérience | Nombre | Oui | 0 à 60 |
| 4 | Effectif | Choix : seul / 2 à 5 / 6 à 10 / 11 à 20 / plus de 20 | Oui |  |
| 4 | Types de chantiers réalisés | Cases à cocher : particuliers, copropriétés, entreprises, collectivités, promoteurs | Oui |  |
| 4 | Plus gros chantier tenu | Fourchette de montant | Oui |  |
| 4 | Labels et qualifications | Cases (RGE, Qualibat, Qualifelec, autre) | Non | Déclaré par l'artisan, non vérifié |
| 4 | Assurance décennale | Oui / en cours / non, avec envoi facultatif de l'attestation | Oui | Si oui : assureur facultatif, date de fin de validité |
| 4 | Attestation de vigilance URSSAF | Oui / non / ne sait pas | Oui |  |
| 4 | Expérience avec des professionnels | Oui / non | Oui |  |
| 4 | Délai habituel de démarrage | Choix : moins de 2 semaines / 2 à 4 semaines / 1 à 2 mois / plus | Oui |  |
| 5 | CGV | Case à cocher | Oui | « J'ai lu et j'accepte les conditions générales des artisans (version du jj/mm/aaaa) », lien qui ouvre /cgv-artisans dans un nouvel onglet ; la version affichée et son identifiant sont enregistrés |
| 5 | Information RGPD | Texte et lien | n/a | Information sur le traitement des données de l'entreprise |
| 5 | Propositions de mise en relation | Case à cocher | Oui | Accepter de recevoir des propositions de chantier par e-mail ; l'inscription est impossible sans |

Au envoi : création de l'artisan avec le statut « À confirmer », mail de confirmation, puis statut « Partenaire » après confirmation de l'e-mail. La fiche anonyme est ensuite créée par les agents à partir de ces réponses.

### 5.3 Retour après un refus (/retour-apres-refus)

Page ouverte par un lien personnalisé dans un mail (jeton signé qui contient la référence de la mise en relation, sans donnée personnelle). Champs : raison du refus (cases : prix trop élevé, budget du chantier trop faible, trop loin, planning, type de chantier, chantier déjà attribué, projet pas assez qualifié, autre), prix qui aurait été acceptable (facultatif), commentaire libre (500 caractères), souhait de rester dans le réseau (oui / non). Les questions exactes sont à reprendre du formulaire actuel. Pas de connexion requise ; le jeton ne sert qu'une fois.

### 5.4 Contact (/contact)

Nom, e-mail, sujet (liste : question particulier, question artisan, presse et partenariat, problème avec le site, autre), message de 10 à 2 000 caractères, case de consentement au traitement de la demande. Le mail part vers artilien.contact@gmail.com et est enregistré en base.

### 5.5 Désinscription et droits (/desinscription)

Une page qui ne demande rien d'autre qu'une adresse e-mail : choix entre « Ne plus recevoir de messages » (opposition), « Supprimer mes données », « Accéder à mes données », « Corriger mes données ». L'envoi déclenche un mail de confirmation avec un lien. Un lien de désinscription en un clic (jeton signé, sans formulaire) est ajouté dans chaque mail et dans les en-têtes List-Unsubscribe. L'opposition est appliquée dans la minute : le contact passe au statut « Désinscrit » en base et dans le CRM, et plus aucun agent ne peut lui écrire. Les demandes de suppression sont traitées sous 30 jours maximum et journalisées.

### 5.6 Liste d'attente par zone

Petit formulaire sur /zones et dans le contrôle de zone du formulaire particulier : e-mail, code postal, particulier ou artisan, consentement à être prévenu de l'ouverture de la zone. Utilisé seulement pour cet objectif ; purge après 12 mois.

## 6. Données, back-office et intégration avec le CRM et les agents IA

Le site écrit d'abord dans sa propre base, puis envoie chaque soumission dans le CRM Google Sheet existant, pour que les agents IA continuent de travailler sans changement. Le Google Sheet reste la source de vérité des agents ; la base du site est la source de vérité des preuves de consentement.

### 6.1 Flux de données

1. Le visiteur envoie un formulaire : le serveur valide, enregistre la soumission et les preuves de consentement dans la base, renvoie la page de confirmation.
2. Un mail de confirmation part aussitôt (section 10), depuis l'adresse artilien.contact@gmail.com (envoi via l'API Gmail ou SMTP Gmail avec mot de passe d'application, limite d'environ 500 mails par jour ; bascule vers l'adresse du nom de domaine dès son achat, avec SPF, DKIM et DMARC). Au clic, la soumission passe à « Confirmée ».
3. Une tâche de synchronisation écrit la ligne correspondante dans le Google Sheet (API Google Sheets, compte de service, accès limité à ce classeur) : demandes dans l'onglet « Réponses au formulaire 1 », inscriptions artisans dans « Inscriptions artisans », retours après refus dans « Retours refus ». Les colonnes et leur ordre sont ceux des onglets actuels (le développeur reçoit un export des en-têtes) ; une colonne « Référence site » est ajoutée. L'écriture est idempotente : la référence empêche les doublons si la tâche est rejouée.
4. Les agents IA lisent ces onglets comme aujourd'hui, créent les lignes Clients ou Artisans et mettent à jour les statuts. Si un statut change vers « Désinscrit », « Refus » ou « Opposition » dans le Sheet, la synchronisation inverse (toutes les 15 minutes) le recopie dans la base pour bloquer tout futur envoi.
5. En cas d'échec de l'écriture dans le Sheet : 5 nouvelles tentatives espacées (1, 5, 15 minutes, 1 heure, 6 heures), puis alerte par mail à Stan. La soumission n'est jamais perdue.

**Transition.** Le Google Form actuel, déjà relié au CRM, reste en service jusqu'à la mise en ligne du site ; il est ensuite remplacé par les formulaires du site (le lien du formulaire dans les mails est alors mis à jour).

### 6.2 Modèle de données minimal

| Table | Contenu principal | Notes |
| --- | --- | --- |
| demandes\_particuliers | référence, date, statut (à confirmer, confirmée, transmise, close, désinscrit), lots, description, surface, avancement, délai, budget, adresse, commune, code postal, type de bien, situation, zone, prénom, nom, e-mail, téléphone, créneau, canal, fichiers | Données personnelles chiffrées au repos |
| consentements | id de la soumission, numéro de la case, texte exact, version, horodatage UTC, empreinte IP, agent utilisateur, URL | Jamais modifiée, seulement ajoutée |
| inscriptions\_artisans | référence, statut (à confirmer, partenaire, désinscrit), SIRET, raison sociale, NAF, contact, e-mail, téléphone, lots, commune de base, rayon, réponses de la fiche, version des CGV acceptées |  |
| retours\_refus | référence de la mise en relation, motifs, prix acceptable, commentaire, souhait de rester |  |
| messages\_contact | nom, e-mail, sujet, message |  |
| liste\_attente | e-mail, code postal, type, consentement |  |
| oppositions | e-mail (en clair et empreinte), date, type de demande, statut | Conservée pour respecter l'opposition |
| journal\_audit | qui, quoi, quand, sur quel enregistrement | Lecture, export, suppression |
| parametres | paliers de prix, rayon maximum, zones actives, version des CGV | Lus par le site, mis à jour depuis le Sheet ou le back-office |

### 6.3 Back-office (/admin)

- **Accès.** Connexion par e-mail avec mot de passe fort et authentification à deux facteurs obligatoire, session de 8 heures, blocage après 5 échecs, page non indexée (robots, balise noindex, en-tête X-Robots-Tag). Rôles : administrateur (Stan) et lecture seule. Un compte technique pour les synchronisations n'a aucun accès à l'interface.
- **Listes.** Demandes, inscriptions, retours, messages, liste d'attente, oppositions : filtres par statut, zone et date, recherche par référence, e-mail ou commune, pagination de 50 lignes.
- **Fiche d'une soumission.** Toutes les réponses, la preuve de consentement, l'historique des statuts, les fichiers, un bouton pour renvoyer le mail de confirmation.
- **Actions.** Changer un statut, marquer comme désinscrit, exporter en CSV (avec entrée au journal d'audit), supprimer définitivement (suppression réelle des données et des fichiers, sauf l'empreinte conservée pour l'opposition), modifier les paramètres.
- **Tableau de bord.** Nombre de demandes et d'inscriptions par jour et par zone, taux de confirmation, taux de départ par étape de formulaire, erreurs de synchronisation en attente.

### 6.4 Conservation des données (durées proposées, à valider par le Conseiller juridique)

- Demandes non confirmées : suppression au bout de 30 jours.
- Demandes confirmées sans suite : suppression après 12 mois.
- Inscriptions d'artisans : conservées tant que l'artisan est membre, puis 3 ans en archive limitée (facturation et litiges), puis suppression.
- Messages de contact : 12 mois. Liste d'attente : 12 mois.
- Preuves de consentement : conservées pendant la durée du traitement puis 5 ans.
- Journal d'audit : 12 mois.

## 7. Légal, RGPD et conformité

Le développeur n'écrit aucun texte juridique : il intègre ceux que fournit le Conseiller juridique (agent IA, non avocat ; à faire relire par un professionnel avant la mise en ligne) et applique les règles techniques ci-dessous. Tout texte légal affiche sa date de version.

### 7.1 Mentions légales obligatoires (/mentions-legales)

- Éditeur : Stanislas Roux, entrepreneur individuel, nom commercial ArtiLien, SIREN 133060277, SIRET 13306027700018, code APE 8299Z, adresse du siège (celle du paramètre « Adresse d'ArtiLien » du CRM), adresse mail de contact, directeur de la publication.
- TVA : mention de la franchise en base ou numéro de TVA, selon la situation réelle (à confirmer).
- Hébergeur : nom, adresse et téléphone de l'hébergeur retenu.
- Statut d'ArtiLien : apporteur d'affaires, qui met en relation sans être partie aux contrats.

### 7.2 Protection des données (/confidentialite)

Politique en langage clair, par public (particuliers, artisans, visiteurs). Pour chaque traitement : finalité, base légale (consentement ou intérêt légitime), données collectées, destinataires (les artisans membres sélectionnés, les sous-traitants techniques), durée de conservation (section 6.4), droits (accès, rectification, effacement, opposition, limitation, portabilité), exercice des droits (lien /desinscription ou mail), droit de réclamation auprès de la CNIL, transferts hors de l'Union européenne s'il y en a. La liste des sous-traitants (hébergeur, envoi de mails, Google pour le CRM) est publiée.

### 7.3 Conditions générales

- **CGV des artisans (/cgv-artisans).** Texte complet de la version en vigueur (Playbook, section 7, version actuelle du 20/11/2026 avec prix fixes par palier). Chaque version a un identifiant, une date d'effet et une URL d'archive ; l'artisan accepte une version précise et la preuve est conservée. Une nouvelle version déclenche un mail aux membres.
- **Conditions des particuliers (/conditions-particuliers).** Service gratuit, rôle d'intermédiaire, absence de garantie sur les travaux, usage des données.

### 7.4 Cookies et traceurs (/cookies)

Par défaut aucun traceur non indispensable. Si une mesure d'audience est mise en place, elle passe soit par un outil exempté de consentement et paramétré selon les recommandations de la CNIL, soit par une bannière de consentement avec trois choix de même importance visuelle (accepter, refuser, paramétrer) ; refuser doit être aussi simple qu'accepter ; le choix est mémorisé 6 mois au plus. Aucun pixel publicitaire en version 1.

### 7.5 Règles de contenu liées au droit

- Aucun contenu n'incite à des travaux de rénovation énergétique ou d'adaptation du logement par démarchage ; ces sujets ne sont pas mis en avant sur le site tant que le Conseiller juridique n'a pas validé leur traitement.
- Aucune affirmation de garantie, de qualification ou de label qui ne soit pas vérifiée ; distinguer toujours « vérifié » et « déclaré ».
- Tarifs affichés TTC ou avec la mention de non-application de la TVA, identiques à ceux des CGV.
- Les mails envoyés depuis le site contiennent le bloc légal standard d'ArtiLien (SIREN, SIRET, droit d'opposition, source des données).

### 7.6 Accessibilité

Visée WCAG 2.1 AA. Une page « Déclaration d'accessibilité » n'est obligatoire que si le seuil légal s'applique ; à vérifier avec le Conseiller juridique.

## 8. Design et identité visuelle

Le site reprend le design des mails ArtiLien (bleu marine, filet orange, cartes blanches) pour que le parcours mail puis site paraisse continu. L'esprit : sobre, rassurant, très lisible, proche d'un document officiel bien fait, loin des maquettes de plateformes tapageuses.

| Élément | Valeur |
| --- | --- |
| Bleu marine (couleur principale, titres, en-tête, pied de page) | #1B2A49 |
| Orange (actions principales, filet, accents) | #F28C28 |
| Fond de page | #FFFFFF avec sections alternant #F5F7FA |
| Texte courant | #1F2937 sur fond clair (contraste supérieur à 12 pour 1) |
| Texte secondaire | #4B5563 |
| Succès, erreur, alerte | #1E7F4F, #B42318, #B54708 (toujours accompagnés d'une icône et d'un texte) |
| Police | Inter (texte et titres), auto-hébergée, 16 px minimum en corps, interligne 1,6 |
| Titres | h1 40 px (28 sur mobile), h2 28 px (22), h3 20 px ; poids 700 |
| Mise en page | Largeur de contenu 1 120 px, texte courant limité à 70 caractères par ligne, grille de 8 px |
| Bordures et cartes | Rayon de 8 px, bordure 1 px #E5E7EB, ombre très légère seulement au survol |
| Boutons | Principal orange avec texte marine (contraste vérifié), secondaire en contour marine ; hauteur 48 px ; état de focus visible de 3 px |
| Icônes | Jeu unique de traits fins (Lucide ou équivalent libre), pas de pictos de couleurs variées |
| Logo | Mot-symbole « ArtiLien » en marine avec un petit trait orange ; à fournir en SVG par Stan, sinon le développeur propose une version simple soumise à validation |
| Images | Photos réelles de chantiers libres de droits ou fournies par Stan ; aucune photo de personnes identifiables sans accord ; aucune fausse photo de client ni de faux avis |

**Mode sombre** : direction de design C retenue par Stan (fond sombre type application) ; à confirmer si elle s'applique à tout le site ou seulement à l'accueil et à l'application. **Animations** : discrètes (fondu, décalage de 8 px), désactivées si l'utilisateur a demandé de réduire les animations (prefers-reduced-motion).

**Composants à livrer dans une bibliothèque commune** : en-tête et pied de page, boutons, cartes, accordéon de FAQ, étapes numérotées, bandeau de preuves, tableau de tarifs, champs de formulaire (texte, nombre, liste, cases, boutons radio, curseur, envoi de fichier, saisie d'adresse), barre de progression, messages d'erreur et de succès, bandeau de cookies, page d'erreur.

**Maquettes.** Avant le code : maquettes mobile (390 px) et ordinateur (1 440 px) de l'accueil, de /particuliers, de /artisans, des deux grands formulaires et des pages de confirmation, validées par Stan ; points de rupture à 640, 1 024 et 1 280 px.

## 9. Technique

Budget d'outils et d'hébergement du site : 20 € par mois au plus, dans l'enveloppe de 50 € par mois de l'ensemble du projet. Le site doit tourner en permanence sur le cloud, sans serveur à surveiller à la main.

### 9.1 Stack recommandée (le développeur peut proposer mieux, en justifiant)

| Besoin | Recommandation | Raison |
| --- | --- | --- |
| Application | Next.js (App Router) en TypeScript | Pages rapides, rendu côté serveur pour le référencement, formulaires avec actions serveur |
| Style | Tailwind CSS avec des variables de design (couleurs, espacements) | Cohérence avec la section 8 |
| Validation | Zod, avec les mêmes schémas côté navigateur et serveur | Une seule source de règles |
| Base de données | PostgreSQL géré dans l'Union européenne (Supabase ou Neon) | Données personnelles hébergées en UE, sauvegardes automatiques |
| Fichiers | Stockage objet privé en UE, liens signés à courte durée | Photos et attestations jamais publiques |
| Hébergement | Vercel (région Paris ou Francfort) ou hébergeur français équivalent | Déploiement continu, SSL automatique, ressource toujours disponible |
| Mails transactionnels | Resend (région UE) ou Brevo | Délivrabilité, journal d'envoi, webhooks de rebond |
| Anti-spam | Cloudflare Turnstile | Sans traceur publicitaire |
| Nom de domaine | À acheter (environ 10 € par an), avec mail professionnel ; SPF, DKIM et DMARC configurés | Décision D3 déjà acceptée : nom de domaine et mail pro |
| Surveillance | Sentry (offre gratuite) pour les erreurs, UptimeRobot pour la disponibilité | Alerte par mail à Stan |
| Application mobile | Expo (React Native) en TypeScript, pour iOS et Android, pour les particuliers et les artisans | Dépôt commun avec le site (pnpm + Turborepo) : mêmes schémas Zod, mêmes couleurs, même base et même connexion (rôle particulier ou artisan) ; notifications push pour les artisans |

### 9.2 Environnements et livraison

- Trois environnements : local, préproduction (accessible par mot de passe), production. Dépôt Git privé (au nom de Stan, dont il reste propriétaire), branche principale protégée, revue de code avant fusion.
- Déploiement automatique à chaque fusion, avec prévisualisation par branche. Retour arrière en un clic.
- Variables secrètes uniquement dans le gestionnaire de secrets de l'hébergeur, jamais dans le code. Aucune clé en clair dans le dépôt.
- Sauvegardes quotidiennes de la base, conservées 14 jours, test de restauration avant la mise en ligne.

### 9.3 Performance

Lighthouse mobile d'au moins 90 en performance, accessibilité, bonnes pratiques et SEO sur toutes les pages publiques. LCP sous 2,5 s, CLS sous 0,1, INP sous 200 ms sur une connexion 4G. Images en WebP ou AVIF avec dimensions déclarées, chargement différé, polices auto-hébergées avec affichage de secours, JavaScript réduit au nécessaire (pages de contenu rendues côté serveur).

### 9.4 Référencement

- Une balise title et une meta description uniques par page, URL canoniques, plan de site XML généré automatiquement, fichier robots.txt qui exclut /admin, les pages de confirmation et les prévisualisations.
- Données structurées : Organization, WebSite, FAQPage sur /faq, BreadcrumbList.
- Balises Open Graph et Twitter avec une image de partage 1 200 par 630 pixels.
- Pages de destination locales (Montpellier, Strasbourg, Lyon) en version 2, une page par métier et par ville, avec du texte réellement utile et non répété.
- Redirection 301 des anciennes adresses si elles existent, aucune page orpheline.

### 9.5 Sécurité

- HTTPS partout avec HSTS ; en-têtes de sécurité (Content-Security-Policy stricte, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, X-Frame-Options).
- Protection contre l'injection SQL (requêtes paramétrées), les scripts intersites (échappement systématique) et les falsifications de requête (jeton CSRF sur les formulaires et actions sensibles).
- Limitation du nombre de requêtes sur les routes de formulaire et de connexion.
- Chiffrement des données personnelles au repos ; mots de passe du back-office hachés (Argon2 ou bcrypt), 2FA obligatoire.
- Fichiers envoyés : contrôle du type réel du fichier, taille, analyse antivirus, stockage hors de la racine web, noms réécrits.
- Aucun secret ni donnée personnelle dans les URL, les journaux ni les messages d'erreur. Journaux conservés 30 jours.
- Liens signés (jetons HMAC) pour la confirmation, la désinscription et le retour après refus : durée limitée, usage unique quand c'est utile, aucune donnée personnelle en clair dans le jeton.
- Analyse des dépendances (Dependabot) et mise à jour mensuelle.

### 9.6 Compatibilité

Dernières versions de Chrome, Safari, Firefox et Edge, plus les deux versions précédentes de Safari iOS et de Chrome Android. Test réel sur un iPhone et un téléphone Android d'entrée de gamme. Le site reste lisible et les formulaires utilisables sans JavaScript pour l'essentiel du contenu.

## 10. E-mails transactionnels et notifications

Le site envoie lui-même huit e-mails automatiques, tous répondant à une action de la personne. Ils sont distincts des mails de prospection envoyés par les agents. Modèle commun : bandeau marine (#1B2A49) avec le mot ArtiLien, filet orange (#F28C28), tableau de 600 px, styles en ligne, version texte brut jointe, bloc légal en bas en 11 px minimum.

**Bloc légal à reprendre sur chaque mail** : ArtiLien, Stanislas Roux EI, SIREN 133060277, SIRET 13306027700018, adresse du siège ; la raison de réception du mail (vous avez rempli un formulaire sur le site) ; un lien « Ne plus recevoir ces messages » ; la mention du droit d'accès, de rectification et d'opposition, avec l'adresse de contact. Les mails de confirmation de désinscription n'ont pas besoin du lien de désinscription.

| # | Mail | Déclencheur | Destinataire | Contenu essentiel |
| --- | --- | --- | --- | --- |
| 1 | Confirmer votre demande | Envoi du formulaire particulier | Particulier | Référence, bouton « Confirmer ma demande » (7 jours), récapitulatif en 3 lignes, lien de désinscription |
| 2 | Votre demande est confirmée | Clic sur le bouton | Particulier | Ce qui se passe ensuite, qui va le contacter, comment modifier ou retirer sa demande |
| 3 | Confirmer votre inscription | Envoi du formulaire artisan | Artisan | Référence, bouton de confirmation de l'e-mail professionnel (7 jours) |
| 4 | Bienvenue dans ArtiLien | Confirmation de l'e-mail | Artisan | Prochaine étape (fiche de présentation), résumé du modèle et des tarifs, rappel de la version des CGV acceptées, lien vers elles |
| 5 | Votre message est bien reçu | Formulaire de contact | Auteur | Copie du message, aucune promesse de délai |
| 6 | Confirmation de désinscription | Formulaire ou lien STOP | Demandeur | Opposition appliquée (ou suppression en cours, avec la date limite de traitement) |
| 7 | Merci pour votre retour | Formulaire après refus | Artisan | Remerciement court, rappel qu'il reste membre (ou qu'il est retiré s'il l'a demandé) |
| 8 | Nouvelle soumission | Toute soumission confirmée | Stan (artilien.contact) | Synthèse d'une ligne par soumission, à regrouper en un résumé quotidien si plus de 10 par jour |

**Exigences techniques.** Expéditeur de la forme contact@\[domaine\] avec SPF, DKIM et DMARC en mode quarantaine puis rejet, adresse de réponse surveillée, en-têtes List-Unsubscribe et List-Unsubscribe-Post sur les mails 1 à 4, journal de délivrance (envoyé, délivré, rebondi, signalé comme spam) consultable dans le back-office, arrêt automatique des envois vers une adresse en rebond définitif, test de rendu sur Gmail, Outlook, Apple Mail et mobile. Les liens des mails utilisent le domaine du site ; aucun suivi d'ouverture ni de clic en version 1.

**Textes.** Chaque mail a un objet de moins de 50 caractères et un texte court rédigé par l'agent Marketing ou par Stan ; le développeur met en place des gabarits modifiables sans redéploiement (fichiers de contenu ou back-office).

## 11. Mesure, tests, livrables, planning et critères d'acceptation

La version 1 doit être livrable en 7 semaines de travail, avec une mise en ligne conditionnée à la liste de critères ci-dessous.

### 11.1 Mesure d'audience

Outil respectueux de la vie privée, sans cookie (Plausible, Umami ou Cloudflare Web Analytics), configuré sans consentement conformément aux recommandations de la CNIL. Événements à suivre : clic sur « Demander un artisan » et « S'inscrire » (avec la page d'origine), début de chaque formulaire, passage de chaque étape, envoi réussi, erreur de validation par champ, confirmation du mail, ouverture de la FAQ. Paramètres UTM conservés dans la soumission (source, medium, campagne) pour savoir quel canal (groupe Facebook, mail, QR code) produit des demandes. Aucune donnée personnelle dans les événements.

### 11.2 Tests

- Tests automatiques des schémas de validation (SIRET, téléphone, adresse, surface, consentements) et des routes de formulaire.
- Tests de bout en bout (Playwright) : demande complète, inscription complète, confirmation par mail, désinscription, doublon de SIRET, département hors zone, tentative de spam.
- Test de la synchronisation avec le Sheet sur une copie du CRM, puis sur le vrai CRM en préproduction.
- Audit d'accessibilité (axe, lecture au clavier, lecteur d'écran sur les deux formulaires).
- Test de charge léger : 50 soumissions en 5 minutes sans erreur.

### 11.3 Livrables

1. Maquettes validées (section 8).
2. Code source dans un dépôt Git privé appartenant à Stan, avec un fichier README qui explique l'installation, les variables d'environnement, le déploiement et la restauration.
3. Site déployé en préproduction puis en production, avec le nom de domaine, le HTTPS et les mails configurés.
4. Documentation courte : schéma de la base, liste des routes, manuel du back-office (1 page), procédure de modification des textes et des tarifs.
5. Accès administrateur remis à Stan pour l'hébergeur, la base, le dépôt, le domaine et l'outil de mails ; le développeur ne garde aucun accès exclusif.
6. Rapport de recette (résultats des tests et de Lighthouse).

### 11.4 Planning indicatif

| Semaine | Contenu | Validation par |
| --- | --- | --- |
| 1 | Cadrage, choix des outils, achat du domaine, dépôt et environnements, export des en-têtes du CRM | Stan |
| 2 à 3 | Maquettes mobile et ordinateur, bibliothèque de composants | Stan |
| 3 à 5 | Pages publiques, formulaires, base de données, preuves de consentement, confirmation par mail | Stan, Conseiller juridique pour les textes |
| 5 à 6 | Synchronisation avec le CRM, back-office, désinscription, mails transactionnels | Stan |
| 6 à 7 | Recette, accessibilité, performance, sécurité, corrections, préproduction | Stan |
| 7 | Relecture juridique des textes et des consentements, mise en production, surveillance renforcée pendant 7 jours | Stan, Conseiller juridique |

### 11.5 Critères d'acceptation

- [ ] Les 6 formulaires envoient, valident, enregistrent les preuves de consentement et affichent une confirmation sur mobile et ordinateur.
- [ ] Une soumission confirmée apparaît dans le bon onglet du CRM en moins de 5 minutes, sans doublon si elle est rejouee.
- [ ] Une opposition faite sur le site bloque l'envoi de mails aux agents en moins de 15 minutes.
- [ ] Aucun texte légal ni consentement n'est rédigé par le développeur ; tous portent leur version et leur date.
- [ ] Les trois consentements particulier ne sont ni précochés ni groupés.
- [ ] Les tarifs affichés viennent des paramètres et correspondent aux CGV.
- [ ] Lighthouse mobile d'au moins 90 sur chaque page publique.
- [ ] Aucune erreur d'accessibilité bloquante (axe) et parcours clavier complet des deux grands formulaires.
- [ ] /admin est protégé par 2FA, non indexé, et les exports sont journalisés.
- [ ] Les 8 e-mails passent SPF, DKIM et DMARC et s'affichent correctement dans Gmail, Outlook et Apple Mail.
- [ ] Sauvegarde restaurée avec succès lors d'un test.
- [ ] Stan dispose de tous les accès et du README.

## 12. Questions ouvertes et décisions à prendre

Ces points bloquent ou orientent le développement ; chacun a un responsable.

| # | Question | Responsable | Impact |
| --- | --- | --- | --- |
| 1 | Quel nom de domaine acheter (artilien.fr, artilien.com, autre) et quelle adresse mail pro utiliser ? | Stan | Mails, SPF/DKIM, mentions légales |
| 2 | Qui développe : freelance, agence, ou développement par Claude Code avec revue humaine ? Budget disponible ? | Stan | Choix de la stack, planning, outils |
| 3 | Le logo existe-t-il ? Sinon le développeur propose-t-il une version simple ? | Stan | Maquettes |
| 4 | Texte exact des 3 consentements du formulaire actuel et des questions du formulaire de retour après refus : à exporter des Google Forms | Stan, Conseiller juridique | Formulaires 5.1 et 5.3 |
| 5 | Quel délai de réponse annoncer à un particulier après sa demande (ou aucun) ? | Stan | Pages de confirmation, honnêteté de la promesse |
| 6 | Présenter publiquement l'équipe d'agents IA (transparence) ou seulement Stan ? Photo et prénom de Stan sur le site ? | Stan | Page À propos |
| 7 | Statut de TVA réel (franchise en base ou assujetti) pour l'affichage des tarifs | Stan, Conseiller juridique | /tarifs, CGV, factures |
| 8 | Que faire des demandes hors des trois zones : liste d'attente seule, ou ouverture des zones à la demande ? | Stan | Contrôle de zone |
| 9 | Le site accepte-t-il les demandes qui portent sur la rénovation énergétique ou l'adaptation du logement ? Les consentements de ces demandes demandent un avis juridique | Conseiller juridique | Liste des lots, contenu |
| 10 | Durées de conservation de la section 6.4 : validées ? | Conseiller juridique | RGPD |
| 11 | Faut-il garder une copie des formulaires Google Forms en secours pendant la transition ? Pendant combien de temps ? | Stan | Migration |
| 12 | Version 2 : page par métier et par ville, blog, espace artisan connecté, paiement Stripe sur le site, avis vérifiés : quel ordre ? | Stan | Planning futur |

**Hypothèses retenues faute de réponse** : domaine à acheter ; stack de la section 9 ; photos et logo libres de droits ou simples ; aucun délai promis ; hors zone = liste d'attente ; rénovation énergétique exclue du site tant qu'elle n'est pas validée.

**Sources internes** : Playbook ArtiLien (sections 2, 5, 7, 10 et 11), CRM Google Sheet (onglets Paramètres, Zones, Artisans, Clients, Journal, « Signaux chantiers », « Sources sociales »), décisions de Stan des 16 au 21/11/2026.
