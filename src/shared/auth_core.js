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
  /* Adds any missing vault entries (admin only). Returns how many were added. */
  async function fillVault(U, master, slugs) {
    var ak = await allKey(master), n = 0;
    U.vault = U.vault || {};
    for (var i = 0; i < slugs.length; i++) {
      if (U.vault[slugs[i]]) continue;
      U.vault[slugs[i]] = await encrypt(ak, b64(await pageKey(master, slugs[i])));
      n++;
    }
    return n;
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
      return { name: "Admin", admin: true, allowed: null, key: function (slug) { return pageKey(m, slug); } };
    }
    var e = (U.users || []).filter(function (x) { return x.id === s.id; })[0];
    if (!e) throw new Error("removed");
    var ring = JSON.parse(await decrypt(u8(s.k), e.iv, e.kr));
    if (ring.all) {
      var ak = u8(ring.a);
      return {
        name: ring.n, admin: false, allowed: null, superUser: true,
        key: async function (slug) {
          if (ring.p && ring.p[slug]) return u8(ring.p[slug]);
          var v = (U.vault || {})[slug];
          if (!v) return null;
          try { return u8(await decrypt(ak, v.iv, v.ct)); } catch (x) { return null; }
        }
      };
    }
    return {
      name: ring.n, admin: false, allowed: Object.keys(ring.p),
      key: function (slug) { return Promise.resolve(ring.p[slug] ? u8(ring.p[slug]) : null); }
    };
  }
  function getSession() { try { return JSON.parse(localStorage.getItem(SESSION) || sessionStorage.getItem(SESSION) || "null"); } catch (e) { return null; } }
  function setSession(v) { var j = JSON.stringify(v); try { localStorage.setItem(SESSION, j); } catch (e) { try { sessionStorage.setItem(SESSION, j); } catch (e2) {} } }
  function clearSession() { try { localStorage.removeItem(SESSION); sessionStorage.removeItem(SESSION); localStorage.removeItem("faclon-glossary-key"); } catch (e) {} }
  return {
    u8: u8, b64: b64, pbkdf2: pbkdf2, hmac: hmac, encrypt: encrypt, decrypt: decrypt, decryptBytes: decryptBytes, sha256hex: sha256hex,
    norm: norm, userId: userId, pageKey: pageKey, allKey: allKey, fillVault: fillVault, loadUsers: loadUsers, adminMaster: adminMaster,
    login: login, access: access, getSession: getSession, setSession: setSession, clearSession: clearSession
  };
})();
