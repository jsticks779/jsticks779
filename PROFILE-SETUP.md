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
│   ├── hero-dark.svg  hero-light.svg        hero banner
│   ├── marquee-dark.svg  marquee-light.svg  static tech strip
│   ├── footer-dark.svg  footer-light.svg    sign-off / contact footer
│   ├── divider.svg                          section rule
│   ├── cards/*.svg                          one card per featured repo
│   ├── showreel.mp4                          the reel (short hero clip)
│   ├── showreel.gif                          auto-playing loop used in the README
│   ├── stats-*.svg  streak-*.svg            generated cards (see cards.yml)
│   ├── top-langs-*.svg  trophy-*.svg        generated cards (see cards.yml)
│   ├── graph-*.svg                          generated contribution calendar
│   └── _build_assets.py                     regenerates every static SVG
├── scripts/profile-graph.py    generates the contribution calendars
└── .github/workflows/
    ├── snake.yml                builds the contribution-snake animation
    └── cards.yml                rebuilds the stats/streak/trophy/graph cards
```

## Regenerating the SVGs

Everything except the hero is generated. Edit the data at the top of
`assets/_build_assets.py` (stack lists, project cards, colours) and run:

```bash
cd assets && python3 _build_assets.py
```

The hero (`hero-dark.svg`) is hand-written. The light variant is the same file with the
palette block at the top swapped — keep both in sync when editing.

The generated assets are static SVGs — no JavaScript, no external requests, nothing to
animate or cache.

## The contribution snake

`.github/workflows/snake.yml` runs twice a day, generates the snake SVGs and pushes them to
an `output` branch, which the README links to. First time:

1. Push this repo.
2. Actions tab → enable workflows.
3. Run **Generate contribution snake** once by hand (`workflow_dispatch`), or wait for the
   schedule. Until it has run once, that image in the README is a broken link.

## The showreel

`assets/showreel.gif` plays inline at the top of the README — an auto-looping clip that links
to `assets/showreel.mp4` when clicked. It's currently a short clip of the hero banner so it
never goes stale. To swap in a real product demo — a screen recording of Sellin, jUNIODEV-UI,
whatever — replace the MP4 and regenerate the GIF:

```bash
# record, then keep both files small — GitHub READMEs choke on huge files
ffmpeg -i demo.mp4 -vf "fps=15,scale=900:-1:flags=lanczos" -c:v libx264 -crf 28 -movflags +faststart assets/showreel.mp4
ffmpeg -i assets/showreel.mp4 -vf "fps=12,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse" assets/showreel.gif
```

## Rendering the current reel from an SVG

`render-showreel.sh` screenshots the hero SVG with headless Chrome, then muxes a slow cinematic
zoom into `assets/showreel.mp4` and re-derives `assets/showreel.gif`.

```bash
./render-showreel.sh
```

## The cards (stats, streak, trophies, graph)

The stats/streak/top-langs/trophy/graph widgets no longer point at the public
`*.vercel.app` services — those run on shared free tiers that get disabled (the trophy and
stats endpoints were returning `402`/`503` at the time of writing), and the README would show
broken images. `.github/workflows/cards.yml` instead generates them **inside GitHub Actions**
from the repo's own `GITHUB_TOKEN` and commits the SVGs back to `assets/`:

- **stats / top-langs** → `stats-organization/github-readme-stats-action`
- **streak** → `DenverCoder1/github-readme-streak-stats`
- **trophies** → `ryo-ma/github-profile-trophy` (pinned to master; v1.0 can't read stars)
- **graph** → `scripts/profile-graph.py` (GraphQL, same endpoint the snake uses)

First time: push the repo, then in the Actions tab enable workflows and run
**Update profile cards** once by hand (or wait for the 03:17 daily schedule). Until it has
run, those images in the README are broken links.

## Things to update when life changes

- `README.md` → the `now.md` list, the "Also in the workshop" table, socials
- `assets/_build_assets.py` → `CARDS` (featured repos) and the marquee rows
- stars/languages on the cards are written by hand — they don't self-update
