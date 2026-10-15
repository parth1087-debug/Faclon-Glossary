"""Inline SVG for the IT-OT Integration reference architecture.

architecture() returns one <svg> drawn from the cloud tenancy (top) down to the
field areas (bottom), with the Faclon platforms placed as in the Example
Architecture for Industrial AI: I/O Connect (plus optional edge UDF and
Deepsense) in the industrial DMZ, and I/O Sense, Bruce, Ontology, Deepsense,
UDF, Foundry and Forge on the platform bus in the customer's tenancy.
Colours come from CSS classes prefixed `a-` defined in build_page.py.
"""
from html import escape as E

W = 1200
X0, X1 = 166, 1188          # content area (left column holds band labels)
CW = X1 - X0


def t(x, y, s, cls="", anchor="middle"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{E(s)}</text>'


def box(x, y, w, h, title, lines=(), cls="a-box", tcls="a-tt", badge=None, bcls="a-core", lh=15, rx=10):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>']
    n = len(lines) + 1 + (1 if badge else 0)
    top = y + h / 2 - (n - 1) * lh / 2 + 4
    out.append(t(x + w / 2, top, title, tcls))
    for i, l in enumerate(lines):
        out.append(t(x + w / 2, top + (i + 1) * lh, l, "a-sm"))
    if badge:
        by = top + (len(lines) + 1) * lh - 10
        bw = len(badge) * 6.6 + 14
        out.append(f'<rect x="{x + w / 2 - bw / 2}" y="{by}" width="{bw}" height="15" rx="7.5" class="{bcls}"/>')
        out.append(t(x + w / 2, by + 11, badge, "a-badge"))
    return "".join(out)


def band(y, h, label, sub=None, cls="a-band"):
    out = [f'<rect x="10" y="{y}" width="{W - 20}" height="{h}" rx="14" class="{cls}"/>']
    ly = y + 26
    for i, part in enumerate(label):
        out.append(t(26, ly + i * 15, part, "a-eb", "start"))
    if sub:
        out.append(t(26, ly + len(label) * 15 + 4, sub, "a-lv", "start"))
    return "".join(out)


def vline(x, y1, y2, cls="a-ln"):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="{cls}"/>'


def up(x, y1, y2, cls="a-up"):
    """Arrow pointing up from y1 (bottom) to y2 (top)."""
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 + 7}" class="{cls}"/>'
            f'<path d="M{x - 5} {y2 + 9} L{x} {y2} L{x + 5} {y2 + 9}Z" class="{cls}h"/>')


def conn(y1, y2, text, xs=None, arrow=True, left=False):
    xm = (y1 + y2) / 2
    out = []
    xs = xs or [X0 + CW / 2]
    for x in xs:
        out.append(up(x, y2, y1) if arrow else vline(x, y1, y2))
    if left:
        out.append(t(xs[0] - 14, xm + 4, text, "a-cn", "end"))
    else:
        out.append(t(xs[0] + 14, xm + 4, text, "a-cn", "start"))
    return "".join(out)


def row(y, h, items, gap=10, x0=X0, width=CW):
    n = len(items)
    w = (width - gap * (n - 1)) / n
    return [(x0 + i * (w + gap), y, w, h, it) for i, it in enumerate(items)]


