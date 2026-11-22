// Direction de design C (moderne, façon application). Source unique pour le web (Tailwind) et le mobile.
export const colors = {
  marine: "#1B2A49",
  orange: "#F28C28",
  orangeTexte: "#C85F0A", // orange lisible sur fond clair (contraste AA)
  fond: "#0E1730",
  surface: "#16224A",
  bordure: "#2C3C66",
  texte: "#E8ECF5",
  texteSecondaire: "#B8C2D9",
  blanc: "#FFFFFF",
  succes: "#1E7F4F",
  erreur: "#B42318",
  alerte: "#B54708",
} as const;

export const radius = { champ: 8, carte: 24, bouton: 999 } as const;
export const bouton = { hauteurMin: 48 } as const;
