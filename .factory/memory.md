# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- run_test/tw-app: NativeWind 4 needs tailwindcss@3 (not 4) and babel-preset-expo installed explicitly; react-dom must match react 19.3.0 exactly or npm ERESOLVE.
- run_test/tw-app: pin native deps to node_modules/expo/bundledNativeModules.json versions (e.g. reanimated 4.7.1, worklets 0.13.0); expo install --fix needs the Expo API, which the sandbox cannot reach.