def architecture():
    s = []
    # ---------- consumers ----------
    s.append(band(10, 162, ["CONSUMERS", "PULL ONLY"], None, "a-band a-cons"))
    roles = ["Users", "AI agents", "Consultants · SMEs", "Citizen data scientists", "Administrators", "Developers"]
    for x, y, w, h, r in row(30, 40, roles):
        cls = "a-pill a-dash" if r == "AI agents" else "a-pill"
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" class="{cls}"/>')
        s.append(t(x + w / 2, y + 25, r, "a-tt a-ag" if r == "AI agents" else "a-tt"))
    apps = ["ERP", "MES", "LIMS", "Data platforms", "Frontier models", "Other enterprise apps"]
    s.append(t(X0, 96, "THIRD-PARTY SOFTWARE, MODELS & SERVICES · NO ENTERPRISE DATA IS COLLECTED INTO THE PLATFORM", "a-mini", "start"))
    for x, y, w, h, a in row(106, 46, apps):
        s.append(box(x, y, w, h, a, ["Pulls plant data"], "a-box", "a-tt"))

    s.append(conn(172, 204, "Consumers pull through the UDF API (HTTPS · OAuth2 · read-only scopes) and the Bruce MCP Gateway (read-only tools)", [X0 + 40, X1 - 40]))

    # ---------- L5 cloud ----------
    s.append(band(204, 252, ["CUSTOMER'S", "CLOUD", "TENANCY"], "Level 5", "a-band a-l5"))
    s.append(t(X0, 228, "FACLON PLATFORMS · ANY PUBLIC CLOUD OR ON-PREMISE, INSIDE THE CUSTOMER'S OWN TENANCY", "a-mini a-mb", "start"))
    plats = [
        ("I/O Sense", ["Dashboards · apps", "Prompt-to-dashboard"], "a-p-green", "CORE"),
        ("Bruce", ["Agent factory", "MCP Gateway"], "a-p-purple a-dash2", "OPTIONAL"),
        ("Ontology", ["Asset model", "Tag metadata"], "a-p-navy a-dash2", "OPTIONAL"),
        ("Deepsense", ["Custom ML / AI", "models"], "a-p-purple a-dash2", "OPTIONAL"),
        ("UDF", ["Ingestion · mTLS", "System of record · API"], "a-p-blue", "CORE"),
        ("Foundry", ["SSO · users", "Roles · access"], "a-p-dark", "CORE"),
        ("Forge", ["Deploys and runs", "the platforms"], "a-p-dark", "CORE"),
    ]
    udf_x = None
    for x, y, w, h, p in row(240, 104, plats):
        name, lines, cls, badge = p
        if name == "UDF":
            udf_x = x + w / 2
        s.append(box(x, y, w, h, name, lines, "a-plat " + cls, "a-pt",
                     badge, "a-core" if badge == "CORE" else "a-opt", lh=16))
        s.append(vline(x + w / 2, y + h, 358, "a-bl"))
    s.append(f'<rect x="{X0}" y="358" width="{CW}" height="26" rx="5" class="a-bus"/>')
    s.append(t(X0 + CW / 2, 375, "FACLON PLATFORM BUS · PLATFORMS CONNECTED INTERNALLY", "a-bust"))
    s.append(f'<rect x="{X0}" y="396" width="{CW}" height="46" rx="10" class="a-ctl"/>')
    s.append(t(X0 + 16, 415, "TENANCY CONTROLS (CUSTOMER-OWNED)", "a-mini", "start"))
    s.append(t(X0 + 16, 432, "Private network · no public IPs · key vault · SSO through Foundry · role-based access · India region · backup + DR · platform logs → customer SIEM", "a-sm", "start"))

    s.append(conn(456, 494, "Private link · site-to-site IPsec or dedicated cloud interconnect · outbound only into UDF ingestion", [udf_x], left=True))

    # ---------- L4 IT ----------
    s.append(band(494, 112, ["ENTERPRISE", "IT"], "Level 4", "a-band"))
    it = [("Perimeter firewall", ["Outbound only to the tenancy", "Cloud never initiates inbound"]),
          ("VPN server", ["MFA · OT pool", "Vendor pool"]),
          ("IT core switch", ["Routes IDMZ subnets", "→ North FW"]),
          ("IT services (existing)", ["Directory · SIEM · NTP", "Patch / AV · identity provider"])]
    itc = []
    for x, y, w, h, b in row(512, 76, it, 14):
        cls = "a-fw" if "firewall" in b[0] else "a-box"
        s.append(box(x, y, w, h, b[0], b[1], cls))
        itc.append(x + w / 2)
    core_x = itc[2]
    s.append(conn(606, 640, "Default → IT core · no routes to field subnets", [core_x]))

    # ---------- L3.5 IDMZ ----------
    s.append(band(640, 352, ["INDUSTRIAL", "DMZ"], "Level 3.5", "a-band a-dmz"))
    s.append(box(X0, 656, CW, 44, "North firewall  ·  HA pair optional", ["Connected: VLAN 11 · 12 · 13 · 14 · default → IT core · no routes to field subnets"], "a-fw", lh=15))
    s.append(vline(X0 + CW / 2, 700, 722, "a-tr"))
    s.append(t(X0 + CW / 2 + 10, 715, "Trunk 11 · 12 · 13 · 14", "a-cn", "start"))
    s.append(box(X0, 722, CW, 34, "IDMZ switch  ·  Layer 2 only · no SVI · VLAN 11 · 12 · 13 · 14", [], "a-sw"))
    srv = [("I/O Connect", ["VLAN 11 · collector + buffer", "Store-and-forward ≥ 7 days", "Uplink → UDF ingestion"], "a-ioc", "CORE", "a-core"),
           ("UDF · Deepsense (edge)", ["VLAN 11 · local data and", "model serving · reads", "I/O Connect only"], "a-plat a-p-blue a-dash2", "OPTIONAL", "a-opt"),
           ("Jump server (PAM)", ["VLAN 12 · MFA · recorded", "Static: field → South FW"], "a-box", None, None),
           ("Firewall manager", ["VLAN 13 · policy · backup", "Collects South FW logs"], "a-box", None, None),
           ("IDMZ services", ["VLAN 14 · NTP · patch / AV", "relay · syslog forwarder"], "a-box", "ADDED", "a-add")]
    xs = []
    for x, y, w, h, b in row(780, 116, srv):
        s.append(vline(x + w / 2, 756, 780, "a-ln"))
        s.append(box(x, y, w, h, b[0], b[1], b[2], "a-pt" if "plat" in b[2] or "ioc" in b[2] else "a-tt", b[3], b[4] or "a-core", lh=15))
        xs.append(x + w / 2)
    s.append(vline(X0 + CW / 2, 896, 932, "a-tr"))
    s.append(t(X0 + CW / 2 + 10, 917, "Trunk 11 · 12 · 13 (I/O Connect, jump, management)", "a-cn", "start"))
    s.append(box(X0, 932, CW, 46, "South firewall  ·  HA pair optional", ["No default route · no static routes · SNAT to FW identities · field VLANs 101 · 201–2nn · 301–303 (translated)"], "a-fw", lh=15))

    s.append(conn(992, 1024, "Trunk: field VLANs only · native unused", None, arrow=False))

    # ---------- L3 aggregation ----------
    s.append(band(1024, 104, ["OT", "AGGREGATION"], "Level 3", "a-band"))
    s.append(box(X0, 1040, CW, 34, "Master L2 switch (termination)  ·  all field VLANs · stack / HA optional", [], "a-sw"))
    s.append(box(X0, 1082, CW, 34, "Common fibre (OFC) termination  ·  master LIU", [], "a-box"))

    # ---------- L0-2 field ----------
    fy = 1162
    s.append(band(fy, 330, ["FIELD", "AREAS"], "Level 0–2", "a-band a-field"))
    groups = [
        ("ELECTRICAL ROOMS", [("ER-1", "Managed L2 switch", "VLAN 101 · no NAT", "Energy meters", ["Modbus RTU", "RS-485"]),
                              ("ER-n", "Managed L2 switch", "VLAN 101 · no NAT", "Energy meters", ["Modbus RTU", "RS-485"])]),
        ("MACHINE LINES (SHOPFLOOR)", [("Line-1", "NAT switch", "VLAN 201 · 1:1 NAT", "PLC · DCS", ["or OPC server", "Existing subnet"]),
                                       ("Line-2", "NAT switch", "VLAN 202 · 1:1 NAT", "PLC · DCS", ["or OPC server", "Existing subnet"]),
                                       ("Line-n", "NAT switch", "VLAN 2nn · 1:1 NAT", "PLC · DCS", ["or OPC server", "Existing subnet"])]),
        ("UTILITY SECTIONS", [("Utility PLCs", "NAT switch", "VLAN 301 · 1:1 NAT", "Controllers", ["Chillers · DGs", "WTP · ETP · air"]),
                              ("Utility meters", "NAT switch", "VLAN 302 · 1:1 NAT", "Meters", ["Flow · air", "BTU"]),
                              ("Boiler & turbine", "NAT switch", "VLAN 303 · 1:1 NAT", "DCS", ["Boiler · turbine", "OPC server"])]),
    ]
    ggap, cgap = 22, 8
    ncol = sum(len(g[1]) for g in groups)
    cw = (CW - ggap * (len(groups) - 1) - cgap * (ncol - len(groups))) / ncol
    x = X0
    heads = []
    for gname, cols in groups:
        gw = len(cols) * cw + (len(cols) - 1) * cgap
        heads.append(t(x, fy + 24, gname, "a-mini a-mb a-halo", "start"))
        for c in cols:
            cx = x + cw / 2
            s.append(vline(cx, 1116, fy + 36, "a-of"))
            s.append(box(x, fy + 36, cw, 22, "LIU", [], "a-liu", "a-sm"))
            s.append(vline(cx, fy + 58, fy + 70, "a-ln"))
            s.append(box(x, fy + 70, cw, 62, c[0], [c[1], c[2]], "a-sw", lh=15))
            s.append(vline(cx, fy + 132, fy + 146, "a-ln"))
            s.append(box(x, fy + 146, cw, 62, "Converter", ["Only if needed", "Serial / bus → TCP"], "a-box a-dash", lh=15))
            s.append(vline(cx, fy + 208, fy + 222, "a-ln"))
            s.append(box(x, fy + 222, cw, 64, c[3], c[4], "a-dev", lh=15))
            x += cw + cgap
        x += ggap - cgap
    s.extend(heads)
    s.append(t(X0, fy + 312, "Existing field devices unchanged · OFC star · armoured single-mode fibre · ≥ 2 spare cores per run · read-only acquisition", "a-sm", "start"))
    H = fy + 330 + 10
    return (f'<svg class="ad" viewBox="0 0 {W} {H}" role="img" aria-label="IT-OT integration reference architecture '
            f'from field areas through OT aggregation, industrial DMZ and enterprise IT to the Faclon platforms in the cloud tenancy">'
            + "".join(s) + "</svg>")


if __name__ == "__main__":
    print(architecture()[:200])
