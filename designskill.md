---
name: faclon-solution-page-design
description: Build a Faclon Labs solution page or AI use-case catalogue as one self-contained HTML file that matches the Faclon glossary site (navy hero, white body, Inter, blue for insight and green for outcomes, British spelling, sentence case), ready to upload with the site's Upload button. Use when creating, restyling or reviewing any Faclon solution, use-case map or product page for the glossary.
---

# Faclon solution page design skill

Use this guide (or hand it to your AI assistant) whenever you build a page to upload to the Faclon glossary site. If you follow it, your page will look and read like every other page on the site, with nothing else to set up.

Brand context comes from www.faclon.com. Faclon Labs makes the **Faclon Intelligence Platform**, a modular industrial AI and IoT platform that connects machines, analyses real-time data and automates decisions from edge to cloud. Its tagline is *One Platform, Safer Assets, Less Downtime, Smarter Operations*. Pages are read by plant heads, engineers and business leaders in power, metals, cement, mining, chemicals, paper and manufacturing.

**Pick one of the two page types the site uses:**

| Type | Use it for | Examples on the site |
|---|---|---|
| **A. Solution page** | One product or solution: how it works, hardware, platform, value and customers | Bus Bar Monitoring, Steam Trap Failure Detection, Condition Based Monitoring, Energy Management, Power Plant AI |
| **B. Use-case catalogue** | Many AI use cases across one industry, grouped by plant area, each with its indicative value | Steel, Cement, Pulp & Paper and Coal Mining AI Use Case Maps, Discrete Manufacturing |

---

## 1. Hard rules (the upload depends on these)

1. **One HTML file.** Put all CSS in one `<style>` tag and any script in one `<script>` tag. Embed images as `data:` URIs (compressed JPEG or WebP) or draw them as inline SVG. Keep the file under **20 MB**; aim for under 3 MB.
2. **The only external resource is the Inter font** from Google Fonts. Use no other CDNs, frameworks, icon fonts, analytics or iframes.
3. **Title format:** `<title>Your Solution · Faclon Labs</title>`. The upload form takes the page title from this tag. The admin can rename the card later without changing your page.
4. **Back link:** link to `../` labelled "← All solutions", both in the hero and in the footer. Links to other solutions use `../<solution-slug>/`. In-page links such as `#use-cases` work normally.
5. **Include `<meta name="robots" content="noindex">`.**
6. **Make it work at phone width (390 px)** with no sideways scrolling, and at desktop (1200 px and up).
7. **Don't rely on browser storage, cookies or pop-ups.** Uploaded pages run in a sandbox: `localStorage` is blocked, and outside links open in the main window.
8. **All content must be visible without clicking.** The site makes a one-page PDF of your page at 1200 px width. Anything inside closed tabs, accordions or "show more" panels is missing from the PDF, so prefer showing everything. Fade-in animation is fine only if the content is visible when animation is off. Avoid `100vh` heights, and keep the page under about 20,000 px tall at desktop width; taller pages are shrunk to fit the PDF.
9. **Never use `position: fixed`.** The site puts its own sign-in bar at the bottom right. `position: sticky` is fine for a jump bar or filter bar.

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
  --amber:#C77A12; --amberBg:#FFF4E2;                   /* in progress, DMZ, platform foundation */
  --red:#B5452F;   --redBg:#FBF1EE;                     /* problems, losses, constraints */
  --violet:#6A45D0; --violetBg:#F1ECFD;                 /* computer vision (Vision AI) */
  --teal:#0E7C8C;  --tealBg:#E4F4F6;                    /* IoT sensing */
}
```

Colour always carries meaning:
- **Blue** is what the platform *knows or advises*: analytics, AI advisory, agents, insights.
- **Green** is what it *does or delivers*: control, automation, savings and results. **Every ₹ value and outcome figure is green.**
- **Amber** marks work in progress, pilots, the DMZ and platform foundations.
- **Red** marks today's problems: losses, failures, constraints. Use it sparingly.
- **Violet** is computer vision and **teal** is IoT sensing, used only for use-case type tags.
- The page is white with navy bands. Keep blue to accents and chips, never a full blue background.

Text on navy is `#fff` for headings, `#C5D0E3` for paragraphs and `#9FB0CC` for small labels. Use `--blue2` for the accent word in a hero headline and `#7FD9B3` for a green figure on navy.

