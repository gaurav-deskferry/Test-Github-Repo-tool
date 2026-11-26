# Project memory

Notes the coding agents read before working here. Written by Loopferry when a run learns something,
and yours to edit, reorder or delete at any time.

## Gotchas

- Sandbox cannot reach cdn.jsdelivr.net, so FastAPI /docs does not render in a browser unless CDN requests are intercepted (e.g. Playwright route to npm swagger-ui-dist). System python has no pip/venv; bootstrap pip from a wheel via files.pythonhosted.org.
