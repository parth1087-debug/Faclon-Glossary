/* Shared crypto + session helpers for the password gate and the User Manager.
   protect.py inlines this file into every protected page and into admin/index.html.
   Must stay in step with the key derivation in protect.py:
     master      = PBKDF2-SHA256(admin password, users.salt, users.iter)
     page key    = HMAC-SHA256(master, "page:" + slug)       (slug "home" = landing page)
     admin key   = HMAC-SHA256(master, "admin")               (encrypts user metadata)
     check       = HMAC-SHA256(master, "check")               (verifies the admin password)
     all key     = HMAC-SHA256(master, "all")                 (super users hold this one key)
     vault[slug] = page key (base64) encrypted with the all key; users.vault, kept current by
                   protect.py, so super users can open every page, including ones added later
     pdf key     = HMAC-SHA256(master, "pdf:" + slug)        (encrypts <slug>/page-pdf.bin)
     dall key    = HMAC-SHA256(master, "dall")                (super users with the Can download right)
     dvault[slug]= pdf key encrypted with the dall key, only for solutions whose Download switch is on
     contrib key = HMAC-SHA256(master, "contrib")             (contributors hold it; unlocks users.contrib.tok)
     upload key  = HMAC-SHA256(contrib key, "page:" + slug)  page key of a contributor upload (users.uploads)
     spub/spriv  = ECDH P-256 key pair; spriv (PKCS8) is locked with the all key. Contributors lock a new
                   upload's page key to spub, so super users see uploads at once: vault entry {e, iv, ct}.
     policy[slug]= {read, download}: global switches set in the User Manager (missing = both on).
                   Read off: the page key leaves every keyring and the vault. Download off: the pdf key
                   leaves every keyring and the dvault, and download options are hidden.
     guides      = GUIDES (the Read me): not solutions. Encrypted with the landing-page key so every signed-in
                   user can open them; never in solutions, keyrings, vaults or downloads. Mirror of GUIDES in protect.py.
     versions[slug] = {of: first version's slug, n: version number}. A newer version of a solution is a
                   separate page with the same name; the first version has no entry (it is v1). The version
                   number is shown next to the name (chip, "Name v2" in lists) and can't be edited. Uploads add entries; the User
                   Manager's "use latest" turns Read off for older versions and gives users the newest.
     keyring     = {n, p:{slug:page key}, d:{slug:pdf key}, c?: contrib key, all?/a?/da?: super user}
     user key    = PBKDF2-SHA256(user password, user.s, users.iter)  (encrypts the user's keyring)
     user id     = SHA-256(users.salt + "|" + lower(username)) as hex
*/
var FA = (function () {
  var te = new TextEncoder(), td = new TextDecoder();
  var SESSION = "faclon-glossary-session";
  function u8(s) { var b = atob(s), a = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) a[i] = b.charCodeAt(i); return a; }
  function b64(buf) { var a = new Uint8Array(buf), s = ""; for (var i = 0; i < a.length; i += 8192) s += String.fromCharCode.apply(null, a.subarray(i, i + 8192)); return btoa(s); }
  async function pbkdf2(pw, salt, iter) {
    var k = await crypto.subtle.importKey("raw", te.encode(pw), "PBKDF2", false, ["deriveBits"]);
    return new Uint8Array(await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: salt, iterations: iter }, k, 256));
  }
  async function hmac(raw, msg) {
    var k = await crypto.subtle.importKey("raw", raw, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
    return new Uint8Array(await crypto.subtle.sign("HMAC", k, te.encode(msg)));
  }
  async function encrypt(raw, text) {
    var iv = crypto.getRandomValues(new Uint8Array(12));
    var k = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["encrypt"]);
    return { iv: b64(iv), ct: b64(await crypto.subtle.encrypt({ name: "AES-GCM", iv: iv }, k, te.encode(text))) };
  }
  async function decrypt(raw, iv, ct) {
    var k = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
    return td.decode(await crypto.subtle.decrypt({ name: "AES-GCM", iv: u8(iv) }, k, u8(ct)));
  }
  async function decryptBytes(raw, iv, ct) {
    var k = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
    return crypto.subtle.decrypt({ name: "AES-GCM", iv: iv }, k, ct);
  }
  async function sha256hex(s) {
    var h = new Uint8Array(await crypto.subtle.digest("SHA-256", te.encode(s)));
    return Array.prototype.map.call(h, function (x) { return ("0" + x.toString(16)).slice(-2); }).join("");
  }
  function norm(u) { return String(u || "").trim().toLowerCase(); }
  function userId(U, username) { return sha256hex(U.salt + "|" + norm(username)); }
  function pageKey(master, slug) { return hmac(master, "page:" + slug); }
  function allKey(master) { return hmac(master, "all"); }
  function dallKey(master) { return hmac(master, "dall"); }
  function contribKey(master) { return hmac(master, "contrib"); }
  function uploadKey(c, slug) { return hmac(c, "page:" + slug); }
  var GUIDES = { readme: 1 };
  function isGuide(slug) { return GUIDES.hasOwnProperty(slug); }
  function isUpload(U, slug) { return !!(U.uploads || {})[slug]; }
  async function keyFor(U, master, slug) { if (isGuide(slug)) return pageKey(master, "home"); return isUpload(U, slug) ? uploadKey(await contribKey(master), slug) : pageKey(master, slug); }
  function pdfKey(master, slug) { return hmac(master, "pdf:" + slug); }
  function canRead(U, slug) { var p = (U.policy || {})[slug]; return slug === "home" || !p || p.read !== false; }
  function canDownload(U, slug) { var p = (U.policy || {})[slug]; return slug !== "home" && !isGuide(slug) && canRead(U, slug) && (!p || p.download !== false); }
  async function sha256(buf) { return new Uint8Array(await crypto.subtle.digest("SHA-256", buf)); }
  /* Locks a page key to the super-user public key (contributors use this; no admin secret needed). */
  async function wrapForSuper(U, key) {
    if (!U.spub) return null;
    var pub = await crypto.subtle.importKey("raw", u8(U.spub), { name: "ECDH", namedCurve: "P-256" }, false, []);
    var eph = await crypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
    var aes = await sha256(await crypto.subtle.deriveBits({ name: "ECDH", public: pub }, eph.privateKey, 256));
    var box = await encrypt(aes, b64(key));
    return { e: b64(await crypto.subtle.exportKey("raw", eph.publicKey)), iv: box.iv, ct: box.ct };
  }
  async function unwrapSuper(U, ak, v) {
    var der = u8(await decrypt(ak, U.spriv.iv, U.spriv.ct));
    var priv = await crypto.subtle.importKey("pkcs8", der, { name: "ECDH", namedCurve: "P-256" }, false, ["deriveBits"]);
    var pub = await crypto.subtle.importKey("raw", u8(v.e), { name: "ECDH", namedCurve: "P-256" }, false, []);
    var aes = await sha256(await crypto.subtle.deriveBits({ name: "ECDH", public: pub }, priv, 256));
    return u8(await decrypt(aes, v.iv, v.ct));
  }
  /* Rebuilds the super-user vaults from the policy (admin only): vault = readable page keys (all key),
     dvault = downloadable pdf keys (dall key). Existing entries are kept. Returns true if anything changed. */
  async function syncVault(U, master, slugs) {
    var ak = await allKey(master), dk = await dallKey(master), changed = false;
    var vault = {}, dvault = {}, ov = U.vault || {}, od = U.dvault || {};
    for (var i = 0; i < slugs.length; i++) {
      var sl = slugs[i];
      if (canRead(U, sl)) { if (ov[sl]) vault[sl] = ov[sl]; else { vault[sl] = await encrypt(ak, b64(await keyFor(U, master, sl))); changed = true; } }
      else if (ov[sl]) changed = true;
      if (canDownload(U, sl)) { if (od[sl]) dvault[sl] = od[sl]; else { dvault[sl] = await encrypt(dk, b64(await pdfKey(master, sl))); changed = true; } }
      else if (od[sl]) changed = true;
    }
    U.vault = vault; U.dvault = dvault;
    return changed;
  }
  function fillVault(U, master, slugs) { return syncVault(U, master, slugs); }
  /* The keyring a user gets from their assignment (meta) under the current policy and their rights.
     Mirror of build_ring in protect.py. */
  async function buildRing(U, master, meta) {
    var ring = { n: meta.name, p: { home: b64(await pageKey(master, "home")) }, d: {} };
    var dl = meta.download !== false;
    if (meta.contrib) ring.c = b64(await contribKey(master));
    if (meta.all) { ring.all = 1; ring.a = b64(await allKey(master)); if (dl) ring.da = b64(await dallKey(master)); return ring; }
    var pages = meta.pages || [];
    for (var i = 0; i < pages.length; i++) {
      if (canRead(U, pages[i])) ring.p[pages[i]] = b64(await keyFor(U, master, pages[i]));
      if (dl && canDownload(U, pages[i])) ring.d[pages[i]] = b64(await pdfKey(master, pages[i]));
    }
    return ring;
  }
  async function loadUsers(base) {
    var r = await fetch(base + "users.json?t=" + Date.now(), { cache: "no-store" });
    if (!r.ok) throw new Error("users.json " + r.status);
    return r.json();
  }
  async function adminMaster(U, pw) {
    var m = await pbkdf2(pw, u8(U.salt), U.iter);
    if (b64(await hmac(m, "check")) !== U.check) throw new Error("bad password");
    return m;
  }
  /* Returns a session object to store, or throws. */
  async function login(U, username, pw) {
    if (norm(username) === "admin") {
      var m = await adminMaster(U, pw);
      return { t: "a", k: b64(m) };
    }
    var id = await userId(U, username);
    var e = (U.users || []).filter(function (x) { return x.id === id; })[0];
    if (!e) throw new Error("bad login");
    var k = await pbkdf2(pw, u8(e.s), U.iter);
    await decrypt(k, e.iv, e.kr); // throws if wrong password
    return { t: "u", id: id, k: b64(k) };
  }
  /* Turns a stored session into access: {name, admin, allowed (array of slugs or null = all), key(slug)}. */
  async function access(U, s) {
    if (!s) throw new Error("no session");
    if (s.t === "a") {
      var m = u8(s.k);
      if (b64(await hmac(m, "check")) !== U.check) throw new Error("stale");
      return { name: "Admin", admin: true, allowed: null, downloadable: null, contrib: await contribKey(m),
        key: function (slug) { return keyFor(U, m, slug); }, dkey: function (slug) { return pdfKey(m, slug); } };
    }
    var e = (U.users || []).filter(function (x) { return x.id === s.id; })[0];
    if (!e) throw new Error("removed");
    var ring = JSON.parse(await decrypt(u8(s.k), e.iv, e.kr));
    var contrib = ring.c ? u8(ring.c) : null;
    if (ring.all) {
      var ak = u8(ring.a), dk = ring.da ? u8(ring.da) : null;
      var open = async function (box, slug, k) {
        var v = (box || {})[slug]; if (!v || !k) return null;
        try { return v.e ? await unwrapSuper(U, ak, v) : u8(await decrypt(k, v.iv, v.ct)); } catch (x) { return null; }
      };
      return {
        name: ring.n, admin: false, superUser: true, contrib: contrib,
        allowed: Object.keys(U.vault || {}), downloadable: dk ? Object.keys(U.dvault || {}) : [],
        key: function (slug) { if (isGuide(slug)) slug = "home"; return slug === "home" && ring.p && ring.p.home ? Promise.resolve(u8(ring.p.home)) : open(U.vault, slug, ak); },
        dkey: function (slug) { return open(U.dvault, slug, dk); }
      };
    }
    var d = ring.d || {};
    return {
      name: ring.n, admin: false, contrib: contrib, allowed: Object.keys(ring.p), downloadable: Object.keys(d),
      key: function (slug) {
        if (isGuide(slug)) slug = "home";
        if (ring.p[slug]) return Promise.resolve(u8(ring.p[slug]));
        return contrib && isUpload(U, slug) && canRead(U, slug) ? uploadKey(contrib, slug) : Promise.resolve(null);
      },
      dkey: function (slug) { return Promise.resolve(d[slug] ? u8(d[slug]) : null); }
    };
  }
  /* Solution names must be unique, except that versions of one solution share its name. Two names clash
     when they match ignoring case, spaces, punctuation, "&" vs "and" and a trailing "· Faclon Labs".
     Mirror of name_key / duplicate_names in protect.py. */
  function nameKey(t) {
    return String(t || "").toLowerCase().replace(/\s*[\u00b7|\u2013\u2014-]\s*faclon labs\s*$/, "").replace(/&/g, " and ")
      .normalize("NFKD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "");
  }
  /* The existing solution name that t clashes with, or null. Ignores solution `except` and every version of
     the solution `family` (a slug of any of its versions). */
  function nameClash(U, t, except, family) {
    var k = nameKey(t), names = U.names || {}, sols = U.solutions || [], fr = family ? rootOf(U, family) : null;
    if (!k) return null;
    for (var i = 0; i < sols.length; i++) {
      var s = sols[i]; if (s.slug === except || (fr && rootOf(U, s.slug) === fr)) continue;
      var shown = names[s.slug] && names[s.slug].t ? names[s.slug].t : s.title;
      if (nameKey(shown) === k || nameKey(s.title) === k) return shown;
    }
    return null;
  }
  function rootOf(U, slug) { var v = (U.versions || {})[slug]; return v ? v.of : slug; }
  /* " v2" for a solution with several versions, "" otherwise: added after the name in lists, tabs and file names. */
  function versionLabel(U, slug) { var f = family(U, slug); return f ? " v" + f.n : ""; }
  /* Versions. family(U, slug) -> {root, members:[{slug, n}] oldest first, n (this slug's number), latest slug};
     null when the solution has only one version. Only solutions still listed in U.solutions count. */
  function family(U, slug) {
    var V = U.versions || {}, listed = {};
    (U.solutions || []).forEach(function (x) { listed[x.slug] = 1; });
    var root = V[slug] ? V[slug].of : slug, m = [];
    if (listed[root]) m.push({ slug: root, n: 1 });
    Object.keys(V).forEach(function (k) { if (V[k].of === root && listed[k]) m.push({ slug: k, n: V[k].n }); });
    if (m.length < 2 || !m.some(function (x) { return x.slug === slug; })) return null;
    m.sort(function (a, b) { return a.n - b.n; });
    return { root: root, members: m, n: m.filter(function (x) { return x.slug === slug; })[0].n, latest: m[m.length - 1].slug };
  }
  /* Number the next version of base's family would get. */
  function nextVersion(U, base) {
    var V = U.versions || {}, root = V[base] ? V[base].of : base, n = 1;
    Object.keys(V).forEach(function (k) { if (V[k].of === root && V[k].n > n) n = V[k].n; });
    return n + 1;
  }
  /* Registers slug as the newest version of base's family in J (a fresh users.json); returns its number. */
  function addVersion(J, slug, base) {
    var V = J.versions = J.versions || {}, root = V[base] ? V[base].of : base, n = nextVersion(J, base);
    V[slug] = { of: root, n: n };
    return n;
  }
  /* Every family with more than one version: [{root, members, latest}]. */
  function families(U) {
    var seen = {}, out = [];
    (U.solutions || []).forEach(function (x) {
      var f = family(U, x.slug); if (!f || seen[f.root]) return;
      seen[f.root] = 1; out.push(f);
    });
    return out;
  }
  function getSession() { try { return JSON.parse(localStorage.getItem(SESSION) || sessionStorage.getItem(SESSION) || "null"); } catch (e) { return null; } }
  function setSession(v) { var j = JSON.stringify(v); try { localStorage.setItem(SESSION, j); } catch (e) { try { sessionStorage.setItem(SESSION, j); } catch (e2) {} } }
  function clearSession() { try { localStorage.removeItem(SESSION); sessionStorage.removeItem(SESSION); localStorage.removeItem("faclon-glossary-key"); } catch (e) {} }
  return {
    u8: u8, b64: b64, pbkdf2: pbkdf2, hmac: hmac, encrypt: encrypt, decrypt: decrypt, decryptBytes: decryptBytes, sha256hex: sha256hex,
    norm: norm, userId: userId, pageKey: pageKey, allKey: allKey, dallKey: dallKey, contribKey: contribKey, uploadKey: uploadKey, isUpload: isUpload, isGuide: isGuide, keyFor: keyFor, wrapForSuper: wrapForSuper, nameKey: nameKey, nameClash: nameClash, family: family, families: families, rootOf: rootOf, versionLabel: versionLabel, nextVersion: nextVersion, addVersion: addVersion, pdfKey: pdfKey, canRead: canRead, canDownload: canDownload, syncVault: syncVault, fillVault: fillVault, buildRing: buildRing, loadUsers: loadUsers, adminMaster: adminMaster,
    login: login, access: access, getSession: getSession, setSession: setSession, clearSession: clearSession
  };
})();