## 3. Typography

- Font: `font-family: Inter, system-ui, -apple-system, "Segoe UI", sans-serif;`. Load weights 400, 500, 600 and 700:
  `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`
- Body text is 15px with line-height 1.55 and colour `--ink`. Add `-webkit-font-smoothing:antialiased`.
- Use tabular figures only in tables: `table{font-variant-numeric:tabular-nums}`. **Never set them on `body`**: in Inter they also widen the hyphen, so "IT-OT" renders as "IT - OT".
- Headings use `letter-spacing:-.015em; line-height:1.2`, weight 700.

| Element | Size |
|---|---|
| Hero h1 | `clamp(34px, 5.4vw, 58px)` |
| Hero lede | `clamp(16px, 1.8vw, 19px)`, colour `#C5D0E3` |
| Section h2 | 32px (26px on phones) |
| Card title | 17–22px |
| Section intro (`.sub`) | 17px, `--ink2`, max-width 720px |
| Card text | 13.5–14.5px, `--ink2` |
| Eyebrow | 12px, 600, uppercase, `letter-spacing:.14em`, `--blue` |

Every section opens with an **eyebrow**, then an h2, then a one- or two-line `.sub`.

## 4. Layout

- Content width: `.wrap{max-width:1180px;margin:0 auto;padding:0 28px}`. On phones the side padding drops to 16px.
- Sections: `section{padding:72px 0}`, or 52px on phones.
- Corner radius: 14–16px for cards, 12px for panels, 9–10px for small tiles and buttons, 999px for chips.
- Prefer borders (`1px solid var(--line)`) over shadows. Content cards have no shadows.
- Grids drop to two columns below 900px and to one column below 640px.

### A. Solution page order

1. **Hero** (navy): the brand row ("FACLON LABS" left, solution and keywords right), "← All solutions", an optional eyebrow, the h1 with one `<em>` accent phrase, a lede, an optional photo on the right, and a strip of 3–4 KPIs.
2. **Jump bar** (optional, sticky): links to each section below.
3. **The problem**: what goes wrong today, with red used lightly.
4. **How it works**: an inline SVG architecture diagram or numbered steps.
5. **Hardware / platform**: spec tables and screenshots, if the solution has them.
6. **Results / benefits**: green top-border tiles, plus an ROI table if you have approved figures.
7. **Customer proof** (on `--bg`): case cards with stat chips, using approved figures only (see §7).
8. **Closing band** (navy): eyebrow "Next step", a sentence-case heading, one sentence on what happens next, then the **Book a demo** and **www.faclon.com** buttons.
9. **Footer** (navy): "← All solutions · Faclon Labs · Solution name" on the left and a short descriptor on the right.

### B. Use-case catalogue order

1. **Hero** (navy): as above, with KPIs such as the number of use cases, plant areas, and the value range in green. Under the KPIs, a row of **area chips** (`01 Mines 1`, `02 Crusher 1` …) that jump to each area.
2. **Filter bar** (sticky, optional): a search box, an area select and type buttons (All · AI Advisory · Vision AI · IoT Sensing · Platform). The page must read fine with no script at all.
3. **One section per plant area**, in value-chain order: a numbered heading (`01 Mines`, with the use-case count on the right), then one **use-case card** per use case.
4. **Value note**: one line on how values are built: "Values are indicative, in ₹ cr per MTPA per year, and are re-baselined against each plant's data."
5. **Closing band** and **footer**, as in type A.

## 5. Components (copy and adapt)

