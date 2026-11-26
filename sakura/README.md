# Sakura Pond (Three.js)

A single-file Three.js scene: a natural meadow with a pond at the centre, ringed by
procedurally generated cherry blossom trees, shore stones, lily pads, swaying grass and
falling petals that land on the grass or float on the water. No buildings or monuments.

## Run

Three.js is loaded from the jsDelivr CDN via an import map, so the page needs a local
web server (ES modules don't load from `file://`):

```sh
cd sakura
python3 -m http.server 8080
# open http://localhost:8080
```

Drag to orbit, scroll to zoom. The camera slowly auto-rotates.

Optional URL parameters for slower machines: `?petals=300&grass=3000&pixelRatio=1`
(defaults: 900 petals, 9000 grass blades, pixel ratio up to 2).
