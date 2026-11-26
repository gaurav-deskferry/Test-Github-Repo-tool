# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- The sandbox can't reach cdn.jsdelivr.net (the npm registry works). To QA CDN-based pages such as sakura/index.html, npm-install the library in /tmp and serve it to the page with Playwright ctx.route.
