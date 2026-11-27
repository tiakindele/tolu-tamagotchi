# Agent instructions: Tolu Tamagotchi

A portable pixel-art companion for web pages: one classic script (`companion.js`), one stylesheet (`companion.css`) and six sprite sheets (`sprites/`). `README.md` is the source of truth for installation, options and the public API; read it before changing behaviour.

## Invariants

Hold these on every change, unless the user explicitly asks to change one:

- **Portable runtime.** Plain browser JavaScript and CSS, served as-is: no packages, no build step, no imports. `window.ToluCompanion` is the only global.
- **Host-agnostic.** The component knows nothing about any host site, framework, sign-in or network service. Host-specific code (adapters, paths, positioning tweaks) and host-specific docs live in the host project.
- **The host owns state.** Stats change only through the API. The component fetches, stores and sends nothing.
- **Stable public API.** `mount` and its options, the instance methods, the six mood names, the error types and the CSS class names are a contract with host pages. When one changes, update the README's tables in the same commit.
- **Approved artwork.** The six sheets in `sprites/` are approved art: keep them, their 288×48 six-frame layout and their pixelated rendering. Edit art only when asked, through `generate_sprites.py`, and check the result against `sprite-preview.png`.
- **Behaviour to keep:** click-to-celebrate, temporary poses that revert to the persistent mood, stats clamped to 0–100, reduced-motion support, the small-screen layout and the accessible labels.

## Making a change

1. Edit the sources: `companion.js`, `companion.css`, `demo.html`, or the art via `generate_sprites.py` (needs Pillow, a dev-only tool).
2. Rebuild the standalone demo, which is generated: `python3 scripts/build-standalone.py`. `--check` must print `OK`.
3. Verify in a real browser, both `standalone-demo.html` opened from disk and `demo.html` served with `python3 -m http.server`. Done means: no console errors and no failed requests; all six moods animate; both sliders move the bars and the numbers; Celebrate, Coffee break and clicking the avatar each play, then revert to the selected mood; a viewport of 480px or less shows the 96px layout; with reduced motion emulated the sprite holds still.
4. Update `README.md` for any change to installation, options, API, moods or styling hooks.

## Releases

Hosts pin a tag, so a tag is never moved. Tag releases `vMAJOR.MINOR.PATCH` on `main`; while on `0.x`, bump the minor for an API or visual change and the patch for a fix.
