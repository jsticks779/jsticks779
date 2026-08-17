#!/usr/bin/env python3
"""Generates the animated SVG assets used by the profile README.

Every asset is emitted in a dark and a light variant so the README can pick one
with <picture media="(prefers-color-scheme: ...)">. Run from this directory:

    python3 _build_assets.py
"""
import os

DARK = dict(
    bg0="#04060d", bg1="#0a1022", bg2="#080614",
    ink="#e8eefc", muted="#8ea0c4",
    c1="#22d3ee", c2="#8b5cf6", c3="#f472b6",
    panel="rgba(12,18,36,.72)", stroke="rgba(120,190,255,.18)",
    chip="rgba(120,190,255,.07)", chipStroke="rgba(120,190,255,.22)",
    grid="rgba(120,190,255,.10)", glow="#9fd8ff",
)
LIGHT = dict(
    bg0="#f7f9ff", bg1="#eef2ff", bg2="#f5f3ff",
    ink="#0b1220", muted="#4c5b7a",
    c1="#0891b2", c2="#7c3aed", c3="#db2777",
    panel="rgba(255,255,255,.82)", stroke="rgba(60,90,150,.20)",
    chip="rgba(60,90,150,.06)", chipStroke="rgba(60,90,150,.20)",
    grid="rgba(60,90,150,.10)", glow="#5b8def",
)

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',ui-monospace,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Inter,system-ui,-apple-system,'Helvetica Neue',sans-serif"


def palette_css(p):
    return "svg{" + "".join(f"--{k}:{v};" for k, v in p.items()) + "}"


# --------------------------------------------------------------------------- #
# 1. Tech marquee — a seamless scrolling strip of the stack
# --------------------------------------------------------------------------- #
ROW_A = ["TypeScript", "React", "Node.js", "Express", "Prisma", "PostgreSQL",
         "Redis", "Tailwind", "Vite", "Socket.IO", "Zustand", "Framer Motion"]
ROW_B = ["Python", "FastAPI", "React Native", "Expo", "Docker", "Linux",
         "Bash", "PHP", "MySQL", "Gemini API", "Solidity", "Figma"]

PILL_PAD, PILL_H, GAP, CHAR_W = 18, 34, 12, 8.1


def marquee(p, out):
    def build_row(items, y, dur, reverse=False):
        pills, x = [], 0
        for it in items:
            w = len(it) * CHAR_W + PILL_PAD * 2
            pills.append(
                f'<g transform="translate({x:.1f},0)">'
                f'<rect class="pill" x="0" y="0" width="{w:.1f}" height="{PILL_H}" rx="{PILL_H/2}"/>'
                f'<text class="ptxt" x="{w/2:.1f}" y="{PILL_H/2 + 5:.1f}" text-anchor="middle">{it}</text>'
                f'</g>')
            x += w + GAP
        span = x
        body = "".join(pills)
        cls = "revrow" if reverse else "row"
        return (f'<g transform="translate(0,{y})"><g class="{cls}" style="--span:{span:.1f}px;'
                f'animation-duration:{dur}s">{body}'
                f'<g transform="translate({span:.1f},0)">{body}</g></g></g>'), span

    row_a, span_a = build_row(ROW_A, 16, 30)
    row_b, span_b = build_row(ROW_B, 66, 36, reverse=True)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 116" width="1200" height="116" role="img" aria-label="Tech stack">
  <title>Stack</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .pill{{fill:var(--chip);stroke:var(--chipStroke);stroke-width:1}}
      .ptxt{{font-family:{MONO};font-size:13.5px;fill:var(--ink)}}
      .row{{animation:scrollL linear infinite}}
      .revrow{{animation:scrollR linear infinite}}
      @keyframes scrollL{{from{{transform:translateX(0)}}to{{transform:translateX(calc(-1 * var(--span)))}}}}
      @keyframes scrollR{{from{{transform:translateX(calc(-1 * var(--span)))}}to{{transform:translateX(0)}}}}
      @media (prefers-reduced-motion: reduce){{*{{animation:none !important}}}}
    ]]></style>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="var(--bg0)" stop-opacity="1"/>
      <stop offset=".08" stop-color="var(--bg0)" stop-opacity="0"/>
      <stop offset=".92" stop-color="var(--bg0)" stop-opacity="0"/>
      <stop offset="1" stop-color="var(--bg0)" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="var(--c1)"/><stop offset=".5" stop-color="var(--c2)"/><stop offset="1" stop-color="var(--c3)"/>
    </linearGradient>
    <clipPath id="clip"><rect x="0" y="0" width="1200" height="116" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="1200" height="116" fill="var(--bg1)"/>
    {row_a}
    {row_b}
    <rect width="1200" height="116" fill="url(#fade)"/>
    <rect x="0" y="0" width="1200" height="2.5" fill="url(#edge)" opacity=".85"/>
    <rect x="0" y="113.5" width="1200" height="2.5" fill="url(#edge)" opacity=".85"/>
    <rect x="0" y="0" width="1200" height="116" rx="14" fill="none" stroke="var(--stroke)" stroke-width="1.5"/>
  </g>
