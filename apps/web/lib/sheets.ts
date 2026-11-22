import { google } from "googleapis";

// Écrit une ligne dans un onglet du CRM. Compte de service Google, accès limité au classeur CRM.
// ATTENTION : l'ordre des colonnes doit être celui des onglets actuels (voir PLAN.md étape 4).
function client() {
  const email = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const key = process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, "\n");
  if (!email || !key) throw new Error("Identifiants Google manquants");
  const auth = new google.auth.JWT({ email, key, scopes: ["https://www.googleapis.com/auth/spreadsheets"] });
  return google.sheets({ version: "v4", auth });
}

export type Onglet = "Réponses au formulaire 1" | "Inscriptions artisans" | "Retours refus";

export async function ajouterLigne(onglet: Onglet, valeurs: (string | number | boolean)[]) {
  const spreadsheetId = process.env.GOOGLE_SHEET_ID;
  if (!spreadsheetId) throw new Error("GOOGLE_SHEET_ID manquant");
  await client().spreadsheets.values.append({
    spreadsheetId,
    range: `'${onglet}'!A1`,
    valueInputOption: "RAW", // RAW : pas d'interprétation de formules (anti-injection de formule)
    insertDataOption: "INSERT_ROWS",
    requestBody: { values: [valeurs.map((v) => neutraliser(v))] },
  });
}

// Une valeur commençant par = + - @ pourrait être interprétée comme formule dans un tableur.
function neutraliser<T extends string | number | boolean>(v: T): T | string {
  return typeof v === "string" && /^[=+\-@]/.test(v) ? `'${v}` : v;
}
