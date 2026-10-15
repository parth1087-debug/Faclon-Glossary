/* Runs inside every unlocked page (injected by the password gate; protect.py inlines this file).
   - hides links/cards for solutions the signed-in user can't open
   - adds the signed-in bar: name, Download, Manage users (admin), Sign out
   - Download dialog: this page as one continuous PDF, or an offline HTML file of chosen solutions
   Args: A = allowed slugs (null = all), N = display name, ADM = admin?, B = relative path to site root,
         SOL = [{slug,title}] every solution, SLUG = this page's slug ("home" for the landing page). */
function FTOOLS(A, N, ADM, B, SOL, SLUG) {
  var slugs = SOL.map(function (s) { return s.slug; });
  var base = new URL(B, location.href).pathname;
  var siteURL = new URL(B || "./", location.href).href;
  var mine = SOL.filter(function (s) { return !A || A.indexOf(s.slug) >= 0; });

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
    '[hidden]{display:none!important}' +
    '</style>' +
    '<div class="bar"><span class="who"></span><button class="pri" id="dl" type="button">Download</button>' +
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
    '<p class="note">Downloaded files are not password-protected. Share them only with people who should see these solutions.</p>' +
    '<div class="row" style="justify-content:flex-end"><button id="close" type="button">Close</button></div>' +
    '</div></div>';
  var $ = function (id) { return root.querySelector("#" + id); };
  root.querySelector(".who").textContent = N;
  function signOut() { try { FA.clearSession(); } catch (e) {} location.href = B || "./"; }
  $("so").onclick = signOut;
  if (ADM) $("mu").onclick = function () { location.href = B + "admin/"; };

  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  $("sols").innerHTML = mine.map(function (s) {
    return '<label><input type="checkbox" value="' + esc(s.slug) + '"' + (s.slug === SLUG ? " checked" : "") + '>' + esc(s.title) + '</label>';
  }).join("") || '<p>No solutions are shared with you yet.</p>';
  if (!mine.length) $("html").disabled = true;
  $("pdfSec").hidden = SLUG === "home" || mine.every(function (s) { return s.slug !== SLUG; });
  $("dl").onclick = function () { $("scrim").hidden = false; $("pst").textContent = ""; $("hst").textContent = ""; };
  $("close").onclick = function () { $("scrim").hidden = true; };
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
      var acc = await access(), k = await acc.key(SLUG);
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
      var json = JSON.stringify({ pages: pages, picked: picked, all: slugs, start: start, site: siteURL }).replace(/</g, "\\u003c");
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
        document.title = doc.title || document.title;
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
