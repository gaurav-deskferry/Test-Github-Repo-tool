# Quick-commerce app (Blinkit-style) — Expo Router + NativeWind

Stack: Expo SDK 58, Expo Router (file routes in `src/app`), NativeWind 4.2 (latest stable) + Tailwind CSS 3.4
(NativeWind 4 does not support Tailwind 4; NativeWind 5 is still `rc`), TypeScript.

## Phases

| # | Phase | Outcome |
|---|-------|---------|
| 1 | **Foundation (this phase)** | Expo Router app, NativeWind/Tailwind wired (Metro, Babel, PostCSS, `global.css`), root layout, className-only index screen, `tw` wrappers (View/Text/Link/Image) |
| 2 | Design system & navigation shell | Theme tokens (brand yellow/green), Button/Chip/Card/Skeleton primitives, bottom tabs (Home, Categories, Cart, Account), safe areas |
| 3 | Catalog & home | Mock API/JSON, category grid, product cards with "ADD" stepper, banners carousel, search with debounced filter, product detail route `product/[id]` |
| 4 | Cart & checkout | Cart store (Zustand) persisted w/ AsyncStorage, bill summary, delivery slot/ETA, address picker, fake payment, order success |
| 5 | Auth & profile | Phone-OTP login (mock → real), secure token storage (expo-secure-store), addresses, order history |
| 6 | Backend integration | REST/GraphQL client + TanStack Query, inventory per dark-store by location, order tracking (polling → websockets), push notifications |
| 7 | Quality & release | Jest + RNTL unit tests, Maestro e2e, a11y pass, perf (FlashList, image caching), EAS Build/Update, Sentry, analytics |

## Target architecture

```
src/
  app/                 # routes only (expo-router)
    _layout.tsx        # root providers + Stack
    index.tsx          # home
    (tabs)/ product/[id].tsx cart.tsx checkout.tsx   # later phases
  components/
    tw/                # className-enabled wrappers (View, Text, Link, Image)
    ui/                # design-system primitives (phase 2)
    features/          # catalog, cart, checkout widgets
  features/<domain>/   # hooks, api, store, types per domain (catalog, cart, auth, orders)
  lib/                 # api client, storage, formatting
  global.css           # Tailwind entry
```
Principles: routes thin, domain logic in `features/`, styling only through `className`, server state in TanStack Query,
client state (cart, session) in Zustand, mock data behind the same interface as the real API so phase 6 is a swap.
Risks: NativeWind 4 / Tailwind 3 pinning; Reanimated + worklets native versions must match SDK (`expo install --fix`).

## Phase 1 — detailed steps
1. Scaffold blank-typescript Expo app; switch `main` to `expo-router/entry`; remove `App.tsx`/`index.ts`.
2. Install expo-router, nativewind, tailwindcss@3, reanimated, worklets, safe-area-context, screens, web deps, expo-image.
3. Config: `tailwind.config.js` (nativewind preset, content globs), `babel.config.js` (jsxImportSource nativewind + nativewind/babel),
   `metro.config.js` (`withNativeWind`, input `src/global.css`), `postcss.config.js`, `nativewind-env.d.ts`, `app.json` (scheme, web bundler metro, router plugin).
4. `src/global.css` with `@tailwind` directives; imported in root layout.
5. `src/components/tw/*`: `cssInterop` wrappers for Link and Image; View/Text are re-exports that rely on babel `jsxImportSource: "nativewind"` for `className`.
6. `src/app/_layout.tsx` (Stack, status bar) and `src/app/index.tsx` using only `className`.
7. Verify: `tsc --noEmit`, `expo export --platform web`, browser screenshot/video of the web build.

## Testing in the browser (Expo web)
`npm run web` serves the app at http://localhost:8081 (Metro + react-native-web), so UI can be checked and automated
(Playwright) without a simulator. `tailwind.config.js` sets `darkMode: "class"`; with the default `media` mode NativeWind 4
throws "Cannot manually set color scheme" on web and an error overlay blocks all clicks.