```css
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
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
.hero .eyebrow{display:block;margin-top:56px;color:var(--blue2)}
.hero h1{font-size:clamp(34px,5.4vw,58px);font-weight:700;margin:16px 0 18px;max-width:820px}
.hero h1:first-of-type{margin-top:72px}
.hero .eyebrow + h1{margin-top:12px}
.hero h1 em{font-style:normal;color:var(--blue2)}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:680px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:40px;border-radius:12px;overflow:hidden;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{display:block;font-size:26px}
.kp span{font-size:12.5px;color:#9FB0CC}
.kp.ac b{color:#7FD9B3}          /* one highlighted KPI at most: savings or outcome, in green */

/* area chips under a catalogue hero */
.areas{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.areas a{display:inline-flex;gap:8px;align-items:center;font-size:13.5px;color:#E4EAF5;text-decoration:none;padding:6px 12px;border-radius:20px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}
.areas em{font-style:normal;font-size:11px;color:#8798B8}
.areas i{font-style:normal;font-size:12px;color:var(--blue2);font-weight:600}

/* sticky jump bar (solution pages) */
.jump{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.jump .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:10px;padding-bottom:10px;scrollbar-width:none}
.jump a{flex:none;text-decoration:none;color:var(--ink2);font-size:14px;padding:6px 12px;border-radius:8px}
.jump a:hover{background:var(--bg);color:var(--ink)}

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

/* spec table (hardware) */
.specs{width:100%;border-collapse:collapse;font-size:14px}
.specs th,.specs td{text-align:left;padding:8px 0;border-top:1px solid var(--line);vertical-align:top}
.specs th{width:38%;font-weight:600;color:var(--mute);padding-right:14px}

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
.stat span{font-size:12.5px;background:var(--greenBg);border-radius:8px;padding:4px 9px;color:var(--ink2)}
.stat span b{color:var(--green);font-size:14px;margin-right:4px}
.stat span.prog{background:var(--amberBg);color:var(--amber);font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase}

/* use-case catalogue: filter bar, area heading, use-case card */
.bar{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar .wrap{padding-top:12px;padding-bottom:12px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.search{flex:1 1 220px;font:inherit;font-size:14.5px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;color:var(--ink);min-width:0}
.bar select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden;max-width:100%}
.seg button{font:inherit;font-size:13.5px;padding:8px 11px;border:0;border-right:1px solid var(--line);background:#fff;color:var(--ink2);cursor:pointer;white-space:nowrap}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--blueBg);color:var(--blue);font-weight:600}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;padding-bottom:12px;border-bottom:2px solid var(--ink);margin-bottom:16px}
.sec-head h2{font-size:28px;margin:0}
.sec-head h2 em{font-style:normal;font-size:13px;letter-spacing:.14em;color:var(--blue);margin-right:12px;vertical-align:middle}
.sec-head .meta{font-size:13px;color:var(--mute)}
.ucs{display:grid;gap:14px}
.uc{border:1px solid var(--line);border-left:4px solid var(--blue);border-radius:14px;padding:18px 20px;display:flex;flex-direction:column;gap:12px;background:#fff}
.uc.cv{border-left-color:var(--violet)} .uc.iot{border-left-color:var(--teal)} .uc.plat{border-left-color:var(--amber)}
.uc-top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}
.uc h4{font-size:17.5px;line-height:1.3;margin-top:6px}
.kind{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);background:var(--blueBg);border-radius:20px;padding:2px 9px}
.cv .kind{color:var(--violet);background:var(--violetBg)} .iot .kind{color:var(--teal);background:var(--tealBg)} .plat .kind{color:var(--amber);background:var(--amberBg)}
.val{flex:none;text-align:right;line-height:1.1;font-size:20px;font-weight:700;color:var(--green);white-space:nowrap}
.val small{display:block;font-size:10.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin-top:4px}
.cols{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:22px}
.cols b{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px}
.cols ul{list-style:none}
.cols li{position:relative;padding-left:15px;font-size:13.5px;line-height:1.5;margin-bottom:5px}
.does b{color:var(--blue)} .does li:before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--blue2)}
.probs b{color:var(--red)} .probs li{color:var(--ink2)} .probs li:before{content:"";position:absolute;left:0;top:10px;width:7px;height:2px;background:#E0A898}
.note{font-size:12.5px;color:var(--mute);margin-top:18px}

/* closing band + footer */
.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap;padding-top:56px;padding-bottom:56px}
.cta h2{color:#fff}.cta p{color:#C5D0E3;max-width:560px}
.ctabtns{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;font-weight:600;font-size:15px;line-height:1.2;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap;color:#fff;background:#3D63F5;border:1.5px solid #3D63F5}
.btn.ghost{background:transparent;border-color:rgba(255,255,255,.4)}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:18px;padding-bottom:22px}
.foot a{color:inherit;text-decoration:none}

@media (max-width:900px){ .grid{grid-template-columns:1fr 1fr} .steps,.benefits,.kpis{grid-template-columns:1fr 1fr} }
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section{padding:52px 0} h2{font-size:26px}
  .grid,.steps,.benefits,.cols{grid-template-columns:1fr}
  .uc{padding:16px} .uc-top{flex-direction:column;gap:6px} .val{text-align:left}
  .seg{width:100%} .seg button{flex:1;padding:7px 2px;font-size:12px}
  .specs th{width:42%}
}
```

