"""Renders a page's HTML to a single continuous PDF page (no page breaks).

Used by protect.py. Needs Playwright with Chromium:
    pip install playwright && playwright install chromium
Fonts come from src/shared/fonts (Inter), so no network is needed.
"""
import base64
from pathlib import Path

FONTS = Path(__file__).resolve().parent / "fonts"
WIDTH_PX = 1200          # layout width the PDF is rendered at (desktop layout)
MAX_IN = 200.0           # PDF readers cap a page at 200 inches; taller pages are scaled down to fit
WEIGHTS = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}


def _font_css():
    rules = []
    for w, name in WEIGHTS.items():
        data = base64.b64encode((FONTS / f"Inter-{name}.woff2").read_bytes()).decode()
        rules.append("@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:block;"
                     "src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, data))
    return "\n".join(rules)


class Renderer:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        self._css = _font_css()

    def close(self):
        self._browser.close()
        self._pw.stop()

    def pdf(self, html):
        page = self._browser.new_page(viewport={"width": WIDTH_PX, "height": 900})
        css = self._css

        def route(r):
            url = r.request.url
            if url.startswith("https://fonts.googleapis.com/"):
                return r.fulfill(status=200, content_type="text/css", body=css)
            if url.startswith("https://fonts.gstatic.com/"):
                return r.fulfill(status=404, body="")
            if url.startswith("data:") or url.startswith("about:"):
                return r.continue_()
            return r.abort()

        page.route("**/*", route)
        page.emulate_media(media="screen", reduced_motion="reduce")
        page.set_content(html, wait_until="load")
        page.evaluate("document.fonts.ready")
        # Scroll through once so anything revealed on scroll is shown, then back to the top.
        h = page.evaluate("document.documentElement.scrollHeight")
        for y in range(0, h + 900, 450):
            page.evaluate(f"window.scrollTo(0,{y})")
            page.wait_for_timeout(40)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(400)
        # Freeze screen-relative sizes (100vh etc.) at the on-screen values, since a single tall PDF page
        # would otherwise stretch them to the full page height; drop floating widgets pinned mid-screen.
        page.evaluate("""() => {
          const all = [...document.querySelectorAll('body *')];
          const vals = all.map(el => { const c = getComputedStyle(el); return [c.minHeight, c.maxHeight, c.position, el.getBoundingClientRect().top]; });
          all.forEach((el, i) => {
            const [mn, mx, pos, top] = vals[i];
            if (mn && mn !== '0px' && mn !== 'auto') el.style.setProperty('min-height', mn, 'important');
            if (mx && mx !== 'none') el.style.setProperty('max-height', mx, 'important');
            if (pos === 'fixed' && top > 80) el.style.setProperty('display', 'none', 'important');
            if (pos === 'sticky') el.style.setProperty('position', 'relative', 'important');
          });
        }""")
        page.add_style_tag(content="*,*:before,*:after{animation:none!important;transition:none!important}"
                                   "html,body{height:auto!important;overflow:visible!important;scroll-snap-type:none!important}")
        page.wait_for_timeout(300)
        h = page.evaluate("Math.ceil(Math.max(document.documentElement.scrollHeight, document.body.scrollHeight))")
        w_in, h_in = WIDTH_PX / 96, h / 96
        scale = min(1.0, MAX_IN / h_in)
        pdf = page.pdf(width=f"{w_in * scale:.3f}in", height=f"{h_in * scale + 0.02:.3f}in",
                       scale=scale, print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                       page_ranges="1")
        page.close()
        return pdf, h, scale
