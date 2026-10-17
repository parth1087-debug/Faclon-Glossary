"""Builds readme/index.html: the Read me guide to the site (presenting, downloads, uploads,
design skill, Claude connector, accounts).

Run from anywhere:  python3 src/readme/build_page.py   (then protect.py as usual)

The Read me is a guide, not a solution: protect.py encrypts it with the landing-page key so every
signed-in user can open it, leaves it out of the solution list, the User Manager and the vaults,
and never renders a PDF of it. The site's Download button is hidden on it and offline HTML files
leave it out (see GUIDES in auth_core.js and protect.py). Linked from the landing page's top menu.
"""
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "readme" / "index.html"
E = html.escape

ICON = {  # 24px line icons, inline SVG (stroke = currentColor)
    "present": '<path d="M3 4h18v12H3z"/><path d="M8 20h8M12 16v4"/><path d="m10 8 4 2-4 2z"/>',
    "share": '<path d="M14 3h7v7"/><path d="M10 14 21 3"/><path d="M21 14v7H3V3h7"/>',
    "build": '<path d="m14.7 6.3 3 3"/><path d="M4 20l4.5-1 11-11a2.1 2.1 0 0 0-3-3l-11 11z"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'


def steps(items):
    return '<ol class="steps">' + "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in items) + "</ol>"


def tips(items):
    return '<ul class="tips">' + "".join(f"<li>{t}</li>" for t in items) + "</ul>"


SECTIONS = [("start", "Start here"), ("present", "Presenting"), ("downloads", "Downloads"), ("upload", "Uploading"),
            ("skill", "Design skill"), ("connector", "Claude connector"), ("access", "Accounts"), ("rules", "Good practice")]

KEYS = [(["→", "↓", "Page Down", "Space"], "Next section"), (["←", "↑", "Page Up"], "Previous section"),
        (["Home", "End"], "First or last section"), (["F"], "Full screen on or off"), (["Esc"], "Leave full screen")]

ROLES = [
    ("User", "Opens the solutions the admin has ticked for them. Can present them and use the Read me.", ""),
    ("Can download", "Also gets the Download button: a PDF of a page, or one HTML file of chosen solutions.", "Set per user, and per solution in Solution access."),
    ("Contributor", "Also gets the Upload button and the Claude connector, and sees every uploaded page.", "Contributors upload straight to the live site, so give this only to people you trust."),
    ("Super user", "Sees every solution, including new ones, without being ticked for each.", ""),
    ("Admin", "Runs the User Manager: users, passwords, rights, solution access, renames and versions.", "Manage users button in the bar."),
]

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Read me · Faclon Labs</title>
<meta name="description" content="How to use the Faclon Labs solutions site: presenting, downloads, uploads, the design skill and the Claude connector.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--blue:#3D63F5;--blue2:#7C95FF;
--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#B7791F;--amberBg:#FDF3E1;--red:#C0392B;--redBg:#FCECEA;color-scheme:light}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{background:#fff;scroll-behavior:smooth}}
body{{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}}
table{{font-variant-numeric:tabular-nums}}
.wrap{{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}}
h1,h2,h3{{letter-spacing:-.015em;line-height:1.2}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}}
a{{color:var(--blue)}}
.hero{{background:var(--navy);color:#fff;position:relative;overflow:hidden}}
.hero:before{{content:"";position:absolute;right:-180px;top:-220px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.3),rgba(124,149,255,0) 68%)}}
.hero .wrap{{position:relative;padding-top:34px;padding-bottom:56px}}
.brand{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC}}
.brand b{{color:#fff;letter-spacing:.22em}}
.back{{color:#fff;text-decoration:none;font-weight:600;letter-spacing:.12em}}
.back:hover{{color:var(--blue2)}}
.hero .eyebrow{{color:var(--blue2);margin-top:64px}}
.hero h1{{font-size:clamp(32px,5vw,52px);font-weight:700;margin:10px 0 16px;max-width:820px;text-wrap:balance}}
.lede{{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:700px}}
.badge{{display:inline-block;margin-top:24px;font-size:13px;color:#D5DEEE;border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:5px 12px}}
.jump{{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}}
.jump .wrap{{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-top:10px;padding-bottom:10px}}
.jump .wrap::-webkit-scrollbar{{display:none}}
.jump a{{flex:none;font-size:13.5px;font-weight:600;color:var(--ink2);text-decoration:none;padding:6px 12px;border-radius:20px}}
.jump a:hover,.jump a:focus-visible{{background:var(--blueBg);color:var(--blue)}}
section{{scroll-margin-top:60px}}
section .wrap{{padding-top:64px;padding-bottom:8px}}
section.alt{{background:var(--bg)}} section.alt .wrap{{padding-bottom:64px}}
h2{{font-size:30px;font-weight:700;margin:8px 0 10px}}
.sub{{color:var(--ink2);font-size:17px;max-width:720px;margin-bottom:28px}}
h3{{font-size:18px;font-weight:700;margin-bottom:6px}}
p{{color:var(--ink2)}}
.grid3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
.grid2{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}
.card{{border:1px solid var(--line);border-radius:16px;background:#fff;padding:22px;position:relative;overflow:hidden}}
.card.top:before{{content:"";position:absolute;left:0;top:0;right:0;height:4px;background:var(--blue)}}
.card.top.g:before{{background:var(--green)}} .card.top.a:before{{background:var(--amber)}}
.ic{{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:var(--blueBg);color:var(--blue);margin-bottom:14px}}
.g .ic{{background:var(--greenBg);color:var(--green)}} .a .ic{{background:var(--amberBg);color:var(--amber)}}
.card .more{{display:inline-block;margin-top:12px;font-weight:600;font-size:14px;text-decoration:none}}
.steps{{list-style:none;counter-reset:s;display:grid;gap:12px}}
.steps li{{counter-increment:s;display:grid;grid-template-columns:34px 1fr;column-gap:12px;align-items:start}}
.steps li:before{{content:counter(s);grid-row:span 2;width:30px;height:30px;border-radius:50%;background:var(--blueBg);color:var(--blue);font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center}}
.steps b{{font-weight:600}} .steps span{{color:var(--ink2)}}
.tips{{list-style:none;display:grid;gap:9px}}
.tips li{{position:relative;padding-left:20px;color:var(--ink2)}}
.tips li:before{{content:"";position:absolute;left:2px;top:.62em;width:7px;height:7px;border-radius:50%;background:var(--blue)}}
.tips b{{color:var(--ink);font-weight:600}}
.note{{border-radius:12px;padding:14px 16px;font-size:14.5px;margin-top:18px}}
.note.blue{{background:var(--blueBg);color:#2A3F8F}} .note.green{{background:var(--greenBg);color:#0C5E43}}
.note.amber{{background:var(--amberBg);color:#7A4F12}} .note.red{{background:var(--redBg);color:#8E2A20}}
.note b{{font-weight:700}}
.keys{{width:100%;border-collapse:collapse;font-size:14px;margin-top:6px}}
.keys td{{padding:8px 0;border-bottom:1px solid var(--line);vertical-align:top}}
.keys td:first-child{{width:46%;padding-right:12px}}
kbd{{display:inline-block;font:600 12px Inter,system-ui,sans-serif;background:var(--bg);border:1px solid var(--line);border-bottom-width:2px;border-radius:6px;padding:2px 7px;color:var(--ink)}}
.cmp h3{{display:flex;align-items:center;gap:10px}}
.tag{{font-size:11.5px;font-weight:600;border-radius:20px;padding:3px 10px;letter-spacing:.02em;white-space:nowrap}}
.tag.b{{background:var(--blueBg);color:var(--blue)}} .tag.g{{background:var(--greenBg);color:var(--green)}}
.cmp .use{{font-weight:600;color:var(--ink);margin:8px 0 12px}}
.roles{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:14.5px}}
.roles th{{text-align:left;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);font-weight:600;padding:12px 16px;background:var(--bg);border-bottom:1px solid var(--line)}}
.roles td{{padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink2)}}
.roles tr:last-child td{{border-bottom:0}}
.roles td:first-child{{font-weight:700;color:var(--ink);white-space:nowrap}}
.roles small{{display:block;color:var(--mute);font-size:13px;margin-top:3px}}
.prompt{{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:#fff;font-size:14.5px;color:var(--ink)}}
.prompt:before{{content:"You: ";font-weight:700;color:var(--blue)}}
.prompts{{display:grid;gap:10px}}
.dlbtn{{display:inline-block;margin-top:14px;background:var(--blue);color:#fff;text-decoration:none;font-weight:600;font-size:14px;border-radius:10px;padding:10px 16px}}
.cta{{background:var(--navy);color:#fff;margin-top:64px}}
.cta .wrap{{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;padding-top:48px;padding-bottom:48px}}
.cta h2{{font-size:26px;margin:6px 0 6px}} .cta p{{color:#C5D0E3;max-width:600px}}
.btn{{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;font-weight:600;border-radius:10px;padding:12px 20px;white-space:nowrap}}
.btn:hover{{filter:brightness(1.1)}}
.foot{{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}}
.foot .wrap{{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}}
@media (max-width:900px){{.grid3{{grid-template-columns:1fr 1fr}}}}
@media (max-width:640px){{
  .wrap{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
  .grid3,.grid2{{grid-template-columns:1fr}} h2{{font-size:25px}} section .wrap{{padding-top:44px}}
  .hero .eyebrow{{margin-top:44px}} .keys td:first-child{{width:52%}}
  .roles,.roles tbody,.roles tr,.roles td{{display:block;width:100%}} .roles thead{{display:none}}
  .roles td{{border-bottom:0;padding:4px 16px}} .roles td:first-child{{padding-top:14px}} .roles td:last-child{{padding-bottom:14px;border-bottom:1px solid var(--line)}}
  .roles tr:last-child td:last-child{{border-bottom:0}}
}}
</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><b>Faclon Labs</b><a class="back" href="../">← All solutions</a></div>
  <div class="eyebrow">Read me</div>
  <h1>How to use the Faclon solutions site</h1>
  <p class="lede">This site is built for presenting Faclon solutions live, in front of a customer. Use downloads to send a customer a glossary made just for them, and use uploads, the design skill and the Claude connector to add new solution pages.</p>
  <span class="badge">For signed-in Faclon users · This guide can't be downloaded</span>
</div></header>

<nav class="jump" aria-label="Sections"><div class="wrap">{"".join(f'<a href="#{i}">{E(t)}</a>' for i, t in SECTIONS)}</div></nav>

<section id="start"><div class="wrap">
  <div class="eyebrow">Start here</div>
  <h2>Three things you can do</h2>
  <p class="sub">The landing page lists the solutions you have access to. Open any of them to see its use cases, architecture and customer results.</p>
  <div class="grid3">
    <div class="card top"><div class="ic">{icon("present")}</div><h3>Present</h3><p>Open a solution in full screen and walk the customer through it, section by section. This is what the site is for.</p><a class="more" href="#present">Presenting →</a></div>
    <div class="card top g"><div class="ic">{icon("share")}</div><h3>Share</h3><p>After the meeting, download one HTML file with only the solutions that customer cares about: their own glossary.</p><a class="more" href="#downloads">Downloads →</a></div>
    <div class="card top a"><div class="ic">{icon("build")}</div><h3>Contribute</h3><p>Build a new solution page with the design skill and upload it, from the site or from Claude.</p><a class="more" href="#upload">Uploading →</a></div>
  </div>
</div></section>

<section id="present"><div class="wrap">
  <div class="eyebrow">Smart presenting</div>
  <h2>Present live from the site</h2>
  <p class="sub">Every page is designed to be shown on a screen: big headlines, one idea per section and figures a plant team can read from the back of the room.</p>
  <div class="grid2">
    <div class="card">
      <h3>Before and during the meeting</h3>
      {steps([
          ("Sign in before you start.", "You stay signed in on that browser, so nothing interrupts the meeting. Use Chrome or Edge on a laptop for the best result."),
          ("Press Full screen.", "It's in the bar at the bottom right. The site stays in full screen while you move between pages, so you can go from the landing page to a solution and back without leaving it."),
          ("Move section by section.", "Use the menu bar at the top of each solution page to jump straight to a section. On the Faclon Labs Overview, use the up and down buttons or the keyboard."),
          ("Show only what matters.", "On the use-case maps, filter by area or search to show the use cases that fit this customer's plant."),
          ("Go back with “All solutions”.", "The link at the top of every page returns to the landing page."),
      ])}
    </div>
    <div class="card">
      <h3>Keyboard shortcuts (Faclon Labs Overview)</h3>
      <table class="keys">{"".join("<tr><td>" + " ".join(f"<kbd>{E(k)}</kbd>" for k in ks) + f"</td><td>{E(d)}</td></tr>" for ks, d in KEYS)}</table>
      <div class="note blue"><b>Tip:</b> present from the site, not from a downloaded file. You always show the latest version, and nothing is left behind on a meeting-room computer.</div>
    </div>
  </div>
</div></section>

<section id="downloads"><div class="wrap">
  <div class="eyebrow">Downloads</div>
  <h2>Which download to use</h2>
  <p class="sub">The Download button is in the bar at the bottom right of every solution page. You only see it if the admin has allowed you to download.</p>
  <div class="grid2">
    <div class="card top g cmp">
      <h3>One HTML file <span class="tag g">Customised glossary</span></h3>
      <p class="use">For sending a customer their own glossary after a meeting.</p>
      {tips([
          "Tick the solutions that are relevant to that customer. You get one file with a landing page showing only those solutions, and each of their pages.",
          "It opens in any browser, offline and without signing in, so the customer can open it straight from your email.",
          "It is a snapshot: later changes to the site don't reach it. Send a fresh file if a page changes.",
      ])}
    </div>
    <div class="card top cmp">
      <h3>PDF of this page <span class="tag b">One page</span></h3>
      <p class="use">For reading, attaching or printing one solution.</p>
      {tips([
          "The whole page as one continuous PDF page, with no page breaks, exactly as it looks on screen.",
          "Good for a quick read on a phone or attaching to a proposal email.",
          "A newly uploaded page gets its PDF after the next site build.",
      ])}
    </div>
  </div>
  <div class="note amber"><b>Downloaded files are not password-protected.</b> Anyone who has the file can open it. Send it only to the customer it was made for.</div>
  <div class="note blue">This Read me is for Faclon users only, so it can't be downloaded and is never included in an HTML file.</div>
</div></section>

<section id="upload" class="alt"><div class="wrap">
  <div class="eyebrow">For contributors</div>
  <h2>Upload a new solution page</h2>
  <p class="sub">Contributors see an Upload button in the bar. Ask the admin if you need it.</p>
  <div class="grid2">
    <div class="card">
      {steps([
          ("Build the page as one HTML file.", "Styles and images go inside the file. Follow the design skill so it looks like every other page. A page saved with Download → HTML also works: the page inside it is uploaded."),
          ("Press Upload and choose the file.", "The title is read from the page; change it if you need to."),
          ("Updating a page? Pick the solution it replaces.", "Choose it under “Is this a newer version of an existing solution?”. It keeps the same name and gets the next version number, v2, v3…, automatically."),
          ("For a new solution, give it a unique title.", "No two solutions can have the same name (only versions of one solution share a name), so an upload with a title that's already taken is refused."),
          ("Add a category, a one-line description and your name.", "They appear on the solution card, with “Contributed by” and your name."),
          ("Publish.", "It's live in about a minute."),
      ])}
    </div>
    <div class="card">
      <h3>After you upload</h3>
      {tips([
          "<b>Who sees it:</b> the admin, super users and contributors straight away. The admin can share it with other users in the User Manager.",
          "<b>Changes:</b> you can't edit or delete an uploaded page yourself. Upload it again as a newer version of the same solution, or ask the admin.",
          "<b>Versions:</b> both versions stay on the site, marked v1, v2… with the newest labelled Latest. Older versions show a “Newer version” button. The admin decides when to hide the older ones.",
          "<b>Sandbox:</b> uploaded pages run in a protected frame, so browser storage and pop-ups don't work in them.",
          "<b>Content:</b> only use figures you are allowed to share. See Good practice below.",
      ])}
    </div>
  </div>
</div></section>

<section id="skill" class="alt"><div class="wrap" style="padding-top:0">
  <div class="eyebrow">Design skill</div>
  <h2>Make your page match the site</h2>
  <div class="grid2">
    <div class="card">
      <p>The design skill is one file that describes the Faclon look: navy hero, white body, Inter, blue for insight and green for outcomes. It has the colours, layout, ready-made components, a starter page, writing rules (British spelling, sentence case) and a checklist to run before you upload.</p>
      <a class="dlbtn" href="../designskill.md" download="Faclon design skill.md">Download design skill</a>
      <p style="margin-top:12px;font-size:14px">It's also in the Download dialog on every page.</p>
    </div>
    <div class="card">
      <h3>Use it with an AI assistant</h3>
      <p>Give the skill file to Claude (or another assistant) along with your notes or a customer deck, and ask:</p>
      <div class="prompts" style="margin-top:12px">
        <div class="prompt">Follow this design skill and build a Faclon solution page on cooling tower optimisation from my notes.</div>
        <div class="prompt">Check my page against the skill's checklist and fix anything that's off.</div>
      </div>
    </div>
  </div>
</div></section>

<section id="connector"><div class="wrap">
  <div class="eyebrow">Claude connector</div>
  <h2>Work with the site from Claude</h2>
  <p class="sub">Contributors can connect the Claude desktop app to this site. Claude can then read and download the pages you can open, fetch the design skill and publish a new page for you, all by asking.</p>
  <div class="grid2">
    <div class="card">
      <h3>Connect it</h3>
      {steps([
          ("Open Download → Claude connector.", "On any solution page. You'll see it once you have the Contributor right."),
          ("Download the connector and install it.", "In the Claude desktop app, open Settings → Extensions and drag the file in, or double-click it."),
          ("Enter your Faclon username and password.", "They stay on your computer."),
      ])}
      <div class="note blue">The connector works in the Claude desktop app (Mac or Windows) and in Claude Code. Claude on the web and phone can't use it. Full steps are under <b>How to connect</b> in the Download dialog.</div>
    </div>
    <div class="card">
      <h3>Things to ask</h3>
      <div class="prompts">
        <div class="prompt">Which Faclon solutions can I open?</div>
        <div class="prompt">Summarise the Steam Trap page for a plant head.</div>
        <div class="prompt">Save the I/O Vision and Energy Management pages as PDF.</div>
        <div class="prompt">Upload cooling-tower.html from my Desktop as Cooling Tower Optimisation, category Utilities.</div>
      </div>
      <p style="margin-top:12px;font-size:14px">You get the same pages and download rights as on the site. Claude checks with you before it publishes anything.</p>
    </div>
  </div>
</div></section>

<section id="access"><div class="wrap">
  <div class="eyebrow">Accounts and access</div>
  <h2>Who can do what</h2>
  <p class="sub">The admin gives each user their own login and decides which solutions they see and what they can do.</p>
  <table class="roles"><thead><tr><th>Right</th><th>What it gives</th></tr></thead><tbody>
  {"".join(f"<tr><td>{E(r)}</td><td>{E(d)}{f'<small>{E(n)}</small>' if n else ''}</td></tr>" for r, d, n in ROLES)}
  </tbody></table>
  <div class="grid2" style="margin-top:18px">
    <div class="note blue" style="margin-top:0"><b>Forgot your password or need a solution?</b> Ask the site admin. Passwords can't be recovered, only reset.</div>
    <div class="note red" style="margin-top:0"><b>Keep your login to yourself.</b> Don't share it, and press Sign out when you use a shared or customer computer.</div>
  </div>
</div></section>

<section id="rules"><div class="wrap">
  <div class="eyebrow">Good practice</div>
  <h2>When you present, share or build</h2>
  <div class="grid3">
    <div class="card"><h3>Customer figures</h3><p>Use only figures from approved sources, which are the ones already on the site. Never add a number from a deal or a conversation without checking first.</p></div>
    <div class="card"><h3>Savings</h3><p>₹ values are indicative, “up to, per 100 MW per year”. Say so when you present them, and re-baseline them against the customer's own plant data.</p></div>
    <div class="card"><h3>Confidential material</h3><p>Keep internal pricing, deal data and anything marked confidential out of every page and every file you send. Example agent conversations stay labelled as illustrative.</p></div>
  </div>
</div></section>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Next step</div><h2>Open a solution and start presenting</h2><p>Questions, access or a new solution page? Ask the site admin.</p></div>
  <a class="btn" href="../">All solutions →</a>
</div></div>
<div class="foot"><div class="wrap"><span>Faclon Labs</span><span>Read me</span></div></div>
</body></html>"""

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
