---
name: faclon-solution-page-design
description: Build a Faclon Labs solution page as one self-contained HTML file that matches the Faclon glossary site's look (navy hero, white body, Inter, blue for insight and green for outcomes), ready to upload with the site's Upload button. Use when creating or restyling any Faclon solution, use-case or product page for the glossary.
---

# Faclon solution page design skill

Use this guide (or hand it to your AI assistant) whenever you build a page to upload to the Faclon glossary site. Following it makes your page look like every other solution page: same colours, type, layout and tone, with nothing else to set up.

Brand context comes from www.faclon.com. Faclon Labs makes the **Faclon Intelligence Platform**, a modular industrial AI and IoT platform that connects machines, analyses real-time data and automates decisions from edge to cloud. Its tagline is *One Platform, Safer Assets, Less Downtime, Smarter Operations*. Pages are read by plant heads, engineers and business leaders in power, metals, cement, chemicals, paper and manufacturing.

---

## 1. Hard rules (the upload depends on these)

1. **One HTML file.** Put all CSS in one `<style>` tag and any script in one `<script>` tag. Embed images as `data:` URIs (JPEG or WebP, compressed) or draw them as inline SVG. Keep the file under **20 MB**; aim for under 3 MB.
2. **The only external resource is the Inter font** from Google Fonts. Use no other CDNs, frameworks, icon fonts, analytics or iframes.
3. **Title format:** `<title>Your Solution · Faclon Labs</title>`. The upload form takes the page title from this tag.
4. **Back link:** link to `../` labelled "← All solutions", both in the hero and in the footer. Links to other solutions use `../<solution-slug>/`.
5. **Include `<meta name="robots" content="noindex">`.**
6. **Make it work at phone width (390 px)** with no sideways scrolling, and at desktop (1200 px and up).
7. **Don't rely on browser storage, cookies or pop-ups.** Uploaded pages run in a sandbox: `localStorage` is blocked, and links open in the main window.
8. **All content must be visible without scrolling or clicking.** The site makes a one-page PDF of your page at 1200 px width in a headless browser. Content that is hidden until it scrolls into view, sits in collapsed tabs, or depends on `100vh` heights will be missing or stretched in the PDF. Fade-in animation is fine only if the content is visible when animation is switched off.
9. **Never use `position: fixed`** for content. The site places its own sign-in bar at the bottom right, so leave that corner clear.

## 2. Colour tokens

Paste this block at the top of your CSS and use only these variables.

```css
:root{
  --ink:#0F1B2D;   /* main text */
  --ink2:#3A4A5F;  /* body copy, secondary text */
  --mute:#6B7A90;  /* captions, labels */
  --line:#E3E8EF;  /* borders, dividers */
  --bg:#F6F8FB;    /* light panels */
  --navy:#0B1A30;  /* hero, CTA and footer bands */
  --navy2:#13264A; /* tiles on navy */
  --blue:#3D63F5;  --blue2:#7C95FF; --blueBg:#EEF2FF;   /* insight, advisory, analytics */
  --green:#11875F; --greenBg:#E5F5EE;                   /* control, closed loop, outcomes, savings */
  --amber:#C77A12; --amberBg:#FFF4E2;                   /* in progress, DMZ, caution */
  --red:#B5452F;   --redBg:#FBF1EE;                     /* problems, losses, constraints */
  --violet:#6A45D0; --violetBg:#F1ECFD;                 /* optional fourth category */
}
```

Colour always carries meaning:
- **Blue** is for what the platform *knows or advises*: analytics, agents, insights.
- **Green** is for what it *does or delivers*: control, automation, savings and results.
- **Amber** marks work in progress, pilots and network middle zones (DMZ).
- **Red** marks today's problems: losses, failures, constraints. Use it sparingly.
- The page is white with navy bands. Keep blue to accents and chips, never a full blue background.

Text on navy is `#fff` for headings, `#C5D0E3` for paragraphs and `#9FB0CC` for small labels. Use `--blue2` for accent words on navy.

## 3. Typography

- Font: `font-family: Inter, system-ui, -apple-system, "Segoe UI", sans-serif;`. Load weights 400, 500, 600 and 700:
  `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`
- Body text is 15px with line-height 1.55 and colour `--ink`. Add `-webkit-font-smoothing:antialiased`.
- Set numbers in tabular figures: `font-variant-numeric: tabular-nums`.
- Headings use `letter-spacing:-.015em; line-height:1.2`, weight 700.

| Element | Size |
|---|---|
| Hero h1 | `clamp(34px, 5.4vw, 58px)` |
| Hero lede | `clamp(16px, 1.8vw, 19px)`, colour `#C5D0E3` |
| Section h2 | 32px (26px on phones) |
| Card h3 | 18–22px |
| Section intro (`.sub`) | 17px, `--ink2`, max-width 720px |
| Card text | 13.5–14.5px, `--ink2` |
| Eyebrow | 12px, 600, uppercase, `letter-spacing:.14em`, `--blue` |

Every section opens with an **eyebrow**, then an h2, then a one- or two-line `.sub`.

## 4. Layout

