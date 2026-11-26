import { Link as RouterLink } from "expo-router";
import { Image as ExpoImage } from "expo-image";
import { cssInterop } from "nativewind";
import { Text as RNText, View as RNView } from "react-native";

// Link and Image come from third-party packages, so cssInterop maps their
// `className` prop to `style`. View and Text are plain re-exports: `className`
// on them works only because babel.config.js sets
// `jsxImportSource: "nativewind"`. Removing that option breaks them silently.
export const View = RNView;
export const Text = RNText;

export const Link = cssInterop(RouterLink, { className: "style" });
export const Image = cssInterop(ExpoImage, { className: "style" });