</svg>
'''
    open(out, "w").write(svg)


# --------------------------------------------------------------------------- #
# 2. Project cards
# --------------------------------------------------------------------------- #
CARDS = [
    dict(slug="hotspot", name="Hotspot on Linux", lang="Shell", langc="#89e051", stars="2",
         desc1="One Wi-Fi card as client AND access point —",
         desc2="hostapd + dnsmasq + NAT, wired up for you.", icon="wifi"),
    dict(slug="juniodev-ui", name="jUNIODEV-UI", lang="JavaScript", langc="#f1e05a", stars="1",
         desc1="Sci-fi terminal overlay with live system",
         desc2="monitoring. One-command install, AppImage.", icon="terminal"),
    dict(slug="mypmanager", name="MyPManager", lang="TypeScript", langc="#3178c6", stars="1",
         desc1="Zero-knowledge password manager —",
         desc2="PBKDF2 + AES-256-GCM, encrypted client-side.", icon="lock"),
    dict(slug="jcamera", name="JCamera for Linux", lang="Python", langc="#3572A5", stars="1",
         desc1="Camera, video and screen recorder for Linux.",
         desc2="PyQt5 + OpenCV, live filters, PulseAudio.", icon="camera"),
    dict(slug="ghost-screen", name="Ghost Screen", lang="Python", langc="#3572A5", stars="1",
         desc1="Animated holographic screensaver overlay",
         desc2="for Linux & Windows. Toggle with Ctrl+3.", icon="ghost"),
    dict(slug="efootball", name="eFootball League Manager", lang="PHP", langc="#4F5D95", stars="2",
         desc1="League system with automated fixtures,",
         desc2="player dashboards and payment tracking.", icon="trophy"),
]

ICONS = dict(
    wifi='<path d="M-16 4a22 22 0 0 1 32 0" /><path d="M-9 12a12 12 0 0 1 18 0"/><circle cx="0" cy="20" r="2.6" fill="currentColor" stroke="none"/>',
    terminal='<rect x="-18" y="-12" width="36" height="30" rx="4"/><path d="M-11 -3l6 5-6 5"/><path d="M-1 12h10"/>',
    lock='<rect x="-13" y="-2" width="26" height="20" rx="4"/><path d="M-7 -2v-6a7 7 0 0 1 14 0v6"/><circle cx="0" cy="8" r="2.4" fill="currentColor" stroke="none"/>',
    camera='<rect x="-18" y="-8" width="36" height="26" rx="5"/><path d="M-7 -8l3-5h8l3 5"/><circle cx="0" cy="5" r="7"/>',
    ghost='<path d="M-14 16V0a14 14 0 0 1 28 0v16l-5-4-5 4-4-4-5 4-5-4z"/><circle cx="-5" cy="-2" r="2.2" fill="currentColor" stroke="none"/><circle cx="5" cy="-2" r="2.2" fill="currentColor" stroke="none"/>',
    trophy='<path d="M-10 -12h20v9a10 10 0 0 1-20 0z"/><path d="M-10 -8h-5a6 6 0 0 0 6 6"/><path d="M10 -8h5a6 6 0 0 1-6 6"/><path d="M0 6v7"/><path d="M-7 16h14"/>',
)

W, H = 480, 168


def card(c, p, out):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{c['name']}">
  <title>{c['name']}</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .name{{font-family:{SANS};font-size:21px;font-weight:700;fill:var(--ink)}}
      .desc{{font-family:{SANS};font-size:13.5px;fill:var(--muted)}}
      .meta{{font-family:{MONO};font-size:12px;fill:var(--muted)}}
      .glyph{{fill:none;stroke:url(#g);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;color:var(--c2);
              animation:float 5s ease-in-out infinite}}
      @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
      .halo{{animation:halo 3.4s ease-in-out infinite}}
      @keyframes halo{{0%,100%{{opacity:.12;transform:scale(.94)}}50%{{opacity:.30;transform:scale(1.06)}}}}
      .march{{stroke:url(#g);stroke-width:2;fill:none;stroke-dasharray:150 1150;stroke-linecap:round;
              animation:march 6s linear infinite}}
      @keyframes march{{to{{stroke-dashoffset:-1300}}}}
      .spark{{stroke:url(#g);stroke-width:2;fill:none;stroke-dasharray:180;stroke-dashoffset:180;
              animation:draw 2.6s .3s ease-out forwards}}
      @keyframes draw{{to{{stroke-dashoffset:0}}}}
      .beam{{animation:beam 6s ease-in-out infinite}}
      @keyframes beam{{0%{{transform:translateX(-160px)}}60%,100%{{transform:translateX(560px)}}}}
      @media (prefers-reduced-motion: reduce){{*{{animation:none !important}}.spark{{stroke-dashoffset:0}}}}
    ]]></style>
    <linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
      <stop offset="0" stop-color="var(--c1)"/><stop offset=".55" stop-color="var(--c2)"/><stop offset="1" stop-color="var(--c3)"/>
    </linearGradient>
    <linearGradient id="beamg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="var(--glow)" stop-opacity=".14"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="halo"><stop offset="0" stop-color="var(--c2)" stop-opacity=".9"/><stop offset="1" stop-color="var(--c2)" stop-opacity="0"/></radialGradient>
    <clipPath id="cc"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#cc)">
    <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="var(--panel)"/>
    <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="var(--bg1)" opacity=".55"/>
    <g class="beam"><rect x="-80" y="-20" width="120" height="220" fill="url(#beamg)" transform="skewX(-16)"/></g>

    <g transform="translate(410,74)">
      <circle class="halo" r="40" fill="url(#halo)"/>
      <g class="glyph">{ICONS[c['icon']]}</g>
    </g>

    <text class="name" x="28" y="52">{c['name']}</text>
    <path class="spark" d="M28 66 H 250" opacity=".7"/>
    <text class="desc" x="28" y="94">{c['desc1']}</text>
    <text class="desc" x="28" y="114">{c['desc2']}</text>

    <g transform="translate(28,138)">
      <circle cx="6" cy="-4" r="6" fill="{c['langc']}"/>
      <text class="meta" x="20" y="0">{c['lang']}</text>
      <text class="meta" x="{20 + len(c['lang'])*7.4 + 22:.0f}" y="0">★ {c['stars']}</text>
    </g>
  </g>
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="none" stroke="var(--stroke)" stroke-width="1.5"/>
  <rect class="march" x="2" y="2" width="{W-4}" height="{H-4}" rx="16"/>
</svg>
'''
    open(out, "w").write(svg)


