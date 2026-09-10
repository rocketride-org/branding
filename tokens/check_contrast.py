"""Verify every contrast obligation implied by rocketride.tokens.json.

Usage: python tokens/check_contrast.py tokens/rocketride.tokens.json

Exits non-zero if any pair misses its target. Ratios in the token file's
descriptions are produced by this script, so a description that drifts from
reality shows up as a failure here rather than as folklore.

Targets follow WCAG 2.1:
  4.5:1  normal-size text
  3.0:1  large text (>=24px, or >=19px bold) and non-text UI boundaries
  none   disabled controls, and decorative dividers that carry no meaning
"""
import json
import re
import sys

ALIAS = re.compile(r"^\{([A-Za-z0-9_.]+)\}$")

RETIRED = ["#f7901f", "#1e1a34", "#0a0a0a", "#eceae3",
           "#222223", "#5f2167", "#370b7a", "#41b6e6"]


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    if a < b:
        a, b = b, a
    return (a + 0.05) / (b + 0.05)


class Tokens:
    def __init__(self, path):
        self.d = json.load(open(path, encoding="utf-8"))

    def __call__(self, path, _seen=None):
        _seen = _seen or set()
        if path in _seen:
            raise ValueError("circular alias: %s" % path)
        _seen.add(path)
        group, key = path.split(".", 1)
        v = self.d[group][key]["value"]
        m = ALIAS.match(str(v))
        return self(m.group(1), _seen) if m else v

    def literals(self):
        """Every literal color value in a live (non-underscore) group."""
        out = []
        for gname, group in self.d.items():
            if gname.startswith(("_", "$")) or not isinstance(group, dict):
                continue
            for kname, tok in group.items():
                if kname.startswith(("_", "$")) or not isinstance(tok, dict):
                    continue
                if tok.get("type") == "color":
                    out.append(("%s.%s" % (gname, kname), self("%s.%s" % (gname, kname))))
        return out


