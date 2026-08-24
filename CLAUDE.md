# vistatypelp.org — the VistaType LP website

The public website for **VistaType LP and Braille Macros**, Jerry Whittaker's Microsoft Word
add-in for producing large-print documents and braille source files. Live at
**https://vistatypelp.org**. Built 8/15/2026.

The add-in's own source code is a **separate project** at
`~/projects/vistatype-lp` (`github.com/jerrywhittaker/vistatype-lp`). That separation is
deliberate and should be preserved — see *Why this is its own project* below.

---

## How to talk to Jerry

**Plain English. Always.** This governs every reply.

Jerry is a capable programmer — he wrote the ~16,500-line add-in himself over roughly twenty
years. Speak Word and VBA to him freely. What he does *not* use is the vocabulary of
professional software engineering: version control, build pipelines, release process, and
now web hosting and DNS. **The jargon to strip is process jargon, not programming jargon.**

Avoid these, or say plainly what they mean the first time: branch, merge, rebase, HEAD,
upstream, origin, checkout, staging, working tree, diff, CI/CD, pipeline, artifact,
idempotent, deploy, build output, DNS record, CNAME, apex, zone, edge, cache invalidation,
canonical.

Say the **effect**, not the mechanism:

| Instead of | Say |
|---|---|
| "I'll push to main and it'll deploy." | "I'll save this to GitHub, and the live site updates about thirty seconds later." |
| "Cloudflare purges the edge cache." | "The new version reaches everyone within a minute." |
| "Add a canonical tag." | "Tell search engines which address is the real one." |
| "The apex and www both resolve." | "Both `vistatypelp.org` and `www.vistatypelp.org` reach the site." |

Other rules:
- **Lead with what happened or what he should do**, then the reason.
- **Never say "just"** — it makes unfamiliar things sound obvious.
- **Don't over-explain programming itself.** Simplify the *process*, never the reasoning.
- Short paragraphs, one idea each. He reads this in a terminal.
- When he'll *see* a term — in a Cloudflare dashboard, or on a GitHub page — name it once and
  explain it in a clause.

---

## The one thing that is genuinely different here

**Every save to GitHub publishes immediately.** There is no release step, no tag, no
approval gate, no installer to test first. Push and it is live worldwide in about thirty
seconds.

This is the opposite of the add-in, where `master` moves only when Jerry says "let's release
3.1". Do not carry that caution over as ceremony — but do carry over the underlying rule:

> **Never push without Jerry's say-so.** On the add-in that rule protects a release. Here it
> protects the live site, which is stricter, not looser.

Show him the change locally first (see *Looking at it* below), then ask.

---

## Why this is its own project

Keeping the website apart from the add-in's source means:

- A website edit can never land inside a release of the add-in.
- A release of the add-in can never publish half-finished website text.
- Neither has to wait for the other, and the add-in's careful two-copy release discipline
  stays uncluttered.

Do not propose merging them back together.

---

## Layout

```
public/            everything served — this IS the site
  index.html         front page: what it does, the typeface, download, about
  install.html       installing in short, pointing at the full guide
  404.html           shown for an address that does not exist
  styles.css         all the styling; there is no other stylesheet
  _headers           security headers, applied by Cloudflare
  img/               the pictures the site serves. MADE BY A SCRIPT — see below.
assets/            Jerry's artwork, copied from the add-in project 8/15/2026.
                   vistatype-icon.png (481x515) and vistatype-wordmark.png (1573x515),
                   both transparent-background RGBA. SOURCE OF TRUTH lives in the add-in
                   project at assets/branding/ — if it changes there, re-copy, do not edit
                   here and do not edit there from this project.
tools/
  preview.py         serves public/ locally, the way Cloudflare serves it
  make-web-images.py makes everything in public/img/ out of assets/
wrangler.jsonc     the Cloudflare settings (see below)
CLAUDE.md          this file
README.md          the same ground, aimed at a human reader
```

### The pictures in `public/img/`

Nothing in that folder is edited by hand. It is all made from `assets/` by one command:

```bash
python3 tools/make-web-images.py     # needs Pillow: pip install pillow
```

The finished pictures are saved into the project like any other file, so **the site still
has no build step** — visitors are served files that are already sitting on disk. The
script only ever needs running again if Jerry's artwork itself changes.

