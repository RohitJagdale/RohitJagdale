"""Generate the inert SVG card assets used by the profile README.

Run from the repository root:  python tools/build_profile_ui.py
It rewrites assets/ui/*.svg and README.md.
Every card has a desktop (1200px wide) and a mobile (800px wide) variant.
The SVGs contain no scripts, links, external fonts, or external resources;
clickable links live in README.md around the contact buttons.
"""

from __future__ import annotations

import random
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "ui"
RAW = "https://raw.githubusercontent.com/RohitJagdale/RohitJagdale"

LINKEDIN = "https://www.linkedin.com/in/rohit-jagadale-317b5020b/"
EMAIL = "rohitjagadale4@gmail.com"
CREDLY = "https://www.credly.com/badges/353ecc9b-15c6-4e49-ad0b-f9968e63480a/linked_in_profile"

SANS = "'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', 'Cascadia Code', Consolas, 'Liberation Mono', monospace"

INK = "#060714"
CARD_TOP = "#0C1130"
CARD_BOTTOM = "#080B1D"
TEXT = "#EEF1FF"
MUTED = "#A3ACCF"
DIM = "#6B7499"
CYAN = "#00E5FF"
VIOLET = "#A855F7"
PINK = "#FF2BD6"
AMBER = "#FFB020"
GREEN = "#34D399"
ACCENTS = (CYAN, VIOLET, PINK, AMBER)

