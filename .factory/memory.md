# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- The sandbox proxies HTTPS with an untrusted cert, so any headless-browser check of a page using CDN assets (index.html loads Vue and Tailwind from CDNs) must launch chromium with args ['--ignore-certificate-errors'] or the scripts fail with ERR_CERT_AUTHORITY_INVALID and the app never mounts.
- index.html renders cards through Vue components whose root element is `surface-card` (a plain <div>), so DOM assertions must target `#agents > div.grid > div` / `#pricing > div.grid > div` — selectors like `article` or `[data-*]` match nothing. The `id` on `<section-shell id="...">` does land on the rendered <section> via attribute fallthrough. Also note the Builder plan is $0 at both billing per…
- main holds only Test.md — index.html does not exist there. Any task about index.html must branch from factory/can-you-make-an-index-html-wiht-nice-hom-cf2e4304 (or a descendant), and the resulting PR cannot merge cleanly into main on its own.
- The sandbox's playwright is not resolvable from a scratch dir: import it from '/opt/npm-tools/node_modules/playwright/index.js' and as a CommonJS default export (`import pw from ...; const { chromium } = pw`). There is no dev server, so serve the repo with `python3 -m http.server` for QA.

## Conventions

- index2.html is a declared byte-identical backup of index.html (commit 8c9db1e). Editing index.html alone silently breaks that invariant; re-copy it and verify with `cmp index.html index2.html`.
