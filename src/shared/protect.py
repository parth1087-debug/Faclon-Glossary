"""Password-protects every generated page and builds the User Manager.

Run this after any build, before committing:

    GLOSSARY_PASSWORD='<admin password>' python3 src/shared/protect.py

How access works
- Each page is encrypted (AES-256-GCM) with its own key. Page keys are derived
  from the admin password, so only someone with that password can make them.
- users.json (repo root, public) holds one entry per user: an encrypted
  "keyring" with the keys for just the solutions that user may open, locked with
  the user's own password. Visitors sign in with a username and password; the
  landing page then shows only their solutions. Signing in as "admin" with the
  admin password opens everything.
- Super users hold one "all pages" key instead of a list. users.json "vault" keeps
  every page key encrypted with that key; this script adds each new page to it on
  every run, so super users see new solutions as soon as they are published.
- Users are created, edited and removed on /admin/ (the User Manager), which
  writes users.json back to GitHub. This script never touches the user list; it
  only refreshes the list of solutions the User Manager offers.

The admin password is never written to the repo. Changing it changes every
page key, so every user would have to be recreated.

    python3 src/shared/protect.py --check   # fails if any page is unprotected or missing its PDF

It also renders each solution page to one continuous PDF page (pagepdf.py, needs
Playwright + Chromium) whenever the page changes, stored encrypted as
<solution>/page-pdf.bin for the in-page Download button. --force-pdf re-renders all.
"""
import base64
import getpass
import hashlib
import hmac
import html as htmllib
import json
import os
import re
import secrets
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SALT_FILE = HERE / "protect_salt.txt"
AUTH_CORE = HERE / "auth_core.js"
TOOLS_JS = HERE / "page_tools.js"
PDF_NAME = "page-pdf.bin"
ADMIN_SRC = ROOT / "src" / "admin" / "index.html"
ADMIN_OUT = ROOT / "admin" / "index.html"
USERS = ROOT / "users.json"
ITERATIONS = 250_000
MARKER = '<meta name="faclon-protected" content="2">'
MARKER_V1 = '<meta name="faclon-protected" content="1">'
SKIP_DIRS = {"src", "admin", ".git", ".github"}


def b64(b):
    return base64.b64encode(b).decode("ascii")


def unb64(s):
    return base64.b64decode(s)


def pages():
    """(slug, path) for the landing page and every solution page."""
    out = [("home", ROOT / "index.html")]
    for p in sorted(ROOT.glob("*/index.html")):
        if p.parent.name not in SKIP_DIRS:
            out.append((p.parent.name, p))
    return [(s, p) for s, p in out if p.exists()]


def salt():
    if not SALT_FILE.exists():
        SALT_FILE.write_text(secrets.token_hex(16) + "\n")
    return bytes.fromhex(SALT_FILE.read_text().strip())


