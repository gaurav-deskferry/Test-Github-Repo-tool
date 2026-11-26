import { Link as RouterLink } from "expo-router";
import { Image as ExpoImage } from "expo-image";
import { cssInterop } from "nativewind";
import { Text as RNText, View as RNView } from "react-native";

// cssInterop maps the `className` prop to `style` for components that
// don't go through NativeWind's jsx runtime (third-party components).
// RN View/Text are already covered by the jsx runtime; wrapping keeps one
// import path (`@/components/tw`) for every styled primitive.
export const View = RNView;
export const Text = RNText;

export const Link = cssInterop(RouterLink, { className: "style" });
export const Image = cssInterop(ExpoImage, { className: "style" });
