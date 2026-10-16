/* Faclon Labs solution library: MCP connector for contributors.
   build_connector.py puts src/shared/auth_core.js (the FA helpers) in front of this file, so the
   connector signs in and decrypts exactly like the website does. It runs on the user's own computer
   (Claude Desktop extension or any stdio MCP client): the password never leaves that computer, and the
   connector only talks to the public site and the GitHub API.
   Env: FACLON_USERNAME, FACLON_PASSWORD, FACLON_DOWNLOAD_DIR (optional), FACLON_SITE (optional). */
/* eslint-disable no-var */
var VERSION = "__VERSION__";
var REPO = "parth1087-debug/Faclon-Glossary";
var nodeFs = require("fs"), nodePath = require("path"), nodeOs = require("os");

function setting(name) {
  var v = process.env[name];
  // Claude Desktop passes "${user_config.x}" through untouched when an optional field is left empty
  return v && v.indexOf("${") < 0 ? v.trim() : "";
}
var SITE = (setting("FACLON_SITE") || "https://parth1087-debug.github.io/Faclon-Glossary/").replace(/\/?$/, "/");
function downloadDir() {
  var d = setting("FACLON_DOWNLOAD_DIR") || nodePath.join(nodeOs.homedir(), "Downloads");
  if (d.charAt(0) === "~") d = nodePath.join(nodeOs.homedir(), d.slice(1));
  return nodePath.join(d, "Faclon Labs");
}
function log(m) { process.stderr.write("[faclon-glossary] " + m + "\n"); }

/* ---------- site access ---------- */
var usersCache = null, usersAt = 0, sessionCache = null;
async function getText(url) {
  var r = await fetch(url, { cache: "no-store", headers: { "User-Agent": "faclon-glossary-connector/" + VERSION } });
  if (!r.ok) throw new Error("couldn't load " + url.replace(SITE, "") + " (" + r.status + ")");
  return r.text();
}
async function users(fresh) {
  if (fresh || !usersCache || Date.now() - usersAt > 60000) {
    usersCache = JSON.parse(await getText(SITE + "users.json?t=" + Date.now()));
    usersAt = Date.now();
  }
  return usersCache;
}
async function signIn() {
  var name = setting("FACLON_USERNAME"), pw = process.env.FACLON_PASSWORD || "";
  if (!name || !pw || pw.indexOf("${") === 0) throw new Error("Add your Faclon username and password in the connector's settings in Claude.");
  var U = await users();
  if (!sessionCache) {
    try { sessionCache = await FA.login(U, name, pw); }
    catch (e) { throw new Error("The Faclon username or password is wrong, or this user was removed. Fix them in the connector's settings in Claude."); }
  }
  var acc;
  try { acc = await FA.access(U, sessionCache); }
  catch (e) { sessionCache = null; usersCache = null; throw new Error("Your sign-in is no longer valid (the user was changed or removed). Check the username and password in the connector's settings."); }
  if (!acc.contrib) throw new Error("This connector is for contributors. Ask the Faclon admin to tick Contributor for your user in the User Manager.");
  return { U: U, acc: acc };
}
async function canOpen(acc, slug) { try { return !!(await acc.key(slug)); } catch (e) { return false; } }
function canSave(U, acc, slug) {
  if (!FA.canDownload(U, slug)) return false;
  return acc.downloadable === null || acc.downloadable.indexOf(slug) >= 0;
}
async function catalogue() {
  var s = await signIn(), U = s.U, acc = s.acc, out = [];
  var sols = (U.solutions || []).slice();
  Object.keys(U.uploads || {}).forEach(function (slug) { if (!sols.some(function (x) { return x.slug === slug; })) sols.push({ slug: slug, title: slug }); });
  for (var i = 0; i < sols.length; i++) {
    var slug = sols[i].slug;
    if (!(await canOpen(acc, slug))) continue;
    var item = { slug: slug, title: sols[i].title, url: SITE + slug + "/", download: canSave(U, acc, slug) };
    var up = (U.uploads || {})[slug];
    if (up) {
      item.uploaded = true;
      try {
        var m = JSON.parse(await FA.decrypt(await acc.key(slug), up.meta.iv, up.meta.ct));
        item.title = (U.names && U.names[slug] && U.names[slug].t) || m.title || item.title;
        if (m.sector) item.category = m.sector;
        if (m.blurb) item.description = m.blurb;
        if (m.by) item.contributedBy = m.by;
      } catch (e) {}
    }
    out.push(item);
  }
  return { U: U, acc: acc, list: out };
}
async function pageHTML(acc, slug) {
  var t = await getText(SITE + slug + "/index.html?t=" + Date.now());
  var iv = (t.match(/iv:"([^"]+)"/) || [])[1], ct = (t.match(/ct:"([^"]+)"/) || [])[1];
  var k = await acc.key(slug);
  if (!k || !iv || !ct) throw new Error("you don't have access to " + slug);
  return FA.decrypt(k, iv, ct);
}
function find(list, q) {
  var s = String(q || "").trim().toLowerCase();
  var hit = list.filter(function (x) { return x.slug === s; })[0] ||
            list.filter(function (x) { return x.title.toLowerCase() === s; })[0] ||
            list.filter(function (x) { return x.title.toLowerCase().indexOf(s) >= 0 || x.slug.indexOf(s.replace(/\s+/g, "-")) >= 0; })[0];
  if (!hit) throw new Error('No solution you can open matches "' + q + '". Use list_solutions to see them.');
  return hit;
}

