# Moebius Scene

Full-bleed narrative scenes. Fine ligne claire linework with flat muted washes. This documents the
25 assets already in the repo, which were previously unlabeled and undocumented.

## When to use

Site heroes, full-bleed banners, deck section breaks, event backdrops, video plates. Anywhere the
art gets 800px or more of width and is allowed to carry atmosphere.

Do not use below about 400px. The linework is dense enough that detail collapses into grey mud on
downscale. Use `minimalist-stipple` instead.

## Subject vocabulary

- Weathered NASA-era spacesuits: segmented joints, thick collar rings, chest control boxes,
  mirror-black visors, no visible faces
- Monumental ruins, colonnades, arches, and plazas at a scale that dwarfs the figure
- Floating platforms and structures, tethered or free
- Multiple moons and ringed planets, low in frame
- Overgrowth reclaiming architecture
- Small craft and gantries at a distance
- Figures are almost always small in frame. Scale is the point of the style.

## Color

Flat muted washes, low saturation. Dusty blue-grey dominant, weathered off-white suits, sparing warm
rust accents on suit hardware.

These 25 assets predate the current token set **and** were built against the superseded palette in
`deprecated/Palette.png`. They are still usable as-is, but never sample colors out of them for UI
work — you would be pulling values off a retired system. UI color comes from
`tokens/rocketride.tokens.json`.

## Composition rules

- Wide or tall, rarely square.
- Figure placed against a much larger structure, off center.
- Atmospheric depth in three layers minimum: foreground element, mid-ground subject, background
  structure.
- No text baked into the image. The one exception is `rocketride-branding-banner.png`, which is a
  composite and should be treated as a finished piece, not a source asset.

## Assets

25 files. Naming is already kebab-case and subject-descriptive, which is the convention. Keep it.

Dimensions cluster into a small number of shapes:

| Shape | Count | Files |
| --- | --- | --- |
| `1672x941` (16:9 landscape) | 6 | `astronaut-crew-walking-spaceport-boulevard`, `astronaut-in-alien-city-with-moons`, `astronaut-in-floating-cloud-city`, `astronaut-overlooking-floating-ruins`, `astronauts-overlooking-floating-city-with-ships`, `crew-approaching-rocket-on-launch-pad` |
| `1068x1473` (portrait) | 3 | `astronaut-entering-concrete-ruins`, `astronaut-floating-above-overgrown-ruins`, `astronaut-walking-futuristic-city-plaza` |
| `941x1672` (9:16 portrait) | 3 | `astronaut-on-walkway-in-vertical-ruins`, `astronaut-sitting-in-field-rear-view`, `two-astronauts-on-geometric-ruins-platform` |
| `2172x724` (3:1 banner) | 2 | `panoramic-ruined-spaceport-with-astronauts`, `rocketride-branding-banner` |
| `1254x1254` (square) | 2 | `astronaut-facing-rocket-in-forest`, `helmet-closeup-in-asteroid-field` |
| `1448x1086` (4:3) | 2 | `astronauts-before-glowing-portal-tower`, `two-astronauts-reaching-in-space` |
| `1001x1572` | 2 | `astronaut-sitting-in-field-gazing-horizon`, `helmet-visor-reflecting-planet-surface` |
| singletons | 5 | `astronaut-helmet-closeup-city-reflection` 1086x1448, `astronaut-in-bustling-spaceport-city` 1122x1402, `helmet-visor-reflecting-rocket-launch` 971x1619, `two-astronauts-approaching-spaceport-gantry` 1437x1095, `two-astronauts-reaching-mosaic-style` 1536x1024 |

`panoramic-ruined-spaceport-with-astronauts.png` and `rocketride-branding-banner.png` are both
`2172x724` but are different images. Do not treat one as a copy of the other.

Subject coverage: alien cities, floating cloud cities, vertical and overgrown ruins, spaceport
gantries and boulevards, helmet close-ups with visor reflections, launch pads, portal towers, and
two-figure reaching compositions.

## Gaps

- **No asset in this set can hold a text overlay.** Every one of them is a full scene edge to edge.
  A scene-style hero with copy on it has to be generated fresh with a deliberate empty region, and
  none of the 25 have one. This is the single biggest limitation of the set.
- **No locked generation prompt.** These assets predate the practice, so this file documents the
  style descriptively rather than reproducibly. Regenerating a matching 26th asset is currently
  guesswork. Writing that prompt is outstanding work, and until it exists this style cannot be
  extended, only used.
- Aspect ratios are scattered across eleven shapes for 25 assets, which makes them awkward to slot
  into a fixed layout. Future additions should converge on the existing clusters.