**Use-case card markup** (type B). Use `class="uc"` for AI Advisory, or add `cv` (Vision AI), `iot` (IoT Sensing) or `plat` (Platform):

```html
<article class="uc cv" data-k="cv" data-q="belt health monitoring conveyor tear misalignment">
  <div class="uc-top">
    <div><span class="kind">Vision AI</span><h4>Belt Health Monitoring</h4></div>
    <div class="val">₹0.3–1.2 cr<small>per MTPA · per year</small></div>
  </div>
  <div class="cols">
    <div class="does"><b>What it does</b><ul><li>Watches the belt for tears, misalignment and spillage.</li><li>Raises an alert with a photo before the belt fails.</li></ul></div>
    <div class="probs"><b>Problem addressed</b><ul><li>Belt damage is found only on inspection rounds.</li><li>Unplanned stoppages and lost throughput.</li></ul></div>
  </div>
</article>
```

**Optional filter script** (type B). It needs no storage and works inside the sandbox. Put `data-k` (type) and `data-q` (search words) on each card, and `data-area` on each area `<section>`:

```html
<script>
(function(){
  var q=document.getElementById('q'),sel=document.getElementById('area'),type='all';
  var segs=document.querySelectorAll('.seg button');
  function run(){
    var t=(q.value||'').toLowerCase().trim(),a=sel.value;
    document.querySelectorAll('section[data-area]').forEach(function(s){
      var shown=0;
      s.querySelectorAll('.uc').forEach(function(c){
        var ok=(type==='all'||c.dataset.k===type)&&(!t||c.dataset.q.indexOf(t)>=0)&&(!a||s.dataset.area===a);
        c.style.display=ok?'':'none'; if(ok)shown++;
      });
      s.style.display=shown?'':'none';
    });
  }
  q.addEventListener('input',run); sel.addEventListener('change',run);
  segs.forEach(function(b){b.addEventListener('click',function(){segs.forEach(function(x){x.setAttribute('aria-pressed',x===b)});type=b.dataset.k;run()})});
})();
</script>
```

**Icons:** draw simple line icons as inline SVG, 22px, `stroke="currentColor" stroke-width="1.8" fill="none"` with round caps and joins. Don't use emoji or icon fonts.

**Diagrams:** use inline SVG with a `viewBox` and `width:100%;height:auto`. Colour with the tokens: blue boxes for data and insight, green for control and outcomes, amber for the DMZ, navy for the platform core. Labels are Inter, 12–14px. If a diagram is wide, put it in a container with `overflow-x:auto` and add "Swipe sideways to see the full diagram" for phones.

**Product names** (spell exactly): **Faclon AI platform**, **Ontology**, **I/O Connect** (a gateway that can sit in OT, DMZ or IT), **I/O Sense**, **I/O Lens**, **I/O Vision**, **Bruce AI**, **I/O DeepSense**, **UDF**, **Foundry** and **Forge**.

## 6. Writing style

