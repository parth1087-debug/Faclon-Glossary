"""The two call-to-action buttons shared by every page: Book a demo and the Faclon website.

Each page builder imports CTA_BUTTONS and drops it into its closing navy band. Styles are
inline so the buttons look the same on every page whatever that page's own CSS is.
Change the links or labels here and re-run the page builders.
"""
BOOK_A_DEMO = "https://www.faclon.com/book-a-demo"
WEBSITE = "https://www.faclon.com"

_BASE = ("display:inline-block;font-family:Inter,system-ui,sans-serif;font-weight:600;font-size:15px;"
         "line-height:1.2;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap;color:#fff;")

CTA_BUTTONS = (
    '<div class="ctabtns" style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">'
    f'<a href="{BOOK_A_DEMO}" style="{_BASE}background:#3D63F5;border:1.5px solid #3D63F5">Book a demo</a>'
    f'<a href="{WEBSITE}" style="{_BASE}background:transparent;border:1.5px solid rgba(255,255,255,.4)">www.faclon.com</a>'
    '</div>'
)
