import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { colors } from "@artilien/shared";

export default function Layout() {
  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: colors.fond },
          headerTintColor: colors.texte,
          contentStyle: { backgroundColor: colors.fond },
        }}
      />
    </>
  );
}
