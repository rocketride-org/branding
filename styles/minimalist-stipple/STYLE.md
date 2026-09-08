# Minimalist Stipple

Isolated black-ink subjects on flat off-white. Built for small formats, crops, and text overlays.

## When to use

Display banners, Meta and social creative, docs spot art, card headers, pricing tiers, slide
corners, README art. Anything under about 800px, anything that gets cropped to more than one aspect
ratio, anything that has copy sitting on top of it.

The style holds up from roughly 320px to 1200px on the long edge. Below 320px only the helmet
close-up crops survive — in this batch that is `visor-grid`.

**The delivered batch caps out well below that range.** See Output and Gaps.

## Color

Pull from `tokens/rocketride.tokens.json`.

| Layer | Token | Value |
| --- | --- | --- |
| Linework | `illustration.ink` | `#12111a` |
| Background | `illustration.ground` | `#eeede7` |
| Overlay accent | `brand.accent` | `#f93822` |

The illustration is two-color, always. Ink and ground, nothing else. Brand red enters only in the
overlay layer (CTA, rule, eyebrow) and stays under 5% of the frame. If red is in the artwork itself,
the asset is wrong.

Ground is warmer than `surface.bg` on purpose. It keeps the art reading as art rather than as a UI
panel that failed to load.

### Accent contrast gate

`brand.accent` on `illustration.ground` measures **3.19:1**. That clears the 3:1 threshold for large
text but fails the 4.5:1 needed for normal-size text. So an accent word in a headline is only legal
at 24px and above. At 300x250 and below, headlines fall under that gate and the accent word must
turn off — small units are ink-only. This is a hard rule, not a preference.

The retired orange `#f7901f` measures 2.00:1 on the same ground and could never have done this job
at any size. That is part of why it was retired; see `_deprecated` in the token file.

## Locked prompt

Every asset uses this base with a per-asset subject delta appended. Same model, same seed family,
one sitting. Generating a second batch weeks later against the same prompt does not reliably produce
the same style.

```
Minimalist black ink stipple and cross-hatch engraving illustration.
Single subject, isolated on a flat warm off-white background (#eeede7).
Pure black linework (#12111a), no gradients, no color, no shading beyond
dotwork and hatching. Retro-futurist NASA-era spacesuit: segmented joints,
thick collar ring, chest control box, mirror-black visor with no visible
face. Sparse four-point star sparkles, six maximum. Generous empty negative
space around the subject. Vintage woodcut poster feel. No text, no logos,
no border, no frame.
```

Negative prompt:

```
color, gradient, photorealism, text, watermark, signature, busy background,
architecture, ground plane, horizon line, rectangular border, drop shadow, glow
```

## Composition rules

- One focal point per frame. Anything needing a second glance is dead at 300x250.
- 40% of the frame stays empty. That empty area is where copy goes, so record which side it is on
  when the asset is committed — the table below does this.
- Subject sits on a horizontal third, not dead center, unless the primary use is a square crop.
- Stars are the only permitted background element. No ruins, no cities, no ground plane. Those
  belong to `moebius-scene`.
- The subject must be readable in silhouette at 160px wide. If it is not, cut the asset rather than
  fixing it.
- No text baked into the image, ever. Copy, logo, and CTA are a separate overlay layer so one
  illustration serves several creatives and several sizes without regeneration.

## Output (this batch, as delivered)

~290-307 x 205-223 px, PNG, 24bpp RGB, **no alpha**.

Source: `20-illustrations-contact-sheet-updated.png`, a single 1536x1024 contact sheet. Each asset is
a tile crop from that sheet with frame borders and captions removed. That sheet is the only artifact
carrying original render fidelity; it is not committed here because source and campaign material
lives outside this repo, but its identity and dimensions are recorded so the provenance survives.

Fit for web thumbnails, docs spot art, and small display units. **Not fit for print or hero use.**

The intended output spec, which this batch does not meet, is 4000px on the long edge, PNG, with two
versions of every asset: one on flat `illustration.ground` and one with the ground knocked out to
alpha. The alpha version is what survives a reframe into an odd IAB ratio without a regeneration.

