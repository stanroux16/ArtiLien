"use client";
import { useActionState } from "react";
import { DELAIS, TYPES_TRAVAUX } from "@artilien/shared";
import { envoyerDemande, type EtatFormulaire } from "@/lib/actions";
import { Champ } from "./Champ";

const initial: EtatFormulaire = { statut: "initial" };

export function FormulaireDemande() {
  const [etat, action, enCours] = useActionState(envoyerDemande, initial);
  const e = etat.statut === "erreur" ? etat.erreurs : {};

  if (etat.statut === "ok") {
    return (
      <div role="status" className="rounded-carte border border-bordure bg-surface p-8">
        <h2 className="font-titre text-2xl font-bold">Demande reçue</h2>
        <p className="mt-2 text-secondaire">
          Référence {etat.reference}. Un mail de confirmation vient de partir. Un artisan membre vous contactera s'il accepte votre projet.
        </p>
      </div>
    );
  }

  return (
    <form action={action} className="flex flex-col gap-5">
      {/* champ piège anti-robots, invisible pour les humains */}
      <input type="text" name="site_web" tabIndex={-1} autoComplete="off" aria-hidden="true" className="hidden" />
      <div className="grid gap-5 md:grid-cols-2">
        <Champ nom="prenom" libelle="Prénom" erreur={e.prenom} autoComplete="given-name" />
        <Champ nom="nom" libelle="Nom" erreur={e.nom} autoComplete="family-name" />
        <Champ nom="email" libelle="Adresse e-mail" type="email" erreur={e.email} autoComplete="email" />
        <Champ nom="telephone" libelle="Téléphone" type="tel" erreur={e.telephone} autoComplete="tel" />
      </div>
      <Champ nom="adresse" libelle="Adresse du chantier" erreur={e.adresse} autoComplete="street-address" />
      <div className="grid gap-5 md:grid-cols-2">
        <Champ nom="codePostal" libelle="Code postal" erreur={e.codePostal} autoComplete="postal-code" />
        <Champ nom="ville" libelle="Ville" erreur={e.ville} autoComplete="address-level2" />
      </div>
      <label className="flex flex-col gap-1 font-medium">Type de travaux
        <select name="typeTravaux" required className="min-h-12 rounded-champ border border-bordure bg-surface px-4 font-normal">
          {TYPES_TRAVAUX.map((t) => <option key={t}>{t}</option>)}
        </select>
      </label>
      <label className="flex flex-col gap-1 font-medium">Décrivez votre chantier
        <textarea name="description" required rows={5} className="rounded-champ border border-bordure bg-surface p-4 font-normal" />
        {e.description && <span role="alert" className="text-sm font-normal text-erreur">{e.description}</span>}
      </label>
      <label className="flex flex-col gap-1 font-medium">Délai souhaité
        <select name="delai" required className="min-h-12 rounded-champ border border-bordure bg-surface px-4 font-normal">
          {DELAIS.map((t) => <option key={t}>{t}</option>)}
        </select>
      </label>
      {/* TODO textes exacts des 3 consentements à valider avec le Conseiller juridique (cahier des charges 5.1) */}
      {(["consentementTraitement", "consentementTransmission", "consentementContact"] as const).map((n, i) => (
        <label key={n} className="flex items-start gap-3 text-sm text-secondaire">
          <input type="checkbox" name={n} required className="mt-1 h-5 w-5" />
          <span>[Texte du consentement {i + 1} à valider]</span>
        </label>
      ))}
      {etat.statut === "erreur" && etat.message && <p role="alert" className="text-erreur">{etat.message}</p>}
      <button disabled={enCours} className="min-h-12 rounded-full bg-orange px-8 py-3 text-lg font-bold text-marine disabled:opacity-60">
        {enCours ? "Envoi…" : "Envoyer ma demande"}
      </button>
    </form>
  );
}
