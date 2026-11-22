"use server";
import { randomUUID } from "node:crypto";
import { demandeSchema } from "@artilien/shared";
import { ajouterLigne } from "./sheets";
import { envoyerConfirmationDemande } from "./mail";

export type EtatFormulaire =
  | { statut: "initial" }
  | { statut: "erreur"; erreurs: Record<string, string>; message?: string }
  | { statut: "ok"; reference: string };

export async function envoyerDemande(_: EtatFormulaire, formData: FormData): Promise<EtatFormulaire> {
  // Anti-spam simple : champ piège (honeypot) ; Turnstile à ajouter à l'étape 3 du plan.
  if (formData.get("site_web")) return { statut: "ok", reference: "ignore" };

  const brut = Object.fromEntries(formData.entries());
  const resultat = demandeSchema.safeParse({
    ...brut,
    consentementTraitement: brut.consentementTraitement === "on",
    consentementTransmission: brut.consentementTransmission === "on",
    consentementContact: brut.consentementContact === "on",
  });
  if (!resultat.success) {
    const erreurs: Record<string, string> = {};
    for (const i of resultat.error.issues) erreurs[String(i.path[0])] = i.message;
    return { statut: "erreur", erreurs };
  }

  const d = resultat.data;
  const reference = `D-${randomUUID().slice(0, 8).toUpperCase()}`;
  const horodatage = new Date().toISOString();

  // TODO étape 4 : enregistrer d'abord en base (source de vérité), puis synchroniser vers le Sheet avec reprise.
  try {
    await ajouterLigne("Réponses au formulaire 1", [
      horodatage, d.prenom, d.nom, d.email, d.telephone, d.adresse, d.codePostal, d.ville,
      d.typeTravaux, d.description, d.delai, "oui", "oui", "oui", reference,
    ]);
  } catch (e) {
    console.error("Échec écriture CRM", reference, e);
    return { statut: "erreur", erreurs: {}, message: "Une erreur est survenue. Réessayez dans quelques minutes." };
  }
  try {
    await envoyerConfirmationDemande(d.email, d.prenom, reference);
  } catch (e) {
    console.error("Échec mail de confirmation", reference, e); // la demande reste enregistrée
  }
  return { statut: "ok", reference };
}
