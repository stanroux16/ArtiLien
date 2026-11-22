import nodemailer from "nodemailer";
import { ENTREPRISE } from "@artilien/shared";

// Envoi depuis artilien.contact@gmail.com (limite ~500 mails/jour). À remplacer par le domaine propre
// (Resend/Brevo + SPF/DKIM/DMARC) après achat du nom de domaine.
function transporteur() {
  const user = process.env.GMAIL_USER;
  const pass = process.env.GMAIL_APP_PASSWORD;
  if (!user || !pass) throw new Error("Identifiants Gmail manquants");
  return nodemailer.createTransport({ service: "gmail", auth: { user, pass } });
}

const echapper = (s: string) =>
  s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);

export async function envoyerConfirmationDemande(destinataire: string, prenom: string, reference: string) {
  const html = `<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;color:#1F2937">
  <h2 style="color:#1B2A49">Votre demande est bien reçue</h2>
  <p>Bonjour ${echapper(prenom)},</p>
  <p>Nous avons bien reçu votre demande (référence <strong>${echapper(reference)}</strong>). Nous cherchons un artisan membre adapté à votre chantier ; s'il accepte, il vous contactera directement.</p>
  <p>Ce service est gratuit pour vous. Vos données ne sont partagées qu'avec l'artisan concerné.</p>
  <hr style="border:none;border-top:1px solid #E5E7EB"/>
  <p style="font-size:12px;color:#4B5563">${ENTREPRISE.nom} – ${ENTREPRISE.exploitant} – SIREN ${ENTREPRISE.siren}<br/>
  Pour ne plus rien recevoir, répondez STOP à ce mail.</p></div>`;
  await transporteur().sendMail({
    from: `"ArtiLien" <${process.env.GMAIL_USER}>`,
    to: destinataire,
    subject: "ArtiLien – Nous avons bien reçu votre demande",
    text: `Bonjour ${prenom}, votre demande (réf. ${reference}) est bien reçue. Un artisan membre vous contactera s'il accepte. Gratuit pour vous. Répondez STOP pour ne plus rien recevoir.`,
    html,
  });
}