| File | Used for |
|---|---|
| `wordmark.png` / `wordmark-dark.png` | the name at the top left of every page |
| `icon.png` / `icon-dark.png` | the mark beside the headline on the front page |
| `favicon.ico` | the little picture on a browser tab |
| `apple-touch-icon.png` | the icon if someone saves the site to a phone's home screen |
| `share-card.png` | the picture shown when someone posts a link to the site |
| `icon-tile.png`, `icon-letters.png` | the tab icon's two drawings, kept in case they are wanted elsewhere |

Two things about them are deliberate and worth not undoing:

- **The `-dark` files are the mark redrawn for a dark page**, not merely lightened. The
  paper goes dark and the magnifying glass goes light, so every edge that separates one
  shape from another in Jerry's original still separates them. The pages pick between the
  two with `<picture>`, which needs no JavaScript. Jerry's artwork is not modified.
- **The tab icon shows the LP on its own at 16 and 32 pixels**, and the whole mark at 48 and
  above. At tab size the paper, the glass and the letters run together into a smudge. Those
  letters are cut out of Jerry's icon by color, not typed, so they are the shapes he drew.
- Every picture is saved with a fixed set of 256 colors. The artwork is drawn in six flat
  colors, so nothing visible is lost, and the front page's mark drops from 136 KB to 11 KB.
  All the pictures together come to about 100 KB.

There is **no build step**. `public/` is served exactly as it sits on disk. No Node, no npm
install, no framework, no generator. Keep it that way unless Jerry asks otherwise — the
whole point is that he can open a file and read it.

---

## Looking at it

**Start this after every change and give Jerry the address.** He does not read a change out
of a diff, and this site publishes the moment it is saved — looking at the page in a browser
is the only review step there is, so getting it in front of him is part of finishing the
work, not an extra.

```bash
python3 tools/preview.py
# then open http://localhost:8080
```

Run it in the background so it stays up. If it is already running, leave it — the files are
read from disk, so a reload shows the latest edit without restarting anything.

**Use that script rather than `python3 -m http.server`.** Plain http.server does not drop
the `.html` from an address the way Cloudflare does, so `/install` — the main navigation
link — comes back not-found, and a wrong address gets Python's gray error page instead of
`404.html`. Both would look like bugs that do not exist on the live site. `tools/preview.py`
is a few lines of standard library that fixes exactly those two things.

Opening `public/index.html` straight off disk is still fine for reading the words, but the
links between pages will not work.

---

## How it is published

Cloudflare serves the site as a **Worker that does nothing but hand out static files**.
Cloudflare no longer offers new Cloudflare Pages projects in its dashboard, which is why it
is a Worker and not Pages; for a static site the two behave the same.

`wrangler.jsonc` holds the settings, so nothing lives only in the dashboard:

| Setting | Value | Why |
|---|---|---|
| `assets.directory` | `./public` | The folder that gets served |
| `assets.not_found_handling` | `404-page` | Shows our own 404 page, not Cloudflare's |
| `workers_dev` | `false` | Turns off the free `…workers.dev` address, so `vistatypelp.org` is the only public name |
| `preview_urls` | `false` | Those live on the same `workers.dev` name and go with it |

**Cloudflare strips `.html` from addresses.** It serves `/install`, and bounces anyone asking
for `/install.html` over to it. **Always link to `/install`, never `/install.html`** — the
`.html` form works but costs every visitor a wasted round trip. This bit us once already.

Dashboard settings that are NOT in any file here, recorded so nobody has to rediscover them:

- **Always Use HTTPS** is ON (domain → SSL/TLS → Edge Certificates). Plain `http://` moves
  people to the secure address.
- **HSTS is deliberately OFF.** It tells browsers to refuse the unencrypted site for months
  and is genuinely hard to undo if a certificate ever goes wrong. Do not turn it on without
  Jerry deciding to.
- `vistatypelp.org` and `www.vistatypelp.org` are both attached and both serve the site. A
  redirect from `www` to the bare name is a reasonable future tidy-up (Cloudflare has a
  ready-made rule for it); until then the pages carry a canonical tag naming the bare name
  as the real address, so search engines are not confused.
- **`jerry@vistatypelp.org` is the address on the site**, and Cloudflare passes mail sent to
  it on to Jerry (domain → Email → Routing). Confirmed working 8/15/2026. The pages used to
  give `jerry@thewhittakers.org`; that is gone and should not come back. If the contact
  address ever changes again, it appears **four** times — the About section and the footer
  on the front page, and "If something is wrong" and the footer on the install page — and
  two of those show the address as text as well as opening it, so the wording has to change
  along with the link.

