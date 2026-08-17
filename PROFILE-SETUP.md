# Profile README — how this works

This repo is my GitHub **profile README**: the page GitHub shows at the top of
<https://github.com/jsticks779>.

## Important: the repo name

GitHub only renders a profile README from a **public repo whose name is exactly the
username** — for me that is `jsticks779`, with the README at the repo root.

`its-junio.dev` will *not* show up on the profile page. Two ways to fix that:

```bash
# Option A — create the special repo and push this folder into it
gh repo create jsticks779 --public --source=. --remote=origin --push

# Option B — rename the existing empty repo, then push
gh repo rename jsticks779 --repo jsticks779/its-junio.dev
git remote add origin https://github.com/jsticks779/jsticks779.git
git push -u origin main
```

When it works, GitHub shows a small hint on the repo page: *"jsticks779/jsticks779 is a
✨special✨ repository."*

## Layout

```
.
├── README.md                     the profile page itself
├── assets/
│   ├── hero-dark.svg  hero-light.svg      animated banner (CSS-animated SVG)
│   ├── marquee-dark.svg  marquee-light.svg  scrolling tech strip
│   ├── footer-dark.svg  footer-light.svg   animated wave footer
│   ├── divider.svg                        animated section rule
│   ├── cards/*.svg                        one animated card per featured repo
│   ├── showreel.gif / showreel.mp4        the reel in the README
│   └── _build_assets.py                   regenerates every SVG above
└── .github/workflows/snake.yml   builds the contribution-snake animation
```

## Regenerating the SVGs

Everything except the hero is generated. Edit the data at the top of
`assets/_build_assets.py` (stack lists, project cards, colours) and run:

```bash
cd assets && python3 _build_assets.py
```

The hero (`hero-dark.svg`) is hand-written. The light variant is the same file with the
palette block at the top swapped — keep both in sync when editing.

All animation is plain CSS inside the SVG, so it runs anywhere GitHub renders an image, with
no JavaScript and no external requests. Every asset honours `prefers-reduced-motion`.

## The contribution snake

`.github/workflows/snake.yml` runs twice a day, generates the snake SVGs and pushes them to
an `output` branch, which the README links to. First time:

1. Push this repo.
2. Actions tab → enable workflows.
3. Run **Generate contribution snake** once by hand (`workflow_dispatch`), or wait for the
   schedule. Until it has run once, that image in the README is a broken link.

## The showreel

`assets/showreel.gif` (and the matching `.mp4`) is a recording of the hero animation. To swap
in a real product demo instead — a screen recording of Sellin, jUNIODEV-UI, whatever:

```bash
# record, then keep it small — GitHub READMEs choke on huge GIFs
ffmpeg -i demo.mp4 -vf "fps=15,scale=900:-1:flags=lanczos" -c:v libx264 -crf 28 assets/showreel.mp4
ffmpeg -i assets/showreel.mp4 -vf "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" assets/showreel.gif
```

Keep the GIF under ~8 MB or the profile page feels slow on mobile data.

## Rebuilding the reel from the hero animation

`render-showreel.sh` renders the hero SVG frame by frame with headless Chrome (seeking each
CSS animation through the Web Animations API, since headless Chrome's virtual clock does not
advance animations on its own) and muxes the frames with ffmpeg.

```bash
./render-showreel.sh
```

## Things to update when life changes

- `README.md` → the `now.md` list, the "Also in the workshop" table, socials
- `assets/_build_assets.py` → `CARDS` (featured repos) and the marquee rows
- stars/languages on the cards are written by hand — they don't self-update
