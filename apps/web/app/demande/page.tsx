import { FormulaireDemande } from "@/components/FormulaireDemande";

export const metadata = { title: "Demander un artisan – ArtiLien" };

export default function Demande() {
  return (
    <section className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="mb-2 font-titre text-4xl font-bold">Décrivez votre chantier</h1>
      <p className="mb-8 text-secondaire">Gratuit pour vous, sans engagement. Trois minutes.</p>
      <FormulaireDemande />
    </section>
  );
}
