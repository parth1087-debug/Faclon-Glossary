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
import unicodedata
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


GUIDES = {"readme"}  # guide pages, not solutions: mirror of GUIDES in auth_core.js


def key_for(users, master, slug):
    """Page key: contributor uploads derive from the contrib key, guides use the landing-page key,
    everything else derives from the master key."""
    if slug in GUIDES:
        return mac(master, "page:home")
    if slug in (users.get("uploads") or {}):
        return mac(mac(master, "contrib"), "page:" + slug)
    return mac(master, "page:" + slug)


def plaintext(html, slug, master, users=None):
    """Returns the page's readable HTML, decrypting older protected versions."""
    if MARKER in html:
        key = key_for(users or {}, master, slug)
    elif MARKER_V1 in html:
        key = master  # first version used one site-wide key
    else:
        return html
    return AESGCM(key).decrypt(unb64(field(html, "iv")), unb64(field(html, "ct")), None).decode("utf-8")


def meta(html, name):
    m = re.search(r'<meta name="%s" content="([^"]*)">' % name, html)
    return m.group(1) if m else None


def name_key(t):
    """Mirror of FA.nameKey in auth_core.js: solution names must be unique under this key."""
    t = re.sub(r"\s*[\u00b7|\u2013\u2014-]\s*faclon labs\s*$", "", (t or "").lower()).replace("&", " and ")
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", t)


def duplicate_names(solutions, versions=None):
    """Pairs of solutions with the same name. Versions of one solution (users.json "versions") share its
    name on purpose and don't count. Mirror of FA.nameClash in auth_core.js."""
    versions = versions or {}
    root = lambda slug: (versions.get(slug) or {}).get("of") or slug
    seen, dups = {}, []
    for s in solutions:
        k = name_key(s["title"])
        if k in seen and root(seen[k]["slug"]) != root(s["slug"]):
            dups.append((seen[k], s))
        elif k not in seen:
            seen[k] = s
    return dups


