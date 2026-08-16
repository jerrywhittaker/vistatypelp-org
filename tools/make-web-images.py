#!/usr/bin/env python3
"""Make the web-sized picture files in public/img/ out of Jerry's artwork in assets/.

Run this only when the artwork itself changes:

    python3 tools/make-web-images.py

Everything it writes is saved into the project alongside the pages, so the site
itself never needs this script to be run — visitors are served finished files.

The artwork in assets/ is never touched. The master copies live in the add-in
project at assets/branding/; assets/ here is a copy of those, and public/img/ is
made from that copy.

Needs Pillow:  pip install pillow
"""

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets"
OUT = ROOT / "public" / "img"

# The colors Jerry's artwork is actually drawn in, sampled from the PNGs.
RED = (0xA6, 0x27, 0x28)  # "VistaType" and the LP in the lens
BLACK = (0x2C, 0x2C, 0x29)  # the magnifying glass
PAPER = (0xEF, 0xEC, 0xE5)  # the sheet of paper
LENS = (0xFD, 0xFC, 0xFB)  # the glass in the middle
LINE = (0xD4, 0xD1, 0xC6)  # the lines of writing on the paper
FOLD = (0xC2, 0xBE, 0xB3)  # the turned-down corner

# The same mark redrawn for a dark page. Reversed rather than merely lightened:
# the paper goes dark and the glass goes light, so every edge that separates one
# shape from another in the original still separates them here.
DARK_MODE = {
    RED: (0xEE, 0x80, 0x78),
    BLACK: (0xED, 0xEA, 0xE2),
    PAPER: (0x3F, 0x3B, 0x34),
    LENS: (0x1E, 0x1D, 0x1B),
    LINE: (0x6E, 0x69, 0x5E),
    FOLD: (0x57, 0x53, 0x4A),
}

ANCHORS = [RED, BLACK, PAPER, LENS, LINE, FOLD]


