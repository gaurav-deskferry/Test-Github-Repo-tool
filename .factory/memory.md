# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- The sandbox proxies HTTPS with an untrusted cert, so any headless-browser check of a page using CDN assets (index.html loads Vue and Tailwind from CDNs) must launch chromium with args ['--ignore-certificate-errors'] or the scripts fail with ERR_CERT_AUTHORITY_INVALID and the app never mounts.
- index.html renders cards through Vue components whose root element is `surface-card` (a plain <div>), so DOM assertions must target `#agents > div.grid > div` / `#pricing > div.grid > div` — selectors like `article` or `[data-*]` match nothing. The `id` on `<section-shell id="...">` does land on the rendered <section> via attribute fallthrough. Also note the Builder plan is $0 at both billing per…
- index.html does not exist on the default branch main (which holds only Test.md); it lives on the factory/in-factory-can-you-make-an-index-html-wi-b03f17e5 branch, so any task touching index.html must branch from there, not main.