STYLE = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.twinkle{{animation:twinkle 4s ease-in-out infinite}}
.aurora{{animation:aurora 16s ease-in-out infinite alternate}}
.aurora.b{{animation-duration:21s;animation-direction:alternate-reverse}}
.glow{{animation:glow 6s ease-in-out infinite}}
.cursor{{animation:blink 1.1s steps(1) infinite}}
.sweep{{animation:sweep 9s ease-in-out infinite}}
.grid{{animation:grid 2.4s linear infinite}}
.drone{{animation:drone 14s ease-in-out infinite alternate}}
.wave{{animation:wave 14s linear infinite}}
.wave.b{{animation-duration:22s;animation-direction:reverse}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}}
@keyframes twinkle{{0%,100%{{opacity:.2}}50%{{opacity:1}}}}
@keyframes aurora{{from{{transform:translate(-40px,0)}}to{{transform:translate(60px,18px)}}}}
@keyframes glow{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes sweep{{0%{{transform:translateX(-30%)}}100%{{transform:translateX(130%)}}}}
@keyframes grid{{from{{transform:translateY(0)}}to{{transform:translateY(24px)}}}}
@keyframes drone{{from{{transform:translate(0,0)}}to{{transform:translate(-140px,26px)}}}}
@keyframes wave{{from{{transform:translateX(0)}}to{{transform:translateX(-600px)}}}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.45;transform:scale(.8)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
"""


def char_width(size: float, mono: bool = False, bold: bool = False, caps: bool = False) -> float:
    if mono:
        return size * 0.61
    if caps:
        return size * (0.7 if bold else 0.64)
    return size * (0.56 if bold else 0.52)


def text_width(text: str, size: float, **kw) -> float:
    return len(text) * char_width(size, **kw)


def wrap(text: str, size: float, max_width: float, **kw) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and text_width(candidate, size, **kw) > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def t(x, y, text, size, fill=TEXT, cls="sans", weight=400, anchor="start", spacing=0, extra=""):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{escape(text)}</text>'
    )


def svg(width: int, height: int, title: str, body: str, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">\n'
        f"<title id=\"title\">{escape(title)}</title>\n"
        f"<style>{STYLE}</style>\n"
        f"<defs>{COMMON_DEFS}{defs}</defs>\n{body}\n</svg>\n"
    )


COMMON_DEFS = f"""
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/>
</linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
</linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{CARD_TOP}"/><stop offset="1" stop-color="{CARD_BOTTOM}"/>
</linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{CYAN}" stop-opacity=".6"/><stop offset=".45" stop-color="{VIOLET}" stop-opacity=".25"/>
  <stop offset="1" stop-color="{PINK}" stop-opacity=".5"/>
</linearGradient>
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#141A3D"/><stop offset="1" stop-color="#0E1230"/>
</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".07"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
<radialGradient id="glowCyan"><stop offset="0" stop-color="{CYAN}" stop-opacity=".45"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowViolet"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowPink"><stop offset="0" stop-color="{PINK}" stop-opacity=".4"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
"""


# ---------------------------------------------------------------- primitives

def card_frame(w, h, number, label, title, title_size=34, pad=56, beam=True, label_size=16):
    parts = [
        f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath>',
        '<g clip-path="url(#clip)">',
        f'<rect width="{w}" height="{h}" fill="url(#card)"/>',
        f'<ellipse cx="{w * 0.9:.0f}" cy="0" rx="{w * 0.35:.0f}" ry="{h * 0.45:.0f}" fill="url(#glowViolet)" opacity=".55"/>',
        f'<ellipse cx="0" cy="{h:.0f}" rx="{w * 0.3:.0f}" ry="{h * 0.35:.0f}" fill="url(#glowCyan)" opacity=".35"/>',
    ]
    if beam:
        parts.append(f'<rect class="sweep" x="0" y="0" width="{w * 0.35:.0f}" height="{h}" fill="url(#beam)"/>')
    parts += [
        "</g>",
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="27.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>',
        f'<rect x="{pad}" y="0" width="120" height="3" rx="1.5" fill="url(#accent)"/>',
        t(pad, 72, f"{number} // {label}", label_size, CYAN, "mono", 600, spacing=4),
        t(pad, 72 + title_size + 16, title, title_size, TEXT, "sans", 700),
    ]
    return "\n".join(parts)


def chip(x, y, label, color, size=14, height=32):
    width = text_width(label, size, mono=True) + 34
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height}" rx="{height / 2}" fill="none" '
        f'stroke="{color}" stroke-opacity=".6"/>'
        + f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height}" rx="{height / 2}" fill="{color}" fill-opacity=".1"/>'
        + t(x + width / 2, y + height / 2 + size * 0.36, label, size, color, "mono", 600, "middle", 1)
    ), width


def chips_row(labels, x, y, max_width, size=14, height=32, gap=10, center=False):
    rows, row, row_w = [], [], 0.0
    for i, label in enumerate(labels):
        w = text_width(label, size, mono=True) + 34
        if row and row_w + gap + w > max_width:
            rows.append((row, row_w))
            row, row_w = [], 0.0
        row_w = row_w + (gap if row else 0) + w
        row.append((label, ACCENTS[i % len(ACCENTS)]))
    if row:
        rows.append((row, row_w))
    out = []
    for r, (items, total) in enumerate(rows):
        cx = x + (max_width - total) / 2 if center else x
        for label, color in items:
            s, w = chip(cx, y + r * (height + gap), label, color, size, height)
            out.append(s)
            cx += w + gap
    return "\n".join(out), len(rows) * (height + gap) - gap


ICONS = {
    "agent": '<circle cx="12" cy="5" r="2.6"/><circle cx="5" cy="18" r="2.6"/><circle cx="19" cy="18" r="2.6"/>'
             '<path d="M10.7 7.3 6.3 15.7M13.3 7.3l4.4 8.4M7.6 18h8.8"/>',
    "cloud": '<path d="M7 18.5h10.2a4.3 4.3 0 0 0 .6-8.6A6 6 0 0 0 6.4 9.4 4.6 4.6 0 0 0 7 18.5Z"/><path d="M12 12v4M10 14h4"/>',
    "cube": '<path d="M12 2.8 20 7.3v9.4l-8 4.5-8-4.5V7.3Z"/><path d="M4 7.3l8 4.5 8-4.5M12 11.8v9.4"/>',
    "spark": '<path d="M12 2.5c.8 5.1 3.4 7.7 8.5 8.5-5.1.8-7.7 3.4-8.5 8.5-.8-5.1-3.4-7.7-8.5-8.5 5.1-.8 7.7-3.4 8.5-8.5Z"/>'
             '<path d="M19 17.5v4M17 19.5h4"/>',
    "station": '<path d="M3 20.5h18M5 20.5V9.5l7-5 7 5v11"/><path d="M9 20.5v-6h6v6M8.5 10.5h7"/>',
    "bolt": '<path d="M13.5 2.5 5 13.5h6l-1 8 8.5-11h-6Z"/>',
    "shield": '<path d="M12 2.8 19.5 6v5.6c0 4.6-3.1 8.2-7.5 9.6-4.4-1.4-7.5-5-7.5-9.6V6Z"/><path d="m8.6 12 2.4 2.4 4.4-4.6"/>',
    "form": '<rect x="4.5" y="3" width="15" height="18" rx="2.5"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    "code": '<path d="m8.5 7-5 5 5 5M15.5 7l5 5-5 5M13.5 4.5l-3 15"/>',
    "brief": '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M9 7V5h6v2M3 12.5h18"/>',
    "medal": '<circle cx="12" cy="14.5" r="5.5"/><path d="M8.5 9.8 6 3h4l2 4.5L14 3h4l-2.5 6.8"/>',
    "trophy": '<path d="M7 4h10v5a5 5 0 0 1-10 0Z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 14v3.5M8 20.5h8"/>',
    "cap": '<path d="M2.5 9 12 4.5 21.5 9 12 13.5Z"/><path d="M6.5 11v4.5c3 2.4 8 2.4 11 0V11M21.5 9v5"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M8 10.5V16M8 7.6v.1M11.5 16v-5.5M11.5 13c0-1.6 1-2.6 2.4-2.6s2.1.9 2.1 2.6V16"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7 8 6 8-6"/>',
}


def icon(kind, x, y, size, color):
    """Small line icons drawn on a 24-unit grid."""
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 24:.3f})" fill="none" stroke="{color}" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>'
    )


def icon_tile(kind, x, y, size, color):
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.28:.1f}" fill="{color}" fill-opacity=".1" '
        f'stroke="{color}" stroke-opacity=".45"/>' + icon(kind, x + size * 0.22, y + size * 0.22, size * 0.56, color)
    )


def stars(w, h, count, seed, max_y_ratio=0.72, avoid=None):
    rnd = random.Random(seed)
    out = []
    for i in range(count):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(8, h * max_y_ratio)
        if avoid and avoid[0] <= x <= avoid[2] and avoid[1] <= y <= avoid[3]:
            continue
        r = rnd.choice((0.7, 0.9, 1.1, 1.4, 1.8))
        if i % 3 == 0:
            out.append(f'<circle class="twinkle" style="animation-delay:{rnd.uniform(-4, 0):.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFFFFF"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFFFFF" opacity="{rnd.uniform(.25, .7):.2f}"/>')
    return "\n".join(out)


# ---------------------------------------------------------------- hero: neon city at dusk

HERO_DEFS = f"""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#04050E"/><stop offset=".6" stop-color="#120B33"/><stop offset="1" stop-color="#2A0E45"/>
</linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1A0A3A"/><stop offset="1" stop-color="#04050E"/>
</linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFE29A"/><stop offset=".45" stop-color="{AMBER}"/><stop offset="1" stop-color="{PINK}"/>
</linearGradient>
<radialGradient id="sunHalo"><stop offset=".4" stop-color="{PINK}" stop-opacity=".4"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
"""


def sun(cx, cy, r):
    stripes = []
    for i in range(6):
        y = cy + r * (0.05 + i * 0.17)
        stripes.append(f'<rect x="{cx - r}" y="{y:.0f}" width="{2 * r}" height="{2 + i * 2.2:.1f}" fill="#000"/>')
    return f"""
<mask id="sunMask"><rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="#fff"/>{''.join(stripes)}</mask>
<circle class="glow" cx="{cx}" cy="{cy}" r="{r * 2:.0f}" fill="url(#sunHalo)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)" mask="url(#sunMask)"/>"""


def city(x0, x1, base, max_h, seed):
    rnd = random.Random(seed)
    out, x = [], x0
    while x < x1:
        bw = rnd.uniform(26, 58)
        bh = rnd.uniform(max_h * 0.3, max_h)
        top = base - bh
        out.append(f'<rect x="{x:.0f}" y="{top:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{INK}" stroke="{VIOLET}" stroke-opacity=".35"/>')
        if bh > max_h * 0.75 and rnd.random() < 0.5:
            out.append(f'<path d="M{x + bw / 2:.0f} {top:.0f}v-18" stroke="{VIOLET}" stroke-opacity=".6"/>')
            out.append(f'<circle class="twinkle" cx="{x + bw / 2:.0f}" cy="{top - 18:.0f}" r="2.2" fill="{PINK}"/>')
        for wy in range(int(top) + 10, int(base) - 6, 12):
            for wx in range(int(x) + 6, int(x + bw) - 6, 10):
                if rnd.random() < 0.22:
                    color = rnd.choice((CYAN, PINK, AMBER))
                    cls = ' class="twinkle"' if rnd.random() < 0.15 else ""
                    out.append(f'<rect{cls} x="{wx}" y="{wy}" width="4" height="5" fill="{color}" opacity=".55"/>')
        x += bw + rnd.uniform(2, 8)
    return "\n".join(out)


def grid_floor(w, h, horizon, vx, step):
    verticals = "".join(
        f'<path d="M{vx} {horizon}L{vx + i * w * 0.09:.0f} {h}" stroke="{PINK}" stroke-opacity=".35"/>'
        for i in range(-16, 17)
    )
    horizontals = "".join(
        f'<path d="M0 {horizon + k * step:.0f}H{w}" stroke="{CYAN}" stroke-opacity="{0.15 + 0.03 * k:.2f}"/>'
        for k in range(0, int((h - horizon) / step) + 2)
    )
    return f"""
<clipPath id="floorClip"><rect x="0" y="{horizon}" width="{w}" height="{h - horizon}"/></clipPath>
<rect x="0" y="{horizon}" width="{w}" height="{h - horizon}" fill="url(#floor)"/>
<g clip-path="url(#floorClip)">{verticals}<g class="grid">{horizontals}</g></g>
<rect x="0" y="{horizon - 1}" width="{w}" height="2" fill="{PINK}" opacity=".7"/>"""


def drone(x, y, s):
    return f"""
<g transform="translate({x} {y}) scale({s})"><g class="drone">
 <path d="M-22 0h44M-14 -6h28" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>
 <rect x="-9" y="-3" width="18" height="9" rx="4" fill="{INK}" stroke="{CYAN}"/>
 <circle class="pulse" cx="0" cy="12" r="2.5" fill="{PINK}"/>
 <path d="M0 14l-26 70h52Z" fill="{CYAN}" opacity=".06"/>
</g></g>"""


TAGLINE = "AI agents · Serverless cloud · Digital twins"
HERO_CHIPS = ["SOFTWARE DEVELOPER @ KONE", "AWS CERTIFIED", "PUNE, INDIA"]
PROMPT = "> teaching AI agents to fix code first."
HERO_ALT = "ROHIT JAGADALE — Software Developer building AI agents, serverless cloud and digital twins. A neon city skyline under a synthwave sun."


def hero_desktop():
    w, h = 1200, 520
    horizon = 372
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#sky)"/>
<ellipse class="aurora" cx="330" cy="120" rx="460" ry="170" fill="url(#glowCyan)" opacity=".45"/>
<ellipse class="aurora b" cx="760" cy="60" rx="420" ry="160" fill="url(#glowViolet)"/>
{stars(w, horizon, 90, 7, 0.8, avoid=(40, 90, 790, 460))}
{sun(930, 262, 128)}
{city(790, w + 20, horizon, 150, 3)}
{grid_floor(w, h, horizon, 930, 24)}
{drone(1080, 110, 1.1)}
<rect class="sweep" x="0" y="0" width="420" height="{h}" fill="url(#beam)"/>
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="27.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
{t(w - 40, 52, "github.com/RohitJagdale", 15, DIM, "mono", 500, "end", 2)}
<circle class="pulse" cx="72" cy="47" r="5" fill="{GREEN}"/>
{t(88, 52, "ONLINE · SHIPPING AGENTS TO PROD", 14, "#6EE7B7", "mono", 600, spacing=3)}
{t(72, 168, "SYSTEM BOOT — USER:", 18, CYAN, "mono", 600, spacing=6)}
<text x="68" y="252" class="sans" font-size="76" font-weight="800" fill="url(#name)" textLength="690" lengthAdjust="spacing">ROHIT JAGADALE</text>
<rect x="72" y="278" width="140" height="4" rx="2" fill="url(#accent)"/>
{t(72, 330, TAGLINE, 27, "#D4DAF7", "sans", 500)}
{t(72, 372, PROMPT, 18, MUTED, "mono", 500)}
<rect class="cursor" x="{72 + text_width(PROMPT, 18, mono=True) + 6:.0f}" y="357" width="10" height="20" fill="{CYAN}"/>
{chips_row(HERO_CHIPS, 72, 412, 700, 14, 34)[0]}
"""
    return svg(w, h, HERO_ALT, body, HERO_DEFS)


def hero_mobile():
    w, h = 800, 1060
    horizon = 400
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="32"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#sky)"/>
<ellipse class="aurora" cx="200" cy="140" rx="380" ry="190" fill="url(#glowCyan)" opacity=".45"/>
<ellipse class="aurora b" cx="600" cy="80" rx="360" ry="170" fill="url(#glowViolet)"/>
{stars(w, horizon, 70, 11, 0.8, avoid=(0, 0, 200, 100))}
{sun(400, 260, 140)}
{city(-10, w + 20, horizon, 170, 9)}
{grid_floor(w, 500, horizon, 400, 24)}
<rect x="0" y="500" width="{w}" height="{h - 500}" fill="{INK}" opacity=".7"/>
<ellipse class="aurora" cx="400" cy="920" rx="420" ry="180" fill="url(#glowPink)" opacity=".45"/>
{drone(640, 120, 1.4)}
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="31" fill="none" stroke="url(#edge)" stroke-width="2"/>
<circle class="pulse" cx="56" cy="62" r="7" fill="{GREEN}"/>
{t(76, 70, "ONLINE · @ KONE", 24, "#6EE7B7", "mono", 600, spacing=4)}
{t(w / 2, 580, "SYSTEM BOOT — USER:", 26, CYAN, "mono", 600, "middle", 6)}
<text x="{w / 2}" y="684" class="sans" font-size="104" font-weight="800" fill="url(#name)" text-anchor="middle">ROHIT</text>
<text x="{w / 2}" y="792" class="sans" font-size="104" font-weight="800" fill="url(#name)" text-anchor="middle" textLength="640" lengthAdjust="spacing">JAGADALE</text>
<rect x="{w / 2 - 80}" y="818" width="160" height="5" rx="2.5" fill="url(#accent)"/>
{t(w / 2, 872, "AI agents · Serverless cloud", 34, "#D4DAF7", "sans", 500, "middle")}
{t(w / 2, 916, "Digital twins", 34, "#D4DAF7", "sans", 500, "middle")}
{chips_row(HERO_CHIPS[1:], 40, 950, w - 80, 22, 48, 14, center=True)[0]}
"""
    return svg(w, h, HERO_ALT, body, HERO_DEFS)


# ---------------------------------------------------------------- contact buttons (wrapped in links in README)

BUTTONS = [
    ("linkedin", "LINKEDIN", "rohit-jagadale", CYAN, LINKEDIN),
    ("mail", "GMAIL", "say hello", PINK, f"mailto:{EMAIL}"),
    ("medal", "AWS CERT", "verify on Credly", AMBER, CREDLY),
]


def button(kind, label, sub, color):
    w, h = 380, 110
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="22"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#card)"/>
<ellipse cx="{w}" cy="0" rx="200" ry="90" fill="url(#glowViolet)" opacity=".5"/>
<rect class="sweep" x="0" y="0" width="140" height="{h}" fill="url(#beam)"/>
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="21.5" fill="none" stroke="{color}" stroke-opacity=".55" stroke-width="1.5"/>
{icon_tile(kind, 22, 21, 68, color)}
{t(110, 56, label, 28, color, "mono", 700, spacing=3)}
{t(110, 86, sub, 19, MUTED, "sans", 500)}
{t(w - 30, 66, "↗", 32, color, "sans", 700, "end")}
"""
    return svg(w, h, f"{label} — {sub}", body)


# ---------------------------------------------------------------- about

ABOUT_TITLE = "Building systems that run themselves."
ABOUT_ITEMS = [
    ("agent", "AI AGENTS", "MCP servers and Bedrock agents wired into GitLab and the IDE", CYAN),
    ("cloud", "SERVERLESS", "Lambda, AppSync, API Gateway and DynamoDB, all in AWS CDK", VIOLET),
    ("cube", "DIGITAL TWINS", "Real-time 3D station twins built with React and Three.js", PINK),
    ("code", "DEV PRODUCTIVITY", "CI/CD automation, AI code review and faster releases", AMBER),
    ("brief", "EXPERIENCE", "3+ years · Software Developer at KONE Elevator since Aug 2023", CYAN),
]
TERMINAL = [
    ("$ whoami", DIM),
    ("→ rohit jagadale", TEXT),
    ("→ full stack & cloud dev", TEXT),
    ("→ pune, india", TEXT),
    ("", TEXT),
    ("$ cat currently.txt", DIM),
    ("agents that fix code first", PINK),
]
ABOUT_ALT = (
    "About Rohit: " + ABOUT_TITLE + " "
    + " ".join(f"{label}: {text}." for _, label, text, _ in ABOUT_ITEMS)
)


def terminal(x, y, w, size, line_h):
    h = 70 + len(TERMINAL) * line_h + 10
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#05061A" stroke="#2A3366"/>',
        f'<path d="M{x} {y + 46}h{w}" stroke="#2A3366"/>',
    ]
    for i, c in enumerate(("#FB7185", AMBER, GREEN)):
        parts.append(f'<circle cx="{x + 26 + i * 22}" cy="{y + 23}" r="6.5" fill="{c}"/>')
    parts.append(t(x + w - 22, y + 28, "rohit@kone: ~", size * 0.78, DIM, "mono", 500, "end"))
    for i, (line, color) in enumerate(TERMINAL):
        if line:
            parts.append(t(x + 26, y + 84 + i * line_h, line, size, color, "mono", 500))
    last_w = text_width(TERMINAL[-1][0], size, mono=True)
    yl = y + 84 + (len(TERMINAL) - 1) * line_h
    parts.append(f'<rect class="cursor" x="{x + 32 + last_w:.0f}" y="{yl - size * 0.85:.0f}" width="{size * 0.55:.0f}" height="{size * 1.05:.0f}" fill="{PINK}"/>')
    return "\n".join(parts), h


def icon_rows(items, x, y, width, label_size, text_size, tile, gap):
    parts, cy = [], y
    for kind, label, text, color in items:
        lines = wrap(text, text_size, width - tile - 24)
        parts.append(icon_tile(kind, x, cy, tile, color))
        parts.append(t(x + tile + 22, cy + label_size + 2, label, label_size, color, "mono", 700, spacing=3))
        for j, line in enumerate(lines):
            parts.append(t(x + tile + 22, cy + label_size + 10 + text_size * 1.05 + j * text_size * 1.3, line, text_size, "#D4DAF7"))
        cy += max(tile, label_size + 14 + len(lines) * text_size * 1.3) + gap
    return "\n".join(parts), cy - gap - y


def about_desktop():
    w = 1200
    rows, rows_h = icon_rows(ABOUT_ITEMS, 56, 160, 640, 14, 21, 52, 22)
    term, term_h = terminal(752, 160, 392, 18, 32)
    h = int(160 + max(rows_h, term_h) + 52)
    return svg(w, h, ABOUT_ALT, card_frame(w, h, "01", "WHOAMI", ABOUT_TITLE, 32) + rows + term)


def about_mobile():
    w = 800
    title = wrap(ABOUT_TITLE, 44, w - 96, bold=True)
    top = 72 + 44 + 16 + (len(title) - 1) * 54 + 48
    rows, rows_h = icon_rows(ABOUT_ITEMS, 48, top, w - 96, 20, 30, 72, 30)
    term, term_h = terminal(48, top + rows_h + 44, w - 96, 26, 44)
    h = int(top + rows_h + 44 + term_h + 48)
    frame = card_frame(w, h, "01", "WHOAMI", title[0], 44, pad=48, label_size=22)
    extra = "".join(t(48, 72 + 44 + 16 + i * 54, line, 44, TEXT, "sans", 700) for i, line in enumerate(title[1:], 1))
    return svg(w, h, ABOUT_ALT, frame + extra + rows + term)


# ---------------------------------------------------------------- missions (projects)

MISSIONS = [
    ("agent", "MCP Servers for Jira & CVMS", "MODEL CONTEXT PROTOCOL · IDE",
     "Python MCP servers that let AI agents in VS Code and Kiro IDE fetch context, analyse issues and run developer workflows from the editor.",
     [], ["Python", "MCP", "Tool Calling"], CYAN),
    ("shield", "Risk-Remediation Agent", "AWS BEDROCK · GITLAB CI/CD",
     "An agent in GitLab CI/CD that fetches CVMS software-risk issues, analyses them and opens merge requests with AI-proposed fixes.",
     [], ["Bedrock", "GitLab CI/CD", "AI Agents"], VIOLET),
    ("code", "AI Code Review System", "BEDROCK · LAMBDA · PROMPTS",
     "Parses merge-request diffs, writes contextual line-level feedback and de-duplicates comments across review cycles.",
     [], ["Bedrock", "Lambda", "Prompt Eng."], PINK),
    ("station", "StationTwin", "METRO DIGITAL TWIN",
     "Real-time 3D twin of metro stations: React + Three.js, GraphQL on AppSync, GenAI summaries every 8 hours, all in AWS CDK.",
     ["▲40% faster 3D loads", "▲50% faster releases", "▼25% latency"], ["React", "Three.js", "AppSync", "CDK"], AMBER),
    ("form", "Customer Onboarding Portal", "REACT · SERVERLESS · DYNAMODB · RDS",
     "Multi-step site-configuration portal with per-stage validation, two-phase storage in DynamoDB and RDS PostgreSQL, and pre-signed S3 uploads for documents and 3D models.",
     [], ["React", "Redux", "Python", "S3", "CDK"], CYAN),
]
MISSIONS_ALT = "Projects: " + " ".join(
    f"{m[1]} ({m[2]}): {m[3]}" + (f" Results: {', '.join(m[4])}." if m[4] else "") for m in MISSIONS
)


def mission_tile(x, y, w, m, s):
    kind, title, sub, desc, stats, tags, color = m
    pad = s["pad"]
    lines = wrap(desc, s["desc"], w - pad * 2)
    tags_svg, tags_h = chips_row(tags, x + pad, 0, w - pad * 2, s["chip"], s["chip_h"], 8)
    head = s["tile"]
    desc_y = y + pad + head + s["desc"] * 1.6
    after = desc_y + (len(lines) - 1) * s["desc"] * 1.4
    parts = [
        "",  # frame placeholder, filled once the height is known
        f'<rect x="{x + 24}" y="{y}" width="{w * 0.35:.0f}" height="2" fill="{color}" opacity=".8"/>',
        icon_tile(kind, x + pad, y + pad, head, color),
        t(x + pad + head + 18, y + pad + head * 0.45, title, s["title"], TEXT, "sans", 700),
        t(x + pad + head + 18, y + pad + head * 0.45 + s["sub"] + 12, sub, s["sub"], color, "mono", 600, spacing=2),
    ]
    for j, line in enumerate(lines):
        parts.append(t(x + pad, desc_y + j * s["desc"] * 1.4, line, s["desc"], "#C9D0F0"))
    if stats:
        sx, sy = x + pad, after + s["desc"] * 0.9
        sh = s["chip_h"] + 6
        for label in stats:
            sw = text_width(label, s["chip"] + 1, mono=True) + 28
            if sx + sw > x + w - pad:
                sx, sy = x + pad, sy + sh + 8
            parts.append(f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="{sh}" rx="10" fill="{GREEN}" fill-opacity=".12" stroke="{GREEN}" stroke-opacity=".5"/>')
            parts.append(t(sx + sw / 2, sy + sh / 2 + (s["chip"] + 1) * 0.36, label, s["chip"] + 1, "#6EE7B7", "mono", 700, "middle"))
            sx += sw + 8
        after = sy + sh - s["desc"] * 0.4
    tags_y = after + s["desc"] * 0.9
    h = tags_y - y + tags_h + pad
    parts.append(f'<g transform="translate(0 {tags_y:.0f})">{tags_svg}</g>')
    return parts, h, (x, y, w, color)


def missions(w, cols, pad, gap, title_size, s):
    top = 72 + title_size + 16 + 40
    full = w - pad * 2
    tile_w = (full - gap * (cols - 1)) / cols
    tiles, y = [], top
    for r in range(0, len(MISSIONS), cols):
        row = MISSIONS[r:r + cols]
        width = tile_w if len(row) > 1 else full  # a lone last tile spans the row
        rendered = [mission_tile(pad + c * (tile_w + gap), y, width, m, s) for c, m in enumerate(row)]
        row_h = max(h for _, h, _ in rendered)
        for parts, _, (tx, ty, tw, color) in rendered:
            parts[0] = f'<rect x="{tx:.1f}" y="{ty:.0f}" width="{tw:.1f}" height="{row_h:.0f}" rx="20" fill="url(#tile)" stroke="{color}" stroke-opacity=".28"/>'
            tiles.append("\n".join(parts))
        y += row_h + gap
    h = int(y - gap + pad * 0.85)
    frame = card_frame(w, h, "02", "MISSION LOG", "Things I've shipped", title_size, pad, label_size=16 if w > 1000 else 22)
    return svg(w, h, MISSIONS_ALT, frame + "\n".join(tiles))


# ---------------------------------------------------------------- loadout

LOADOUT = [
    ("AI / AGENTIC", ["AWS Bedrock", "MCP", "LLMs", "AI Agents", "Tool Calling", "Prompt Eng."], CYAN),
    ("AWS CLOUD", ["Lambda", "S3", "CloudFront", "ECS", "EC2", "API Gateway", "AppSync", "DynamoDB", "RDS"], VIOLET),
    ("DEVOPS", ["AWS CDK", "GitLab CI/CD", "Docker"], PINK),
    ("FRONTEND", ["React", "Redux", "Three.js", "Chakra UI"], AMBER),
    ("BACKEND", ["Python", "FastAPI", "REST", "GraphQL", "MySQL"], CYAN),
    ("LANGUAGES", ["TypeScript", "Python", "Java"], VIOLET),
]
LOADOUT_ALT = "Loadout: " + "; ".join(f"{cat}: {', '.join(items)}" for cat, items, _ in LOADOUT)


def pill(x, y, label, color, size, h):
    w = text_width(label, size) + h * 0.9 + 26
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="url(#tile)" stroke="{color}" stroke-opacity=".4"/>'
        f'<circle cx="{x + h * 0.55:.1f}" cy="{y + h / 2:.1f}" r="{h * 0.14:.1f}" fill="{color}"/>'
        + t(x + h * 0.55 + h * 0.35, y + h / 2 + size * 0.36, label, size, TEXT, "sans", 600)
    ), w


def loadout(w, pad, title_size, stacked, label_size, size, h_pill, gap_row):
    y = 72 + title_size + 16 + 40
    parts = []
    label_w = 0 if stacked else 230
    for cat, items, color in LOADOUT:
        if stacked:
            parts.append(t(pad, y + label_size, cat, label_size, color, "mono", 700, spacing=3))
            y += label_size + 16
        else:
            parts.append(t(pad, y + h_pill / 2 + label_size * 0.36, cat, label_size, color, "mono", 700, spacing=3))
        x, row_y = pad + label_w, y
        for label in items:
            _, pw = pill(0, 0, label, color, size, h_pill)
            if x + pw > w - pad:
                x, row_y = pad + label_w, row_y + h_pill + 12
            s, pw = pill(x, row_y, label, color, size, h_pill)
            parts.append(s)
            x += pw + 12
        y = row_y + h_pill + gap_row
        if not stacked:
            parts.append(f'<path d="M{pad} {y - gap_row / 2:.0f}h{w - pad * 2}" stroke="#FFFFFF" stroke-opacity=".05"/>')
    h = int(y - gap_row + pad * 0.85)
    frame = card_frame(w, h, "03", "LOADOUT", "Tools of the trade", title_size, pad, label_size=16 if w > 1000 else 22)
    return svg(w, h, LOADOUT_ALT, frame + "\n".join(parts))


# ---------------------------------------------------------------- achievements

ACHIEVEMENTS = [
    ("medal", "AWS CERTIFIED DEVELOPER", "Associate (DVA-C02) · valid Nov 2025 – Nov 2028", AMBER),
    ("trophy", "AWS GAMEDAY 2025 · 2ND", "Cloud architecture & operations challenge", CYAN),
    ("trophy", "AWS DEEPRACER 2024 · 3RD", "Reinforcement learning on AWS AI/ML", PINK),
    ("cap", "B.TECH, COMPUTER SCIENCE", "Rajarambapu Institute of Technology · 2023", VIOLET),
]
ACH_ALT = "Achievements: " + " ".join(f"{label}: {text}." for _, label, text, _ in ACHIEVEMENTS)


def achievements(w, cols, pad, title_size, label_size, text_size, tile, gap):
    top = 72 + title_size + 16 + 44
    col_w = (w - pad * 2 - gap * (cols - 1)) / cols
    parts, max_h = [], 0
    per = -(-len(ACHIEVEMENTS) // cols)
    for c in range(cols):
        rows, rh = icon_rows(ACHIEVEMENTS[c * per:(c + 1) * per], pad + c * (col_w + gap), top, col_w, label_size, text_size, tile, gap * 0.6)
        parts.append(rows)
        max_h = max(max_h, rh)
    h = int(top + max_h + pad * 0.85)
    frame = card_frame(w, h, "04", "ACHIEVEMENTS", "Trophy cabinet", title_size, pad, label_size=16 if w > 1000 else 22)
    return svg(w, h, ACH_ALT, frame + "\n".join(parts))


# ---------------------------------------------------------------- snake header & footer

SNAKE_ALT = "05 // Contribution trail — public contributions, eaten by a snake."


def snake_header(w, pad, title_size, sub_size):
    h = 72 + title_size + 16 + sub_size + 46
    body = card_frame(w, h, "05", "CONTRIBUTION TRAIL", "Every commit feeds the snake", title_size, pad, beam=False, label_size=16 if w > 1000 else 22)
    body += t(pad, 72 + title_size + 16 + sub_size + 18, "Public contributions · refreshed daily", sub_size, MUTED, "sans", 500)
    return svg(w, int(h), SNAKE_ALT, body)


QUOTE = "I like systems that run themselves — and ship faster because of it."
FOOTER_ALT = QUOTE + " Open to conversations on AI agents, cloud architecture and dev tooling."


def footer(w, h, quote_size, meta_size, meta):
    lines = wrap(QUOTE, quote_size, w - 120)
    waves = []
    for color, op, amp, base, cls in ((CYAN, 0.18, 18, h - 70, "wave"), (VIOLET, 0.22, 24, h - 50, "wave b"), (PINK, 0.16, 14, h - 30, "wave")):
        d = f"M0 {base}"
        for k in range(0, int(w / 150) + 6):
            d += f" q75 {-amp if k % 2 == 0 else amp} 150 0"
        d += f" V{h} H0Z"
        waves.append(f'<path class="{cls}" d="{d}" fill="{color}" opacity="{op}"/>')
    start = h * 0.4 - (len(lines) - 1) * quote_size * 0.65
    quote = "".join(
        t(w / 2, start + i * quote_size * 1.3, line, quote_size, TEXT, "sans", 500, "middle", extra=' font-style="italic"')
        for i, line in enumerate(lines)
    )
    meta_y = start + (len(lines) - 1) * quote_size * 1.3 + meta_size + 30
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#card)"/>
<ellipse cx="{w / 2}" cy="{h}" rx="{w * 0.45}" ry="{h * 0.7}" fill="url(#glowViolet)" opacity=".7"/>
{stars(w, h, 40, 21, 0.5)}
{''.join(waves)}
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="27.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
{quote}
{t(w / 2, meta_y, meta, meta_size, CYAN, "mono", 600, "middle", 2)}
"""
    return svg(w, h, FOOTER_ALT, body)


# ---------------------------------------------------------------- build

DESKTOP_MISSION = dict(pad=30, tile=54, title=24, sub=13, desc=19, chip=13, chip_h=30)
MOBILE_MISSION = dict(pad=36, tile=72, title=34, sub=20, desc=28, chip=21, chip_h=46)

ASSETS = {
    "hero.svg": hero_desktop,
    "hero-mobile.svg": hero_mobile,
    "about.svg": about_desktop,
    "about-mobile.svg": about_mobile,
    "missions.svg": lambda: missions(1200, 2, 56, 24, 34, DESKTOP_MISSION),
    "missions-mobile.svg": lambda: missions(800, 1, 48, 28, 46, MOBILE_MISSION),
    "loadout.svg": lambda: loadout(1200, 56, 34, False, 15, 18, 42, 22),
    "loadout-mobile.svg": lambda: loadout(800, 48, 46, True, 21, 27, 60, 34),
    "achievements.svg": lambda: achievements(1200, 2, 56, 34, 14, 20, 52, 40),
    "achievements-mobile.svg": lambda: achievements(800, 1, 48, 46, 20, 28, 72, 50),
    "snake-header.svg": lambda: snake_header(1200, 56, 34, 19),
    "snake-header-mobile.svg": lambda: snake_header(800, 48, 46, 28),
    "footer.svg": lambda: footer(1200, 240, 28, 16, "open to talk: AI agents · cloud architecture · dev tooling"),
    "footer-mobile.svg": lambda: footer(800, 340, 38, 24, "AI agents · cloud · dev tooling"),
}
for _kind, _label, _sub, _color, _ in BUTTONS:
    ASSETS[f"btn-{_kind}.svg"] = (lambda k=_kind, l=_label, s=_sub, c=_color: button(k, l, s, c))


def responsive(name, alt):
    return (
        f'<picture>\n  <source media="(max-width: 700px)" srcset="{RAW}/main/assets/ui/{name}-mobile.svg">\n'
        f'  <img src="assets/ui/{name}.svg" width="100%" alt="{escape(alt)}">\n</picture>'
    )


def readme():
    buttons = "\n".join(
        f'<a href="{escape(url)}"><img src="assets/ui/btn-{kind}.svg" width="32%" alt="{escape(label.title())} — {escape(sub)}"></a>'
        for kind, label, sub, _, url in BUTTONS
    )
    snake = (
        f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{RAW}/output/github-snake-dark.svg">\n'
        f'  <img src="{RAW}/output/github-snake.svg" width="100%" alt="Contribution snake eating the public contribution grid">\n</picture>'
    )
    parts = [
        "<!-- Generated by tools/build_profile_ui.py; edit that script, then re-run it. -->",
        '<div align="center">',
        responsive("hero", HERO_ALT),
        buttons,
        responsive("about", ABOUT_ALT),
        responsive("missions", MISSIONS_ALT),
        responsive("loadout", LOADOUT_ALT),
        responsive("achievements", ACH_ALT),
        responsive("snake-header", SNAKE_ALT),
        snake,
        responsive("footer", FOOTER_ALT),
        f'<a href="{LINKEDIN}">LinkedIn</a> · <a href="mailto:{EMAIL}">{EMAIL}</a>',
        "</div>",
    ]
    return "\n\n".join(parts) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in ASSETS.items():
        (OUT / name).write_text(build(), encoding="utf-8", newline="\n")
        print("wrote", (OUT / name).relative_to(ROOT))
    (ROOT / "README.md").write_text(readme(), encoding="utf-8", newline="\n")
    print("wrote README.md")


if __name__ == "__main__":
    main()