def derive_master(password, s):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=s, iterations=ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def mac(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def field(html, name):
    m = re.search(name + r'\s*:\s*"([^"]*)"', html)
    return m.group(1) if m else None


def plaintext(html, slug, master):
    """Returns the page's readable HTML, decrypting older protected versions."""
    if MARKER in html:
        key = mac(master, "page:" + slug)
    elif MARKER_V1 in html:
        key = master  # first version used one site-wide key
    else:
        return html
    return AESGCM(key).decrypt(unb64(field(html, "iv")), unb64(field(html, "ct")), None).decode("utf-8")


def meta(html, name):
    m = re.search(r'<meta name="%s" content="([^"]*)">' % name, html)
    return m.group(1) if m else None


def title_of(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = htmllib.unescape(m.group(1).strip()) if m else ""
    return re.sub(r"\s*·\s*Faclon Labs$", "", t) or "Faclon Labs"


GATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
__MARKER__
<meta name="robots" content="noindex">
<title>Faclon Labs</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;background:#0B1A30;color:#fff;display:flex;align-items:center;justify-content:center;padding:16px;-webkit-font-smoothing:antialiased}
.card{width:100%;max-width:380px;background:#13264A;border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:32px 28px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#7C95FF}
h1{font-size:22px;letter-spacing:-.015em;line-height:1.25;margin:10px 0 6px}
p{font-size:14px;color:#B6C2D6;line-height:1.5}
form{margin-top:22px;display:flex;flex-direction:column;gap:10px}
input{font:inherit;font-size:15px;padding:12px 14px;border-radius:9px;border:1px solid rgba(255,255,255,.18);background:#0B1A30;color:#fff;outline:none;width:100%}
input:focus{border-color:#3D63F5}
button,.btn{font:inherit;font-size:15px;font-weight:600;padding:12px 14px;border-radius:9px;border:0;background:#3D63F5;color:#fff;cursor:pointer;text-align:center;text-decoration:none;display:block}
.ghost{background:transparent;border:1px solid rgba(255,255,255,.2)}
button:disabled{opacity:.6;cursor:default}
.err{min-height:18px;font-size:13px;color:#FF9B9B}
.acts{margin-top:22px;display:flex;flex-direction:column;gap:10px}
[hidden]{display:none!important}
</style></head>
<body>
<div class="card" id="gate" style="visibility:hidden">
  <div class="eyebrow">Faclon Labs</div>
  <h1>Sign in</h1>
  <p id="lead">These solution pages are shared privately. Sign in with the username and password you were given.</p>
  <form id="f" autocomplete="on">
    <input id="u" type="text" placeholder="Username" aria-label="Username" autocomplete="username" autocapitalize="none" spellcheck="false" required>
    <input id="pw" type="password" placeholder="Password" aria-label="Password" autocomplete="current-password" required>
    <div class="err" id="err" role="alert"></div>
    <button id="go" type="submit">Sign in</button>
  </form>
</div>
<div class="card" id="noacc" hidden>
  <div class="eyebrow">Faclon Labs</div>
  <h1 id="nah">No access to this page</h1>
  <p id="nap">You're signed in as <b id="who"></b>, but this solution hasn't been shared with you. Ask your Faclon contact if you need it.</p>
  <div class="acts"><a class="btn" id="home" href="#">See your solutions</a><button class="ghost" id="out" type="button">Sign in as someone else</button></div>
</div>
<script id="fa-core">
__AUTH_CORE__
</script>
<script>
(async function(){
var TOOLS=__TOOLS__;
var D={slug:"__SLUG__",base:"__BASE__",iv:"__IV__",ct:"__CT__"};
var $=function(i){return document.getElementById(i)};
var gate=$("gate"),noacc=$("noacc"),err=$("err");
function after(html,acc,U){
  var args=[acc.allowed,acc.name,acc.admin,D.base,U.solutions||[],D.slug,acc.downloadable,U.policy||{}].map(function(v){return JSON.stringify(v).replace(/</g,"\\u003c")}).join(",");
  var js='<script>'+$("fa-core").textContent+'\n'+TOOLS+'\nFTOOLS('+args+')<\/script>';
  var i=html.toLowerCase().lastIndexOf("</body>");
  return i<0?html+js:html.slice(0,i)+js+html.slice(i);
}
function show(html){function go(){document.open();document.write(html);document.close()}if(document.readyState==="complete")go();else window.addEventListener("load",go)}
async function open(U,acc){
  var k=await acc.key(D.slug);
  if(!k){gate.hidden=true;$("who").textContent=acc.name;if(!FA.canRead(U,D.slug)){$("nah").textContent="This solution isn't available right now";$("nap").textContent="It has been switched off for all users. Ask your Faclon contact if you need it."}$("home").href=D.base||"./";noacc.hidden=false;return}
  show(after(await FA.decrypt(k,D.iv,D.ct),acc,U));
}
$("out").onclick=function(){FA.clearSession();noacc.hidden=true;gate.hidden=false;gate.style.visibility="visible";$("u").focus()};
var U;
try{U=await FA.loadUsers(D.base)}catch(e){gate.style.visibility="visible";err.textContent="Couldn't reach the site. Check your connection and reload.";$("go").disabled=true;return}
var s=FA.getSession();
if(s){try{await open(U,await FA.access(U,s));return}catch(e){FA.clearSession();if(e.message==="removed")$("lead").textContent="Your access has changed. Please sign in again."}}
gate.style.visibility="visible";$("u").focus();
$("f").addEventListener("submit",async function(e){
  e.preventDefault();var b=$("go");b.disabled=true;b.textContent="Checking…";err.textContent="";
  try{var s=await FA.login(U,$("u").value,$("pw").value);var acc=await FA.access(U,s);FA.setSession(s);await open(U,acc)}
  catch(x){err.textContent="That username and password didn't match. Try again.";b.disabled=false;b.textContent="Sign in"}
});
})();
</script>
</body></html>
"""


def gate_html(slug, base, iv, ct, core, gate_ver, content):
    tools = json.dumps(TOOLS_JS.read_text(encoding="utf-8")).replace("</", "<\\/")
    return (GATE.replace("__MARKER__", MARKER + f'\n<meta name="faclon-gate" content="{gate_ver}"><meta name="faclon-content" content="{content}">')
                .replace("__TOOLS__", tools)
                .replace("__AUTH_CORE__", core)
                .replace("__SLUG__", slug)
                .replace("__BASE__", base)
                .replace("__IV__", b64(iv))
                .replace("__CT__", b64(ct)))


def build_admin(core):
    if not ADMIN_SRC.exists():
        return None
    out = ADMIN_SRC.read_text(encoding="utf-8").replace("/*__AUTH_CORE__*/", core)
    return out


def can_read(users, slug):
    p = (users.get("policy") or {}).get(slug) or {}
    return slug == "home" or p.get("read", True) is not False


def can_download(users, slug):
    p = (users.get("policy") or {}).get(slug) or {}
    return slug != "home" and can_read(users, slug) and p.get("download", True) is not False


def sync_box(old, all_key, wanted):
    """Keeps a vault ({slug: key encrypted with the all key}) equal to `wanted`, reusing unchanged entries."""
    out = {}
    for slug, want in wanted.items():
        v = old.get(slug)
        try:
            if v and unb64(AESGCM(all_key).decrypt(unb64(v["iv"]), unb64(v["ct"]), None).decode()) == want:
                out[slug] = v
                continue
        except Exception:
            pass
        iv = secrets.token_bytes(12)
        out[slug] = {"iv": b64(iv), "ct": b64(AESGCM(all_key).encrypt(iv, b64(want).encode(), None))}
    return out


def migrate_pdfs(targets, master, fresh):
    """PDFs used to share the page key; re-lock older ones with their own pdf key."""
    for slug, path in targets:
        f = path.parent / PDF_NAME
        if slug == "home" or slug in fresh or not f.exists():
            continue
        data = f.read_bytes()
        try:
            AESGCM(mac(master, "pdf:" + slug)).decrypt(data[:12], data[12:], None)
            continue
        except Exception:
            pdf = AESGCM(mac(master, "page:" + slug)).decrypt(data[:12], data[12:], None)
        iv = secrets.token_bytes(12)
        f.write_bytes(iv + AESGCM(mac(master, "pdf:" + slug)).encrypt(iv, pdf, None))
        print("re-locked pdf", slug)


def build_ring(users, master, m):
    """Mirror of FA.buildRing in auth_core.js."""
    ring = {"n": m["name"], "p": {"home": b64(mac(master, "page:home"))}, "d": {}}
    if m.get("all"):
        ring["all"] = 1
        ring["a"] = b64(mac(master, "all"))
        return ring
    for slug in m.get("pages") or []:
        if can_read(users, slug):
            ring["p"][slug] = b64(mac(master, "page:" + slug))
        if can_download(users, slug):
            ring["d"][slug] = b64(mac(master, "pdf:" + slug))
    return ring


def upgrade_rings(users, master):
    """One-off: rebuilds every keyring so it carries download keys (ring.d) under the current policy."""
    admin_key = mac(master, "admin")
    n = 0
    for e in users.get("users") or []:
        try:
            m = json.loads(AESGCM(admin_key).decrypt(unb64(e["miv"]), unb64(e["meta"]), None))
            uk = unb64(m["uk"])
        except Exception:
            print("  skipped an unreadable user entry")
            continue
        iv = secrets.token_bytes(12)
        e["iv"] = b64(iv)
        e["kr"] = b64(AESGCM(uk).encrypt(iv, json.dumps(build_ring(users, master, m), separators=(",", ":")).encode(), None))
        n += 1
    return n


def main():
    targets = pages()
    core = AUTH_CORE.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        bad = [p for _, p in targets if MARKER not in p.read_text(encoding="utf-8")]
        for p in bad:
            print("UNPROTECTED:", p.relative_to(ROOT))
        admin = build_admin(core)
        if admin is not None and (not ADMIN_OUT.exists() or ADMIN_OUT.read_text(encoding="utf-8") != admin):
            print("STALE: admin/index.html (re-run protect.py)")
            bad.append(ADMIN_OUT)
        for slug, p in targets:
            if slug != "home" and not (p.parent / PDF_NAME).exists():
                print("MISSING PDF:", (p.parent / PDF_NAME).relative_to(ROOT))
                bad.append(p)
        if not USERS.exists():
            print("MISSING: users.json")
            bad.append(USERS)
        else:
            u = json.loads(USERS.read_text(encoding="utf-8"))
            vault = u.get("vault") or {}
            for slug, _ in targets:
                if slug not in vault and can_read(u, slug):
                    print("MISSING VAULT KEY:", slug, "(re-run protect.py)")
                    bad.append(USERS)
        sys.exit(1 if bad else 0)

    password = os.environ.get("GLOSSARY_PASSWORD") or getpass.getpass("Admin password: ")
    if not password:
        sys.exit("No password given (set GLOSSARY_PASSWORD).")
    s = salt()
    master = derive_master(password, s)
    check = b64(mac(master, "check"))

    users = json.loads(USERS.read_text(encoding="utf-8")) if USERS.exists() else {
        "version": 2, "salt": b64(s), "iter": ITERATIONS, "check": check, "solutions": [], "users": []}
    if users.get("check") != check or users.get("salt") != b64(s):
        sys.exit("That password doesn't match this site's admin password (users.json check failed).")

    gate_ver = hashlib.sha256((GATE + core + TOOLS_JS.read_text(encoding="utf-8")).encode()).hexdigest()[:16]
    force_pdf = "--force-pdf" in sys.argv
    solutions, need_pdf = [], []
    for slug, path in targets:
        raw = path.read_text(encoding="utf-8")
        plain = plaintext(raw, slug, master)
        content = hashlib.sha256(plain.encode("utf-8")).hexdigest()[:16]
        if slug != "home":
            solutions.append({"slug": slug, "title": title_of(plain)})
            if force_pdf or not (path.parent / PDF_NAME).exists() or meta(raw, "faclon-content") != content:
                need_pdf.append((slug, path, plain))
        if MARKER in raw and meta(raw, "faclon-gate") == gate_ver and meta(raw, "faclon-content") == content:
            print("already protected", path.relative_to(ROOT))
            continue
        iv = secrets.token_bytes(12)
        ct = AESGCM(mac(master, "page:" + slug)).encrypt(iv, plain.encode("utf-8"), None)
        base = "" if slug == "home" else "../"
        path.write_text(gate_html(slug, base, iv, ct, core, gate_ver, content), encoding="utf-8")
        print("protected", path.relative_to(ROOT))

    if need_pdf:
        try:
            import pagepdf
        except ImportError:
            sys.path.insert(0, str(HERE))
            import pagepdf
        r = pagepdf.Renderer()
        try:
            for slug, path, plain in need_pdf:
                pdf, h, scale = r.pdf(plain)
                iv = secrets.token_bytes(12)
                (path.parent / PDF_NAME).write_bytes(iv + AESGCM(mac(master, "pdf:" + slug)).encrypt(iv, pdf, None))
                print(f"pdf {slug}: one page, {h}px tall" + (f", scaled to {scale:.2f}" if scale < 1 else ""))
        finally:
            r.close()

    users["solutions"] = solutions
    migrate_pdfs(targets, master, [x[0] for x in need_pdf])
    all_key = mac(master, "all")
    users["vault"] = sync_box(users.get("vault") or {}, all_key,
                              {slug: mac(master, "page:" + slug) for slug, _ in targets if can_read(users, slug)})
    users["dvault"] = sync_box(users.get("dvault") or {}, all_key,
                               {slug: mac(master, "pdf:" + slug) for slug, _ in targets if can_download(users, slug)})
    if users.get("version", 2) < 3:
        n = upgrade_rings(users, master)
        users["version"] = 3
        print(f"upgraded {n} user keyrings to separate read and download keys")
    USERS.write_text(json.dumps(users, indent=1) + "\n", encoding="utf-8")
    print("updated users.json solutions:", ", ".join(x["slug"] for x in solutions))

    admin = build_admin(core)
    if admin is not None:
        ADMIN_OUT.parent.mkdir(exist_ok=True)
        ADMIN_OUT.write_text(admin, encoding="utf-8")
        print("wrote", ADMIN_OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
