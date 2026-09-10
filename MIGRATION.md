# Migration: v1.0 to v2.0

What changed, what it breaks, and why. v1.0 is preserved on the `version/1.0` branch.

## Breaking path changes

Every path below moved. Nothing inside this repo referenced them, so nothing here broke — but
external consumers (the Cloud site, docs, decks, the org README, Slack) are invisible from this
checkout and are the real exposure.

| v1.0 | v2.0 |
| --- | --- |
| `assets/<name>.png` | `styles/moebius-scene/assets/<name>.png` |
| `Palette.png` | `deprecated/Palette.png` |

### The free redirect

`version/1.0` preserves the entire v1 tree, so any live raw URL can be repointed without duplicating
a single file:

```
https://raw.githubusercontent.com/rocketride-org/branding/main/assets/<name>.png
                                                          ^^^^
https://raw.githubusercontent.com/rocketride-org/branding/version/1.0/assets/<name>.png
```

That branch is a permanent redirect target. Point stale links at it, then migrate them to the new
paths at leisure.

### Precedent

This is not the first break. Commit `ca683e7` (2026-06-03) renamed every logo file from PascalCase
(`RocketRide-logo-fullcolor-transparent.svg`) to the current lowercase scheme, with no shim and no
deprecation window. Anything pinned to pre-June-2026 logo names has been broken since then.

## Color: orange is retired, red is the brand

The v1 draft token file called brand `#f7901f` orange. The shipping Cloud hero was sampled directly
and uses `#f93822` — the logo red — as its accent, on `#eeede7` ground with `#12111a` ink. All three
draft values drifted from what shipped, and the accent one was not a rounding error.

Red is now `brand.brand`. Orange is in `_deprecated` and appears in no live token.

This was not simply ratifying an accident. Orange **cannot** do the accent job: `#f7901f` measures
2.00:1 on the illustration ground, so it fails as an accent word at any size, while `#f93822`
measures 3.19:1 and clears the large-text threshold. The token file and the product disagreed, and
the product was right.

| Value | v1 role | v2 |
| --- | --- | --- |
| `#f7901f` | `brand.brand` | retired |
| `#f93822` | `logo.red`, a documented exception | `brand.brand` |
| `#1e1a34` | `logo.ink` (Abyss Blue) | retired |
| `#0a0a0a` | `illustration.ink` | replaced by `#12111a` |
| `#eceae3` | `illustration.ground` | replaced by `#eeede7` |

## Logos

- Hex casing normalized to lowercase across all four SVGs. The two `-icon-` files used uppercase
  inline fills; the two `-logo-` files used lowercase in an Illustrator `<style>` block.
- Abyss Blue `#1e1a34` replaced with `#12111a` in `rocketride-icon-color.svg` and
  `rocketride-logo-color.svg`. The logo no longer references the superseded palette.
- A circle-™ glyph was added to both wordmark SVGs. The viewBox widened from `0 0 1315.1 192.5` to
  `0 0 1363.3 192.5` to fit it.
- All four PNGs re-exported by `logos/export_png.py`. **The wordmark PNGs changed size**, 1920x332 to
  1996x332, because the viewBox grew. Wordmark height and padding are unchanged, so the letterforms
  keep their optical size and only the canvas is wider. Icon PNGs stay 382x383.

### Why `chore/update-logos` was not merged

That branch (two commits by a different author, 2026-06-17) is where the ™ came from, and its intent
was legitimate. Its delivery was not:

- It adds two duplicate opaque `<rect fill="#ffffff" x="-144" width="1728" y="-24.9" height="298.8">`
  covering the whole viewBox. All four of its logo files are 24bpp RGB with corner pixel
  `A=255 RGB=255,255,255`, against `A=0` on `main`. **`rocketride-logo-white.png` on that branch is
  white artwork on an opaque white plate — invisible.**
- It bloats `rocketride-logo-color.svg` from 5,565 to 19,203 bytes via a clipPath-heavy generic
  export that discards the clean Illustrator class structure.
- It hardcodes `width="1920" height="332"` on the `<svg>`, which breaks CSS-scalable usage.
- It colors the ™ `#000000` rather than a brand token.

So only the glyph was carried across. The three ™ paths were lifted from that branch and wrapped in
a transform mapping its coordinate space into `main`'s. The map was derived by fitting the icon
rocket and swoosh path origins, which are the same authored shapes in both files:

```
branch = main * 1.03802 + (6.0134, 34.0703)     residuals < 0.1 user units
```

giving the inverse `transform="scale(0.963391) translate(-6.0134 -34.0703)"` on the glyph group. The
glyph takes `class="st1"`, so it inherits the wordmark color in both variants rather than carrying
its own. Result was rendered and inspected at 520px, 260px, and 130px on white, on dark, and on the
illustration ground before commit.

**Do not merge `chore/update-logos`.** If it is ever revived, the transparency regression has to be
fixed first.

### `version/1.0` also carries `logos/rocketride-profile.jpg`

136KB, not on `main`, added when v1.0 was branched. It was **not** brought into v2.0 — it is a social
profile crop with no `STYLE.md`, no documented dimensions, and no clear owner. Retrieve it from
`version/1.0` if it turns out to be in use.

## New: verification that actually runs

Two scripts now back claims that used to be prose.

```sh
python tokens/check_contrast.py tokens/rocketride.tokens.json
python tokens/gen_css.py tokens/rocketride.tokens.json | diff - tokens/rocketride.css
```

`check_contrast.py` computes all 66 contrast obligations, asserts no live token resolves to a retired
value, and cross-checks every ratio quoted in the token file's own descriptions against a computed
one. That last check caught five wrong numbers during this migration — four dark-theme status ratios
measured against a superseded surface value, and a disabled-text ratio measured against the wrong
background. They are fixed. The point is that the next such error is a failing script rather than a
number someone believes.

## Assets

- 25 `moebius-scene` assets moved, unchanged. `git log --follow` reaches `46a4acb`.
- 20 `minimalist-stipple` assets added, checksums matching the delivered originals. The `01-`..`20-`
  contact-sheet ordinal prefix was dropped, since it describes neither subject nor campaign; the
  mapping is preserved in that style's `STYLE.md`.
- Not brought in, because campaign material lives outside this repo: `gen_poc.py`, the 12 POC
  creatives, the 36 wave-1 creatives, `manifest.csv`, and the four contact sheets.

The stipple batch ships at roughly a thirteenth of its own target resolution, with two assets clipped
in the source sheet and 19 of 20 alpha knockouts missing. That is documented in its `STYLE.md` Gaps
section rather than smoothed over, because a spec that describes an aspiration while the directory
contains something else is how a style quietly dies.
