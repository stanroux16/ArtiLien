import { Text, View } from "react-native";
import { colors } from "@artilien/shared";

export default function Artisan() {
  return (
    <View style={{ padding: 24 }}>
      <Text style={{ color: colors.texte, fontSize: 18 }}>
        Espace artisan : demandes reçues, accepter ou refuser, notifications (à construire, PLAN.md étape 7).
      </Text>
    </View>
  );
}
