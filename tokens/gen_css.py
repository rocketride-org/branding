"""Generate tokens/rocketride.css from tokens/rocketride.tokens.json.

Usage: python gen_css.py <tokens.json>   -> writes CSS to stdout
"""
import json
import re
import sys

# (json group, json key) -> css custom property name.
# Explicit rather than derived, so a rename in either file is a visible diff here.
LIGHT = [
    ("Brand", [
        ("brand", "brand", "--rr-brand"),
        ("brand", "accent", "--rr-accent"),
    ]),
    ("Surface", [
        ("surface", "bg", "--rr-bg"),
        ("surface", "surfaceAlt", "--rr-surface-alt"),
        ("surface", "widget", "--rr-widget"),
    ]),
    ("Text", [
        ("text", "primary", "--rr-text-primary"),
        ("text", "secondary", "--rr-text-secondary"),
    ]),
    ("Border. border-default is a decorative divider only at 1.37:1. Use border-strong for anything a user interacts with.", [
        ("border", "default", "--rr-border"),
        ("border", "strong", "--rr-border-strong"),
    ]),
    ("Button. Primary is INK filled with an offset accent block, not accent filled. White on the accent is 3.74:1 and fails AA for a normal-size label.", [
        ("button", "primaryBg", "--rr-btn-primary-bg"),
        ("button", "primaryFg", "--rr-btn-primary-fg"),
        ("button", "primaryBgHover", "--rr-btn-primary-bg-hover"),
        ("button", "primaryBgActive", "--rr-btn-primary-bg-active"),
        ("button", "primaryAccentBlock", "--rr-btn-primary-accent-block"),
        ("button", "primaryAccentBlockOffset", "--rr-btn-primary-accent-block-offset"),
    ]),
    ("Interaction. Proposed, awaiting design review.", [
        ("interaction", "accentHover", "--rr-accent-hover"),
        ("interaction", "accentActive", "--rr-accent-active"),
        ("interaction", "accentSubtle", "--rr-accent-subtle"),
        ("interaction", "widgetHover", "--rr-widget-hover"),
        ("interaction", "disabledBg", "--rr-disabled-bg"),
        ("interaction", "disabledFg", "--rr-disabled-fg"),
        ("interaction", "focusRing", "--rr-focus-ring"),
        ("interaction", "focusRingHalo", "--rr-focus-ring-halo"),
        ("interaction", "focusRingWidth", "--rr-focus-ring-width"),
        ("interaction", "focusRingOffset", "--rr-focus-ring-offset"),
    ]),
    ("Status. Proposed, awaiting design review. The brand accent is red, so status must never be conveyed by color alone.", [
        ("status", "error", "--rr-error"),
        ("status", "errorSubtle", "--rr-error-subtle"),
        ("status", "errorOnFill", "--rr-error-on-fill"),
        ("status", "warning", "--rr-warning"),
        ("status", "warningSubtle", "--rr-warning-subtle"),
        ("status", "warningOnFill", "--rr-warning-on-fill"),
        ("status", "success", "--rr-success"),
        ("status", "successSubtle", "--rr-success-subtle"),
        ("status", "successOnFill", "--rr-success-on-fill"),
        ("status", "info", "--rr-info"),
        ("status", "infoSubtle", "--rr-info-subtle"),
        ("status", "infoOnFill", "--rr-info-on-fill"),
    ]),
    ("Illustration. Applies to generated art, not to UI chrome.", [
        ("illustration", "ink", "--rr-ink"),
        ("illustration", "ground", "--rr-ground"),
    ]),
    ("Logo. Reconciled with brand in v2.0 - the red IS the brand color.", [
        ("logo", "red", "--rr-logo-red"),
        ("logo", "ink", "--rr-logo-ink"),
        ("logo", "offWhite", "--rr-logo-offwhite"),
    ]),
]

