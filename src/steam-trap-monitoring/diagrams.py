"""Inline SVG architecture diagrams for the steam trap page (redrawn from the deck's
architecture, header trap and heat exchanger installation slides).

Each function returns one <svg>. Styling comes from the .dg rules in build_page.py CSS,
so the diagrams share the page's colours and Inter type. Edit coordinates here and re-run
build_page.py.
"""

DEFS = """<defs>
<marker id="{p}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#3D63F5"/></marker>
<marker id="{p}o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#E0701B"/></marker>
<marker id="{p}g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#6B7A90"/></marker>
</defs>"""


def t(x, y, s, cls="", anchor="start"):
    lines = s.split("\n")
    if len(lines) == 1:
        return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{s}</text>'
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else 1.25}em">{l}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{spans}</text>'


def node(x, y, label=True):
    """Flameproof LoRa node: round enclosure with antenna. (x, y) = centre."""
    return (f'<g class="node"><line x1="{x + 14}" y1="{y - 18}" x2="{x + 22}" y2="{y - 62}" class="ant"/>'
            f'<rect x="{x - 26}" y="{y - 22}" width="52" height="44" rx="10" class="nbox"/>'
            f'<circle cx="{x}" cy="{y}" r="13" class="nface"/>'
            + (t(x, y + 40, "Steam trap node", "lbl b", "middle") if label else "") + "</g>")


def gateway(x, y, w=92, h=64):
    return (f'<g><line x1="{x}" y1="{y - h / 2}" x2="{x}" y2="{y - h / 2 - 34}" class="ant"/>'
            f'<path d="M{x - 9} {y - h / 2 - 28} q9 -9 18 0 M{x - 15} {y - h / 2 - 34} q15 -14 30 0" class="wave"/>'
            f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" class="gbox"/>'
            f'{t(x, y - 2, "LoRa", "gt", "middle")}{t(x, y + 15, "gateway", "gt s", "middle")}</g>')


def cloud(x, y, title="I/O Sense Cloud", sub="Analytics · Automation · AI", w=210, h=86):
    return (f'<g><rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="16" class="cbox"/>'
            f'{t(x, y - 4, title, "ct", "middle")}{t(x, y + 18, sub, "cs", "middle")}</g>')


def trap(x, y, s=1.0):
    """Trap body on a horizontal pipe at (x, y)."""
    return (f'<g class="trap"><rect x="{x - 22 * s}" y="{y - 12 * s}" width="{44 * s}" height="{24 * s}" rx="{7 * s}"/>'
            f'<rect x="{x - 9 * s}" y="{y - 22 * s}" width="{18 * s}" height="{12 * s}" rx="3"/>'
            f'<line x1="{x - 30 * s}" y1="{y - 14 * s}" x2="{x - 30 * s}" y2="{y + 14 * s}"/>'
            f'<line x1="{x + 30 * s}" y1="{y - 14 * s}" x2="{x + 30 * s}" y2="{y + 14 * s}"/></g>')


def valve(x, y, vertical=False):
    if vertical:
        return (f'<g class="valve"><path d="M{x - 10} {y - 12} L{x + 10} {y - 12} L{x - 10} {y + 12} L{x + 10} {y + 12} Z"/>'
                f'<line x1="{x}" y1="{y}" x2="{x + 20}" y2="{y}"/><line x1="{x + 20}" y1="{y - 8}" x2="{x + 20}" y2="{y + 8}" class="hdl"/></g>')
    return (f'<g class="valve"><path d="M{x - 12} {y - 10} L{x - 12} {y + 10} L{x + 12} {y - 10} L{x + 12} {y + 10} Z"/>'
            f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 20}"/><line x1="{x - 9}" y1="{y - 20}" x2="{x + 9}" y2="{y - 20}" class="hdl"/></g>')


def diamond(x, y, r=11):
    return f'<path d="M{x} {y - r} L{x + r} {y} L{x} {y + r} L{x - r} {y} Z" class="tag"/>'


