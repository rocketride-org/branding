"""Re-export the logo PNGs from the SVGs, preserving transparency.

Usage: python logos/export_png.py [path/to/chrome.exe]

Why this exists: the PNGs are raster derivatives of the SVGs and drift the moment
anyone edits an SVG without re-exporting. It also pins the one property that the
unmerged chore/update-logos branch broke - every PNG here MUST be 32bpp RGBA with
transparent padding. Chrome is used headless with a fully transparent default
background; any other exporter is fine as long as alpha survives.

Canvas convention is carried over from the original Illustrator exports, measured
off them rather than guessed:
  wordmarks  ink height 278px, padding 13/14 left/right and 27 top/bottom
  icons      ink height 383px, 1px transparent column on the right

The wordmark canvas is wider than the original 1920px because the viewBox grew to
fit the trademark glyph. Wordmark HEIGHT is what stays fixed, so the letterforms
keep their optical size and only the canvas grows.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
]

# svg, ink height, pad left, pad top, pad right, pad bottom
JOBS = [
    ("rocketride-logo-color.svg", "rocketride-logo-color.png", 278, 13, 27, 14, 27),
    ("rocketride-logo-white.svg", "rocketride-logo-white.png", 278, 13, 27, 14, 27),
    ("rocketride-icon-color.svg", "rocketride-icon-color@2x.png", 383, 0, 0, 1, 0),
    ("rocketride-icon-white.svg", "rocketride-icon-white@2x.png", 383, 0, 0, 1, 0),
]

PAGE = """<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;padding:0;background:transparent}
img{display:block;width:%dpx;height:%dpx}</style>
<img src="%s">
"""


def find_chrome():
    if len(sys.argv) > 1:
        return sys.argv[1]
    for c in CHROME_CANDIDATES:
        if os.path.sep in c or "/" in c:
            if os.path.isfile(c):
                return c
        elif shutil.which(c):
            return shutil.which(c)
    raise SystemExit("chrome not found; pass its path as the first argument")


def viewbox(svg_path):
    s = io.open(svg_path, encoding="utf-8").read()
    m = re.search(r'viewBox="([\d.\s-]+)"', s)
    if not m:
        raise SystemExit("%s: no viewBox" % svg_path)
    _, _, w, h = (float(v) for v in m.group(1).split())
    return w, h


def render(chrome, svg_path, w, h, out):
    tmp = tempfile.mkdtemp(prefix="rr-logo-")
    try:
        shutil.copy(svg_path, tmp)
        page = os.path.join(tmp, "p.html")
        io.open(page, "w", encoding="utf-8").write(
            PAGE % (w, h, os.path.basename(svg_path)))
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1",
             "--default-background-color=00000000",
             "--window-size=%d,%d" % (w, h),
             "--screenshot=%s" % out,
             "file:///" + page.replace("\\", "/")],
            capture_output=True, check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    chrome = find_chrome()
    print("chrome: %s" % chrome)
    for svg_name, png_name, ink_h, pl, pt, pr, pb in JOBS:
        svg = os.path.join(HERE, svg_name)
        vw, vh = viewbox(svg)
        ink_w = int(round(ink_h * vw / vh))
        raw = os.path.join(tempfile.gettempdir(), "rr-raw-%s" % png_name)
        render(chrome, svg, ink_w, ink_h, raw)

        art = Image.open(raw).convert("RGBA")
        if art.size != (ink_w, ink_h):
            art = art.resize((ink_w, ink_h), Image.LANCZOS)
        canvas = Image.new("RGBA", (pl + ink_w + pr, pt + ink_h + pb), (0, 0, 0, 0))
        canvas.paste(art, (pl, pt), art)

        out = os.path.join(HERE, png_name)
        canvas.save(out, optimize=True)
        os.remove(raw)

        assert canvas.mode == "RGBA", png_name
        assert canvas.getpixel((0, 0))[3] == 0, "%s: opaque corner" % png_name
        print("  %-30s %dx%d  RGBA  corner alpha 0" % (png_name, *canvas.size))


if __name__ == "__main__":
    main()