**Voice**
- Write plain language for plant and business readers. Say what the system *does*, never how it works as maths or formulas.
- Headlines are short and confident. Use either an outcome-first line ("See every critical joint's temperature, live") or the product name with one accent word ("Steam Trap *Failure Detection*").
- Use one idea per card: a bold title of 2–5 words, then one or two sentences.
- In use-case cards, start "What it does" bullets with a verb ("Tracks…", "Flags…", "Recommends…") and write "Problem addressed" bullets as the problem itself ("Belt damage is found only on inspection rounds").
- Don't overclaim. Avoid "ensures 100%", "eliminates all" and "guarantees". Say what the system detects, flags or reduces.
- If you use the shared tagline, write it exactly: "Decision intelligence at scale to unlock the latent potential of each plant." The three value pillars that can follow it are "Improve production throughput and yield", "Reduce operational cost and wastage" and "AI agents enable decision intelligence at scale".
- Label example conversations or screens as **illustrative**.

**Spelling and case**
- Use British spelling throughout: optimise, analyse, digitise, behaviour, colour, catalogue, mould, fibre, tonne, aluminium.
- Headings, card titles, labels, chips and buttons are sentence case ("Lower energy bills", not "Lower Energy Bills"). Keep Title Case only for product names and named use cases ("Kiln SHC Optimiser").
- Hyphenate compound adjectives: real-time data, closed-loop control, condition-based monitoring, long-term, field-tested.

**Numbers and units**
- Show numbers big, with units and context in the label underneath ("Net heat rate reduction").
- Write ₹ values as "₹1.3 cr" or "₹60 lakh" and always give the basis in the label: per year, per MTPA, per 100 MW, per 100 traps. Values are indicative: say "up to" where it is a ceiling, and add a short note that they are re-baselined against each plant's data.
- Put a space between number and unit: 0.2 Hz, 6 kHz, 24 V DC, 230 V AC, 40 mm, 78 g, 100 °C. Use "−" (minus sign) for negatives, "±" for tolerances, "–" (en dash) for ranges (2–8 weeks), and "×" for dimensions (40 × 40 × 33 mm).
- Use standard spellings: Wi-Fi, RS-485, 4G, IP67, ISO 50001, SOC 2, MTPA, OEE, kWh.
- Make totals add up. If a table lists ₹50 lakh + ₹7.5 lakh + ₹4 lakh, the total says ₹61.5 lakh, or the label explains the difference (for example "net of solution cost").
- Make counts match the page. "13 use cases" in the hero means 13 cards below.

## 7. Content you may and may not use

- **Customer names and figures must come from approved Faclon sources**: the Faclon Labs Presentation 2026 deck, approved solution decks, or figures already shown on the site. If you're not sure a number is approved, leave it out or describe the result without the number.
- **Never include** internal pricing, deal values, unreleased roadmap, personal phone numbers or emails, or anything marked confidential. Point people to "Book a demo" instead.
- Don't copy text or images from competitors or third-party sites.

## 8. Starter page (type A)

Save this as `my-solution.html`, replace the bracketed text, and paste the tokens from §2 and the CSS from §5 where marked. For a use-case catalogue (type B), keep the hero, closing band and footer, and replace the middle with the filter bar, area sections and use-case cards from §5.

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
  <span class="eyebrow">[Category, e.g. Predictive maintenance]</span>
  <h1>[Outcome-first headline with one <em>accent phrase</em>]</h1>
  <p class="lede">[Two sentences: who it is for and what changes for them.]</p>
  <div class="kpis">
    <div class="kp ac"><b>[₹x cr / yr]</b><span>[Indicative saving, and its basis]</span></div>
    <div class="kp"><b>[24/7]</b><span>[What it covers]</span></div>
    <div class="kp"><b>[2–8 weeks]</b><span>[Early warning, payback…]</span></div>
    <div class="kp"><b>[1,000+]</b><span>[Scale proof]</span></div>
  </div>
</div></div>

<nav class="jump" aria-label="On this page"><div class="wrap">
  <a href="#problem">Problem</a><a href="#how">How it works</a><a href="#cases">Use cases</a><a href="#results">Results</a><a href="#proof">Customers</a>
</div></nav>