def lora(x1, y1, x2, y2, p):
    return f'<path d="M{x1} {y1} L{x2} {y2}" class="radio" marker-end="url(#{p}o)"/>'


def svg(p, w, h, body, label):
    return (f'<svg class="dg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">{DEFS.format(p=p)}{body}</svg>')


# ---------------------------------------------------------------------------
def architecture():
    p = "ar"
    b = []
    # trap + node rows
    rows = [80, 190, 360]
    for y in rows:
        b.append(f'<line x1="30" y1="{y + 24}" x2="190" y2="{y + 24}" class="pipe"/>')
        b.append(trap(110, y + 24, .85))
        b.append(f'<path d="M92 {y + 12} C92 {y - 14} 196 {y - 14} 232 {y - 2}" class="lead li"/>')
        b.append(f'<path d="M128 {y + 12} C128 {y - 4} 196 {y + 4} 232 {y + 6}" class="lead lo"/>')
        b.append(node(260, y, label=False))
    b.append(t(260, 290, "· · ·", "dots", "middle"))
    b.append(t(110, 290, "Up to 30 traps\nper gateway", "lbl", "middle"))
    b.append(t(30, 22, "STEAM TRAP HEADER", "eb"))
    b.append(t(330, 22, "STEAM TRAP NODE", "eb"))
    gx, gy = 520, 220
    for y in rows:
        b.append(lora(292, y - 6, gx - 52, gy - 6 + (y - 190) * .08, p))
    b.append(t(400, 108, "Wireless LoRa", "lbl o b", "middle"))
    b.append(t(400, 126, "up to 1,000 m", "lbl", "middle"))
    b.append(gateway(gx, gy))
    b.append(t(gx, gy + 56, "Gateway", "lbl b", "middle"))
    b.append(t(gx, gy + 73, "4G uplink · local buffer", "lbl", "middle"))
    cx, cy = 790, 220
    b.append(f'<line x1="{gx + 50}" y1="{gy}" x2="{cx - 110}" y2="{cy}" class="flow" marker-end="url(#{p}a)"/>')
    b.append(t((gx + cx - 60) / 2, gy - 12, "4G", "lbl a b", "middle"))
    b.append(cloud(cx, cy))
    # optional DCS
    b.append(f'<rect x="{cx - 150}" y="22" width="300" height="88" rx="12" class="opt"/>')
    b.append(t(cx, 46, "Key process parameters", "lbl b", "middle"))
    b.append(t(cx, 66, "Control valve · header pressure · header temperature", "lbl", "middle"))
    b.append(t(cx, 83, "steam flow · condensate temperature", "lbl", "middle"))
    b.append(t(cx, 101, "OPTIONAL", "eb a", "middle"))
    b.append(f'<line x1="{cx}" y1="112" x2="{cx}" y2="{cy - 46}" class="flow dash" marker-end="url(#{p}a)"/>')
    b.append(t(cx + 8, 148, "DCS / Historian / API", "lbl a", "start"))
    b.append(t(cx + 8, 164, "not mandatory", "lbl", "start"))
    # outputs
    outs = ["Failure diagnostics & status", "Steam loss & saving", "SMS & email alerts", "Excel reports & maintenance log"]
    b.append(f'<line x1="{cx}" y1="{cy + 44}" x2="{cx}" y2="{cy + 76}" class="flow" marker-end="url(#{p}a)"/>')
    for i, o in enumerate(outs):
        x = cx - 200 + (i % 2) * 205
        y = cy + 82 + (i // 2) * 44
        b.append(f'<rect x="{x}" y="{y}" width="195" height="36" rx="9" class="out"/>')
        b.append(t(x + 97.5, y + 23, o, "lbl", "middle"))
    return svg(p, 1000, 420, "".join(b),
               "Steam trap nodes send inlet and outlet temperatures over LoRa to a gateway, "
               "which sends them over 4G to the I/O Sense cloud; DCS data is optional.")


# ---------------------------------------------------------------------------
def header_install():
    p = "hd"
    b = []
    # main header
    b.append('<rect x="20" y="40" width="640" height="46" rx="4" class="hdr"/>')
    b.append(t(150, 69, "Main steam pipe header  →", "hl"))
    # well + insulated drop leg
    b.append('<rect x="44" y="86" width="48" height="40" class="well"/>')
    b.append(t(68, 112, "Well", "lbl", "middle"))
    b.append('<path d="M60 126 V330 H600" class="insul"/>')
    b.append('<path d="M60 126 V330 H600" class="pipe"/>')
    b.append(t(72, 200, "Insulation", "lbl"))
    b.append(f'<line x1="68" y1="214" x2="68" y2="244" class="flow g" marker-end="url(#{p}g)"/>')
    # bypass
    b.append('<path d="M60 330 V392 H520 V330" class="pipe thin"/>')
    b.append(valve(250, 392))
    b.append(t(250, 418, "Bypass", "lbl", "middle"))
    # main run
    b.append(valve(150, 330))
    b.append(trap(330, 330))
    b.append(f'<line x1="600" y1="330" x2="640" y2="330" class="pipe" marker-end="url(#{p}g)"/>')
    b.append(t(552, 360, "To environment or\ncondensate recovery line", "lbl"))
    # RTDs
    b.append('<rect x="268" y="320" width="8" height="20" class="rtd ri"/>')
    b.append('<rect x="384" y="320" width="8" height="20" class="rtd ro"/>')
    b.append(t(272, 366, "Inlet RTD", "lbl o b", "middle"))
    b.append(t(388, 366, "Outlet RTD", "lbl bl b", "middle"))
    # support pillar + node
    b.append('<rect x="568" y="96" width="28" height="216" rx="3" class="pillar"/>')
    b.append(t(582, 220, "Support pillar", "lbl v", "middle"))
    b.append('<path d="M272 320 C272 250 400 210 476 206" class="lead li"/>')
    b.append('<path d="M388 320 C388 270 440 236 476 222" class="lead lo"/>')
    b.append(node(516, 214, label=False))
    b.append(t(516, 258, "Steam trap", "lbl b", "middle"))
    b.append(t(516, 274, "monitoring LoRa node", "lbl b", "middle"))
    # plant + gateway
    b.append('<path d="M760 420 V250 H810 V200 H880 V250 H930 V420" class="bldg"/>')
    b.append('<path d="M790 270 h20 M790 300 h20 M790 330 h20 M850 220 h20 M850 270 h20 M850 300 h20 M850 330 h20 M900 270 h20 M900 300 h20" class="win"/>')
    b.append(f'<line x1="845" y1="200" x2="845" y2="160" class="mast"/>')
    b.append(gateway(845, 124, 84, 56))
    b.append(t(950, 230, "4G LoRa gateway at\nheight, in the open", "lbl"))
    b.append(lora(544, 196, 798, 124, p))
    b.append(t(690, 128, "Wireless LoRa", "lbl o b", "middle"))
    b.append(t(690, 146, "up to 1,000 m", "lbl", "middle"))
    b.append(f'<line x1="890" y1="110" x2="956" y2="70" class="flow" marker-end="url(#{p}a)"/>')
    b.append(t(918, 76, "4G", "lbl a b", "end"))
    b.append(cloud(1010, 52, "Faclon Cloud", "I/O Sense", 120, 64))
    return svg(p, 1080, 440, "".join(b),
               "Header trap installation: inlet and outlet RTDs either side of the trap, a LoRa node on the support "
               "pillar, and a 4G gateway installed at height sending data to the Faclon cloud.")


# ---------------------------------------------------------------------------
def hx_install():
    p = "hx"
    b = []
    # steam header with tags
    b.append('<line x1="20" y1="120" x2="790" y2="120" class="pipe hdrl"/>')
    b.append(t(24, 106, "Steam header", "lbl b"))
    b.append(diamond(470, 120))
    b.append(t(470, 92, "Header pressure", "lbl", "middle"))
    b.append(t(470, 76, "e.g. 15 bar", "lbl m", "middle"))
    b.append(diamond(640, 120))
    b.append(t(640, 92, "Header temperature", "lbl", "middle"))
    b.append(t(640, 76, "e.g. 230 °C", "lbl m", "middle"))
    # control valve + HX
    b.append('<line x1="190" y1="120" x2="190" y2="228" class="pipe"/>')
    b.append(valve(190, 170, vertical=True))
    b.append('<rect x="120" y="228" width="140" height="84" rx="10" class="hx"/>')
    b.append('<path d="M140 248 h20 v44 h20 v-44 h20 v44 h20 v-44 h20" class="coil"/>')
    b.append(t(172, 334, "Heat exchanger", "lbl b", "middle"))
    b.append(diamond(76, 270))
    b.append(t(76, 300, "Process\ntemperature\nsensor", "lbl", "middle"))
    # condensate line
    b.append('<path d="M240 312 V400 H880" class="pipe"/>')
    b.append(f'<line x1="880" y1="400" x2="930" y2="400" class="pipe" marker-end="url(#{p}g)"/>')
    b.append(t(940, 396, "Condensate\nrecovery line", "lbl"))
    b.append(diamond(420, 400))
    b.append(trap(540, 400))
    b.append(diamond(660, 400))
    b.append(t(420, 432, "Inlet temperature", "lbl o b", "middle"))
    b.append(t(660, 432, "Outlet temperature", "lbl bl b", "middle"))
    # node
    b.append('<path d="M420 389 C420 330 470 300 512 296" class="lead li"/>')
    b.append('<path d="M660 389 C660 330 610 300 568 296" class="lead lo"/>')
    b.append(node(540, 296, label=False))
    b.append(t(504, 300, "Steam trap node", "lbl b", "end"))
    # control valve position -> DCS -> IPC -> cloud
    b.append(f'<path d="M214 170 H340" class="data" marker-end="url(#{p}o)"/>')
    b.append(t(222, 150, "Control valve position", "lbl o"))
    b.append('<rect x="344" y="150" width="150" height="40" rx="10" class="sys"/>')
    b.append(t(419, 175, "DCS / Historian", "lbl b", "middle"))
    b.append(f'<path d="M494 170 H640" class="data" marker-end="url(#{p}o)"/>')
    b.append('<rect x="644" y="150" width="130" height="40" rx="10" class="sys"/>')
    b.append(t(709, 175, "Industrial PC", "lbl b", "middle"))
    # gateway + cloud
    b.append(gateway(870, 290, 84, 56))
    b.append(t(870, 340, "Gateway at height,", "lbl", "middle"))
    b.append(t(870, 356, "open location", "lbl", "middle"))
    b.append(lora(570, 284, 822, 288, p))
    b.append(t(700, 274, "Wireless LoRa · up to 1,000 m", "lbl o", "middle"))
    b.append(cloud(960, 50, "Faclon Cloud", "I/O Sense", 130, 64))
    b.append(f'<path d="M774 160 C840 150 880 110 905 80" class="flow" marker-end="url(#{p}a)"/>')
    b.append(f'<path d="M900 230 C930 180 950 130 958 86" class="flow" marker-end="url(#{p}a)"/>')
    b.append(t(828, 108, "4G", "lbl a b"))
    b.append(t(946, 168, "4G", "lbl a b"))
    return svg(p, 1060, 450, "".join(b),
               "Heat exchanger installation: trap inlet and outlet sensors feed a LoRa node and gateway; control "
               "valve position goes from the DCS or historian through an industrial PC; both reach the Faclon cloud over 4G.")