def upload_title(users, master, slug):
    """The title a contributor gave their upload (shown on its card), or None."""
    m = ((users.get("uploads") or {}).get(slug) or {}).get("meta")
    if not m:
        return None
    try:
        return json.loads(AESGCM(key_for(users, master, slug)).decrypt(unb64(m["iv"]), unb64(m["ct"]), None)).get("title") or None
    except Exception:
        return None


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
  var html=await FA.decrypt(k,D.iv,D.ct);
  show(after(D.up?sandboxed(html):html,acc,U));
}
/* Contributor uploads run in a sandboxed frame: their scripts can't reach the site's storage or logins. */
function sandboxed(html){
  var dir=location.href.split("#")[0].split("?")[0].replace(/[^\/]*$/,"");
  var baseTag='<base href="'+dir+'" target="_top">';
  var src=/<head[^>]*>/i.test(html)?html.replace(/<head[^>]*>/i,function(m){return m+baseTag}):baseTag+html;
  var t=(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)||[])[1]||"Faclon Labs";
  var attr=function(x){return String(x).replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;")};
  return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex"><title>'+t+'</title>'+
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'+
    '<style>html,body{margin:0;height:100%;overflow:hidden;background:#fff}iframe{border:0;width:100%;height:100%;display:block}</style></head><body>'+
    '<iframe title="'+attr(t)+'" sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation allow-forms allow-modals allow-downloads" srcdoc="'+attr(src)+'"></iframe></body></html>';
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


def gate_html(slug, base, iv, ct, core, gate_ver, content, up=False):
    tools = json.dumps(TOOLS_JS.read_text(encoding="utf-8")).replace("</", "<\\/")
    gate = GATE.replace('var D={slug:"__SLUG__"', 'var D={up:1,slug:"__SLUG__"') if up else GATE
    return (gate.replace("__MARKER__", MARKER + f'\n<meta name="faclon-gate" content="{gate_ver}"><meta name="faclon-content" content="{content}">')
                .replace("__TOOLS__", tools)
                .replace("__AUTH_CORE__", core)
                .replace("__SLUG__", slug)
                .replace("__BASE__", base)
                .replace("__IV__", b64(iv))
                .replace("__CT__", b64(ct)))


def connector():
    """The Claude connector for contributors (src/connector/build_connector.py) bundles auth_core.js, so it is rebuilt with every run."""
    sys.path.insert(0, str(ROOT / "src" / "connector"))
    import build_connector
    return build_connector


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


def migrate_pdfs(targets, master, fresh, users):
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
            pdf = AESGCM(key_for(users, master, slug)).decrypt(data[:12], data[12:], None)
        iv = secrets.token_bytes(12)
        f.write_bytes(iv + AESGCM(mac(master, "pdf:" + slug)).encrypt(iv, pdf, None))
        print("re-locked pdf", slug)


def build_ring(users, master, m):
    """Mirror of FA.buildRing in auth_core.js."""
    ring = {"n": m["name"], "p": {"home": b64(mac(master, "page:home"))}, "d": {}}
    dl = m.get("download", True) is not False
    if m.get("contrib"):
        ring["c"] = b64(mac(master, "contrib"))
    if m.get("all"):
        ring["all"] = 1
        ring["a"] = b64(mac(master, "all"))
        if dl:
            ring["da"] = b64(mac(master, "dall"))
        return ring
    for slug in m.get("pages") or []:
        if can_read(users, slug):
            ring["p"][slug] = b64(key_for(users, master, slug))
        if dl and can_download(users, slug):
            ring["d"][slug] = b64(mac(master, "pdf:" + slug))
    return ring


def ensure_super_keypair(users, master):
    """ECDH key pair contributors use to hand new uploads to super users (private half locked with the all key)."""
    if users.get("spub") and users.get("spriv"):
        return
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization as ser
    priv = ec.generate_private_key(ec.SECP256R1())
    der = priv.private_bytes(ser.Encoding.DER, ser.PrivateFormat.PKCS8, ser.NoEncryption())
    pub = priv.public_key().public_bytes(ser.Encoding.X962, ser.PublicFormat.UncompressedPoint)
    iv = secrets.token_bytes(12)
    users["spub"] = b64(pub)
    users["spriv"] = {"iv": b64(iv), "ct": b64(AESGCM(mac(master, "all")).encrypt(iv, b64(der).encode(), None))}
    print("created the super-user key pair for contributor uploads")


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
            if slug != "home" and slug not in GUIDES and not (p.parent / PDF_NAME).exists():
                print("MISSING PDF:", (p.parent / PDF_NAME).relative_to(ROOT))
                bad.append(p)
        if not USERS.exists():
            print("MISSING: users.json")
            bad.append(USERS)
        else:
            u = json.loads(USERS.read_text(encoding="utf-8"))
            vault = u.get("vault") or {}
            for a, b in duplicate_names(u.get("solutions") or [], u.get("versions")):
                print(f'DUPLICATE NAME: {a["slug"]} and {b["slug"]} are both called "{b["title"]}"')
                bad.append(USERS)
            for slug, _ in targets:
                if slug not in vault and slug not in GUIDES and can_read(u, slug):
                    print("MISSING VAULT KEY:", slug, "(re-run protect.py)")
                    bad.append(USERS)
        for p in connector().stale():
            print("STALE:", p.relative_to(ROOT), "(re-run protect.py)")
            bad.append(p)
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
        plain = plaintext(raw, slug, master, users)
        content = hashlib.sha256(plain.encode("utf-8")).hexdigest()[:16]
        if slug != "home" and slug not in GUIDES:
            own = upload_title(users, master, slug) or title_of(plain)
            ren = (users.get("names") or {}).get(slug)
            if ren:
                ren["o"] = own  # keep the page's own title current so "Reset name" restores it
            solutions.append({"slug": slug, "title": ren["t"] if ren else own})
            if force_pdf or not (path.parent / PDF_NAME).exists() or meta(raw, "faclon-content") != content:
                need_pdf.append((slug, path, plain))
        if MARKER in raw and meta(raw, "faclon-gate") == gate_ver and meta(raw, "faclon-content") == content:
            print("already protected", path.relative_to(ROOT))
            continue
        iv = secrets.token_bytes(12)
        ct = AESGCM(key_for(users, master, slug)).encrypt(iv, plain.encode("utf-8"), None)
        base = "" if slug == "home" else "../"
        path.write_text(gate_html(slug, base, iv, ct, core, gate_ver, content, slug in (users.get("uploads") or {})), encoding="utf-8")
        print("protected", path.relative_to(ROOT))

    dups = duplicate_names(solutions, users.get("versions"))
    if dups:
        for a, b in dups:
            print(f'DUPLICATE NAME: {a["slug"]} and {b["slug"]} are both called "{b["title"]}"')
        sys.exit("Solution names must be unique. Change one page's <title> (or rename it in the User Manager) and run protect.py again. users.json was not updated.")

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
    migrate_pdfs(targets, master, [x[0] for x in need_pdf], users)
    all_key = mac(master, "all")
    users["vault"] = sync_box(users.get("vault") or {}, all_key,
                              {slug: key_for(users, master, slug) for slug, _ in targets if slug not in GUIDES and can_read(users, slug)})
    users["dvault"] = sync_box(users.get("dvault") or {}, mac(master, "dall"),
                               {slug: mac(master, "pdf:" + slug) for slug, _ in targets if slug not in GUIDES and can_download(users, slug)})
    ensure_super_keypair(users, master)
    if users.get("version", 2) < 4:
        n = upgrade_rings(users, master)
        users["version"] = 4
        print(f"upgraded {n} user keyrings (download and contributor rights)")
    USERS.write_text(json.dumps(users, indent=1) + "\n", encoding="utf-8")
    print("updated users.json solutions:", ", ".join(x["slug"] for x in solutions))

    admin = build_admin(core)
    if admin is not None:
        ADMIN_OUT.parent.mkdir(exist_ok=True)
        ADMIN_OUT.write_text(admin, encoding="utf-8")
        print("wrote", ADMIN_OUT.relative_to(ROOT))
    for p in connector().build():
        print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