/* ---------- HTML to readable text ---------- */
var ENT = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", rarr: "→", larr: "←", harr: "↔", rsquo: "’", lsquo: "‘", rdquo: "”", ldquo: "“", ndash: "–", mdash: "—", middot: "·", bull: "•", hellip: "…", times: "×", deg: "°", plusmn: "±", copy: "©", reg: "®", trade: "™", le: "≤", ge: "≥", asymp: "≈", rupee: "₹" };
function toText(html) {
  var title = ((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || "").trim();
  var s = (html.match(/<body[^>]*>([\s\S]*)<\/body>/i) || [, html])[1];
  s = s.replace(/<(script|style|svg|noscript|template|canvas)\b[\s\S]*?<\/\1>/gi, " ").replace(/<!--[\s\S]*?-->/g, " ");
  s = s.replace(/<img\b[^>]*\balt="([^"]+)"[^>]*>/gi, " [image: $1] ");
  s = s.replace(/<h([1-6])\b[^>]*>/gi, function (m, n) { return "\n\n" + "#".repeat(+n) + " "; }).replace(/<\/h[1-6]>/gi, "\n");
  s = s.replace(/<\/(span|a|button|small|b|strong|em|i|label)>/gi, " ");
  s = s.replace(/<li\b[^>]*>/gi, "\n- ").replace(/<br\s*\/?>/gi, "\n");
  s = s.replace(/<\/t[dh]>/gi, " | ").replace(/<tr\b[^>]*>/gi, "\n| ");
  s = s.replace(/<\/(p|div|section|article|header|footer|nav|main|ul|ol|table|figure|figcaption|blockquote|summary|details|dt|dd|label)>/gi, "\n");
  s = s.replace(/<[^>]+>/g, "");
  s = s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, function (m, e) {
    if (e.charAt(0) === "#") { var c = e.charAt(1).toLowerCase() === "x" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10); try { return String.fromCodePoint(c); } catch (x) { return m; } }
    return ENT[e.toLowerCase()] != null ? ENT[e.toLowerCase()] : m;
  });
  s = s.split("\n").map(function (l) { return l.replace(/[ \t\u00a0]+/g, " ").replace(/ ([,.;:!?)])/g, "$1").trim(); }).join("\n").replace(/\n{3,}/g, "\n\n").trim();
  return (title ? "Title: " + title + "\n\n" : "") + s;
}
function lightHTML(html) {
  return html.replace(/(["'(])data:([a-z0-9.+-]+\/[a-z0-9.+-]+)[^"')]{200,}/gi, function (m, q, type) { return q + "data:" + type + ";base64,[image data removed]"; });
}

/* ---------- files ---------- */
function safeName(t) { return String(t).replace(/[\\/:*?"<>|\u0000-\u001f]+/g, "").replace(/\s+/g, " ").trim().slice(0, 120) || "page"; }
function writeOut(name, data) {
  var dir = downloadDir();
  nodeFs.mkdirSync(dir, { recursive: true });
  var p = nodePath.join(dir, name);
  nodeFs.writeFileSync(p, data);
  return p;
}

/* ---------- GitHub (uploads) ---------- */
function gh(token, path, opt) {
  opt = opt || {};
  opt.headers = Object.assign({ "Accept": "application/vnd.github+json", "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "faclon-glossary-connector/" + VERSION }, opt.headers || {});
  return fetch((setting("FACLON_GITHUB_API") || "https://api.github.com") + "/repos/" + REPO + path, opt);
}
function slugify(t) { return t.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 50) || "solution"; }
function sleep(ms) { return new Promise(function (ok) { setTimeout(ok, ms); }); }

/* ---------- tools ---------- */
var TOOLS = [
  {
    name: "list_solutions",
    title: "List Faclon solutions",
    description: "Lists the Faclon Labs solution pages this user can open, with each page's slug, title, link and whether it can be downloaded. Includes pages uploaded by contributors. Call this first to find the slug for the other tools.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true, openWorldHint: true },
    run: async function () {
      var c = await catalogue();
      if (!c.list.length) return "No solution pages are shared with this user yet. Ask the Faclon admin to tick some in the User Manager.";
      var lines = c.list.map(function (x) {
        return "- " + x.title + " (slug: " + x.slug + ")" + (x.category ? " · " + x.category : "") +
          (x.uploaded ? " · uploaded" + (x.contributedBy ? " by " + x.contributedBy : "") : "") +
          " · " + (x.download ? "can download" : "view only") + "\n  " + x.url + (x.description ? "\n  " + x.description : "");
      });
      return "Signed in as " + c.acc.name + ". " + c.list.length + " solution page" + (c.list.length === 1 ? "" : "s") + " you can open:\n\n" + lines.join("\n") +
        "\n\nThe site and every page need the same Faclon sign-in in a browser.";
    }
  },
  {
    name: "read_page",
    title: "Read a solution page",
    description: "Returns the content of one Faclon solution page. format \"text\" (default) gives readable text with headings, lists and tables; \"html\" gives the page source (embedded images are shortened) so you can study its layout and styling before building a new page.",
    inputSchema: { type: "object", properties: {
      solution: { type: "string", description: "Slug or title from list_solutions, e.g. \"steam-trap-monitoring\"" },
      format: { type: "string", enum: ["text", "html"], default: "text" } }, required: ["solution"], additionalProperties: false },
    annotations: { readOnlyHint: true, openWorldHint: true },
    run: async function (a) {
      var c = await catalogue(), hit = find(c.list, a.solution), html = await pageHTML(c.acc, hit.slug);
      var LIMIT = 250000;
      var body = a.format === "html" ? lightHTML(html) : toText(html);
      var cut = body.length > LIMIT;
      return hit.title + " — " + hit.url + "\n\n" + (cut ? body.slice(0, LIMIT) + "\n\n[cut at " + LIMIT + " characters; use download_pages for the full file]" : body);
    }
  },
  {
    name: "download_pages",
    title: "Download solution pages",
    description: "Saves Faclon solution pages to the user's computer, in the \"Faclon Labs\" folder inside their chosen downloads folder: as a self-contained HTML file that opens offline, as a one-page PDF, or both. Only pages with downloads allowed for this user can be saved.",
    inputSchema: { type: "object", properties: {
      solutions: { type: "array", items: { type: "string" }, description: "Slugs or titles from list_solutions. Use [\"all\"] for every page this user can download." },
      format: { type: "string", enum: ["html", "pdf", "both"], default: "pdf" } }, required: ["solutions"], additionalProperties: false },
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    run: async function (a) {
      var c = await catalogue(), fmt = a.format || "pdf", want = a.solutions || [], done = [], skipped = [];
      var picked = want.some(function (w) { return String(w).toLowerCase() === "all"; }) ? c.list.filter(function (x) { return x.download; }) :
        want.map(function (w) { return find(c.list, w); });
      if (!picked.length) return "None of your pages can be downloaded. The admin controls downloads in the User Manager.";
      for (var i = 0; i < picked.length; i++) {
        var x = picked[i], base = safeName(x.title + " - Faclon Labs");
        if (!x.download) { skipped.push(x.title + ": downloads are off for you or for this solution"); continue; }
        try {
          if (fmt === "html" || fmt === "both") done.push(writeOut(base + ".html", await pageHTML(c.acc, x.slug)));
          if (fmt === "pdf" || fmt === "both") {
            var k = await c.acc.dkey(x.slug);
            if (!k) throw new Error("downloads are off");
            var r = await fetch(SITE + x.slug + "/page-pdf.bin?t=" + Date.now(), { cache: "no-store" });
            if (!r.ok) throw new Error(x.uploaded ? "the PDF of a newly uploaded page appears after the next site build" : "the PDF isn't available (" + r.status + ")");
            var all = new Uint8Array(await r.arrayBuffer());
            done.push(writeOut(base + ".pdf", Buffer.from(await FA.decryptBytes(k, all.slice(0, 12), all.slice(12)))));
          }
        } catch (e) { skipped.push(x.title + ": " + e.message); }
      }
      return (done.length ? "Saved:\n" + done.map(function (p) { return "- " + p; }).join("\n") : "Nothing was saved.") +
        (skipped.length ? "\n\nNot saved:\n" + skipped.map(function (s) { return "- " + s; }).join("\n") : "") +
        (done.length ? "\n\nDownloaded files are not password-protected; share them only with people who should see these solutions." : "");
    }
  },
  {
    name: "get_design_skill",
    title: "Get the Faclon design skill",
    description: "Returns the Faclon design skill (designskill.md): colours, fonts, layout, components, content rules and a starter page for building a new solution page that matches the site. Read it before writing any page you will upload. Set save to true to also save it to the downloads folder.",
    inputSchema: { type: "object", properties: { save: { type: "boolean", default: false } }, additionalProperties: false },
    annotations: { readOnlyHint: true, openWorldHint: true },
    run: async function (a) {
      await signIn();
      var md = await getText(SITE + "designskill.md?t=" + Date.now());
      var where = a.save ? "Saved to " + writeOut("Faclon design skill.md", md) + "\n\n" : "";
      return where + md;
    }
  },
  {
    name: "upload_page",
    title: "Upload a new solution page",
    description: "Publishes a self-contained HTML file (styles and images inside the file) as a new Faclon solution page. It goes live on the site in about a minute for the admin, super users and contributors; the admin can then share it with other users. Give either file_path (a file on this computer) or html. Confirm the title with the user before uploading, and follow get_design_skill so the page matches the site.",
    inputSchema: { type: "object", properties: {
      title: { type: "string", description: "Page title shown on the solution card, e.g. \"Cooling Tower Optimisation\"" },
      file_path: { type: "string", description: "Full path of the HTML file on this computer" },
      html: { type: "string", description: "The full HTML of the page, if there is no file" },
      category: { type: "string", description: "Optional card category, e.g. Power, Metals, Utilities" },
      description: { type: "string", description: "Optional one or two lines shown on the solution card" },
      contributor_name: { type: "string", description: "Optional name shown as \"Contributed by\"; defaults to the signed-in user's name" } },
      required: ["title"], additionalProperties: false },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: true },
    run: async function (a) {
      var t = String(a.title || "").trim().slice(0, 80);
      if (!t) throw new Error("Give the page a title.");
      var html = a.html;
      if (!html && a.file_path) {
        var fp = a.file_path.charAt(0) === "~" ? nodePath.join(nodeOs.homedir(), a.file_path.slice(1)) : a.file_path;
        if (!nodeFs.existsSync(fp)) throw new Error("Couldn't find " + fp + " on this computer.");
        html = nodeFs.readFileSync(fp, "utf8");
      }
      if (!html) throw new Error("Give either file_path or html.");
      if (Buffer.byteLength(html) > 20 * 1048576) throw new Error("That page is over 20 MB. Compress its images and try again.");
      if (!/<html[\s>]/i.test(html) || !/<body[\s>]/i.test(html)) throw new Error("That doesn't look like a complete HTML page (it needs <html> and <body>).");
      var s = await signIn(), C = s.acc.contrib, U = await users(true);
      var token = U.contrib && U.contrib.tok ? await FA.decrypt(C, U.contrib.tok.iv, U.contrib.tok.ct) : null;
      if (!token) throw new Error("The admin hasn't set up contributor GitHub access yet (User Manager → Contributor GitHub access).");
      var taken = { home: 1, admin: 1, src: 1, connector: 1 };
      (U.solutions || []).forEach(function (x) { taken[x.slug] = 1; }); Object.keys(U.uploads || {}).forEach(function (x) { taken[x] = 1; });
      var slug = slugify(t), n = 2; while (taken[slug]) slug = slugify(t).slice(0, 46) + "-" + n++;
      var K = await FA.uploadKey(C, slug), box = await FA.encrypt(K, html);
      var content = (await FA.sha256hex(html)).slice(0, 16);
      var tpl = (U.solutions || []).filter(function (x) { return !(U.uploads || {})[x.slug]; })[0];
      if (!tpl) throw new Error("couldn't find a page to copy the sign-in wrapper from");
      var gate = await getText(SITE + tpl.slug + "/index.html?t=" + Date.now());
      var dLine = /\nvar D=\{(up:1,)?slug:"[^"\\]*",base:"[^"\\]*",iv:"[^"\\]*",ct:"[^"\\]*"\};/;
      if (!dLine.test(gate)) throw new Error("couldn't prepare the page wrapper");
      gate = gate.replace(dLine, function () { return '\nvar D={up:1,slug:"' + slug + '",base:"../",iv:"' + box.iv + '",ct:"' + box.ct + '"};'; })
                 .replace(/<meta name="faclon-content" content="[^"]*">/, function () { return '<meta name="faclon-content" content="' + content + '">'; });
      var by = String(a.contributor_name || s.acc.name || "").trim().slice(0, 60);
      var meta = await FA.encrypt(K, JSON.stringify({ title: t, sector: String(a.category || "").trim().slice(0, 40), blurb: String(a.description || "").trim().slice(0, 240), by: by, user: s.acc.name, at: new Date().toISOString(), via: "connector" }));
      var sup = await FA.wrapForSuper(U, K);
      var r = await gh(token, "/contents/" + slug + "/index.html", { method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Add " + t + " (uploaded by " + (by || s.acc.name) + " via Claude connector)", content: Buffer.from(gate, "utf8").toString("base64"), branch: "main" }) });
      if (r.status === 401 || r.status === 403) throw new Error("GitHub didn't accept the contributor access token; ask the admin to renew it.");
      if (!r.ok) throw new Error("GitHub said " + r.status + " while publishing the page.");
      for (var tries = 0; ; tries++) {
        var g = await gh(token, "/contents/users.json?ref=main&t=" + Date.now());
        if (!g.ok) throw new Error("couldn't read the user list (" + g.status + ")");
        var gj = await g.json(), J = JSON.parse(Buffer.from(gj.content.replace(/\s/g, ""), "base64").toString("utf8"));
        J.solutions = (J.solutions || []).filter(function (x) { return x.slug !== slug; }).concat([{ slug: slug, title: t }]);
        J.uploads = J.uploads || {}; J.uploads[slug] = { meta: meta, at: new Date().toISOString() };
        if (sup) { J.vault = J.vault || {}; J.vault[slug] = sup; }
        var pr = await gh(token, "/contents/users.json", { method: "PUT", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: "Register uploaded page " + t, content: Buffer.from(JSON.stringify(J, null, 1) + "\n", "utf8").toString("base64"), sha: gj.sha, branch: "main" }) });
        if (pr.ok) break;
        if ((pr.status === 409 || pr.status === 422) && tries < 4) { await sleep(800 * (tries + 1)); continue; }
        throw new Error("the page was published but couldn't be registered (" + pr.status + "); ask the admin to check users.json");
      }
      usersCache = null;
      return "Published \"" + t + "\". It will be live in about a minute at " + SITE + slug + "/ (sign in with your Faclon login). " +
        "It shows on the landing page for the admin, super users and contributors; the admin can share it with other users in the User Manager. Its PDF download appears after the next site build.";
    }
  }
];

/* ---------- MCP over stdio (newline-delimited JSON-RPC) ---------- */
var INSTRUCTIONS = "Faclon Labs solution library. list_solutions shows the pages this user can open; read_page returns a page as text or HTML; " +
  "download_pages saves pages as HTML or PDF; get_design_skill returns the design rules to follow before building a new page; upload_page publishes a new page " +
  "(it goes live straight away, so confirm the title and file with the user first). Pages are confidential to Faclon and its customers.";
function send(o) { process.stdout.write(JSON.stringify(o) + "\n"); }
async function handle(m) {
  if (!m || typeof m !== "object" || !m.method) return;
  var reply = function (result) { if (m.id !== undefined && m.id !== null) send({ jsonrpc: "2.0", id: m.id, result: result }); };
  var fail = function (code, msg) { if (m.id !== undefined && m.id !== null) send({ jsonrpc: "2.0", id: m.id, error: { code: code, message: msg } }); };
  switch (m.method) {
    case "initialize":
      return reply({ protocolVersion: (m.params && m.params.protocolVersion) || "2025-06-18",
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: "faclon-glossary", title: "Faclon Labs solutions", version: VERSION }, instructions: INSTRUCTIONS });
    case "ping": return reply({});
    case "tools/list":
      return reply({ tools: TOOLS.map(function (t) { return { name: t.name, title: t.title, description: t.description, inputSchema: t.inputSchema, annotations: t.annotations }; }) });
    case "resources/list": return reply({ resources: [] });
    case "resources/templates/list": return reply({ resourceTemplates: [] });
    case "prompts/list": return reply({ prompts: [] });
    case "tools/call": {
      var p = m.params || {}, tool = TOOLS.filter(function (t) { return t.name === p.name; })[0];
      if (!tool) return fail(-32602, "Unknown tool: " + p.name);
      try { return reply({ content: [{ type: "text", text: await tool.run(p.arguments || {}) }] }); }
      catch (e) { log(p.name + ": " + (e && e.message || e)); return reply({ content: [{ type: "text", text: "Couldn't " + p.name.replace(/_/g, " ") + ": " + (e && e.message || e) }], isError: true }); }
    }
    default:
      if (m.method.indexOf("notifications/") === 0) return;
      return fail(-32601, "Method not found: " + m.method);
  }
}
if (!globalThis.crypto || !globalThis.crypto.subtle) globalThis.crypto = require("crypto").webcrypto;
var buf = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", function (chunk) {
  buf += chunk;
  var i;
  while ((i = buf.indexOf("\n")) >= 0) {
    var line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!line) continue;
    var msg; try { msg = JSON.parse(line); } catch (e) { send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }); continue; }
    handle(msg).catch(function (e) { log(String(e && e.stack || e)); });
  }
});
process.stdin.on("end", function () { process.exit(0); });
log("ready (" + VERSION + "), site " + SITE);
