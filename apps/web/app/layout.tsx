import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "ArtiLien – Trouvez un artisan pour vos travaux",
  description: "Décrivez votre chantier, nous trouvons un artisan du bâtiment près de chez vous. Gratuit pour les particuliers.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap"
        />
      </head>
      <body>
        <header className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-5">
          <Link href="/" className="font-titre text-2xl font-bold">ArtiLien</Link>
          <nav className="flex gap-6 text-secondaire">
            <Link href="/demande">Particuliers</Link>
            <Link href="/artisans">Artisans</Link>
          </nav>
          <Link href="/demande" className="rounded-full bg-orange px-5 py-3 font-bold text-marine">Demander un artisan</Link>
        </header>
        <main>{children}</main>
        <footer className="mx-auto mt-16 max-w-6xl border-t border-bordure px-6 py-8 text-sm text-secondaire">
          ArtiLien – Stanislas Roux, EI – SIREN 133060277
        </footer>
      </body>
    </html>
  );
}