# --------------------------------------------------------------------------- #
# 3. Footer wave
# --------------------------------------------------------------------------- #
def footer(p, out):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 190" width="1200" height="190" role="img" aria-label="Thanks for visiting">
  <title>Let's build</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .w{{animation:wave linear infinite}}
      @keyframes wave{{from{{transform:translateX(0)}}to{{transform:translateX(-600px)}}}}
      .t1{{font-family:{SANS};font-size:24px;font-weight:700;fill:var(--ink)}}
      .t2{{font-family:{MONO};font-size:14px;fill:var(--muted)}}
      .heart{{animation:beat 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
      @keyframes beat{{0%,100%{{transform:scale(1)}}25%{{transform:scale(1.18)}}45%{{transform:scale(1)}}}}
      .rise{{opacity:0;animation:rise .8s ease-out forwards}}
      .r2{{animation-delay:.25s}}
      @keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
      @media (prefers-reduced-motion: reduce){{*{{animation:none !important}}.rise{{opacity:1}}}}
    ]]></style>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="var(--c1)"/><stop offset=".5" stop-color="var(--c2)"/><stop offset="1" stop-color="var(--c3)"/>
    </linearGradient>
    <clipPath id="fc"><rect width="1200" height="190" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#fc)">
    <rect width="1200" height="190" fill="var(--bg1)"/>
    <g class="w" style="animation-duration:14s" opacity=".28">
      <path d="M0 118 q150 -34 300 0 t300 0 t300 0 t300 0 t300 0 V190 H0Z" fill="url(#g1)"/>
    </g>
    <g class="w" style="animation-duration:9s" opacity=".38">
      <path d="M0 138 q150 -28 300 0 t300 0 t300 0 t300 0 t300 0 V190 H0Z" fill="url(#g1)"/>
    </g>
    <g class="w" style="animation-duration:6s" opacity=".55">
      <path d="M0 158 q150 -22 300 0 t300 0 t300 0 t300 0 t300 0 V190 H0Z" fill="url(#g1)"/>
    </g>
    <text class="t1 rise" x="600" y="66" text-anchor="middle">Thanks for scrolling — let’s build something</text>
    <text class="t2 rise r2" x="600" y="96" text-anchor="middle">open to collaborations, freelance work and open-source contributions</text>
    <g class="heart" transform="translate(600,120)">
      <path d="M0 8 C-9 0 -13 -5 -13 -9 A6 6 0 0 1 0 -12 A6 6 0 0 1 13 -9 C13 -5 9 0 0 8Z" fill="var(--c3)"/>
    </g>
  </g>