- Content width: `.wrap{max-width:1080px;margin:0 auto;padding:0 28px}`. On phones the side padding drops to 16px.
- Sections: `section{padding:72px 0}`, or 52px on phones.
- Corner radius: 14–16px for cards, 12px for panels, 9px for small tiles, 999px for chips and buttons.
- Prefer borders (`1px solid var(--line)`) over shadows. Use no shadows on content cards.
- Grids collapse to one column below 640px and to two columns below 900px where four would be too tight.

### Page order (keep it)

1. **Hero** (navy): a brand row ("FACLON LABS" left, solution and keywords right), the "← All solutions" link, the h1 with one `<em>` accent phrase, a lede paragraph, optional two "part" tiles, and a strip of 3–4 KPIs.
2. **The problem**: what goes wrong today, with red accents used lightly.
3. **How it works**: an architecture diagram in inline SVG, or numbered steps.
4. **Use cases / capabilities**: a grid of cards.
5. **Results / benefits**: green top-border tiles.
6. **Customer proof** (on `--bg`): case cards with stat chips. Use approved figures only (see §7).
7. **CTA band** (navy): one sentence on the next step, plus a button to `https://www.faclon.com`.
8. **Footer** (navy): "← All solutions · Faclon Labs · Solution name".

## 5. Components (copy and adapt)

```css
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{letter-spacing:-.015em;line-height:1.2}
section{padding:72px 0}
h2{font-size:32px;font-weight:700;margin:8px 0 12px}
.sub{color:var(--ink2);font-size:17px;max-width:720px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}

/* hero */
.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.32),rgba(124,149,255,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:64px}
.brand{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.hero h1{font-size:clamp(34px,5.4vw,58px);font-weight:700;margin:72px 0 18px;max-width:820px}
.hero h1 em{font-style:normal;color:var(--blue2)}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:680px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:40px;border-radius:12px;overflow:hidden;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{display:block;font-size:26px}
.kp span{font-size:12.5px;color:#9FB0CC}
.kp.ac b{color:#F2B256}          /* highlight one KPI at most */

/* cards */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.card{border:1px solid var(--line);border-radius:14px;padding:20px;background:#fff}
.card h3{font-size:18px;margin-bottom:6px}
.card p{font-size:13.5px;color:var(--ink2)}
.ic{width:42px;height:42px;border-radius:11px;background:var(--blueBg);color:var(--blue);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.ic.g{background:var(--greenBg);color:var(--green)}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.tags span{font-size:12px;font-weight:500;background:var(--blueBg);color:var(--blue);border-radius:999px;padding:3px 9px}

/* numbered steps */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:32px;counter-reset:s}
.steps div{background:var(--bg);border-radius:12px;padding:16px}
.steps div:before{counter-increment:s;content:counter(s);display:inline-flex;width:24px;height:24px;border-radius:50%;background:var(--blue);color:#fff;font-size:12px;font-weight:700;align-items:center;justify-content:center;margin-bottom:8px}
.steps b{display:block;font-size:14.5px;margin-bottom:3px}
.steps p{font-size:13px;color:var(--ink2)}

/* benefits */
.benefits{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:28px}
.bn{border-top:3px solid var(--green);padding:14px 2px 0}
.bn b{font-size:16px;display:block;margin-bottom:4px}
.bn p{font-size:13.5px;color:var(--ink2)}

/* customer proof */
.proof{background:var(--bg)}
.case{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px}
.case .cn{font-size:18px;font-weight:700}
.case .cx{font-size:12.5px;color:var(--mute);margin-bottom:12px}
.stat{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.stat span{font-size:12.5px;background:var(--blueBg);border-radius:8px;padding:4px 9px;color:var(--ink2)}
.stat span b{color:var(--blue);font-size:14px;margin-right:4px}
.stat span.prog{background:var(--amberBg);color:var(--amber);font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase}

/* CTA + footer */
.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap;padding-top:56px;padding-bottom:56px}
.cta h2{color:#fff}.cta p{color:#C5D0E3;max-width:560px}
.btn{background:var(--blue2);color:#fff;font-weight:700;padding:13px 24px;border-radius:30px;text-decoration:none;white-space:nowrap}
.btn.ghost{background:transparent;border:1.5px solid var(--blue2)}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:18px;padding-bottom:22px}
.foot a{color:inherit;text-decoration:none}

@media (max-width:900px){ .grid{grid-template-columns:1fr 1fr} .steps,.benefits,.kpis{grid-template-columns:1fr 1fr} }
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section{padding:52px 0} h2{font-size:26px}
  .grid,.steps,.benefits{grid-template-columns:1fr}
}
```

**Icons:** draw simple line icons as inline SVG, 22px, `stroke="currentColor" stroke-width="1.8" fill="none"` with round caps and joins. Don't use emoji or icon fonts.

**Diagrams:** use inline SVG with a `viewBox` and `width:100%;height:auto`. Use the tokens for colour: blue boxes for data and insight, green for control and outcomes, amber for DMZ, navy for the platform core. Labels are Inter, 12–14px. Name platform parts exactly: **Faclon AI platform**, **Ontology**, **I/O Connect** (a gateway that can sit in OT, DMZ or IT). Other product names from faclon.com are **I/O Sense**, **Bruce AI**, **I/O DeepSense**, **Foundry** and **Forge**.