# Dark overrides reuse the SAME property names, so consuming code never branches on theme.
DARK = [
    ("dark", "accent", "--rr-brand"),
    ("dark", "accent", "--rr-accent"),
    ("dark", "bg", "--rr-bg"),
    ("dark", "surfaceAlt", "--rr-surface-alt"),
    ("dark", "widget", "--rr-widget"),
    ("dark", "textPrimary", "--rr-text-primary"),
    ("dark", "textSecondary", "--rr-text-secondary"),
    ("dark", "borderDefault", "--rr-border"),
    ("dark", "borderStrong", "--rr-border-strong"),
    ("dark", "buttonPrimaryBg", "--rr-btn-primary-bg"),
    ("dark", "buttonPrimaryFg", "--rr-btn-primary-fg"),
    ("dark", "error", "--rr-error"),
    ("dark", "warning", "--rr-warning"),
    ("dark", "success", "--rr-success"),
    ("dark", "info", "--rr-info"),
    ("dark", "focusRing", "--rr-focus-ring"),
    ("dark", "focusRingHalo", "--rr-focus-ring-halo"),
    ("illustration", "inkDark", "--rr-ink"),
    ("illustration", "groundDark", "--rr-ground"),
]

ALIAS = re.compile(r"^\{([A-Za-z0-9_.]+)\}$")

# Paths whose CSS property is REDEFINED in the dark block. An alias pointing at one
# of these must be emitted as a literal, never as var(): illustration.ink flips from
# #12111a to #eeede7 in dark theme, so `--rr-logo-ink: var(--rr-ink)` would silently
# turn the logo ink into the ground color. The JSON keeps the alias to record intent;
# the CSS resolves it so the intent survives theming.
INVERTED = {"illustration.ink", "illustration.ground"}


def raw(tokens, group, key):
    return tokens[group][key]["value"]


def resolve(tokens, value, seen=None):
    """Follow {group.key} aliases to a literal."""
    seen = seen or set()
    m = ALIAS.match(str(value))
    if not m:
        return value
    path = m.group(1)
    if path in seen:
        raise ValueError("circular alias: %s" % path)
    seen.add(path)
    group, key = path.split(".", 1)
    return resolve(tokens, tokens[group][key]["value"], seen)


def css_value(tokens, group, key, prop_by_path):
    """Emit var() for an alias whose target has its own custom property, else the literal."""
    v = raw(tokens, group, key)
    m = ALIAS.match(str(v))
    if m and m.group(1) in prop_by_path and m.group(1) not in INVERTED:
        return "var(%s)" % prop_by_path[m.group(1)]
    return resolve(tokens, v)


def main():
    tokens = json.load(open(sys.argv[1], encoding="utf-8"))

    # First light definition of a path wins as its canonical property name.
    prop_by_path = {}
    for _, entries in LIGHT:
        for group, key, prop in entries:
            prop_by_path.setdefault("%s.%s" % (group, key), prop)

    out = []
    out.append("/* Generated from rocketride.tokens.json by tokens/gen_css.py. Do not hand-edit.")
    out.append("   Regenerate and diff to verify:  python tokens/gen_css.py tokens/rocketride.tokens.json | diff - tokens/rocketride.css")
    out.append("")
    out.append("   Status: the interaction, status, and dark groups are proposed and await design review.")
    out.append("   Every contrast ratio in the source JSON is computed, not estimated. */")
    out.append("")
    out.append(":root {")
    for i, (heading, entries) in enumerate(LIGHT):
        if i:
            out.append("")
        out.append("  /* %s */" % heading)
        for group, key, prop in entries:
            out.append("  %s: %s;" % (prop, css_value(tokens, group, key, prop_by_path)))
    out.append("}")
    out.append("")

    dark_lines = []
    for group, key, prop in DARK:
        v = raw(tokens, group, key)
        m = ALIAS.match(str(v))
        # Inside a dark block an alias must resolve to a literal: the referenced
        # property is itself being overridden here, so var() would be circular.
        dark_lines.append("    %s: %s;" % (prop, resolve(tokens, v) if m else v))

    body = "\n".join(dark_lines)
    out.append("/* Dark theme. Same property names, so consuming code never branches on theme. */")
    out.append("@media (prefers-color-scheme: dark) {")
    out.append("  :root:not([data-theme=\"light\"]) {")
    out.append(body)
    out.append("  }")
    out.append("}")
    out.append("")
    out.append("/* Explicit choice wins over the system preference in both directions. */")
    out.append(":root[data-theme=\"dark\"] {")
    out.append(body.replace("    ", "  "))
    out.append("}")
    out.append("")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