</svg>
'''
    open(out, "w").write(svg)


# --------------------------------------------------------------------------- #
# 4. Divider
# --------------------------------------------------------------------------- #
def divider(out):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 8" width="1200" height="8" role="img" aria-label="">
  <defs>
    <style><![CDATA[
      .sh{animation:sh 5s linear infinite}
      @keyframes sh{0%{transform:translateX(-300px)}100%{transform:translateX(1300px)}}
      @media (prefers-reduced-motion: reduce){*{animation:none !important}}
    ]]></style>
    <linearGradient id="d" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset=".2" stop-color="#22d3ee"/><stop offset=".5" stop-color="#8b5cf6"/><stop offset=".8" stop-color="#f472b6"/>
      <stop offset="1" stop-color="#f472b6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="s" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".85"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="3" width="1200" height="2.5" rx="1.25" fill="url(#d)"/>
  <rect class="sh" x="-300" y="2" width="220" height="4" rx="2" fill="url(#s)" opacity=".5"/>
</svg>
'''
    open(out, "w").write(svg)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "cards"), exist_ok=True)
    for tag, pal in (("dark", DARK), ("light", LIGHT)):
        marquee(pal, os.path.join(here, f"marquee-{tag}.svg"))
        footer(pal, os.path.join(here, f"footer-{tag}.svg"))
        for c in CARDS:
            card(c, pal, os.path.join(here, "cards", f"{c['slug']}-{tag}.svg"))
    divider(os.path.join(here, "divider.svg"))
    print("assets written")
