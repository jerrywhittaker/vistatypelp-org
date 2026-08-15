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
  _headers           security headers, applied by Cloudflare Pages
README.md          this file
```

There is no build step. The files in `public/` are the site exactly as it is served.

## Working on it

Open `public/index.html` in a browser and edit. Nothing to install, nothing to compile.

To view it the way the live site works — with `/install.html` and `/styles.css` resolving
from the root — serve the folder instead of opening the file directly:

```bash
cd public && python3 -m http.server 8080
# then open http://localhost:8080
```

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