def recolor(im, mapping):
    """Swap the artwork's colors for the dark-page ones.

    Each pixel is matched to whichever of the six drawing colors it is closest
    to, then replaced. Pixels along the edge of a shape are a blend of two
    colors, so this makes them slightly ragged — which is why every caller
    shrinks the result afterwards. Shrinking smooths those edges back out.
    """
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    cache = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            key = (r, g, b)
            if key not in cache:
                nearest = min(
                    ANCHORS,
                    key=lambda c: (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2,
                )
                cache[key] = mapping[nearest]
            nr, ng, nb = cache[key]
            px[x, y] = (nr, ng, nb, a)
    return im


def fit_width(im, width):
    """Shrink to an exact width, keeping the shape."""
    height = round(im.height * width / im.width)
    return im.resize((width, height), Image.LANCZOS)


def compress(im):
    """Cut the file size by writing the picture with a fixed set of colors.

    The artwork is drawn in six flat colors, so the only places it uses more
    are the softened edges of a shape. 256 shades covers those with nothing
    visible to tell apart, and turns a 136 KB file into an 11 KB one. On a
    page about readability, a picture nobody waits for is part of the job.
    """
    return im.convert("RGBA").quantize(colors=256, method=Image.FASTOCTREE)


def save(im, name):
    path = OUT / name
    compress(im).save(path, optimize=True)
    print(f"  {path.relative_to(ROOT)}  {im.width}x{im.height}  {path.stat().st_size // 1024} KB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    wordmark = Image.open(SRC / "vistatype-wordmark.png").convert("RGBA")
    icon = Image.open(SRC / "vistatype-icon.png").convert("RGBA")

    print("Name at the top of every page:")
    save(fit_width(wordmark, 640), "wordmark.png")
    save(fit_width(recolor(wordmark, DARK_MODE), 640), "wordmark-dark.png")

    print("Mark beside the headline on the front page:")
    save(fit_width(icon, 440), "icon.png")
    save(fit_width(recolor(icon, DARK_MODE), 440), "icon-dark.png")

    print("Tab icon:")
    # The paper in the mark is nearly white, so on its own it would disappear
    # into a light browser tab. Everything sits on a red tile instead.
    #
    # At the size a tab actually uses — 16 pixels across — the paper, the
    # magnifying glass and the letters all run together into a smudge, so the
    # small sizes drop to the LP on its own. Those letters are cut out of
    # Jerry's icon, not typed, so they are the same shapes he drew.
    ico = OUT / "favicon.ico"
    save_ico(ico, {
        16: letters_tile(icon, 64),
        32: letters_tile(icon, 128),
        48: mark_tile(icon, 192),
        64: mark_tile(icon, 256),
    })
    print(f"  {ico.relative_to(ROOT)}  16/32/48/64  {ico.stat().st_size // 1024} KB")
    save(letters_tile(icon, 256), "icon-letters.png")
    save(mark_tile(icon, 256), "icon-tile.png")

    print("Icon for a phone's home screen:")
    save(mark_tile(icon, 180, radius_fraction=0.0), "apple-touch-icon.png")

    print("Picture shown when someone shares a link:")
    save(share_card(wordmark), "share-card.png")

    screenshots()


# Jerry's raw captures go in assets/screenshots/ under these names; the site
# serves the shrunk copies on the right. Missing ones are skipped, so this
# script still runs before they have been taken.
SCREENSHOTS = {
    "ribbon-vistatype-lp.png": "ribbon-lp.png",
    "ribbon-braille-macros.png": "ribbon-brl.png",
}

# Twice the widest the page ever draws them, so they stay sharp on a high
# resolution screen. A capture narrower than this is left at its own size
# rather than being blown up.
SHOT_WIDTH = 2240


def screenshots():
    """Shrink the ribbon captures for the front page.

    Unlike the artwork these are NOT cut down to 256 colors — a screenshot is
    full of softened text edges and shading, and flattening it would smear the
    ribbon's own labels, which are the whole point of showing it.

    If a capture's size changes, the width and height on the <img> tags in
    index.html have to change with it, or the page jumps as the picture loads.
    This prints the numbers to paste in.
    """
    src_dir = ROOT / "assets" / "screenshots"
    found = False
    for src_name, out_name in SCREENSHOTS.items():
        src = src_dir / src_name
        if not src.exists():
            continue
        if not found:
            print("Ribbon screenshots:")
            found = True
        im = Image.open(src).convert("RGB")
        if im.width > SHOT_WIDTH:
            im = fit_width(im, SHOT_WIDTH)
        path = OUT / out_name
        im.save(path, optimize=True)
        print(
            f"  {path.relative_to(ROOT)}  {im.width}x{im.height}  "
            f"{path.stat().st_size // 1024} KB"
            f"   <img … width=\"{im.width}\" height=\"{im.height}\">"
        )
    if not found:
        print(f"Ribbon screenshots: none yet — put captures in {src_dir.relative_to(ROOT)}/")


def red_tile(size, radius_fraction=0.22):
    from PIL import ImageDraw

    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    radius = round(size * radius_fraction)
    if radius:
        draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=RED + (255,))
    else:
        draw.rectangle([0, 0, size - 1, size - 1], fill=RED + (255,))
    return tile


def mark_tile(icon, size, radius_fraction=0.22):
    """The whole mark, on a red tile. For sizes with room to show detail."""
    tile = red_tile(size, radius_fraction)
    inner = round(size * 0.72)
    mark = icon.copy()
    mark.thumbnail((inner, inner), Image.LANCZOS)
    tile.alpha_composite(mark, ((size - mark.width) // 2, (size - mark.height) // 2))
    return tile


def letters_tile(icon, size, radius_fraction=0.22):
    """Only the LP, in the paper color, on a red tile. For very small sizes."""
    # Pick the LP out of the icon by its color — it is the only red in there —
    # and use its shape as a stencil to print the letters in the paper color.
    px = icon.load()
    mask = Image.new("L", icon.size, 0)
    mpx = mask.load()
    for y in range(icon.height):
        for x in range(icon.width):
            r, g, b, a = px[x, y]
            if a > 128 and r > 110 and r - g > 55 and r - b > 55:
                mpx[x, y] = 255
    mask = mask.crop(mask.getbbox())

    inner = round(size * 0.62)
    scale = min(inner / mask.width, inner / mask.height)
    mask = mask.resize((round(mask.width * scale), round(mask.height * scale)), Image.LANCZOS)

    letters = Image.new("RGBA", mask.size, PAPER + (0,))
    letters.putalpha(mask)

    tile = red_tile(size, radius_fraction)
    tile.alpha_composite(letters, ((size - mask.width) // 2, (size - mask.height) // 2))
    return tile


def save_ico(path, images_by_size):
    """Write a .ico holding a different drawing at each size.

    Each drawing has to be handed over already at the size it will be stored
    at, or it is quietly left out of the file.
    """
    sizes = sorted(images_by_size)
    exact = {s: images_by_size[s].resize((s, s), Image.LANCZOS) for s in sizes}
    exact[sizes[-1]].save(
        path,
        sizes=[(s, s) for s in sizes],
        append_images=[exact[s] for s in sizes[:-1]],
    )


def share_card(wordmark):
    """The 1200x630 picture a link preview shows, on the paper color."""
    card = Image.new("RGBA", (1200, 630), PAPER + (255,))
    mark = fit_width(wordmark, 820)
    card.alpha_composite(mark, ((1200 - mark.width) // 2, (630 - mark.height) // 2 - 20))
    return card


if __name__ == "__main__":
    main()
