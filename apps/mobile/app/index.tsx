import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { Link } from "expo-router";
import { bouton, colors, radius } from "@artilien/shared";

// Écran d'accueil : choix du profil. Les écrans particulier (suivi de demande) et artisan
// (demandes reçues, accepter/refuser, notifications) sont à construire : voir PLAN.md étape 7.
export default function Accueil() {
  return (
    <ScrollView contentContainerStyle={s.page}>
      <Text style={s.titre}>Un chantier, un artisan, une demande.</Text>
      <Text style={s.texte}>
        Décrivez vos travaux, un artisan membre vous contacte. Gratuit pour les particuliers.
      </Text>
      <Link href="/particulier" asChild>
        <Pressable style={[s.bouton, { backgroundColor: colors.orange }]} accessibilityRole="button">
          <Text style={[s.boutonTexte, { color: colors.marine }]}>Je cherche un artisan</Text>
        </Pressable>
      </Link>
      <Link href="/artisan" asChild>
        <Pressable style={[s.bouton, s.bordure]} accessibilityRole="button">
          <Text style={[s.boutonTexte, { color: colors.texte }]}>Je suis artisan</Text>
        </Pressable>
      </Link>
      <View style={{ height: 24 }} />
    </ScrollView>
  );
}

const s = StyleSheet.create({
  page: { padding: 24, gap: 16 },
  titre: { color: colors.blanc, fontSize: 32, fontWeight: "700", lineHeight: 38 },
  texte: { color: colors.texteSecondaire, fontSize: 17, lineHeight: 25 },
  bouton: { minHeight: bouton.hauteurMin, borderRadius: radius.bouton, alignItems: "center", justifyContent: "center", paddingHorizontal: 24 },
  bordure: { borderWidth: 1, borderColor: colors.bordure },
  boutonTexte: { fontSize: 17, fontWeight: "700" },
});
