# RocketRide Branding

Colors, logos, and illustration styles. `tokens/` is the source of truth for color. Everything else
references it.

## Structure

```
tokens/                        color tokens, machine readable
  rocketride.tokens.json       canonical values
  rocketride.css               --rr-* custom properties, generated from the JSON
  gen_css.py                   the generator
  check_contrast.py            verifies every contrast obligation in the JSON
logos/                         logo and icon files
  export_png.py                re-exports the PNGs from the SVGs, preserving alpha
styles/                        illustration styles, one directory each
  moebius-scene/               full-bleed narrative scenes (25 assets)
  minimalist-stipple/          isolated black-ink subjects for small formats (20 assets)
deprecated/                    superseded, kept for reference only
MIGRATION.md                   what changed in v2.0 and what it breaks
```

## Rules

1. Color values live in `tokens/rocketride.tokens.json` and nowhere else. Do not hardcode hex in a
   doc, a deck, or a site. If a value is missing, add it to the token file first.
2. `rocketride.css` is generated from the JSON. Do not hand-edit it. Run
   `python tokens/gen_css.py tokens/rocketride.tokens.json` and commit the result.
3. Every illustration style gets a `STYLE.md` before any asset lands in its directory. The spec comes
   first, then the assets, so the style is reproducible by someone who was not in the room.
4. Asset filenames are kebab-case and describe the subject, not the campaign.
   `astronaut-planting-flag.png`, not `q4-banner-3.png`. Campaign use is tracked outside this repo.
5. Anything in `deprecated/` is reference only. Do not pull from it.
6. After changing a color, run `python tokens/check_contrast.py tokens/rocketride.tokens.json`. It
   must exit clean. Every ratio quoted in the token file is produced by that script, so a stale
   number is a test failure rather than folklore.

## Verify the repo

```sh
python tokens/check_contrast.py tokens/rocketride.tokens.json
python tokens/gen_css.py tokens/rocketride.tokens.json | diff - tokens/rocketride.css
```

The first asserts every contrast obligation. The second proves `rocketride.css` really is generated
and has not been hand-edited.

## Color at a glance

| Role | Token | Light | Dark |
| --- | --- | --- | --- |
| Brand / accent | `brand.accent` | `#f93822` | `#fa4c38` |
| Page background | `surface.bg` | `#ffffff` | `#12111a` |
| Body text | `text.primary` | `#1a1a1a` | `#f4f3f0` |
| Illustration ink | `illustration.ink` | `#12111a` | `#eeede7` |
| Illustration ground | `illustration.ground` | `#eeede7` | `#12111a` |

Two constraints that are easy to break by accident:

**The primary button is ink-filled, not accent-filled.** White on `#f93822` is 3.74:1, which fails
the 4.5:1 a normal-size label needs. The button fills with `#12111a` (18.74:1) and the accent
survives as a hard block offset down-left behind it, carrying no text. This is the construction the
shipping Cloud hero already uses. Anyone who "simplifies" it back to an accent-filled button
reintroduces an AA failure.

**The accent is large-text-only on light grounds.** 3.74:1 on white and 3.19:1 on the illustration
ground. Legal at 24px and above, illegal below it. Small display units are ink-only.

## Resolved in v2.0

**Logo color vs brand token.** The logo used `#f93822` red while the draft token file called brand
`#f7901f` orange. Sampling the shipping Cloud hero settled it: the product was already using the
logo red as its UI accent. Red is now `brand.brand`; orange is retired. Orange could not have taken
the job even if wanted — it measures 2.00:1 on the illustration ground and fails as an accent at any
size. The decision was made deliberately rather than left to the site to decide by default.

**Abyss Blue in the logo.** `#1e1a34` came from the superseded palette, which made the logo the last
artifact in the repo built on the old system. Replaced with `logo.ink` `#12111a`.

**Hex casing.** All logo SVGs are lowercase.

## Open decisions

**Dark theme, status colors, and interaction states are proposed, not approved.** They are in the
token file marked `$status: proposed`. Contrast is verified on every one of them; the hues have had
no design review. `dark.accent` is deliberately not `brand.accent` — the pure brand red only reaches
4.22:1 on `dark.widget` — and that divergence should be reviewed alongside the rest.

**Trademark mark.** The wordmark now carries a circle-™, ported from the unmerged
`chore/update-logos` branch. Whether it should be ™ or ®, and whether the icon variants need one
too, is a legal question this repo cannot answer.

**The stipple assets are a thirteenth of their own spec.** 20 assets at ~300px against a 4000px
target, cropped from a single contact sheet with no higher-resolution source. Usable for web
thumbnails and small display units, unusable for print or hero. See
`styles/minimalist-stipple/STYLE.md`.

**`moebius-scene` has no locked generation prompt.** It can be used but not extended — a matching
26th asset is currently guesswork.

**Typography, spacing, radius, and elevation do not exist here.** This repo is color, logos, and
illustration only.
