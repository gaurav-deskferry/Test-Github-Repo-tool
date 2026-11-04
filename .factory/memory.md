# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- The sandbox proxies HTTPS with an untrusted cert, so any headless-browser check of a page using CDN assets (index.html loads Vue and Tailwind from CDNs) must launch chromium with args ['--ignore-certificate-errors'] or the scripts fail with ERR_CERT_AUTHORITY_INVALID and the app never mounts.
