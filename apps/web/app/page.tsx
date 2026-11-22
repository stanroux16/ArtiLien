import Link from "next/link";

export default function Accueil() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-16">
      <p className="mb-4 inline-block rounded-full border border-bordure px-4 py-1 text-sm text-secondaire">
        Montpellier · Strasbourg · Lyon
      </p>
      <h1 className="font-titre text-5xl font-bold leading-tight tracking-tight md:text-6xl">
        Un chantier, un artisan, une demande.
      </h1>
      <p className="mt-6 max-w-2xl text-xl text-secondaire">
        Décrivez vos travaux en trois minutes. Nous cherchons un artisan membre adapté et il vous contacte
        directement. Gratuit pour les particuliers.
      </p>
      <div className="mt-8 flex flex-wrap gap-3">
        <Link href="/demande" className="rounded-full bg-orange px-8 py-4 text-lg font-bold text-marine">Faire ma demande</Link>
        <Link href="/artisans" className="rounded-full border border-bordure px-8 py-4 text-lg font-bold">Je suis artisan</Link>
      </div>
    </section>
  );
}
