# Fiche de choix – votre futur site

Répondez simplement par mail, en reprenant les numéros. Tout reste modifiable après.

**Brochure de personnalisation** (couleurs, polices, 7 logos, tons, photos, sections en plus) : page `https://<DOMAINE>/m/<slug>/personnalisation.html` + PDF joint. Réponse type : « Couleurs B – Police A – Logo 3 – Ton C – Photos A ».

**1. Couleurs** (3 ambiances, voir la maquette) : A / B / C
**2. Ton des textes** : A convivial et proche · B sérieux et rassurant · C haut de gamme et sobre
**3. Photos** : j'envoie mes photos / je n'en ai pas (on utilise des visuels génériques provisoires)
**4. Nom de domaine** (adresse du site) : choisissez dans la liste ci-dessous, ou proposez le vôtre
**5. Vos services à mettre en avant** (4 à 6, avec une phrase chacun) :
**6. Votre zone d'intervention / votre adresse :**
**7. Horaires :**
**8. Email et téléphone à afficher :**
**9. Vos informations légales** (pour les mentions légales) : forme juridique, SIRET, assurance, médiateur si vous vendez à des particuliers
**10. Sections en plus ?** galerie de réalisations · avis clients · prise de rendez-vous · tarifs · FAQ
**11. Votre logo** : j'en ai un / je n'en ai pas
**12. Un site que vous aimez** (facultatif) : lien

## Correspondance technique (usage interne / agents)

| N° | Champ du fichier client JSON |
|----|------------------------------|
| 1 | `palette` (A/B/C = ordre des palettes du secteur dans `THEMES`) |
| 1bis | `police` (A = absent, B = `classique`, C = `moderne`) |
| 11bis | `logo` (1 `icone`, 2 `capitales`, 3 `souligne`, 4 `deux-lignes`, 5 `point`, 6 `encadre`, 7 `serif`) |
| 2 | `ton` (à utiliser pour réécrire `accroche` et `presentation`) |
| 3 | `photos` |
| 4 | domaine choisi |
| 5 | `services` (liste de `titre`, `texte`, `icone`) |
| 6 | `ville`, `zone`, `adresse` |
| 7 | `horaires` |
| 8 | `email`, `tel` |
| 9 | `legal` (`forme`, `siret`, `tva`, `directeur`, `reglemente`, `mediateur`) |
| 10 | sections à ajouter |
| 11 | `logo` |
