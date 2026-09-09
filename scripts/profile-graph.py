#!/usr/bin/env python3
"""Render a GitHub-style yearly contribution calendar as dark/light SVGs.

Runs in CI (.github/workflows/cards.yml) with the repo's GITHUB_TOKEN, which can
read public contribution calendars through GraphQL. `--fixture` allows a local
dry run with a saved JSON response (the token is not needed on the command line
then).

    python3 scripts/profile-graph.py jsticks779 --token "$GITHUB_TOKEN" [--out assets]
    python3 scripts/profile-graph.py jsticks779 --fixture calendar.json [--out assets]

On any fetch/render failure the script exits 0 without touching the existing
files, so a flaky API call never breaks the profile README.
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime

GRAPHQL = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
  }
}"""

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',ui-monospace,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Inter,system-ui,-apple-system,'Helvetica Neue',sans-serif"

DARK = dict(
    panel="#0a1022", stroke="rgba(120,190,255,.18)", ink="#e8eefc", muted="#8ea0c4",
    cell=("#18202e", "#12313f", "#0e5266", "#0891b2", "#a3e9fb"),
)
LIGHT = dict(
    panel="#ffffff", stroke="rgba(60,90,150,.20)", ink="#0b1220", muted="#64748b",
    cell=("#e9edf8", "#d8f2f9", "#7de0f2", "#06b6d4", "#155e75"),
)

CELL, GAP = 11, 3
GRID_T, MONTH_Y, TITLE_Y, GUTTER, ROWS = 60, 40, 22, 30, 7


def fetch(token, username):
    body = json.dumps({"query": GRAPHQL, "variables": {"login": username}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-graph",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    days = []
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    total = cal["totalContributions"]
    for wk in cal["weeks"]:
        for d in wk["contributionDays"]:
            days.append((d["date"], d["contributionCount"]))
    return total, days


def levels(counts, max_nonzero):
    q1 = max_nonzero * 0.30
    q2 = max_nonzero * 0.60
    q3 = max_nonzero * 0.90
    if counts <= 0:
        return 0
    if counts <= q1:
        return 1
    if counts <= q2:
        return 2
    if counts <= q3:
        return 3
    return 4


def render(total, days, pal):
    weeks = []
    for i in range(0, len(days), 7):
        weeks.append(days[i:i + 7])
    while weeks and len(weeks[-1]) < 7:
        weeks[-1].append((weeks[-1][-1][0], 0))
    cols = len(weeks)
    grid_w = cols * (CELL + GAP) - GAP
    legend_w = 150
    width = GUTTER + 20 + grid_w + 20 + legend_w
    grid_y = GRID_T + 6
    grid_h = ROWS * (CELL + GAP) - GAP
    height = grid_y + grid_h + 34

    max_nonzero = max((c for _, c in days), default=0) or 1

    cells, months = [], {}
    for ci, wk in enumerate(weeks):
        x0 = GUTTER + 20 + ci * (CELL + GAP)
        for ri, (date_s, count) in enumerate(wk):
            y0 = grid_y + ri * (CELL + GAP)
            lvl = levels(count, max_nonzero)
            cells.append(
                f'<rect x="{x0}" y="{y0}" width="{CELL}" height="{CELL}" rx="2" fill="{pal["cell"][lvl]}"/>'
            )
        first = datetime.strptime(wk[0][0], "%Y-%m-%d")
        if ci == 0 or first.month != datetime.strptime(weeks[ci - 1][0][0], "%Y-%m-%d").month:
            months[x0 + CELL / 2] = first.strftime("%b")

    month_labels = "".join(
        f'<text class="mnth" x="{x:.1f}" y="{MONTH_Y}" text-anchor="middle">{m}</text>'
        for x, m in months.items()
    )
    row_labels = "".join(
        f'<text class="wday" x="{GUTTER - 8}" y="{grid_y + r * (CELL + GAP) + CELL - 2:.1f}" '
        f'text-anchor="end">{w}</text>'
        for r, w in zip((1, 3, 5), ("Mon", "Wed", "Fri"))
    )
    legend_x = width - legend_w + 6
    legend = (
        f'<text class="lg" x="{legend_x}" y="{grid_y + grid_h + 16}">Less</text>'
        + "".join(
            f'<rect x="{legend_x + 34 + i * (CELL + GAP)}" y="{grid_y + grid_h + 8}" '
            f'width="{CELL}" height="{CELL}" rx="2" fill="{pal["cell"][l]}"/>'
            for i, l in enumerate((1, 2, 3, 4))
        )
        + f'<text class="lg" x="{legend_x + 34 + 5 * (CELL + GAP) + 4}" y="{grid_y + grid_h + 16}">More</text>'
    )

    total_txt = f"{total:,}".replace(",", " ")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" role="img" aria-label="{total_txt} contributions in the last year">
  <title>{total_txt} contributions in the last year</title>
  <defs>
    <style><![CDATA[
      .panel{{fill:{pal["panel"]};stroke:{pal["stroke"]};stroke-width:1.5}}
      .t{{font-family:{SANS};font-size:13.5px;font-weight:600;fill:{pal["ink"]}}}
      .mnth{{font-family:{SANS};font-size:10.5px;fill:{pal["muted"]}}}
      .wday{{font-family:{SANS};font-size:10px;fill:{pal["muted"]}}}
      .lg{{font-family:{SANS};font-size:10px;fill:{pal["muted"]}}}
    ]]></style>
    <clipPath id="clip"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="{pal["panel"]}"/>
    <text class="t" x="24" y="{TITLE_Y}">{total_txt} contributions in the last year</text>
    {month_labels}
    {cells}
    {row_labels}
    {legend}
  </g>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="none" stroke="{pal["stroke"]}"/>
</svg>
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("username")
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    ap.add_argument("--out", default="assets")
    ap.add_argument("--fixture", help="local JSON dump of the GraphQL response (skip fetch)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    try:
        if args.fixture:
            with open(args.fixture) as f:
                data = json.load(f)
            total = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
            days = []
            for wk in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
                for d in wk["contributionDays"]:
                    days.append((d["date"], d["contributionCount"]))
        else:
            if not args.token:
                print("no token provided; leaving existing graphs untouched", file=sys.stderr)
                sys.exit(0)
            total, days = fetch(args.token, args.username)
        if not days:
            print("empty calendar; leaving existing graphs untouched", file=sys.stderr)
            sys.exit(0)
        for tag, pal in (("dark", DARK), ("light", LIGHT)):
            svg = render(total, days, pal)
            path = os.path.join(args.out, f"graph-{tag}.svg")
            with open(path, "w") as f:
                f.write(svg)
            print(f"wrote {path} ({len(svg)} bytes)")
    except Exception as e:  # noqa: BLE001
        print(f"graph generation failed ({e}); keeping existing files", file=sys.stderr)


if __name__ == "__main__":
    main()