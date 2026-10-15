/* Runs inside every unlocked page (injected by the password gate; protect.py inlines this file).
   - hides links/cards for solutions the signed-in user can't open
   - adds the signed-in bar: name, Download, Manage users (admin), Sign out
   - site-wide full screen: the site runs inside one full-screen frame, so moving between pages stays full screen
   - Download dialog: this page as one continuous PDF, or an offline HTML file of chosen solutions
   Args: A = allowed slugs (null = all), N = display name, ADM = admin?, B = relative path to site root,
         SOL = [{slug,title}] every solution, SLUG = this page's slug ("home" for the landing page),
         DL = slugs this user may download (null = all), POL = global {slug:{read,download}} switches. */
function FTOOLS(A, N, ADM, B, SOL, SLUG, DL, POL) {
  var REPO = "parth1087-debug/Faclon-Glossary";
  var slugs = SOL.map(function (s) { return s.slug; });
  var base = new URL(B, location.href).pathname;
  var siteURL = new URL(B || "./", location.href).href;
  POL = POL || {};
  var mine = SOL.filter(function (s) { return (!A || A.indexOf(s.slug) >= 0) && (!DL || DL.indexOf(s.slug) >= 0); });

  // admin preview: label solutions whose global switches are off
  if (ADM) document.querySelectorAll("article.card a.main[href]").forEach(function (a) {
    var u; try { u = new URL(a.getAttribute("href"), location.href); } catch (e) { return; }
    var seg = u.pathname.slice(base.length).split("/")[0], p = POL[seg];
    if (!p || (p.read !== false && p.download !== false)) return;
    var t = document.createElement("span");
    t.textContent = p.read === false ? "Hidden from users" : "Download off";
    t.setAttribute("style", "display:inline-block;margin:0 0 8px;font:600 11px Inter,system-ui,sans-serif;letter-spacing:.04em;padding:3px 8px;border-radius:999px;" +
      (p.read === false ? "background:#FCECEA;color:#C0392B" : "background:#FDF3E1;color:#B7791F"));
    a.insertBefore(t, a.firstChild);
  });

  // 1. hide what this user can't open
  if (A) document.querySelectorAll("a[href]").forEach(function (a) {
    var u; try { u = new URL(a.getAttribute("href"), location.href); } catch (e) { return; }
    if (u.origin !== location.origin || u.pathname.indexOf(base) !== 0) return;
    var seg = u.pathname.slice(base.length).split("/")[0];
    if (slugs.indexOf(seg) < 0 || A.indexOf(seg) >= 0) return;
    var c = a.closest("article.card"); (c || a).style.display = "none";
  });

  // 2. signed-in bar (in a shadow root so page styles can't touch it)
  var host = document.createElement("div");
  host.setAttribute("style", "position:fixed;right:12px;bottom:12px;z-index:2147483000");
  document.body.appendChild(host);
  var root = host.attachShadow ? host.attachShadow({ mode: "open" }) : host;
  root.innerHTML = '<style>' +
    ':host,*{box-sizing:border-box;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}' +
    '.bar{display:flex;align-items:center;gap:8px;max-width:calc(100vw - 24px);background:#fff;color:#0F1B2D;border:1px solid #E3E8EF;border-radius:999px;padding:6px 6px 6px 14px;font-size:13px;font-weight:500;box-shadow:0 6px 24px rgba(11,26,48,.14)}' +
    '.who{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}' +
    'button{font:600 12px Inter,system-ui,sans-serif;border:0;border-radius:999px;padding:7px 11px;cursor:pointer;white-space:nowrap;background:#EEF2FF;color:#3D63F5}' +
    'button.pri{background:#3D63F5;color:#fff}button:disabled{opacity:.55;cursor:default}' +
    '.scrim{position:fixed;inset:0;background:rgba(11,26,48,.5);display:flex;align-items:center;justify-content:center;padding:16px}' +
    '.dlg{background:#fff;color:#0F1B2D;border-radius:14px;width:100%;max-width:460px;max-height:calc(100vh - 32px);overflow:auto;padding:22px;box-shadow:0 20px 60px rgba(11,26,48,.3)}' +
    '.dlg h2{margin:0 0 4px;font-size:18px;letter-spacing:-.01em}' +
    '.eb{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#3D63F5;margin:18px 0 6px}' +
    'p{margin:0;font-size:13px;line-height:1.5;color:#3A4A5F}' +
    '.box{border:1px solid #E3E8EF;border-radius:12px;padding:14px;margin-top:6px}' +
    '.sols{display:flex;flex-direction:column;gap:6px;margin:12px 0}' +
    'label{display:flex;align-items:center;gap:10px;font-size:14px;padding:8px 10px;border:1px solid #E3E8EF;border-radius:9px;cursor:pointer}' +
    'label input{width:16px;height:16px;accent-color:#3D63F5;margin:0;flex:none}' +
    '.row{display:flex;gap:8px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-top:12px}' +
    '.link{background:none;padding:0;color:#3D63F5;font-size:13px}' +
    '.big{font-size:14px;padding:10px 16px;border-radius:9px}' +
    '.note{margin-top:16px;font-size:12px;color:#6B7A90}' +
    '.st{font-size:13px;color:#11875F;min-height:18px}.st.err{color:#C0392B}' +
    '.fl{display:block;font-size:12px;font-weight:600;color:#3A4A5F;margin:12px 0 5px}' +
    '.fl em{font-style:normal;font-weight:500;color:#6B7A90}' +
    '.in{display:block;width:100%;font:14px Inter,system-ui,sans-serif;padding:9px 11px;border:1px solid #E3E8EF;border-radius:9px;color:#0F1B2D;background:#fff;outline:none}' +
    '.in:focus{border-color:#3D63F5}textarea.in{min-height:64px;resize:vertical}' +
    '.drop{display:block;border:1.5px dashed #C9D2DF;border-radius:12px;padding:16px;text-align:center;font-size:13px;color:#3A4A5F;cursor:pointer;margin-top:12px}' +
    '.drop b{color:#3D63F5}.drop input{display:none}.drop.has{border-style:solid;border-color:#11875F;background:#E5F5EE}' +
    '.st a{color:#3D63F5;font-weight:600}' +
    '.dlink{display:inline-block;text-decoration:none;font:600 14px Inter,system-ui,sans-serif;padding:10px 16px;border-radius:9px;background:#3D63F5;color:#fff}' +
    '[hidden]{display:none!important}' +
    '@media (max-width:560px){.bar{flex-wrap:wrap;justify-content:flex-end;row-gap:6px;border-radius:18px}}' +
    '</style>' +
    '<div class="bar"><span class="who"></span><button id="fsb" type="button" hidden>Full screen</button><button class="pri" id="dl" type="button">Download</button><button id="upb" type="button" hidden>Upload</button>' +
    (ADM ? '<button id="mu" type="button">Manage users</button>' : '') +
    '<button id="so" type="button">Sign out</button></div>' +
    '<div class="scrim" id="scrim" hidden><div class="dlg" role="dialog" aria-modal="true" aria-labelledby="dh">' +
    '<h2 id="dh">Download</h2><p>Save solutions to share or open offline.</p>' +
    '<div id="pdfSec"><div class="eb">This page as PDF</div><div class="box"><p>One continuous page with no page breaks, exactly as it looks on screen.</p>' +
    '<div class="row"><span class="st" id="pst"></span><button class="pri big" id="pdf" type="button">Download PDF</button></div></div></div>' +
    '<div class="eb">One HTML file</div><div class="box"><p>Pick the solutions to include. You get a single file that opens in any browser, offline and without signing in.</p>' +
    '<div class="sols" id="sols"></div>' +
    '<div class="row"><button class="link" id="all" type="button">Select all</button><button class="pri big" id="html" type="button">Download HTML</button></div>' +
    '<div class="st" id="hst"></div></div>' +
    '<div class="eb">Design guide</div><div class="box"><p>Building your own solution page? The design skill has the Faclon colours, fonts, layout, ready-made components and a starter page, so it matches this site. Use it yourself or give it to an AI assistant.</p>' +
    '<div class="row"><span class="st" id="gst"></span><a class="pri big dlink" id="guide" href="' + B + 'designskill.md" download="Faclon design skill.md">Download design skill</a></div></div>' +
    '<p class="note">Downloaded files are not password-protected. Share them only with people who should see these solutions.</p>' +
    '<div class="row" style="justify-content:flex-end"><button id="close" type="button">Close</button></div>' +
    '</div></div>' +
    '<div class="scrim" id="uscrim" hidden><div class="dlg" role="dialog" aria-modal="true" aria-labelledby="uh">' +
    '<h2 id="uh">Upload a solution page</h2><p>Add a self-contained HTML page (styles and images inside the file). It goes live straight away for admin, super users and contributors; the admin can share it with other users. Building one? Follow the <a href="' + B + 'designskill.md" download="designskill.md" style="color:#3D63F5;font-weight:600">design guide</a> so it matches the site.</p>' +
    '<label class="drop" id="drop"><input type="file" id="uf" accept=".html,.htm,text/html"><span id="ufl"><b>Choose an HTML file</b> or drop it here</span></label>' +
    '<span class="fl">Title</span><input class="in" id="ut" maxlength="80" placeholder="e.g. Cooling Tower Optimisation">' +
    '<span class="fl">Category <em>(optional)</em></span><input class="in" id="uc" maxlength="40" placeholder="e.g. Power, Metals, Utilities">' +
    '<span class="fl">Short description <em>(optional)</em></span><textarea class="in" id="ud" maxlength="240" placeholder="One or two lines shown on the solution card"></textarea>' +
    '<span class="fl">Your name <em>(optional, shown as \u201cContributed by\u201d)</em></span><input class="in" id="un" maxlength="60">' +
    '<div class="st" id="ust" style="margin-top:12px"></div>' +
    '<div class="row" style="justify-content:flex-end"><button id="ucancel" type="button">Cancel</button><button class="pri big" id="ugo" type="button">Upload and publish</button></div>' +
    '</div></div>';
  var $ = function (id) { return root.querySelector("#" + id); };
  root.querySelector(".who").textContent = N;
  // 3. site-wide full screen. Browsers leave full screen whenever a page changes, so full screen
  //    shows the site inside one frame (#fa-fs) and pages change inside that frame instead.
  var shell = null;
  try { if (window.parent !== window && window.parent.document.getElementById("fa-fs")) shell = window.parent; } catch (e) {}
  var topWin = shell || window;
  function fsEnter() {
    if (document.getElementById("fa-fs")) return;
    var box = document.createElement("div"), f = document.createElement("iframe");
    box.id = "fa-fs";
    box.setAttribute("style", "position:fixed;inset:0;z-index:2147483647;background:#0B1A30");
    f.setAttribute("allow", "fullscreen");
    f.setAttribute("title", document.title);
    f.setAttribute("style", "border:0;width:100%;height:100%;display:block;background:#fff");
    f.src = location.href;
    f.onload = function () { try { f.contentWindow.focus(); } catch (e) {} };
    box.appendChild(f); document.body.appendChild(box);
    function done() {
      if (document.fullscreenElement === box) return;
      document.removeEventListener("fullscreenchange", done);
      var href = null; try { href = f.contentWindow.location.href; } catch (e) {}
      box.remove();
      // leaving full screen: stay on the page that was open in it
      if (href && href !== "about:blank" && href.split("#")[0] !== location.href.split("#")[0]) location.href = href;
    }
    document.addEventListener("fullscreenchange", done);
    try {
      var p = box.requestFullscreen();
      if (p && p.catch) p.catch(function () { document.removeEventListener("fullscreenchange", done); box.remove(); });
    } catch (e) { document.removeEventListener("fullscreenchange", done); box.remove(); }
  }
  function fsToggle() {
    if (shell) { try { shell.document.exitFullscreen(); } catch (e) {} return; }
    if (document.fullscreenElement) { document.exitFullscreen().catch(function () {}); return; }
    fsEnter();
  }
  if (shell || document.fullscreenEnabled) {
    $("fsb").hidden = false;
    if (shell) $("fsb").textContent = "Exit full screen";
    $("fsb").onclick = fsToggle;
    // pages with their own full-screen button (#fs, e.g. the Overview) use the site-wide one
    document.addEventListener("click", function (e) {
      var b = e.target && e.target.closest && e.target.closest("#fs");
      if (!b) return;
      e.preventDefault(); e.stopImmediatePropagation(); fsToggle();
    }, true);
  }
  // inside the full-screen frame, links to other websites open in a new tab (many sites refuse to load in a frame)
  if (shell) document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest && e.target.closest("a[href]");
    if (!a || a.target || a.hasAttribute("download")) return;
    var u; try { u = new URL(a.getAttribute("href"), location.href); } catch (x) { return; }
    if ((u.protocol === "http:" || u.protocol === "https:") && u.origin !== location.origin) a.target = "_blank";
  }, true);

  function signOut() { try { FA.clearSession(); } catch (e) {} topWin.location.href = new URL(B || "./", location.href).href; }
  $("so").onclick = signOut;
  if (ADM) $("mu").onclick = function () { location.href = B + "admin/"; };

  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  $("sols").innerHTML = mine.map(function (s) {
    return '<label><input type="checkbox" value="' + esc(s.slug) + '"' + (s.slug === SLUG ? " checked" : "") + '>' + esc(s.title) + '</label>';
  }).join("") || '<p>No solutions are shared with you yet.</p>';
  if (!mine.length) $("dl").hidden = true;
  $("pdfSec").hidden = SLUG === "home" || mine.every(function (s) { return s.slug !== SLUG; });
  $("dl").onclick = function () {
    $("scrim").hidden = false; $("pst").textContent = ""; $("hst").textContent = "";
    if (!$("pdfSec").hidden) fetch(B + SLUG + "/page-pdf.bin?t=" + Date.now(), { method: "HEAD", cache: "no-store" }).then(function (r) {
      if (r.ok) return; $("pdf").disabled = true; $("pst").className = "st"; $("pst").textContent = "The PDF of a newly uploaded page appears after the next site build.";
    }).catch(function () {});
  };
  $("close").onclick = function () { $("scrim").hidden = true; };
  $("guide").onclick = function () { $("gst").textContent = "Downloaded."; };
  $("scrim").onclick = function (e) { if (e.target === $("scrim")) $("scrim").hidden = true; };
  $("all").onclick = function () {
    var b = root.querySelectorAll("#sols input"), on = Array.prototype.some.call(b, function (i) { return !i.checked; });
    b.forEach(function (i) { i.checked = on; });
  };

  var accP = null;
  function access() {
    if (!accP) accP = FA.loadUsers(B).then(function (U) { return FA.access(U, FA.getSession()); });
    return accP;
  }
  function title(slug) { var s = SOL.filter(function (x) { return x.slug === slug; })[0]; return s ? s.title : "Faclon Labs"; }

  // contributor uploads: cards on the landing page + the Upload button
  function cardHTML(slug, m) {
    var tags = m.by ? '<div class="tags"><span>Contributed by ' + esc(m.by) + '</span></div>' : '';
    return '<article class="card live b" data-upload="' + esc(slug) + '"><a class="main" href="' + esc(slug) + '/">' +
      '<div class="top"><span class="sec">' + esc(m.sector || "Contributed") + '</span><span class="pill on">Live</span></div>' +
      '<h3>' + esc(NAMES[slug] || m.title) + '</h3>' + (m.blurb ? '<p>' + esc(m.blurb) + '</p>' : '') + tags +
      '<span class="open">Open solution →</span></a></article>';
  }
  async function uploadCards(acc, U, only) {
    var out = [], ups = U.uploads || {};
    for (var slug in ups) {
      if (only && only.indexOf(slug) < 0) continue;
      try {
        var k = await acc.key(slug); if (!k) continue;
        out.push({ slug: slug, html: cardHTML(slug, JSON.parse(await FA.decrypt(k, ups[slug].meta.iv, ups[slug].meta.ct))) });
      } catch (e) {}
    }
    return out;
  }
  function placeCards(doc, cards) {
    var first = doc.querySelector("article.card"); if (!first || !cards.length) return;
    var box = first.parentNode;
    cards.forEach(function (c) { if (!doc.querySelector('[data-upload="' + c.slug + '"]')) box.insertAdjacentHTML("beforeend", c.html); });
  }
  var usersP = FA.loadUsers(B);
  // names the admin changed in the User Manager (users.json "names"): cards and the browser tab follow them
  var NAMES = {};
  function rename(doc, names, here) {
    doc.querySelectorAll("article.card a.main[href]").forEach(function (a) {
      var u; try { u = new URL(a.getAttribute("href"), location.href); } catch (e) { return; }
      var seg = u.pathname.slice(base.length).split("/")[0], h = a.querySelector("h3");
      if (names[seg] && h) h.textContent = names[seg];
    });
    if (names[here]) doc.title = names[here] + " · Faclon Labs";
  }
  usersP.then(function (U) {
    var n = U.names || {}; for (var k in n) if (n[k] && n[k].t) NAMES[k] = n[k].t;
    rename(document, NAMES, SLUG);
  }).catch(function () {});
  access().then(async function (acc) {
    var U = await usersP;
    if (acc.contrib) $("upb").hidden = false;
    if (SLUG === "home") placeCards(document, await uploadCards(acc, U));
  }).catch(function () {});
  $("upb").onclick = function () { $("uscrim").hidden = false; $("ust").textContent = ""; if (!$("un").value) $("un").value = ADM ? "" : N; };
  $("ucancel").onclick = function () { $("uscrim").hidden = true; };
  $("uscrim").onclick = function (e) { if (e.target === $("uscrim")) $("uscrim").hidden = true; };
  var upFile = null;
  function pick(f) {
    if (!f) return; upFile = f; $("drop").classList.add("has"); $("ufl").textContent = f.name + " (" + (f.size / 1048576).toFixed(1) + " MB)";
    f.text().then(function (t) { var m = t.match(/<title[^>]*>([\s\S]*?)<\/title>/i); if (m && !$("ut").value) $("ut").value = m[1].replace(/\s+/g, " ").trim().slice(0, 80); });
  }
  $("uf").onchange = function () { pick(this.files[0]); };
  $("drop").ondragover = function (e) { e.preventDefault(); };
  $("drop").ondrop = function (e) { e.preventDefault(); pick(e.dataTransfer.files[0]); };
  function slugify(t) { return t.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 50) || "solution"; }
  function gh(token, path, opt) {
    opt = opt || {};
    opt.headers = Object.assign({ "Accept": "application/vnd.github+json", "Authorization": "Bearer " + token, "X-GitHub-Api-Version": "2022-11-28" }, opt.headers || {});
    return fetch(GH_API + path, opt);
  }
  var GH_API = "https://api.github.com/repos/" + REPO;
  $("ugo").onclick = async function () {
    var st = $("ust"), b = this; st.className = "st";
    var t = $("ut").value.trim();
    if (!upFile) { st.className = "st err"; st.textContent = "Choose an HTML file first."; return; }
    if (!t) { st.className = "st err"; st.textContent = "Give the page a title."; return; }
    if (upFile.size > 20 * 1048576) { st.className = "st err"; st.textContent = "That file is over 20 MB. Compress its images and try again."; return; }
    b.disabled = true;
    try {
      var acc = await access(), U = await FA.loadUsers(B), C = acc.contrib;
      if (!C) throw new Error("you don't have contributor rights");
      st.textContent = "Preparing…";
      var token = null;
      if (U.contrib && U.contrib.tok) token = await FA.decrypt(C, U.contrib.tok.iv, U.contrib.tok.ct);
      if (!token && ADM) { try { token = localStorage.getItem("faclon-glossary-gh-token"); } catch (e) {} }
      if (!token) throw new Error("the admin hasn't set up contributor GitHub access yet");
      var html = await upFile.text();
      var taken = {}; (U.solutions || []).forEach(function (x) { taken[x.slug] = 1; }); Object.keys(U.uploads || {}).forEach(function (x) { taken[x] = 1; });
      ["home", "admin", "src"].forEach(function (x) { taken[x] = 1; });
      var slug = slugify(t), n = 2; while (taken[slug]) slug = slugify(t).slice(0, 46) + "-" + n++;
      var K = await FA.uploadKey(C, slug), box = await FA.encrypt(K, html);
      var content = (await FA.sha256hex(html)).slice(0, 16);
      var tpl = (U.solutions || []).filter(function (x) { return !(U.uploads || {})[x.slug]; })[0];
      var tr = await fetch(B + tpl.slug + "/index.html?t=" + Date.now(), { cache: "no-store" });
      var gate = await tr.text();
      var dLine = /\nvar D=\{(up:1,)?slug:"[^"\\]*",base:"[^"\\]*",iv:"[^"\\]*",ct:"[^"\\]*"\};/;
      if (!dLine.test(gate)) throw new Error("couldn't prepare the page wrapper");
      gate = gate.replace(dLine, function () { return '\nvar D={up:1,slug:"' + slug + '",base:"../",iv:"' + box.iv + '",ct:"' + box.ct + '"};'; })
                 .replace(/<meta name="faclon-content" content="[^"]*">/, function () { return '<meta name="faclon-content" content="' + content + '">'; });
      var by = $("un").value.trim();
      var meta = await FA.encrypt(K, JSON.stringify({ title: t, sector: $("uc").value.trim(), blurb: $("ud").value.trim(), by: by, user: N, at: new Date().toISOString() }));
      var sup = await FA.wrapForSuper(U, K);
      st.textContent = "Publishing the page…";
      var r = await gh(token, "/contents/" + slug + "/index.html", { method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Add " + t + " (uploaded by " + (by || N) + ")", content: FA.b64(new TextEncoder().encode(gate)), branch: "main" }) });
      if (r.status === 401 || r.status === 403) throw new Error("GitHub didn't accept the contributor access token; ask the admin to renew it");
      if (!r.ok) throw new Error("GitHub said " + r.status);
      st.textContent = "Adding it to the site…";
      for (var tries = 0; ; tries++) {
        var g = await gh(token, "/contents/users.json?ref=main&t=" + Date.now(), { cache: "no-store" });
        if (!g.ok) throw new Error("couldn't read the user list (" + g.status + ")");
        var gj = await g.json(), J = JSON.parse(new TextDecoder().decode(FA.u8(gj.content.replace(/\s/g, ""))));
        J.solutions = (J.solutions || []).filter(function (x) { return x.slug !== slug; }).concat([{ slug: slug, title: t }]);
        J.uploads = J.uploads || {}; J.uploads[slug] = { meta: meta, at: new Date().toISOString() };
        if (sup) { J.vault = J.vault || {}; J.vault[slug] = sup; }
        var pr = await gh(token, "/contents/users.json", { method: "PUT", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: "Register uploaded page " + t, content: FA.b64(new TextEncoder().encode(JSON.stringify(J, null, 1) + "\n")), sha: gj.sha, branch: "main" }) });
        if (pr.ok) break;
        if ((pr.status === 409 || pr.status === 422) && tries < 4) { await new Promise(function (ok) { setTimeout(ok, 800 * (tries + 1)); }); continue; }
        throw new Error("couldn't register the page (" + pr.status + ")");
      }
      st.innerHTML = 'Published. It will be live in about a minute: <a href="' + esc(B + slug + "/") + '">open ' + esc(t) + '</a>';
      upFile = null; $("drop").classList.remove("has"); $("ufl").innerHTML = "<b>Choose an HTML file</b> or drop it here"; $("ut").value = ""; $("uc").value = ""; $("ud").value = ""; $("uf").value = "";
    } catch (e) { st.className = "st err"; st.textContent = "Couldn't upload: " + e.message; }
    b.disabled = false;
  };
  function save(blob, name) {
    var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
  }
  function fname(t) { return t.replace(/[\\/:*?"<>|]+/g, "").trim(); }
  async function pageHTML(acc, slug) {
    var url = B + (slug === "home" ? "" : slug + "/") + "index.html?t=" + Date.now();
    var r = await fetch(url, { cache: "no-store" }); if (!r.ok) throw new Error("couldn't load " + slug);
    var t = await r.text();
    var iv = (t.match(/iv:"([^"]+)"/) || [])[1], ct = (t.match(/ct:"([^"]+)"/) || [])[1];
    var k = await acc.key(slug); if (!k || !iv || !ct) throw new Error("no access to " + slug);
    return FA.decrypt(k, iv, ct);
  }

  $("pdf").onclick = async function () {
    var b = this, st = $("pst"); b.disabled = true; st.className = "st"; st.textContent = "Preparing PDF…";
    try {
      var acc = await access(), k = await acc.dkey(SLUG);
      if (!k) throw new Error("downloads are switched off for this solution");
      var r = await fetch(B + SLUG + "/page-pdf.bin?t=" + Date.now(), { cache: "no-store" });
      if (!r.ok) throw new Error("the PDF isn't available yet");
      var all = new Uint8Array(await r.arrayBuffer());
      var pdf = await FA.decryptBytes(k, all.slice(0, 12), all.slice(12));
      save(new Blob([pdf], { type: "application/pdf" }), fname(title(SLUG) + " - Faclon Labs") + ".pdf");
      st.textContent = "Downloaded.";
    } catch (e) { st.className = "st err"; st.textContent = "Couldn't download: " + e.message; }
    b.disabled = false;
  };

  $("html").onclick = async function () {
    var picked = Array.prototype.map.call(root.querySelectorAll("#sols input:checked"), function (i) { return i.value; });
    var st = $("hst"), b = this; st.className = "st";
    if (!picked.length) { st.className = "st err"; st.textContent = "Tick at least one solution."; return; }
    b.disabled = true; st.textContent = "Building your file…";
    try {
      var acc = await access(), pages = {};
      pages.home = await pageHTML(acc, "home");
      for (var i = 0; i < picked.length; i++) { st.textContent = "Adding " + title(picked[i]) + "…"; pages[picked[i]] = await pageHTML(acc, picked[i]); }
      var start = picked.length === 1 ? picked[0] : "home";
      var name = picked.length === 1 ? title(picked[0]) + " - Faclon Labs" : "Faclon Labs Solutions";
      var cards = await uploadCards(acc, await usersP, picked);
      var json = JSON.stringify({ pages: pages, picked: picked, all: slugs, start: start, site: siteURL, cards: cards, names: NAMES }).replace(/</g, "\\u003c");
      var html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' +
        '<meta name="robots" content="noindex"><title>' + esc(name) + '</title>' +
        '<style>html,body{margin:0;height:100%;background:#fff}iframe{border:0;width:100%;height:100%;display:block}</style></head>' +
        '<body><iframe id="v" title="' + esc(name) + '"></iframe>' +
        '<script type="application/json" id="data">' + json + '<\/script>' +
        '<script>(' + VIEWER.toString() + ')()<\/script></body></html>';
      save(new Blob([html], { type: "text/html" }), fname(name) + ".html");
      st.textContent = "Downloaded (" + (html.length / 1048576).toFixed(1) + " MB).";
    } catch (e) { st.className = "st err"; st.textContent = "Couldn't build the file: " + e.message; }
    b.disabled = false;
  };

  /* The offline viewer that runs inside the downloaded HTML file. */
  function VIEWER() {
    var D = JSON.parse(document.getElementById("data").textContent), v = document.getElementById("v");
    function route() { var h = location.hash.replace(/^#\/?/, ""); return D.pages[h] ? h : D.start; }
    function target(href, from) {
      if (!href || href.charAt(0) === "#") return null;
      var u; try { u = new URL(href, D.site + (from === "home" ? "" : from + "/")); } catch (e) { return null; }
      if (u.href.indexOf(D.site) !== 0) return { ext: u.href };
      var rest = u.href.slice(D.site.length).split("#")[0].split("?")[0];
      if (rest === "" || rest === "index.html") return { page: "home" };
      var seg = rest.split("/")[0], tail = rest.slice(seg.length);
      if (D.all.indexOf(seg) >= 0 && (tail === "/" || tail === "/index.html" || tail === "")) return D.pages[seg] ? { page: seg } : { hide: true };
      return { ext: u.href };
    }
    function show() {
      var p = route();
      v.onload = function () {
        var doc = v.contentDocument; if (!doc) return;
        var nm = D.names || {};
        if (nm[p]) doc.title = nm[p] + " · Faclon Labs";
        document.title = doc.title || document.title;
        if (p === "home") doc.querySelectorAll("article.card a.main[href]").forEach(function (a) {
          var t = target(a.getAttribute("href"), "home"), h = a.querySelector("h3");
          if (t && t.page && nm[t.page] && h) h.textContent = nm[t.page];
        });
        if (p === "home" && D.cards && D.cards.length) {
          var first = doc.querySelector("article.card");
          if (first) D.cards.forEach(function (c) { first.parentNode.insertAdjacentHTML("beforeend", c.html); });
        }
        doc.querySelectorAll("a[href]").forEach(function (a) {
          var t = target(a.getAttribute("href"), p); if (!t) return;
          if (t.hide) { var c = a.closest("article.card"); (c || a).style.display = "none"; return; }
          if (t.ext) { a.href = t.ext; a.target = "_blank"; a.rel = "noopener"; return; }
          a.addEventListener("click", function (e) { e.preventDefault(); location.hash = "#/" + t.page; });
        });
      };
      v.srcdoc = D.pages[p];
    }
    window.addEventListener("hashchange", show);
    show();
  }
}
