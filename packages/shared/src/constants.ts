export const SIRET_REGEX = /^\d{14}$/;

export const ZONES = [
  { code: "34", nom: "Hérault (Montpellier)" },
  { code: "67", nom: "Bas-Rhin (Strasbourg)" },
  { code: "69", nom: "Rhône (Lyon)" },
] as const;

export const TYPES_TRAVAUX = [
  "Maçonnerie / gros œuvre",
  "Toiture / charpente",
  "Plomberie / chauffage",
  "Électricité",
  "Peinture / revêtements",
  "Menuiserie / isolation",
  "Rénovation complète",
  "Autre",
] as const;

export const DELAIS = ["Dès que possible", "Dans 1 à 3 mois", "Dans 3 à 6 mois", "Plus tard"] as const;

// Prix par mise en relation (€) - premier client 10 € ; voir cahier des charges section 4.5
export const PRIX_PREMIER_CLIENT = 10;
export const PALIERS_PRIX = [
  { jusquA: 10_000, prix: 49 },
  { jusquA: 50_000, prix: 99 },
  { jusquA: 150_000, prix: 199 },
  { jusquA: 1_000_000, prix: 399 },
] as const;

export const ENTREPRISE = {
  nom: "ArtiLien",
  exploitant: "Stanislas Roux, EI",
  siren: "133060277",
  siret: "13306027700018",
  contact: "artilien.contact@gmail.com",
} as const;
