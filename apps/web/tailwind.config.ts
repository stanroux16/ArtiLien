import type { Config } from "tailwindcss";
import { colors } from "@artilien/shared";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        marine: colors.marine,
        orange: colors.orange,
        fond: colors.fond,
        surface: colors.surface,
        bordure: colors.bordure,
        texte: colors.texte,
        secondaire: colors.texteSecondaire,
        erreur: "#FF8A80", // erreur lisible sur fond sombre
      },
      borderRadius: { champ: "8px", carte: "24px" },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"], titre: ["Space Grotesk", "Inter", "sans-serif"] },
    },
  },
  plugins: [],
};
export default config;
