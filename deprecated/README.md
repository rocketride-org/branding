# Deprecated

Reference only. **Do not pull anything from this directory.** Nothing here is part of the current
brand, and no current asset should reference it.

## `Palette.png`

The superseded color palette, 2570x1318. Retired in v2.0.

| Swatch | Name | Value | Used anywhere? |
| --- | --- | --- | --- |
| 01 | Deep Graphite | `#222223` | no |
| 02 | Abyss Blue | `#1e1a34` | was the logo wordmark and rocket, until v2.0 |
| 03 | Night Amethyst | `#5f2167` | no |
| 04 | Imperial Indigo | `#370b7a` | no |
| 05 | Horizon Blue | `#41b6e6` | no |

Two things worth knowing about this file, because they explain why the v2.0 token work was needed.

**It never contained the brand red.** `#f93822` — the color in the logo since the first commit, and
the color the product actually ships as its accent — appears nowhere on this sheet. The palette and
the logo were never the same system.

**Four of its five colors were used nowhere.** Only Abyss Blue ever made it into an artifact, and
only inside the logo SVGs. So this was an aspirational sheet, not a description of the brand. That is
precisely the failure mode `tokens/rocketride.tokens.json` is built to avoid, which is why that file
carries an explicit `_unresolved` block instead of implying completeness.

It is also a PNG, which means nobody could diff it, script against it, or copy a value out of it
without an eyedropper. It is kept because it is the only record of the old system, and because
knowing what a color used to be is occasionally necessary when auditing an old deck.

Every value above is recorded in the `_deprecated` block of `tokens/rocketride.tokens.json`, along
with the reason each was retired. `tokens/check_contrast.py` asserts that no live token resolves to
any of them.
