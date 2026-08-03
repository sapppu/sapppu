#!/usr/bin/env python3
"""Hand-author a neofetch-style info-card.svg that fades/slides in line by line."""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")
STATIC = os.environ.get("STATIC", "") == "1"

W, H = 490, 340
PAD = 22
TITLEBAR_H = 30
BG, BG2 = "#0a0e14", "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
KEY = "#58a6ff"
ACCENT = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"
PINK = "#f778ba"

# (key, value, value_color)
ROWS = [
    ("OS", "MCA · MIT World Peace University, Pune", TEXT),
    ("Host", "sapppu", ACCENT),
    ("Now", "Full-stack · Distributed systems · Agentic AI", GREEN),
    ("Focus", "Transaction isolation · LLM tool-use patterns", TEXT),
    ("Stack", "Java · Spring Boot · React · TypeScript · PG", KEY),
    ("Also", "Python · NestJS · C++ · IoT (Pi / ESP32)", MUTED),
    ("Highlight", "National Finalist — La Trobe × Cisco 2026", GOLD),
    ("Highlight", "Runner-Up — Savoir Faire Hackathon 2024", GOLD),
    ("Ship", "SQL Playground — hand-written Java query engine", PINK),
]


def fade(i):
    if STATIC:
        return ""
    delay = 0.18 + i * 0.11
    return (
        f' opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.2f}s" dur="0.40s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 8" to="0 0" begin="{delay:.2f}s" dur="0.40s" fill="freeze"/>'
    )


def main():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs>'
        f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f'</linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" '
        f'stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(
            f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>'
        )
    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{MUTED}" font-size="12" '
        f'text-anchor="middle">swapnaj@github: ~/whoami</text>'
    )

    # title block
    y0 = TITLEBAR_H + 28
    anim0 = fade(0)
    if STATIC:
        parts.append(
            f'<text x="{PAD}" y="{y0}" fill="{TEXT}" font-size="16" font-weight="700">'
            f'Swapnaj Tolnure</text>'
        )
        parts.append(
            f'<text x="{PAD}" y="{y0 + 18}" fill="{MUTED}" font-size="11">'
            f'--------------</text>'
        )
    else:
        parts.append(
            f'<g{anim0}>'
            f'<text x="{PAD}" y="{y0}" fill="{TEXT}" font-size="16" font-weight="700">'
            f'Swapnaj Tolnure</text>'
            f'<text x="{PAD}" y="{y0 + 18}" fill="{MUTED}" font-size="11">'
            f'--------------</text></g>'
        )

    key_w = 78
    row_y = y0 + 42
    for i, (key, val, color) in enumerate(ROWS):
        anim = fade(i + 1)
        if STATIC:
            parts.append(
                f'<text x="{PAD}" y="{row_y}" fill="{KEY}" font-size="12" '
                f'font-weight="600">{key}</text>'
                f'<text x="{PAD + key_w}" y="{row_y}" fill="{MUTED}" font-size="12">:</text>'
                f'<text x="{PAD + key_w + 14}" y="{row_y}" fill="{color}" font-size="12">{val}</text>'
            )
        else:
            parts.append(
                f'<g{anim}>'
                f'<text x="{PAD}" y="{row_y}" fill="{KEY}" font-size="12" '
                f'font-weight="600">{key}</text>'
                f'<text x="{PAD + key_w}" y="{row_y}" fill="{MUTED}" font-size="12">:</text>'
                f'<text x="{PAD + key_w + 14}" y="{row_y}" fill="{color}" font-size="12">{val}</text>'
                f'</g>'
            )
        row_y += 22

    # footer links hint
    anim_f = fade(len(ROWS) + 1)
    foot_y = H - 18
    if STATIC:
        parts.append(
            f'<text x="{PAD}" y="{foot_y}" fill="{MUTED}" font-size="10">'
            f'email · linkedin · github</text>'
        )
    else:
        parts.append(
            f'<g{anim_f}>'
            f'<text x="{PAD}" y="{foot_y}" fill="{MUTED}" font-size="10">'
            f'email · linkedin · github</text></g>'
        )

    parts.append("</svg>")
    svg = "".join(parts)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
