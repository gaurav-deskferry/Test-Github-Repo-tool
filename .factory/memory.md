# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- As of 2026-11-24, main contains only Test.md. There is no source code, no package.json and no test framework, so tasks about code or tests have nothing to act on until code is merged into main.
- sakura/index.html is too heavy for the sandbox's software GL: at 1280x720 the record.cjs step runner hangs. Record with your own Playwright script at 640x360 and ?petals=100&grass=500&pixelRatio=1.
- sakura/index.html loads three.js from cdn.jsdelivr.net, which is unreachable in the sandbox, and the WebGL scene is too heavy for software rendering even at ?petals=20; browser QA of it is not feasible here.
- Sandbox lacks bun and pip; bun installs via `npm i bun` in a temp dir, and root package.json dev:api calls `python3`, so put a venv with requirements.txt first on PATH before `bun run dev`.
