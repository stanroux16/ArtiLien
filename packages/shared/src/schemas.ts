import { z } from "zod";
import { DELAIS, SIRET_REGEX, TYPES_TRAVAUX } from "./constants";

const telephone = z
  .string()
  .trim()
  .regex(/^(?:\+33|0)[1-9](?:[\s.-]?\d{2}){4}$/, "Numéro de téléphone français invalide");
const codePostal = z.string().trim().regex(/^\d{5}$/, "Code postal à 5 chiffres");
// Un champ texte libre : jamais de HTML, longueur bornée
const texte = (min: number, max: number) => z.string().trim().min(min).max(max);

export const demandeSchema = z.object({
  prenom: texte(1, 60),
  nom: texte(1, 60),
  email: z.string().trim().toLowerCase().email().max(120),
  telephone,
  adresse: texte(3, 160),
  codePostal,
  ville: texte(1, 80),
  typeTravaux: z.enum(TYPES_TRAVAUX),
  description: texte(10, 2000),
  delai: z.enum(DELAIS),
  // 3 consentements distincts, textes exacts à valider (cahier des charges 5.1)
  consentementTraitement: z.literal(true, { errorMap: () => ({ message: "Obligatoire" }) }),
  consentementTransmission: z.literal(true, { errorMap: () => ({ message: "Obligatoire" }) }),
  consentementContact: z.literal(true, { errorMap: () => ({ message: "Obligatoire" }) }),
});
export type Demande = z.infer<typeof demandeSchema>;

export const artisanSchema = z.object({
  siret: z.string().trim().regex(SIRET_REGEX, "SIRET à 14 chiffres, sans espaces"),
  raisonSociale: texte(1, 120),
  contactNom: texte(1, 80),
  email: z.string().trim().toLowerCase().email().max(120),
  telephone,
  metiers: z.array(texte(1, 60)).min(1).max(8),
  zones: z.array(z.string().regex(/^\d{2}$/)).min(1),
  decennale: z.boolean(),
  cgvAcceptees: z.literal(true, { errorMap: () => ({ message: "Obligatoire" }) }),
});
export type Artisan = z.infer<typeof artisanSchema>;

export const refusSchema = z.object({
  reference: texte(1, 40),
  motif: texte(1, 80),
  commentaire: z.string().trim().max(1000).optional(),
});
export type Refus = z.infer<typeof refusSchema>;

export const contactSchema = z.object({
  nom: texte(1, 80),
  email: z.string().trim().toLowerCase().email().max(120),
  message: texte(10, 2000),
});

export const desinscriptionSchema = z.object({ email: z.string().trim().toLowerCase().email().max(120) });
export const listeAttenteSchema = z.object({
  email: z.string().trim().toLowerCase().email().max(120),
  profil: z.enum(["particulier", "artisan"]),
});