Filenames are kebab-case and describe the subject: `two-hands-reaching.png`, `geodesic-assembly.png`.
Not the campaign, not the size. The delivered files carried a `01-`..`20-` contact-sheet ordinal
prefix, which is neither subject nor campaign; it was dropped on commit and is preserved in the
table below for traceability back to the sheet.

## Assets

20 files. Copy space is measured, not eyeballed: ink coverage was computed per asset and split
left/right and top/bottom.

| # | Asset | Size | Ink | Copy space |
| --- | --- | --- | --- | --- |
| 01 | `two-hands-reaching` | 307x216 | 11.2% | none decisive |
| 02 | `tether-line` | 300x212 | 14.6% | **left** |
| 03 | `handoff-cube` | 290x212 | 17.5% | top |
| 04 | `three-helmets-row` | 300x212 | 26.2% | top |
| 05 | `umbilical-port` | 299x212 | 34.4% | **right** |
| 06 | `geodesic-assembly` | 306x220 | 30.2% | top |
| 07 | `gantry-arm` | 301x220 | 22.3% | none decisive |
| 08 | `module-stack` | 290x220 | 14.0% | none decisive |
| 09 | `blueprint-sheet` | 300x220 | 9.9% | the blank sheet itself |
| 10 | `keystone` | 299x223 | 25.6% | top |
| 11 | `boot-prints` | 306x205 | 5.3% | **right** |
| 12 | `crew-formation` | 300x205 | 24.9% | bottom |
| 13 | `hands-off` | 290x205 | 21.3% | none decisive |
| 14 | `satellite-swarm` | 300x205 | 13.2% | none decisive |
| 15 | `visor-grid` | 299x207 | 59.4% | none — full bleed |
| 16 | `geodesic-world` | 306x217 | 19.9% | top |
| 17 | `ignition` | 299x216 | 28.4% | top (plume fills bottom 93%) |
| 18 | `crescent-perch` | 290x215 | 19.6% | **right** |
| 19 | `orbital-ring` | 301x217 | 33.5% | top |
| 20 | `flag-crest` | 299x216 | 11.3% | top |

All 20 were reviewed at 1:1 and again downscaled to 160px. Every one still reads in silhouette at
160px, so none were cut. `satellite-swarm` and `boot-prints` are the weakest at that size — the thin
orbit lines and the faint footprints start to break up — but the subject still resolves.

## Gaps

- **Masters were never generated at 4000px.** The batch is roughly a thirteenth of the target
  resolution, and no higher-resolution source exists — the 1536x1024 contact sheet is the origin, so
  re-exporting cannot recover detail that was never rendered. Regenerating the set at full
  resolution is outstanding work and blocks all print and hero use.
- **19 of 20 alpha knockouts are missing.** Only `visor-grid` has ever been knocked out, and that
  version lives outside this repo. Without alpha, reframing into a new aspect ratio means
  regenerating rather than recompositing.
- **Two assets are clipped in the source sheet itself.** `two-hands-reaching` is cut on the left edge
  and `module-stack` is cut at the bottom. Both are visible at 1:1. Not fixable by re-crop, because
  the sheet is the origin.
- **The delivered plate is not `illustration.ground`.** It is a non-uniform near-white sampling
  `#f1f1f1` to `#ffffff` at the corners, against a token value of `#eeede7`. Compositing these onto
  the real ground requires an alpha knockout, not a background swap — pasting a tile straight onto
  `#eeede7` leaves a visible lighter rectangle. Likewise the ink is near-black rather than `#12111a`.
- **Seven assets have no decisive empty side**, against a composition rule that requires 40% of the
  frame to stay empty and recorded. `visor-grid` at 59.4% ink breaks the rule outright — it is a
  deliberate full-bleed helmet crop, useful precisely because it survives below 320px, but it cannot
  carry an overlay. Treat the seven as ink-only or icon-scale assets until the set is regenerated.
