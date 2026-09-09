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
# 1. Project cards
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
# 5. Stack card — the full toolkit, grouped by layer
# --------------------------------------------------------------------------- #
STACK_GROUPS = [
    ("Frontend",         [("React", "#61dafb"), ("TypeScript", "#3178c6"), ("Tailwind", "#38bdf8"),
                          ("Vite", "#646cff"), ("Zustand", "#ca8a04"), ("Framer Motion", "#f472b6")]),
    ("Backend",          [("Node.js", "#339933"), ("Express", "#9aa0a6"), ("Prisma", "#0d9488"),
                          ("Zod", "#6366f1"), ("Socket.IO", "#64748b"), ("Bull", "#ef4444")]),
    ("Data",             [("PostgreSQL", "#336791"), ("Redis", "#dc2626"), ("MySQL", "#00758f")]),
    ("Mobile",           [("React Native", "#61dafb"), ("Expo", "#1e293b"), ("PWA", "#8b5cf6")]),
    ("Infra",            [("Docker", "#2496ed"), ("Coolify", "#2dd4bf"), ("Vercel", "#9aa0a6"),
                          ("GitHub Actions", "#2088ff"), ("Nginx", "#009639")]),
    ("Desktop & systems", [("Python", "#3572A5"), ("PyQt5", "#41cd52"), ("Bash", "#4eaa25"),
                           ("systemd", "#8b5cf6"), ("hostapd", "#f59e0b")]),
]
LCOL, PILL_H, PILL_GAP = 208, 32, 10
MAX_X = 1176


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def stack(p, out):
    def pill(name, color, x, y):
        w = len(name) * 7.6 + 38
        return (f'<rect class="chip" x="{x}" y="{y}" width="{w}" height="{PILL_H}" rx="16"/>'
                f'<circle cx="{x + 13}" cy="{y + PILL_H / 2}" r="4" fill="{color}"/>'
                f'<text class="chipT" x="{x + 26}" y="{y + 21}">{esc(name)}</text>')

    y = 74
    bodies = []
    for label, items in STACK_GROUPS:
        x, line_y = LCOL, y
        parts = []
        for name, color in items:
            w = len(name) * 7.6 + 38
            if x + w > MAX_X:
                x, line_y = LCOL, line_y + PILL_H + 6
            parts.append(pill(name, color, x, line_y))
            x += w + PILL_GAP
        bodies.append(f'<text class="lbl" x="26" y="{line_y + 21}">{esc(label)}</text>')
        bodies.extend(parts)
        y = line_y + PILL_H + 6 + 12
    height = y + 16

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" width="1200" height="{height}" role="img" aria-label="Tech stack grouped by layer">
  <title>Tech stack</title>
  <defs>
    <style><![CDATA[
      {palette_css(p)}
      .chip{{fill:var(--chip);stroke:var(--chipStroke);stroke-width:1}}
      .chipT{{font-family:{MONO};font-size:12.5px;fill:var(--ink)}}
      .lbl{{font-family:{SANS};font-size:15px;font-weight:600;fill:var(--ink)}}
      .hdr{{font-family:{MONO};font-size:13.5px;fill:var(--muted)}}
    ]]></style>
    <clipPath id="cc"><rect x="1" y="1" width="1198" height="{height - 2}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#cc)">
    <rect x="1" y="1" width="1198" height="{height - 2}" rx="14" fill="var(--bg1)"/>
    <text class="hdr" x="26" y="44">THE STACK I BUILD WITH</text>
    <text class="hdr" x="1174" y="44" text-anchor="end">FULL-STACK · MOBILE · SYSTEMS</text>
    <line x1="26" y1="58" x2="1174" y2="58" stroke="var(--stroke)" stroke-width="1"/>
    {''.join(bodies)}
  </g>
  <rect x="1" y="1" width="1198" height="{height - 2}" rx="14" fill="none" stroke="var(--stroke)" stroke-width="1.5"/>
</svg>
'''
    open(out, "w").write(svg)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "cards"), exist_ok=True)
    for tag, pal in (("dark", DARK), ("light", LIGHT)):
        stack(pal, os.path.join(here, f"stack-{tag}.svg"))
        footer(pal, os.path.join(here, f"footer-{tag}.svg"))
        for c in CARDS:
            card(c, pal, os.path.join(here, "cards", f"{c['slug']}-{tag}.svg"))
    divider(os.path.join(here, "divider.svg"))
    print("assets written")
