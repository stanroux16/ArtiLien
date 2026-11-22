import { PALIERS_PRIX, PRIX_PREMIER_CLIENT } from "@artilien/shared";

export const metadata = { title: "Artisans – ArtiLien" };

export default function Artisans() {
  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="mb-4 font-titre text-4xl font-bold">Artisans : l'inscription est gratuite</h1>
      <p className="mb-6 text-lg text-secondaire">
        Vous payez seulement les mises en relation que vous acceptez, au prix annoncé d'avance. Premier client : {PRIX_PREMIER_CLIENT} €.
      </p>
      <ul className="rounded-carte border border-bordure bg-surface p-6">
        {PALIERS_PRIX.map((p) => (
          <li key={p.jusquA} className="flex justify-between border-b border-bordure py-2 last:border-0">
            <span>Lot jusqu'à {p.jusquA.toLocaleString("fr-FR")} €</span><strong>{p.prix} €</strong>
          </li>
        ))}
      </ul>
      <p className="mt-6 text-secondaire">Le formulaire d'inscription (5 étapes, vérification du SIRET) est à construire : voir PLAN.md, étape 5.</p>
    </section>
  );
}