---

## Design rules, and why they are not negotiable

**The audience is people whose job is making documents readable.** A website about large
print that is itself hard to read fails before a word is read. Every rule below is already
in `styles.css`; keep new work inside them.

- **Base text is 19px**, above the web default, and everything is sized in `rem` so browser
  zoom enlarges the whole page proportionally. Never set a font size in `px`.
- **Nothing is smaller than 1rem.** No fine print, no small captions, no 14px footer.
- **Contrast is well past the WCAG AA minimum** in both the light and dark color schemes.
  The page follows whichever the reader's system asks for — both are defined with CSS
  variables at the top of `styles.css`. Check any new color against both.
- **Every interactive thing has a visible focus outline**, and there is a skip link at the
  top of each page. Do not remove `:focus-visible` styling.
- **Line length is capped around 66 characters** (`.prose`, `max-width: 40rem`).
- **Nothing important is carried by color alone.**
- `prefers-reduced-motion` is honored. Do not add animation that ignores it.
- **No web fonts.** The site uses the reader's own system font stack, which is the most
  legible thing available on any machine and costs nothing to load. If shipping
  **VistaTypeLP Sans** as a web font is ever considered, read the OFL conditions in the
  add-in project's `assets/fonts/README.md` first — the reserved-name rules bind any copy.
- **No JavaScript.** There is none on the site today and nothing needs it.

### The colors, and where they came from

The site's colors are Jerry's logo colors, read straight out of the artwork rather than
guessed at:

| | Where it is in the logo |
|---|---|
| `#A62728` | the crimson of "VistaType", and the LP in the lens |
| `#2C2C29` | the warm near-black of the magnifying glass |
| `#EFECE5` | the sheet of paper |
| `#D4D1C6` | the lines of writing on the paper |

The page uses the crimson for links, buttons, the numbered steps and the focus outline; the
paper color for the banded sections; and the near-black, taken a little darker, for text.
The dark color scheme uses warm dark grays rather than the blue-gray ones the site started
with, because a cool gray next to that crimson looks like a mistake.

Red is the site's accent everywhere, including the notes. It is not a warning color here —
every note leads with a bold label, so nothing depends on the reader seeing red.

**Every pairing was measured, not eyeballed.** All thirteen clear the WCAG AA minimum of
4.5:1, and body text clears the stricter AAA level of 7:1 in both schemes. Worst case in the
light scheme is a link on a banded section at 6.05:1; in the dark scheme, a link on a card at
6.25:1. If you change a color, measure again — light *and* dark, and against `--bg`,
`--surface` and `--band`, since text sits on all three.

---

## Content rules

- **Never write a version number into a page.** The download button points at
  `github.com/jerrywhittaker/vistatype-lp/releases/latest`, which always resolves to the
  newest release. That is deliberate: releasing the add-in must never require a website
  edit. Keep it that way.
- **American spellings and usage throughout** — same rule as the add-in. license, color,
  behavior, recognize, gray, dialog. Periods, not full stops. Parentheses, not brackets.
  Quotation marks, not inverted commas.
- **Say "VistaType LP", never "our" or "we".** It is Jerry's product; the site speaks about
  it by name.
- **Do not invent claims about the add-in.** Everything on the site today came from the add-in
  project's `README.md` and `docs/Installation-Guide.md`. If you need a fact about how the
  product behaves, read those files — do not reason it out.
- The install page is a **short** version. Anything detailed links to the full guide on
  GitHub rather than being duplicated here, so the two cannot drift apart.

---

## Known open item

**The v3.0 release on GitHub has no installer attached** (`assets: []`, confirmed
8/15/2026). The Download button therefore lands a transcriber on a page with nothing to
download. This is the same gap already recorded in the add-in project's own notes. Until it
is fixed, the site should not be advertised to anyone.

Check it with:

```bash
gh release view --repo jerrywhittaker/vistatype-lp --json tagName,assets
```

---

## Things worth doing, none urgent

- Screenshots of the two ribbon tabs. The site describes them but shows nothing, and a
  transcriber deciding whether to install would want to see them.
- Redirect `www` to the bare name (Cloudflare → Rules → Redirect Rules; there is a template).
- A page about what the add-in actually produces — a large-print page, a braille file — aimed
  at someone evaluating it rather than someone installing it.
