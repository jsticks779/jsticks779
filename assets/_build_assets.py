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
    def build_row(items, y):
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
        x0 = max((1200 - span) / 2, 0)
        return f'<g transform="translate({x0:.1f},{y})">{body}</g>'

    row_a = build_row(ROW_A, 16)
    row_b = build_row(ROW_B, 66)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 116" width="1200" height="116" role="img" aria-label="Tech stack">
  <title>Stack</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .pill{{fill:var(--chip);stroke:var(--chipStroke);stroke-width:1}}
      .ptxt{{font-family:{MONO};font-size:13.5px;fill:var(--ink)}}
      .edge{{fill:var(--c1)}}
    ]]></style>
    <clipPath id="clip"><rect x="0" y="0" width="1200" height="116" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="1200" height="116" fill="var(--bg1)"/>
    {row_a}
    {row_b}
    <rect class="edge" x="0" y="0" width="1200" height="2.5"/>
    <rect class="edge" x="0" y="113.5" width="1200" height="2.5"/>
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
      .glyph{{fill:none;stroke:var(--c1);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;color:var(--c1)}}
    ]]></style>
    <clipPath id="cc"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#cc)">
    <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="var(--panel)"/>
    <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="var(--bg1)" opacity=".55"/>

    <g transform="translate(410,74)">
      <g class="glyph">{ICONS[c['icon']]}</g>
    </g>

    <text class="name" x="28" y="52">{c['name']}</text>
    <line x1="28" y1="66" x2="250" y2="66" stroke="var(--c1)" stroke-width="1.5" opacity=".45"/>
    <text class="desc" x="28" y="94">{c['desc1']}</text>
    <text class="desc" x="28" y="114">{c['desc2']}</text>

    <g transform="translate(28,138)">
      <circle cx="6" cy="-4" r="6" fill="{c['langc']}"/>
      <text class="meta" x="20" y="0">{c['lang']}</text>
      <text class="meta" x="{20 + len(c['lang'])*7.4 + 22:.0f}" y="0">★ {c['stars']}</text>
    </g>
  </g>
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="none" stroke="var(--stroke)" stroke-width="1.5"/>
</svg>
'''
    open(out, "w").write(svg)


# --------------------------------------------------------------------------- #
# 3. Footer
# --------------------------------------------------------------------------- #
def footer(p, out):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 160" width="1200" height="160" role="img" aria-label="Open to collaborations and freelance work">
  <title>Get in touch</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .t1{{font-family:{SANS};font-size:26px;font-weight:700;fill:var(--ink)}}
      .t2{{font-family:{SANS};font-size:16px;fill:var(--muted)}}
      .t3{{font-family:{MONO};font-size:14px;fill:var(--muted)}}
      .bar{{fill:var(--c1)}}
    ]]></style>
    <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
      <path d="M34 0H0V34" fill="none" stroke="var(--grid)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="1200" height="160" fill="var(--bg1)"/>
  <rect width="1200" height="160" fill="url(#grid)" opacity=".55"/>
  <text class="t1" x="600" y="72" text-anchor="middle">Junior Jovin — Full-Stack Engineer</text>
  <text class="t2" x="600" y="102" text-anchor="middle">open to collaborations, freelance work and open-source contributions</text>
  <text class="t3" x="600" y="128" text-anchor="middle">juniorjovin208@gmail.com</text>
  <rect class="bar" x="0" y="156" width="1200" height="4"/>
</svg>
'''
    open(out, "w").write(svg)


# --------------------------------------------------------------------------- #
# 4. Divider
# --------------------------------------------------------------------------- #
def divider(out):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 8" width="1200" height="8" role="img" aria-label="">
  <rect x="0" y="3" width="1200" height="2.5" rx="1.25" fill="#64748b"/>
</svg>
'''
    open(out, "w").write(svg)


# --------------------------------------------------------------------------- #
# 5. Showreel poster — a nearly-square, clickable placeholder linking to the MP4
# --------------------------------------------------------------------------- #
def showreel(p, out):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 700" width="800" height="700" role="img" aria-label="Showreel - a quick tour of the projects I build">
  <title>Showreel</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .bezel{{fill:var(--bg0)}}
      .panel{{fill:var(--bg1);stroke:var(--stroke);stroke-width:1.5}}
      .label{{font-family:{MONO};font-size:15px;fill:var(--muted)}}
      .ring{{fill:none;stroke:var(--c1);stroke-width:4}}
      .tri{{fill:var(--c1)}}
      .t1{{font-family:{SANS};font-size:26px;font-weight:700;fill:var(--ink)}}
      .t2{{font-family:{MONO};font-size:14.5px;fill:var(--muted)}}
    ]]></style>
  </defs>
  <rect class="bezel" width="800" height="700"/>
  <rect class="panel" x="32" y="32" width="736" height="636" rx="28"/>
  <text class="label" x="64" y="80">SHOWREEL — A QUICK TOUR</text>
  <circle class="ring" cx="400" cy="360" r="74"/>
  <path class="tri" d="M384 322 l70 38 -70 38Z"/>
  <text class="t1" x="400" y="548" text-anchor="middle">A quick tour of the projects I build</text>
  <text class="t2" x="400" y="580" text-anchor="middle">POS &middot; fintech &middot; Linux tools &middot; mobile</text>
  <text class="t2" x="400" y="634" text-anchor="middle">click to play the demo</text>
</svg>
'''
    open(out, "w").write(svg)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "cards"), exist_ok=True)
    for tag, pal in (("dark", DARK), ("light", LIGHT)):
        marquee(pal, os.path.join(here, f"marquee-{tag}.svg"))
        footer(pal, os.path.join(here, f"footer-{tag}.svg"))
        showreel(pal, os.path.join(here, f"showreel-{tag}.svg"))
        for c in CARDS:
            card(c, pal, os.path.join(here, "cards", f"{c['slug']}-{tag}.svg"))
    divider(os.path.join(here, "divider.svg"))
    print("assets written")
