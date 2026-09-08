# Illustration Styles

Two styles, split by how much space the art gets. Picking between them is a size decision before
it is a taste decision.

| Style | Use when | Breaks when |
| --- | --- | --- |
| `moebius-scene` | The art gets 800px or more of width and can carry atmosphere. Site heroes, full-bleed banners, deck section breaks, event backdrops. | Scaled below about 400px. The linework is dense enough that detail collapses into grey mud. |
| `minimalist-stipple` | The art has to survive a crop, a resize, or a text overlay. Display and social banners, docs spot art, card headers, slide corners, pricing tiers. | Used as a full-bleed hero. A single isolated subject on empty ground reads as thin at 2000px wide — and the current batch is only ~300px on the long edge, so it physically cannot fill one. |

Both styles share the same world: retro-futurist NASA-era suits, mirror-black visors, monumental
ruins, floating structures, multiple moons. Same universe, two levels of detail. They should never
look like they came from different brands.

## Adding a style

1. Write `STYLE.md` first. It has to include a locked generation prompt, a negative prompt,
   composition rules, and the size range the style holds up in.
2. Generate a test set of at least 10 assets in one sitting, one model, one seed family.
3. Review the set at target size, not at full resolution. Most style failures only show up after
   the downscale.
4. Then commit the assets.

A style with no `STYLE.md` is a folder of pictures, not a style. It will not survive the next person.

## What a STYLE.md owes the reader

The point of the spec is that someone who was not in the room can regenerate the style. That means
it has to be honest about the batch that actually shipped, not just the batch that was intended.
Both current styles carry a **Gaps** section for exactly this reason — `minimalist-stipple` ships at
roughly a thirteenth of its own target resolution, and saying so in the file is what makes it
fixable. A spec that describes an aspiration and an assets directory that contains something else is
how a style quietly dies.

## Color

Neither style hardcodes color. Both pull from `tokens/rocketride.tokens.json`. The illustration
tokens (`illustration.ink`, `illustration.ground`) are separate from the UI surface tokens on
purpose: art should read as art, not as a UI panel that failed to load.
