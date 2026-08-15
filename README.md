# vistatypelp.org — the VistaType LP website

The public website for **VistaType LP and Braille Macros**. This is deliberately a
**separate project from the add-in's source code**, which lives at
[jerrywhittaker/vistatype-lp](https://github.com/jerrywhittaker/vistatype-lp).

Keeping them apart means a website edit can never land inside a release, a release can
never publish half-finished website text, and neither one has to wait for the other.

## What's here

```
public/            everything that gets served — this is the whole site
  index.html         front page
  install.html       installing, in short, pointing at the full guide
  404.html           shown for an address that doesn't exist
  styles.css         all the styling
  _headers           security headers, applied by Cloudflare
  img/               the pictures the site serves — all made from assets/ by a script
assets/            Jerry's artwork — the icon and the wordmark. Copied from the add-in
                   project, where the originals live in assets/branding/.
tools/
  preview.py         serves public/ locally, the way Cloudflare serves it
  make-web-images.py makes everything in public/img/ out of assets/
wrangler.jsonc     the Cloudflare settings
CLAUDE.md          the same ground in more detail, for Claude
README.md          this file
```

There is no build step. The files in `public/` are the site exactly as it is served.

Nothing in `public/img/` is edited by hand. If the artwork ever changes, re-copy it into
`assets/` and run the script once:

```bash
python3 tools/make-web-images.py     # needs Pillow: pip install pillow
```

It writes the finished pictures into `public/img/`, and they get saved into the project like
any other file — so the site itself never depends on the script having been run.

## Working on it

Edit the files in `public/`. Nothing to install, nothing to compile.

To see it exactly as the live site serves it:

```bash
python3 tools/preview.py
# then open http://localhost:8080
```

That serves `public/` the way Cloudflare does — `/install` works without the `.html`, and a
wrong address gets `404.html` rather than Python's own error page. `python3 -m http.server`
gets both of those wrong, which makes working links look broken.

Opening `public/index.html` straight off disk is fine for reading the words, but the links
between pages won't work.

## Publishing

The site is served by **Cloudflare**, as a Worker that does nothing but hand out the
files in `public/`. Cloudflare no longer offers new Cloudflare Pages projects in its
dashboard, so this is the current route; it behaves the same for a static site.

`wrangler.jsonc` holds the settings, so the dashboard needs almost nothing:

| Setting | Value |
|---|---|
| Project name | `vistatypelp-org` |
| Build command | *(leave empty)* |
| Deploy command | `npx wrangler deploy` (its default) |

Once it is connected, pushing to this project updates the live site.

## Design rules, and why

The audience is people who make documents readable. The site has to practice that.

- Base text is **19px**, above the web default, and everything is sized in `rem` so
  browser zoom enlarges the whole page proportionally.
- Text and background contrast is well past the WCAG AA minimum in both the light and dark
  color schemes; the page follows whichever the reader's system asks for.
- Every interactive thing has a **visible focus outline**, and there is a skip link for
  keyboard users.
- Line length is capped around 66 characters.
- No text anywhere is smaller than 1rem, and nothing important is carried by color alone.

The colors are the logo's own, read out of the artwork: the crimson `#A62728` of
"VistaType", the warm near-black `#2C2C29` of the magnifying glass, and the paper color
`#EFECE5`. Every text-and-background pairing was measured — all of them clear the WCAG AA
minimum of 4.5:1, and body text clears the stricter AAA level of 7:1 in both the light and
dark schemes. If you change a color, measure it again in both.

Keep new pages inside those rules.

## Two things that will go stale

- **The download button** points at
  `github.com/jerrywhittaker/vistatype-lp/releases/latest`, which always resolves to the
  newest release without naming a version. That only works if the release actually carries
  its `Setup.exe` as an attachment. **The current v3.0 release has no attachment**, so the
  button lands on a page with nothing to download until that is fixed.
- **Version numbers** are not written into any page on purpose, so that releasing does not
  require a website edit. Keep it that way.

## American spellings

Same rule as the add-in: this is for American transcribers, so the site uses American
spellings and usage throughout — license, color, behavior, gray, dialog; periods, not full
stops; parentheses, not brackets.