## 6. Writing style

- Write plain language for plant and business readers. Say what the system *does*, never how it works as maths or formulas.
- Headlines are short, confident and outcome-first: "Catch failing steam traps before they waste steam", not "AI-based acoustic anomaly detection framework".
- Use one idea per card: a bold title of 2–5 words, then one or two sentences.
- Show numbers big. Give units and context in the label underneath ("Net heat rate reduction").
- Write ₹ values as **"up to … per year"** and keep them indicative. Write "₹1.3 cr", "1,000+ sensors", "2–8 weeks".
- Label example conversations or screens as **illustrative**.
- Use British/Indian spelling (optimise, analyse) to match the existing pages.

## 7. Content you may and may not use

- **Customer names and figures must come from approved Faclon sources**: the Faclon Labs Presentation 2026 deck, approved solution decks, or figures already shown on the site. If you're not sure a number is approved, leave it out or describe the result without the number.
- **Never include** internal pricing, deal values, unreleased roadmap, personal contact details or anything marked confidential.
- Don't copy text or images from competitors or third-party sites.

## 8. Starter page

Save this as `my-solution.html`, replace the bracketed text, and add the component CSS from §5 where marked.

```html
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>[Solution name] · Faclon Labs</title>
<meta name="description" content="[One sentence on what it does]">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* paste the :root tokens from section 2 and the component CSS from section 5 here */
</style></head>
<body>

<div class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>[Solution] · [Keyword] · [Keyword]</span></div>
  <a class="back" href="../">← All solutions</a>
  <h1>[Outcome-first headline with one <em>accent phrase</em>]</h1>
  <p class="lede">[Two sentences: who it is for and what changes for them.]</p>
  <div class="kpis">
    <div class="kp ac"><b>[3–5%]</b><span>[What improves]</span></div>
    <div class="kp"><b>[24/7]</b><span>[What it covers]</span></div>
    <div class="kp"><b>[2–8 weeks]</b><span>[Early warning, payback…]</span></div>
    <div class="kp"><b>[1,000+]</b><span>[Scale proof]</span></div>
  </div>
</div></div>

<div class="wrap">
<section>
  <div class="eyebrow">The problem</div><h2>[What goes wrong today]</h2>
  <p class="sub">[One or two lines in the plant's language.]</p>
</section>

<section>
  <div class="eyebrow">How it works</div><h2>[From data to decision]</h2>
  <div class="steps">
    <div><b>Connect</b><p>I/O Connect brings in [sensors / DCS / lab data].</p></div>
    <div><b>Understand</b><p>The Ontology links each signal to the right asset.</p></div>
    <div><b>Detect</b><p>[What the AI spots, in plain words.]</p></div>
    <div><b>Act</b><p>[Who gets told, or what is controlled.]</p></div>
  </div>
</section>

<section>
  <div class="eyebrow">Use cases</div><h2>[What it covers]</h2>
  <div class="grid">
    <div class="card"><div class="ic"><!-- inline SVG icon --></div><h3>[Use case]</h3><p>[One sentence.]</p><div class="tags"><span>[Tag]</span></div></div>
    <!-- more cards -->
  </div>
</section>

<section>
  <div class="eyebrow" style="color:var(--green)">Results</div><h2>[What the plant gains]</h2>
  <div class="benefits">
    <div class="bn"><b>[Less downtime]</b><p>[How, in one line.]</p></div>
    <!-- 3–4 tiles -->
  </div>
</section>
</div>

<div class="proof"><div class="wrap"><section>
  <div class="eyebrow">Customer proof</div><h2>[Proven in plants like yours]</h2>
  <div class="grid">
    <div class="case"><div class="cn">[Customer]</div><div class="cx">[Plant · scope]</div>
      <p>[What was done.]</p><div class="stat"><span><b>[15+]</b>[failures caught]</span></div></div>
  </div>
</section></div></div>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Next step</div><h2>[Start with your data]</h2><p>[What the customer shares, what Faclon returns.]</p></div>
  <a class="btn" href="https://www.faclon.com">www.faclon.com</a>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · [Solution]</span><span>[Short descriptor]</span></div></div>
</body></html>
```

## 9. Before you upload: checklist

- [ ] Opens straight from your computer (double-click) with everything showing: no missing images and no console errors.
- [ ] Looks right at 390 px and 1200 px wide (use the browser's device toolbar), with no sideways scroll.
- [ ] Title reads `… · Faclon Labs`; there is a hero, sections with eyebrows, a CTA and a footer; "← All solutions" links to `../`.
- [ ] Uses only the colour tokens, with blue for insight and green for outcomes.
- [ ] Every number and customer name comes from an approved source; nothing is confidential.
- [ ] File is under 20 MB with images compressed.
- [ ] Upload with the site's **Upload** button. Give a short category (e.g. "Power", "Utilities"), a one-line description for the card, and your name if you want the "Contributed by" credit.
