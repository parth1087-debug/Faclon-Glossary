"""Password-protects every generated page on the site.

Run this after any build, before committing:

    GLOSSARY_PASSWORD='...' python3 src/shared/protect.py

Each page (index.html and <solution>/index.html) is encrypted with AES-256-GCM
using a key derived from the password (PBKDF2-SHA256). The committed file is a
small login screen plus the ciphertext; the browser decrypts it locally once the
right password is entered. The derived key is remembered in the visitor's
browser, so one login unlocks every page.

The password is never written to the repo. Pages already protected are skipped,
so it is safe to run repeatedly. Use --check to fail if any page is unprotected.
"""
import base64
import getpass
import os
import secrets
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = Path(__file__).resolve().parents[2]
SALT_FILE = Path(__file__).with_name("protect_salt.txt")
ITERATIONS = 250_000
MARKER = '<meta name="faclon-protected" content="1">'
STORAGE_KEY = "faclon-glossary-key"


def pages():
    out = [ROOT / "index.html"]
    out += sorted(p for p in ROOT.glob("*/index.html") if p.parent.name not in ("src", ".git"))
    return [p for p in out if p.exists()]


def salt():
    if not SALT_FILE.exists():
        SALT_FILE.write_text(secrets.token_hex(16) + "\n")
    return bytes.fromhex(SALT_FILE.read_text().strip())


def derive(password, s):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=s, iterations=ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def b64(b):
    return base64.b64encode(b).decode("ascii")


GATE = """<!doctype html>
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
button{font:inherit;font-size:15px;font-weight:600;padding:12px 14px;border-radius:9px;border:0;background:#3D63F5;color:#fff;cursor:pointer}
button:disabled{opacity:.6;cursor:default}
.err{min-height:18px;font-size:13px;color:#FF9B9B}
#app{display:none}
</style></head>
<body>
<div class="card" id="gate">
  <div class="eyebrow">Faclon Labs</div>
  <h1>Enter password</h1>
  <p>These solution pages are shared privately. Enter the password you were given to continue.</p>
  <form id="f" autocomplete="off">
    <input id="pw" type="password" placeholder="Password" aria-label="Password" autofocus required>
    <div class="err" id="err" role="alert"></div>
    <button id="go" type="submit">Unlock</button>
  </form>
</div>
<script>
(function(){
var D={salt:"__SALT__",iter:__ITER__,iv:"__IV__",ct:"__CT__"},K="__STORAGE_KEY__";
function u8(s){var b=atob(s),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a}
function b64(buf){var a=new Uint8Array(buf),s="";for(var i=0;i<a.length;i+=8192)s+=String.fromCharCode.apply(null,a.subarray(i,i+8192));return btoa(s)}
function get(){try{return localStorage.getItem(K)||sessionStorage.getItem(K)}catch(e){return null}}
function put(v){try{localStorage.setItem(K,v)}catch(e){try{sessionStorage.setItem(K,v)}catch(e2){}}}
function drop(){try{localStorage.removeItem(K);sessionStorage.removeItem(K)}catch(e){}}
function open(raw){
  return crypto.subtle.importKey("raw",raw,"AES-GCM",false,["decrypt"])
    .then(function(k){return crypto.subtle.decrypt({name:"AES-GCM",iv:u8(D.iv)},k,u8(D.ct))})
    .then(function(pt){return new TextDecoder().decode(pt)});
}
function show(html){function go(){document.open();document.write(html);document.close()}if(document.readyState==="complete")go();else window.addEventListener("load",go)}
function derive(pw){
  var enc=new TextEncoder();
  return crypto.subtle.importKey("raw",enc.encode(pw),"PBKDF2",false,["deriveBits"])
    .then(function(k){return crypto.subtle.deriveBits({name:"PBKDF2",hash:"SHA-256",salt:u8(D.salt),iterations:D.iter},k,256)});
}
var saved=get();
var gate=document.getElementById("gate");
if(saved){gate.style.visibility="hidden";open(u8(saved)).then(show,function(){drop();gate.style.visibility="visible"});}
document.getElementById("f").addEventListener("submit",function(e){
  e.preventDefault();
  var btn=document.getElementById("go"),err=document.getElementById("err");
  btn.disabled=true;btn.textContent="Checking…";err.textContent="";
  derive(document.getElementById("pw").value).then(function(raw){
    return open(raw).then(function(html){put(b64(raw));show(html)});
  }).catch(function(){
    err.textContent="That password didn't work. Try again.";
    btn.disabled=false;btn.textContent="Unlock";
  });
});
})();
</script>
</body></html>
"""


def protect(path, key, s):
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        return False
    iv = secrets.token_bytes(12)
    ct = AESGCM(key).encrypt(iv, html.encode("utf-8"), None)
    out = (GATE.replace("__MARKER__", MARKER)
               .replace("__SALT__", b64(s))
               .replace("__ITER__", str(ITERATIONS))
               .replace("__IV__", b64(iv))
               .replace("__STORAGE_KEY__", STORAGE_KEY)
               .replace("__CT__", b64(ct)))
    path.write_text(out, encoding="utf-8")
    return True


def main():
    targets = pages()
    if "--check" in sys.argv:
        bad = [p for p in targets if MARKER not in p.read_text(encoding="utf-8")]
        for p in bad:
            print("UNPROTECTED:", p.relative_to(ROOT))
        sys.exit(1 if bad else 0)
    password = os.environ.get("GLOSSARY_PASSWORD") or getpass.getpass("Site password: ")
    if not password:
        sys.exit("No password given (set GLOSSARY_PASSWORD).")
    s = salt()
    key = derive(password, s)
    for p in targets:
        print("protected" if protect(p, key, s) else "already protected", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