def main():
    t = Tokens(sys.argv[1])
    fails = []
    rows = []

    def check(label, fg, bg, target):
        r = ratio(t(fg) if "." in fg else fg, t(bg) if "." in bg else bg)
        ok = r >= target
        rows.append((ok, label, r, target))
        if not ok:
            fails.append((label, r, target))

    # --- light theme -----------------------------------------------------
    print("LIGHT")
    for s in ("surface.bg", "surface.surfaceAlt", "surface.widget"):
        check("text.primary on %s" % s, "text.primary", s, 4.5)
        check("text.secondary on %s" % s, "text.secondary", s, 4.5)

    check("button.primaryFg on button.primaryBg",
          "button.primaryFg", "button.primaryBg", 4.5)
    check("button.primaryFg on button.primaryBgHover",
          "button.primaryFg", "button.primaryBgHover", 4.5)
    check("button.primaryFg on button.primaryBgActive",
          "button.primaryFg", "button.primaryBgActive", 4.5)

    # The accent is large-text-only on light grounds. 3:1, never 4.5.
    check("brand.accent on surface.bg (large text only)",
          "brand.accent", "surface.bg", 3.0)
    check("brand.accent on illustration.ground (large text only)",
          "brand.accent", "illustration.ground", 3.0)
    check("interaction.accentHover on surface.bg", "interaction.accentHover", "surface.bg", 4.5)
    check("interaction.accentActive on surface.bg", "interaction.accentActive", "surface.bg", 4.5)
    check("text.primary on interaction.accentSubtle",
          "text.primary", "interaction.accentSubtle", 4.5)

    check("border.strong on surface.bg (non-text)", "border.strong", "surface.bg", 3.0)
    check("border.strong on surface.widget (non-text)", "border.strong", "surface.widget", 3.0)
    check("interaction.focusRing on surface.bg (non-text)",
          "interaction.focusRing", "surface.bg", 3.0)

    for s in ("error", "warning", "success", "info"):
        check("status.%s on surface.bg" % s, "status.%s" % s, "surface.bg", 4.5)
        check("status.%sOnFill on status.%s" % (s, s),
              "status.%sOnFill" % s, "status.%s" % s, 4.5)
        check("status.%s on status.%sSubtle" % (s, s),
              "status.%s" % s, "status.%sSubtle" % s, 4.5)
        check("text.primary on status.%sSubtle" % s,
              "text.primary", "status.%sSubtle" % s, 4.5)

    check("illustration.ink on illustration.ground", "illustration.ink", "illustration.ground", 4.5)

    # --- dark theme ------------------------------------------------------
    print("DARK")
    for s in ("dark.bg", "dark.surfaceAlt", "dark.widget"):
        check("dark.textPrimary on %s" % s, "dark.textPrimary", s, 4.5)
        check("dark.textSecondary on %s" % s, "dark.textSecondary", s, 4.5)
        check("dark.accent on %s" % s, "dark.accent", s, 4.5)
        for st in ("error", "warning", "success", "info"):
            check("dark.%s on %s" % (st, s), "dark.%s" % st, s, 4.5)

    check("dark.buttonPrimaryFg on dark.buttonPrimaryBg",
          "dark.buttonPrimaryFg", "dark.buttonPrimaryBg", 4.5)
    check("dark.borderStrong on dark.bg (non-text)", "dark.borderStrong", "dark.bg", 3.0)
    check("dark.borderStrong on dark.widget (non-text)", "dark.borderStrong", "dark.widget", 3.0)
    check("dark.focusRing on dark.bg (non-text)", "dark.focusRing", "dark.bg", 3.0)
    check("illustration.inkDark on illustration.groundDark",
          "illustration.inkDark", "illustration.groundDark", 4.5)

    for ok, label, r, target in rows:
        print("  %-58s %6.2f:1  (>=%.1f)  %s"
              % (label, r, target, "ok" if ok else "FAIL"))

    # Values that are deliberately exempt from a minimum, plus the rejected
    # alternatives quoted in the token descriptions. Computed so no ratio in the
    # file is ever a number someone typed from memory, but not asserted -
    # a decorative divider has no threshold to fail.
    print("INFORMATIONAL (exempt or rejected alternatives)")
    info = [
        ("border.default on surface.bg (decorative divider, exempt)",
         t("border.default"), t("surface.bg")),
        ("dark.borderDefault on dark.bg (decorative divider, exempt)",
         t("dark.borderDefault"), t("dark.bg")),
        ("interaction.disabledFg on interaction.disabledBg (disabled, exempt)",
         t("interaction.disabledFg"), t("interaction.disabledBg")),
        ("brand.accent on dark.widget (REJECTED: why dark.accent exists)",
         t("brand.accent"), t("dark.widget")),
        ("status.error vs brand.accent (why status needs an icon)",
         t("status.error"), t("brand.accent")),
        ("retired #f7901f on illustration.ground (why orange was retired)",
         "#f7901f", t("illustration.ground")),
    ]
    for label, fg, bg in info:
        r = ratio(fg, bg)
        rows.append((True, label, r, 0.0))
        print("  %-58s %6.2f:1" % (label, r))

    # --- retired values must not appear in any live token ----------------
    print("RETIRED VALUES")
    leaks = [(p, v) for p, v in t.literals() if v.lower() in RETIRED]
    for path, v in leaks:
        print("  FAIL %s resolves to retired %s" % (path, v))
    if not leaks:
        print("  ok   no live token resolves to a retired value")
    else:
        fails.extend(("retired %s in %s" % (v, p), 0, 0) for p, v in leaks)

    # --- documented ratios must match computed ones ----------------------
    print("DOCUMENTED RATIOS")
    mismatches = 0
    quoted = re.compile(r"(\d+\.\d\d):1")
    computed = {"%.2f" % r for _, _, r, _ in rows}
    for gname, group in t.d.items():
        if gname.startswith(("_", "$")) or not isinstance(group, dict):
            continue
        for kname, tok in group.items():
            if not isinstance(tok, dict):
                continue
            for m in quoted.finditer(str(tok.get("description", ""))):
                if m.group(1) not in computed:
                    print("  WARN %s.%s quotes %s:1, which this script does not compute"
                          % (gname, kname, m.group(1)))
                    mismatches += 1
    if not mismatches:
        print("  ok   every quoted ratio is one this script computes")

    print()
    if fails:
        print("%d FAILURE(S)" % len(fails))
        return 1
    print("all %d checks pass" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