<div class="wrap">
<section id="problem">
  <div class="eyebrow">The problem</div><h2>[What goes wrong today]</h2>
  <p class="sub">[One or two lines in the plant's language.]</p>
</section>

<section id="how">
  <div class="eyebrow">How it works</div><h2>[From data to decision]</h2>
  <div class="steps">
    <div><b>Connect</b><p>I/O Connect brings in [sensors / DCS / lab data].</p></div>
    <div><b>Understand</b><p>The Ontology links each signal to the right asset.</p></div>
    <div><b>Detect</b><p>[What the AI spots, in plain words.]</p></div>
    <div><b>Act</b><p>[Who gets told, or what is controlled.]</p></div>
  </div>
</section>

<section id="cases">
  <div class="eyebrow">Use cases</div><h2>[What it covers]</h2>
  <div class="grid">
    <div class="card"><div class="ic"><!-- inline SVG icon --></div><h3>[Use case]</h3><p>[One sentence.]</p><div class="tags"><span>[Tag]</span></div></div>
    <!-- more cards -->
  </div>
</section>

<section id="results">
  <div class="eyebrow" style="color:var(--green)">Results</div><h2>[What the plant gains]</h2>
  <div class="benefits">
    <div class="bn"><b>[Less downtime]</b><p>[How, in one line.]</p></div>
    <!-- 3–4 tiles -->
  </div>
  <p class="note">[Values are indicative and are re-baselined against each plant's data.]</p>
</section>
</div>

<div class="proof" id="proof"><div class="wrap"><section>
  <div class="eyebrow">Customer proof</div><h2>[Proven in plants like yours]</h2>
  <div class="grid">
    <div class="case"><div class="cn">[Customer]</div><div class="cx">[Plant · scope]</div>
      <p>[What was done.]</p><div class="stat"><span><b>[15+]</b>[failures caught]</span></div></div>
  </div>
</section></div></div>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Next step</div><h2>[Start with your data]</h2><p>[What the customer shares, what Faclon returns.]</p></div>
  <div class="ctabtns"><a class="btn" href="https://www.faclon.com/book-a-demo">Book a demo</a><a class="btn ghost" href="https://www.faclon.com">www.faclon.com</a></div>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · [Solution]</span><span>[Short descriptor]</span></div></div>
</body></html>
```

## 9. Before you upload: checklist

**Works**
- [ ] Opens straight from your computer (double-click) with everything showing: no missing images and no console errors.
- [ ] Looks right at 390 px and 1200 px wide (use the browser's device toolbar), with no sideways scroll.
- [ ] Every button, filter and search box works, and the page still reads fine with scripts switched off.
- [ ] Nothing important is hidden in tabs or accordions, and nothing uses `position: fixed` or `localStorage`.
- [ ] File is under 20 MB with images compressed.

**Looks like the site**
- [ ] Title reads `… · Faclon Labs`; there is a hero with the brand row, sections with eyebrows, a "Next step" closing band with both buttons, and a footer; "← All solutions" links to `../`.
- [ ] Uses only the colour tokens: blue for insight, green for outcomes and every ₹ value.
- [ ] Content width is 1180 px, and tabular figures are only on tables (hyphens look normal: "IT-OT", not "IT - OT").

**Reads like the site**
- [ ] British spelling, sentence-case headings and labels, hyphenated compound adjectives.
- [ ] Units spaced and written the standard way (0.2 Hz, 24 V DC, Wi-Fi, IP67); ₹ values give their basis.
- [ ] Totals add up and counts match the page.
- [ ] No third-party technology names (databases, frameworks, cloud or container tools such as MongoDB, React or Kubernetes). Describe what the platform does, not what it is built with.
- [ ] Every number and customer name comes from an approved source; no personal contact details or confidential data.

**Upload**
- [ ] Pick a title no other solution on the site already uses. Uploads with a duplicate name are refused.
- [ ] Use the site's **Upload** button. Choose the category it's listed under on the main menu (Core documents, Solution documents, Industry use case maps, Case studies, Technical documents or Others; a newer version keeps its solution's category), optionally an industry ("Power", "Utilities") shown on the card, and your name if you want the "Contributed by" credit.
- [ ] Working in the Claude desktop app with the **Claude connector** (Download dialog → Claude connector)? Ask Claude to upload the file instead: it takes the same title, category, industry and name, and checks with you before publishing. Claude can also fetch this skill and read existing pages through the connector.
