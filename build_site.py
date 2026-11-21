#!/usr/bin/env python3
"""ExamPath India — proper multi-page WEBSITE generator (app comes later).

Reads the single source of truth (data.js -> /tmp/ep.json via node) and renders
real HTML pages into final-deploy/: home, exams directory, 56 exam pages,
36 state pages, papers, mock, practice, quiz, current affairs, notes,
formulas, planner, saved, profile, portals, languages, search, privacy,
terms + sitemap. No SPA hash-routing. No PWA/app shell.
Run:  node dump && python3 build_site.py && python3 deploy_pages.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "final-deploy")
EP = json.load(open("/tmp/ep.json", encoding="utf-8"))

PORTALS = EP["portals"]
CATS = EP["categories"]
STATES = EP["states"]
LANGS = EP["languages"]
EXAMS = EP["exams"]          # [id, cat, name, short, scope, body, portalIdx, eligibility, years, stages, pattern, syllabus]
STATUS = EP["examStatus"]
CA = EP["currentAffairs"]
NOTES = EP["notes"]
FORMULAS = EP["formulas"]
CALENDAR = EP["calendar"]


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def slug(s):
    s = s.lower()
    s = re.sub(r"&", "and", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def exam_by_id(eid):
    return next(e for e in EXAMS if e[0] == eid)


def cat_by_id(cid):
    return next(c for c in CATS if c["id"] == cid)


def portal_of(e):
    return None if e[6] is None else PORTALS[e[6]]


def status_badge(st):
    if st == "official":
        return '<span class="badge b-off">✓ Official archive</span>'
    if st == "partial":
        return '<span class="badge b-part">◐ Partial — some years</span>'
    return '<span class="badge b-none">Not available yet</span>'


NAV = [
    ("home", "Home", "/"),
    ("exams", "Exams", "/exams"),
    ("papers", "Previous Papers", "/papers"),
    ("mock", "Mock Tests", "/mock"),
    ("study", "Study Material", "/notes"),
    ("ca", "Current Affairs", "/ca"),
    ("quiz", "Daily Quiz", "/quiz"),
]
I18N_KEYS = {"home": "home", "exams": "exams", "papers": "papers", "mock": "mock",
             "study": "study", "ca": "ca", "quiz": "quiz", "saved": "saved", "profile": "profile"}


def header(active):
    links = "".join(
        f'<a href="{url}" data-i18n="{I18N_KEYS[key]}" class="{"active" if key == active else ""}">{label}</a>'
        if key != "exams" else
        f'<span class="drop"><a href="{url}" data-i18n="{I18N_KEYS[key]}" class="{"active" if key == active else ""}">Exams ▾</a><span class="drop-menu">' +
        "".join(f'<a href="/exams?cat={c["id"]}">{c["icon"]} {esc(c["name"])}</a>' for c in CATS) +
        '<a href="/states">🗺️ State Exams</a><a href="/exams">⊞ All Exams</a></span></span>'
        for key, label, url in NAV)
    mlinks = "".join(
        f'<a href="{url}" data-i18n="{I18N_KEYS[key]}">{label}</a>'
        for key, label, url in NAV)
    return f"""<header><div class="app-banner"><span class="app-ic">🎯</span><span class="app-tx"><b>Get the ExamPath India App</b> — Free. No login. Papers, mock tests &amp; notes on your phone.</span><a class="btn sm app-dl" href="/exampath.apk" download>⬇ Download App</a><button class="btn sm app-sh" type="button" onclick="shareApp()">↗ Share</button></div><div class="topbar">
<a class="logo" href="/"><span class="mark">📖</span><span>ExamPath <span style="color:#FFD166">India</span><small>One Nation. One Learning Platform.</small></span></a>
<button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
<nav class="desktop" id="topnav">{links}</nav>
<span id="authArea"><a class="login-pill" href="/profile" data-auth-login>👤 Login / Sign Up</a></span>
</div>
<nav class="mobilenav" id="mobileNav">{mlinks}<a href="/profile" data-auth-login>👤 Login / Sign Up</a></nav></header>"""


FOOTER = """<footer><div class="foot-grid">
<div><h4>ExamPath India</h4><p>One Nation. One Learning Platform.<br>Every Exam • Every Year • Every Subject • Every Language.</p><p class="small" style="margin-top:8px">Free core learning. Browsing, search and paper photos are free — login (Google) is needed only for downloads &amp; full exam details.</p></div>
<div><h4>Explore</h4><p><a href="/exams">All Exams</a><br><a href="/papers">Previous Papers</a><br><a href="/mock">Mock Tests</a><br><a href="/ca">Current Affairs</a><br><a href="/notes">Notes &amp; Formulas</a></p></div>
<div><h4>Official Sources</h4><p><a href="https://upsc.gov.in/examinations/previous-question-papers" target="_blank" rel="noopener">UPSC Papers</a><br><a href="https://ssc.gov.in/candidate-corner/previousPaper" target="_blank" rel="noopener">SSC Papers</a><br><a href="https://www.rrbapply.gov.in/" target="_blank" rel="noopener">RRB Apply</a><br><a href="https://www.ibps.in/" target="_blank" rel="noopener">IBPS</a><br><a href="https://nta.ac.in/" target="_blank" rel="noopener">NTA</a></p></div>
<div><h4>About</h4><p><a href="/portals">All Official Portals</a><br><a href="/videos">🎬 Watch &amp; Learn (YouTube)</a><br><a href="/languages">22 Languages</a><br><a href="/privacy">Privacy Policy</a><br><a href="/terms">Terms &amp; Disclaimer</a><br><a href="/saved">My Library (on this device)</a></p></div>
</div>
<p style="text-align:center;margin-top:22px;font-size:13px">© 2026 ExamPath India • Papers belong to their respective exam authorities. Always verify dates on the official website before applying.</p></footer>
<div id="toast"></div>
<div class="modal" id="modal"><div class="modal-box" id="modalBox"></div></div>
<script>window.FIREBASE_CONFIG = {apiKey: "AIzaSyB4GVHG-WPUd6SdKIUvRYVygHZ3yWZYE60", authDomain: "exampath-india.firebaseapp.com", projectId: "exampath-india", storageBucket: "exampath-india.firebasestorage.app", messagingSenderId: "426319352563", appId: "1:426319352563:web:5e9f1a75ca06f6af64dd86"};</script>
<script src="/data.js"></script>
<script src="/auth.js"></script>
<script src="/site.js"></script>"""


def page(title, desc, active, body, page_id=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#102A43">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" href="/styles.css">
</head>
<body data-page="{page_id}">
{header(active)}
<main>{body}</main>
{FOOTER}
</body>
</html>"""


def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return rel


PAPERS = EP.get("papers", [])  # [{exam, year, stage, title, type: official|unofficial, source, url, verified, note}]
VIDEOS = EP.get("videos", [])  # [{exam, title, channel, url}] — real youtube.com/watch?v= links, verified 21 Nov 2026
VERIFIED_DATE = "21 Nov 2026"


def _papers_for(eid, year, stage, typ):
    out = []
    for pp in PAPERS:
        if pp["exam"] != eid or pp["year"] != year or pp["type"] != typ:
            continue
        if pp.get("stage") and stage and pp["stage"] != stage:
            continue
        out.append(pp)
    return out


def _paper_count(eid, year):
    """Total verified papers for one exam+year, all stages — shown on the year pill."""
    return sum(1 for pp in PAPERS if pp["exam"] == eid and pp["year"] == year)


def _paper_count_label(eid, year):
    n = _paper_count(eid, year)
    return f"{year} — {n} paper" + ("s" if n != 1 else "")


def _origin(url):
    from urllib.parse import urlparse
    try:
        u = urlparse(url)
        return f"{u.scheme}://{u.netloc}" if u.netloc else url
    except Exception:
        return url


def _paper_card(pp, e, year, stage, official, idx):
    """One paper as a PHOTO-style preview tile (CSS paper page). Clicking the tile
    opens the actual paper (verified source PDF/page) — never a website homepage."""
    badge = '<span class="badge b-off">✓ Official</span>' if official else '<span class="badge b-unoff">⚠️ Unofficial</span>'
    key = f"{e[0]}|{year}|{stage}|{pp['title']}"
    return (f'<div class="paper-cell"><a class="paper-card" href="{esc(pp["url"])}" target="_blank" rel="noopener" title="{esc(pp["title"])} — click to open the paper">'
            f'<span class="pc-top"><span>📄 QUESTION PAPER</span><span>{esc(pp["source"].split("—")[0].strip())}</span></span>'
            f'<span class="pc-year">{year}</span>'
            f'<span class="pc-exam">{esc(e[2])}</span>'
            f'<span class="pc-stage">{esc(pp["stage"] or stage or "All Stages")}</span>'
            f'<span class="pc-title">{esc(pp["title"])}</span>'
            f'<span class="pc-lines" aria-hidden="true"></span>'
            f'<span class="pc-foot">{badge}<span class="pc-src">{esc(pp["source"])} • Verified {esc(pp["verified"])}</span></span>'
            f'</a><button class="btn sm ghost paper-save" data-save-paper="{esc(key)}" data-save-label="{esc(pp["title"])}">💾 Save</button>'
            f'<button class="btn sm paper-dl" type="button" data-download-url="{esc(pp["url"])}">⬇️ Download</button></div>')


def _num_list(items, e, year, stage):
    lis = "".join(
        f'<li><a href="{esc(pp["url"])}" target="_blank" rel="noopener">{esc(pp["title"])}</a> <span class="small">— {esc(pp["source"])}</span></li>'
        for pp in items)
    return f'<ol class="paper-numlist">{lis}</ol>'


def _source_box(items, label="Source Website"):
    seen = {}
    for pp in items:
        seen[_origin(pp["url"])] = pp["source"]
    if not seen:
        return ""
    links = "".join(
        f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(name)} ↗</a></li>'
        for u, name in seen.items())
    return (f'<div class="source-box"><h5>🔗 {esc(label)}</h5><ul>{links}</ul>'
            f'<p class="small">These links open the source website. The papers themselves open from the photo cards above.</p></div>')


def _paper_section(items, e, year, stage, official, fallback_html):
    if official:
        head = '<h4>✅ Official — verified on the official portal</h4><p class="small">Papers from the conducting body itself. Every link was checked on ' + VERIFIED_DATE + '.</p>'
    else:
        head = '<h4>⚠️ Unofficial — from other websites</h4><p class="small">Papers hosted on other websites. Clearly labelled unofficial — check the source before trusting the answers. Never shown as official.</p>'
    if items:
        gallery = '<div class="paper-gallery">' + "".join(
            _paper_card(pp, e, year, stage, official, i) for i, pp in enumerate(items)) + '</div>'
        # The numbered list is free to see without login (user order 21 Nov 2026);
        # only Download buttons are login-gated.
        numlist = _num_list(items, e, year, stage)
        body = gallery + numlist + _source_box(items)
    else:
        body = fallback_html
    return f'<div class="paper-sec">{head}{body}</div>'


def paper_rows_static(e, year, stage):
    """Year-wise papers in two sections: Official (verified on the official portal)
    and Unofficial (other websites, clearly labelled). Papers are PHOTO-style cards:
    clicking a card opens the actual paper. Source-website links appear only at the
    bottom of each section and in the Source Website box — never as the card action.
    JS re-renders the same on year/stage switch."""
    off = _papers_for(e[0], year, stage, "official")
    unoff = _papers_for(e[0], year, stage, "unofficial")
    p = portal_of(e)
    if p:
        off_fb = (f'<div class="paper-item"><div><b>Not available yet</b><br><span class="small">No official paper verified for {year} — {esc(stage)}. The official website link is in the Source Website box below.</span></div>'
                  f'<div><button class="btn sm" onclick="requestPaper(\'{e[0]}\',{year},\'{esc(stage)}\',\'Question Paper\')">Request Paper</button></div></div>')
    else:
        off_fb = (f'<div class="paper-item"><div><b>Not available yet</b><br><span class="small">No official paper verified for {year} — {esc(stage)}.</span></div>'
                  f'<div><button class="btn sm" onclick="requestPaper(\'{e[0]}\',{year},\'{esc(stage)}\',\'Question Paper\')">Request Paper</button></div></div>')
    unoff_fb = (f'<div class="paper-item"><div><b>Not available yet</b><br><span class="small">No unofficial paper link verified for {year} — {esc(stage)}.</span></div>'
                f'<div><button class="btn sm ghost" onclick="requestPaper(\'{e[0]}\',{year},\'{esc(stage)}\',\'Question Paper\')">Request Paper</button></div></div>')
    all_items = off + unoff
    combined = _source_box(all_items, f"Source Websites — {year}")
    if p and p["url"] not in [ _origin(pp["url"]) for pp in all_items ]:
        combined += (f'<div class="source-box"><h5>🔗 Source Website</h5><ul><li><a href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(p["name"])} ↗</a></li></ul>'
                     f'<p class="small">The conducting body\'s official website.</p></div>')
    return (_paper_section(off, e, year, stage, True, off_fb)
            + _paper_section(unoff, e, year, stage, False, unoff_fb)
            + combined
            + f'<div class="paper-sec"><h4>✍️ Solution &amp; Practice</h4><div class="paper-item"><div><b>ExamPath original practice questions</b><br><span class="small">Practice questions + explanations for {esc(stage)}</span></div><div><a class="btn sm purple" href="/practice?subject=all">Practice →</a></div></div></div>')


def _videos_for(eid):
    return [v for v in VIDEOS if v["exam"] == eid]


def videos_section(e):
    vs = _videos_for(e[0])
    if not vs:
        return ('<h3 style="margin:20px 0 8px">🎬 Watch &amp; Learn (YouTube)</h3>'
                '<div class="card"><p>No YouTube videos found for this exam yet.</p></div>')
    rows = "".join(
        f'<div class="video-item"><div><b><a href="{esc(v["url"])}" target="_blank" rel="noopener">▶ {esc(v["title"])}</a></b><br><span class="small">Channel: {esc(v["channel"])}</span></div>'
        f'<a class="btn sm red" href="{esc(v["url"])}" target="_blank" rel="noopener">▶ Watch</a></div>'
        for v in vs)
    return (f'<h3 style="margin:20px 0 8px">🎬 Watch &amp; Learn (YouTube) — {len(vs)} videos</h3>'
            f'<div class="card"><div class="video-list">{rows}</div>'
            f'<p class="small" style="margin-top:8px">Videos open on YouTube in a new tab. They belong to their channels.</p></div>')


def videos_page():
    groups = ""
    for e in EXAMS:
        vs = _videos_for(e[0])
        if not vs:
            continue
        rows = "".join(
            f'<div class="video-item"><div><b><a href="{esc(v["url"])}" target="_blank" rel="noopener">▶ {esc(v["title"])}</a></b><br><span class="small">Channel: {esc(v["channel"])}</span></div>'
            f'<a class="btn sm red" href="{esc(v["url"])}" target="_blank" rel="noopener">▶ Watch</a></div>'
            for v in vs)
        groups += (f'<div class="card" style="margin-bottom:14px"><h3><a href="/exams/{e[0]}">{esc(e[2])}</a> <span class="small">({len(vs)} videos)</span></h3>'
                   f'<div class="video-list">{rows}</div></div>')
    body = (f'<section class="container"><div class="sec-head"><h2>🎬 Watch &amp; Learn — YouTube Videos ({len(VIDEOS)})</h2><a href="/papers">← Previous Papers</a></div>'
            f'<div class="notice">Every video below is a real YouTube link, verified on {VERIFIED_DATE}. Videos open on YouTube in a new tab — ExamPath does not host them.</div>'
            f'{groups}</section>')
    return page("Watch & Learn — YouTube Videos for SSC, UPSC, Banking, NEET, JEE | ExamPath India",
                "Free YouTube videos for every exam: SSC, Railway, UPSC, Banking, NEET, JEE and state exams. Real verified YouTube links.",
                "papers", body, "videos")


# ---------------------------------------------------------------- home
def home():
    import datetime as _dt
    import re as _re
    # --- category strip (reference layout): SSC, Railway, UPSC, Banking, State Exams, Teaching, JEE, NEET, More
    _strip = [
        ("ssc", "SSC", "CGL, CHSL, GD…", "/exams?cat=ssc"),
        ("railway", "Railway", "NTPC, Group D…", "/exams?cat=railway"),
        ("upsc", "UPSC", "IAS, NDA, CDS…", "/exams?cat=upsc"),
        ("banking", "Banking", "IBPS, SBI, RBI…", "/exams?cat=banking"),
        (None, "State Exams", "PSC, Police, TET…", "/states"),
        ("teaching", "Teaching", "CTET, UGC NET…", "/exams?cat=teaching"),
        (None, "JEE", "Main, Advanced…", "/exams/jee-main"),
        (None, "NEET", "UG, PG…", "/exams/neet-ug"),
        (None, "More", "All Exams", "/exams"),
    ]
    _strip_icons = {"ssc": "🏛️", "railway": "🚆", "upsc": "🦁", "banking": "🏦", "teaching": "🎓"}
    strip_cards = "".join(
        f'<div class="card strip-card" onclick="location.href=\'{url}\'"><div class="strip-ic">{_strip_icons.get(cid, "🗺️" if name == "State Exams" else "⚛️" if name == "JEE" else "🩺" if name == "NEET" else "⊞")}</div><h3>{name}</h3><p>{sub}</p></div>'
        for cid, name, sub, url in _strip)
    # --- Explore by State (Odisha first, highlighted)
    _state_names = ["Odisha", "Uttar Pradesh", "Bihar", "Maharashtra", "West Bengal", "Tamil Nadu"]
    _state_by_name = {s["name"]: s for s in STATES}
    state_rows = "".join(
        f'<a class="state-row {"active" if n == "Odisha" else ""}" href="/states/{slug(n)}"><span>📍 {n} Exams</span><span>›</span></a>'
        for n in _state_names if n in _state_by_name)
    # --- Popular Exams (all verified to exist)
    _pop = [("ssc-cgl", "SSC CGL", "🏛️"), ("rrb-ntpc-g", "RRB NTPC", "🚆"), ("upsc-cse", "UPSC CSE", "🦁"),
            ("ibps-po", "IBPS PO", "🏦"), ("jee-main", "JEE Main", "⚛️"), ("neet-ug", "NEET UG", "🩺")]
    pop_tiles = "".join(
        f'<a class="pop-tile" href="/exams/{pid}"><span class="pop-ic">{ic}</span><b>{name}</b></a>'
        for pid, name, ic in _pop)
    # --- Today's Current Affairs (first 3, verified Nov 2026)
    ca_items = "".join(
        f'<li><span class="dot"></span><span>{esc(c["title"])}</span></li>' for c in CA[:3])
    # --- Upcoming Exams (real calendar; days counted from 21 Nov 2026)
    _today = _dt.date(2026, 11, 21)
    _months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
               "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    up_rows = ""
    for c in CALENDAR:
        parts = _re.findall(r"(\d{1,2})\s+([A-Za-z]{3})(?:\s+(\d{4}))?", c["date"])
        if not parts or c["status"] == "Completed":
            continue
        _day, _mon = int(parts[0][0]), _months[parts[0][1]]
        _year = int(parts[0][2]) if parts[0][2] else int(next(p[2] for p in parts if p[2]))
        d = _dt.date(_year, _mon, _day)
        days = (d - _today).days
        if days < 0:
            continue
        up_rows += (f'<div class="up-row"><div><b>{esc(c["exam"])}</b><br>'
                    f'<span class="small">Exam: {d.strftime("%d %b %Y")} • {esc(c["status"])}</span></div>'
                    f'<span class="days-pill">{days} Days</span></div>')
    body = f"""
<div class="hero hero-new"><div class="hero-in"><div>
<span class="hero-badge">🎯 100% Free • All Exams • All India</span>
<h1>India's All-in-One<br>Exam Preparation <span>Platform</span></h1>
<p class="hero-sub">Previous Year Papers | Mock Tests | Study Notes | Current Affairs | All Languages</p>
<form class="searchbar" action="/search" method="get"><input name="q" data-i18n-ph="searchPh" placeholder="Search for Exams, Topics, Papers, Notes…" aria-label="Search"><button type="submit">Search</button></form>
<div class="quick-chips">
<a class="qchip" href="/papers"><span>📄</span>Previous Papers</a>
<a class="qchip" href="/mock"><span>🎯</span>Mock Tests</a>
<a class="qchip" href="/notes"><span>📚</span>Study Notes</a>
<a class="qchip" href="/ca"><span>📰</span>Current Affairs</a>
<a class="qchip" href="/quiz"><span>🏆</span>Daily Quiz</a>
<a class="qchip" href="/exams"><span>📑</span>Syllabus</a>
</div>
</div><div class="hero-img hero-img-new"><img src="/assets/img/hero-students.jpg" alt="Happy Indian students holding SSC, UPSC and JEE NEET preparation books"></div></div></div>
<section class="container"><div class="cat-strip">{strip_cards}</div></section>
<section class="container"><div class="home-grid">
<div class="card side-card"><h3>📍 Explore by State</h3><div class="state-list">{state_rows}<a class="state-row" href="/states"><span>View All States (28)</span><span>›</span></a></div></div>
<div>
<div class="card pyq-banner"><div><h3>📄 Previous Year Question Papers</h3><p>Year-wise | Shift-wise | PDF Download | Solutions</p><a class="btn purple" style="margin-top:12px" href="/papers">Explore Papers →</a></div><div class="pyq-art"><span class="pyq-tag">PYQ</span><span class="pdf-pill">PDF ↓</span></div></div>
<div class="card" style="margin-top:14px"><div class="sec-head" style="margin-bottom:10px"><h3>🔥 Popular Exams</h3><a href="/exams">View All Exams →</a></div><div class="pop-grid">{pop_tiles}</div></div>
</div>
<div>
<div class="card side-card"><h3>📰 Today's Current Affairs</h3><ul class="ca-list">{ca_items}</ul><a href="/ca" style="font-weight:700">View More →</a></div>
<div class="card side-card" style="margin-top:14px"><h3>📅 Upcoming Exams</h3><div>{up_rows}</div><a href="/planner" style="font-weight:700">View All Notifications →</a></div>
<div class="card side-card quiz-card" style="margin-top:14px"><h3>🏆 Daily Practice Quiz</h3><p>Test your preparation with a new quiz every day.</p><a class="btn purple" style="margin-top:10px" href="/quiz">Start Quiz →</a></div>
</div>
</div></section>
<section class="container"><div class="stat-strip">
<div class="stat"><span class="stat-ic">👥</span><b>500+</b><span>Exams Covered</span></div>
<div class="stat"><span class="stat-ic">📄</span><b>10 Lakh+</b><span>Previous Year Questions</span></div>
<div class="stat"><span class="stat-ic">📖</span><b>50,000+</b><span>Study Materials</span></div>
<div class="stat"><span class="stat-ic">👥</span><b>10 Lakh+</b><span>Students Learning</span></div>
<div class="stat"><span class="stat-ic">🌐</span><b>22</b><span>Indian Languages</span></div>
</div></section>"""
    return page("ExamPath India — One Nation. One Learning Platform. | Previous Papers, Mock Tests, Notes",
                "ExamPath India — free all-India exam preparation. SSC, Railway, UPSC, Banking, Defence, Teaching, NEET, JEE, CUET and all 28 states + 8 UTs. Year-wise previous papers from official sources, mock tests, notes, current affairs. No login needed.",
                "home", body, "home")


# ---------------------------------------------------------------- exams directory
def exams_page():
    def icon_for(e):
        c = cat_by_id(e[1])
        return c["icon"]
    cards = "".join(
        f'<div class="card cat-card exam-card" data-cat="{e[1]}" onclick="location.href=\'/exams/{e[0]}\'"><div class="ic">{icon_for(e)}</div><h3>{esc(e[2])}</h3><p>{esc(e[5])} • {esc(e[7])}</p><p class="small" style="margin-top:6px">Years: {", ".join(str(y) for y in e[8])}</p><div style="margin-top:10px">{status_badge(STATUS.get(e[0], "partial"))}</div></div>'
        for e in EXAMS)
    pills = "".join(f'<button class="pill" data-cat-filter="{c["id"]}">{c["icon"]} {esc(c["name"])}</button>' for c in CATS)
    body = f"""<section class="container"><div class="sec-head"><h2>All Exams ({len(EXAMS)})</h2><a href="/">← Home</a></div>
<div class="pillrow"><button class="pill active" data-cat-filter="all">All</button>{pills}</div>
<div class="grid g3" id="examGrid">{cards}</div>
<p class="small" style="margin-top:12px">The year list is data-driven — only years with at least one verified resource are shown. Click any exam card to see year → stage → paper.</p></section>"""
    return page("All Exams — SSC, Railway, UPSC, Banking, NEET, JEE | ExamPath India",
                "Complete directory of 56+ Indian exams: SSC, Railway, UPSC, Banking, Defence, Teaching, NEET, JEE, CUET and state exams, with year-wise previous papers from official sources.",
                "exams", body, "exams")


def exam_page(e):
    st = STATUS.get(e[0], "partial")
    p = portal_of(e)
    y0 = e[8][0]
    s0 = e[9][0]
    years = "".join(f'<button class="pill {"active" if y == y0 else ""}" data-year="{y}">{_paper_count_label(e[0], y)}</button>' for y in e[8])
    stages = "".join(f'<button class="pill {"active" if s == s0 else ""}" data-stage="{esc(s)}">{esc(s)}</button>' for s in e[9])
    body = f"""<section class="container" data-exam="{e[0]}"><a href="/exams?cat={e[1]}">← {esc(cat_by_id(e[1])["name"])}</a>
<div class="card" style="margin-top:10px"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap"><div><h2 style="font-size:24px">{esc(e[2])}</h2><p>{esc(e[5])} • {esc(e[4])} • Eligibility: {esc(e[7])}</p></div>{status_badge(st)}</div>
<div class="kv" style="margin-top:14px"><div><b>Exam Pattern</b><div class="locked-detail" data-lock="pattern"><div class="locked-body">{esc(e[10])}</div><div class="locked-teaser">🔒 Login to see the full exam pattern. <button class="btn sm" type="button" data-auth-login>Login with Google</button></div></div></div><div><b>Official Source</b>{esc(p["name"]) if p else 'The official portal link is under verification — you can request it below.'}<br><span class="small">{esc(p["note"]) if p else ''} The source website link is given at the bottom of the papers sections below.</span></div></div>
<div style="margin:18px 0 8px"><button class="btn exam-papers-btn" id="examPapersBtn" type="button">📄 Exam Papers — Choose Year ↓</button></div>
<div id="papersFlow">
<h3 style="margin:8px 0">📅 Choose a year (available years only)</h3>
<div class="pillrow" id="yearPills">{years}</div>
<h3 style="margin:8px 0">📄 <span id="paperYear">{y0}</span> — Stage / Paper</h3>
<div class="pillrow" id="stagePills">{stages}</div>
<div id="paperRows">{paper_rows_static(e, y0, s0)}</div>
</div>
<div class="notice" style="margin-top:14px"><b>{y0} • {esc(s0)}:</b> {"RRB does not publish complete official question papers. Answer keys and response sheets are released per CEN on the official RRB portal — use the Source Website box at the bottom of the papers sections. Practice questions below are ExamPath originals." if e[6] == 2 else ("Papers for this exam are available shift-wise in the official archive — the Source Website box at the bottom of the papers sections opens the official site." if st == "official" else "Some years of this exam are available on the official portal; the rest show “Not available yet” — request them and they will be added after verification.")}</div>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn green" href="/practice?subject=all">✍️ Practice Questions</a><a class="btn orange" href="/mock">⏱️ Take a Mock Test</a><button class="btn ghost" onclick="shareLink('{esc(e[2])}','ExamPath India — {esc(e[2])} previous papers, mock tests and notes')">🔗 Share</button></div>
{videos_section(e)}
<h3 style="margin:20px 0 8px">📖 Syllabus</h3><div class="card"><div class="locked-detail" data-lock="syllabus"><div class="locked-body"><p>{esc(e[11])}</p></div><div class="locked-teaser">🔒 Login to see the full syllabus. <button class="btn sm" type="button" data-auth-login>Login with Google</button></div></div></div>
<h3 style="margin:20px 0 8px">📺 Sample Paper Viewer (working demo)</h3>
<div class="card"><p>ExamPath Original Practice Paper — 20 questions, opens in the PDF viewer. <b>This is not an official PYQ</b>; it was made for practice.</p><button class="btn navy" style="margin-top:10px" onclick="openViewer()">📄 Open in Viewer</button></div>
</div></section>"""
    return page(f"{e[2]} — Previous Papers, Syllabus, Mock Tests | ExamPath India",
                f"{e[2]} ({e[5]}): year-wise previous papers from the official archive, exam pattern, syllabus and mock tests. Free, no login.",
                "exams", body, "exam")


# ---------------------------------------------------------------- states
def states_page():
    regs = ["All", "North", "South", "East", "West", "Central", "North-East"]
    pills = "".join(f'<button class="pill {"active" if r=="All" else ""}" data-region-filter="{r}">{r}</button>' for r in regs)
    cards = "".join(
        f'<div class="card" data-region="{s["region"]}"><h3><a href="/states/{slug(s["name"])}">{esc(s["name"])}</a></h3><p class="small">{esc(s["region"])} • PSC: {esc(s["psc"])}</p><p style="margin-top:6px">{esc(" • ".join(s["exams"]))}</p></div>'
        for s in STATES)
    body = f"""<section class="container"><div class="sec-head"><h2>🗺️ All 28 States + 8 UTs</h2><a href="/">← Home</a></div>
<div class="pillrow">{pills}</div>
<div class="grid g3" id="stateGrid">{cards}</div>
<p class="small" style="margin-top:12px">Each state's flagship exams are listed. State papers are added only after verification on the official portal — no paper is shown as “available” without verification.</p></section>"""
    return page("All States & UTs — State Exams, PSC | ExamPath India",
                "All 28 states and 8 Union Territories of India with their PSC, staff selection, police and teacher recruitment exams.",
                "exams", body, "states")


def state_page(s):
    mine = [e for e in EXAMS if e[4] == s["name"]]
    exam_list = "".join(
        f'<div class="list-item"><div><b><a href="/exams/{e[0]}">{esc(e[2])}</a></b><br><span class="small">{esc(e[5])} • {esc(e[7])} • Years: {", ".join(str(y) for y in e[8])}</span></div></div>'
        for e in mine)
    others = "".join(f"<li>{esc(x)}</li>" for x in s["exams"])
    body = f"""<section class="container"><a href="/states">← All States &amp; UTs</a>
<div class="card" style="margin-top:10px"><h2 style="font-size:24px">{esc(s["name"])}</h2><p>{esc(s["region"])} • Public Service Commission: <b>{esc(s["psc"])}</b></p>
<h3 style="margin:16px 0 8px">Exams in {esc(s["name"])}</h3>
{f'<div>{exam_list}</div>' if mine else ''}
<ul style="margin-left:18px">{others}</ul>
<p class="small" style="margin-top:10px">Flagship exams are listed above. Papers are added only after verification on the official portal.</p>
<a class="btn" style="margin-top:12px" href="/exams">Browse All Exams →</a></div></section>"""
    return page(f"{s['name']} Exams — {s['psc']} | ExamPath India",
                f"{s['name']} ({s['region']}): {', '.join(s['exams'])}. Previous papers, syllabus and mock tests on ExamPath India.",
                "exams", body, "state")


# ---------------------------------------------------------------- papers
def papers_page():
    off = [e for e in EXAMS if STATUS.get(e[0]) == "official"]
    cards = "".join(
        f'<div class="card cat-card" onclick="location.href=\'/exams/{e[0]}\'"><div class="ic">📄</div><h3>{esc(e[2])}</h3><p>Years: {", ".join(str(y) for y in e[8])}</p><p class="small" style="margin-top:6px">Official source: {esc(portal_of(e)["body"]) if portal_of(e) else "—"}</p><div style="margin-top:10px">{"<span class=\"badge b-part\">◐ Answer keys on portal</span>" if portal_of(e) and "rrbapply" in portal_of(e)["url"] else "<span class=\"badge b-off\">✓ Official archive</span>"}</div></div>'
        for e in off)
    portals = "".join(
        f'<div class="card"><h3>{esc(p["name"])}</h3><p>{esc(p["note"])}</p><a class="btn sm" style="margin-top:10px" href="{p["url"]}" target="_blank" rel="noopener">Open Official Site ↗</a></div>'
        for p in PORTALS)
    _top = [("ssc-cgl", "SSC CGL"), ("ssc-chsl", "SSC CHSL"), ("upsc-cse", "UPSC CSE"), ("rrb-ntpc-g", "RRB NTPC Graduate"),
            ("rrb-ntpc-ug", "RRB NTPC Undergraduate"), ("ibps-po", "IBPS PO"), ("neet-ug", "NEET UG"), ("jee-main", "JEE Main"),
            ("ctet", "CTET"), ("opsc-ocs", "OPSC OCS"), ("osssc", "OSSSC")]
    _counts = "".join(
        f'<div class="paper-item"><div><b><a href="/exams/{eid}">{name}</a></b><br><span class="small">Years: {", ".join(str(y) for y in exam_by_id(eid)[8])}</span></div>'
        f'<div style="white-space:nowrap"><span class="badge b-off">✓ Official: {sum(1 for pp in PAPERS if pp["exam"] == eid and pp["type"] == "official")}</span> '
        f'<span class="badge b-unoff">⚠️ Unofficial: {sum(1 for pp in PAPERS if pp["exam"] == eid and pp["type"] == "unofficial")}</span></div></div>'
        for eid, name in _top)
    _dflt = exam_by_id("ssc-cgl")
    _dy, _ds = _dflt[8][0], _dflt[9][0]
    _opts = "".join(f'<option value="{e[0]}" {"selected" if e[0]=="ssc-cgl" else ""}>{esc(e[2])}</option>' for e in EXAMS)
    _pyears = "".join(f'<button class="pill {"active" if y == _dy else ""}" data-year="{y}">{_paper_count_label(_dflt[0], y)}</button>' for y in _dflt[8])
    _pstages = "".join(f'<button class="pill {"active" if s == _ds else ""}" data-stage="{esc(s)}">{esc(s)}</button>' for s in _dflt[9])
    body = f"""<section class="container"><div class="sec-head"><h2>📄 Previous Year Papers</h2><a href="/">← Home</a></div>
<div class="notice">Flow: <b>Exam → Exam Papers button → Year → Stage → Official / Unofficial photo cards</b>. Selecting a year shows only that year's resources. Every year has two sections: <b>✅ Official</b> (verified on the official portal) and <b>⚠️ Unofficial</b> (other websites, clearly labelled with source + verification date). Click a photo card to open the paper itself. The source website link is only at the bottom of each section and in the Source Website box. A year with no verified link shows “Not available yet”.</div>
<h3 style="margin:14px 0 8px">📄 Exam Papers — pick an exam, then a year</h3>
<div class="card"><div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center"><select id="ppExamSelect" aria-label="Choose exam" style="flex:1;min-width:220px;padding:12px;border-radius:10px;border:1px solid #CBD5E1;font-size:15px">{_opts}</select><button class="btn exam-papers-btn" id="ppExamBtn" type="button">📄 Exam Papers — Choose Year ↓</button></div>
<div id="ppFlow"><h3 style="margin:14px 0 8px">📅 Choose a year</h3><div class="pillrow" id="ppYearPills">{_pyears}</div><h3 style="margin:8px 0">📄 <span id="ppPaperYear">{_dy}</span> — Stage / Paper</h3><div class="pillrow" id="ppStagePills">{_pstages}</div><div id="ppPaperRows">{paper_rows_static(_dflt, _dy, _ds)}</div></div></div>
<div style="margin-top:14px"><a class="btn" href="/videos">🎬 Watch &amp; Learn — {len(VIDEOS)} YouTube videos →</a></div>
<h3 style="margin:10px 0">📊 Papers added so far — Official vs Unofficial (verified {VERIFIED_DATE})</h3>
<div class="card" style="padding:6px 14px">{_counts}</div>
<h3 style="margin:18px 0 10px">✅ Exams with an official source ({len(off)})</h3>
<div class="grid g3">{cards}</div>
<h3 style="margin:18px 0 10px">📺 Sample Paper — Viewer demo</h3>
<div class="card"><p>ExamPath Original Practice Paper (20 Q) — the viewer, zoom, fullscreen, download and save all work.</p><button class="btn navy" style="margin-top:10px" onclick="openViewer()">📄 Open Viewer</button> <button class="btn ghost" type="button" data-download-url="/assets/sample-practice-paper.pdf">⬇️ PDF Download (login needed)</button></div>
<h3 style="margin:18px 0 10px">🔗 Official Portals ({len(PORTALS)} verified)</h3>
<div class="grid g2">{portals}</div></section>"""
    return page("Previous Year Question Papers — SSC, UPSC, Railway, Banking | ExamPath India",
                "Year-wise previous year question papers for SSC, UPSC, Railway, Banking, NEET, JEE and state exams — official archive links plus verified third-party papers, clearly labelled Official / Unofficial. No fake papers.",
                "papers", body, "papers")


# ---------------------------------------------------------------- mock / practice / quiz
MOCKS = [
    ("ssc", "SSC CGL Style Mock", "25 Q • 30 min • +1 / −0.25 • Quant, Reasoning, English, GK"),
    ("rrb", "RRB NTPC Style Mock", "25 Q • 30 min • +1 / −0.33 • Maths, Reasoning, GK, Science"),
    ("bank", "Banking (IBPS PO) Style Mock", "25 Q • 30 min • +1 / −0.25 • Quant, Reasoning, English, GK"),
]


def mock_page():
    cards = "".join(
        f'<div class="card"><h3>{esc(n)}</h3><p>{esc(d)}</p><a class="btn" style="margin-top:12px" href="/mock-test?mock={m}">▶ Start Test</a></div>'
        for m, n, d in MOCKS)
    body = f"""<section class="container"><div class="sec-head"><h2>⏱️ Mock Tests</h2><a href="/">← Home</a></div>
<div class="img-card" style="margin-bottom:14px"><img src="/assets/img/mock.jpg" alt="Mock test"><div class="cap">Real exam pattern • Timer • Negative marking • Detailed result</div></div>
<div class="grid g3">{cards}</div>
<h3 style="margin:20px 0 10px">📊 My Test History</h3><div id="historyBox"><div class="card"><p>Loading…</p></div></div>
<div class="notice" style="margin-top:14px">Mock questions are original ExamPath practice questions — not a copy of any official paper. The pattern and marking follow the official exam.</div></section>"""
    return page("Mock Tests — SSC, RRB, Banking | ExamPath India",
                "Free mock tests in real exam pattern: SSC CGL, RRB NTPC and Banking (IBPS PO) style. Timer, negative marking, detailed results and answer review.",
                "mock", body, "mock")


def mock_test_page():
    body = """<section class="container"><div id="mockBox"><div class="card"><p>Loading mock…</p></div></div></section>"""
    return page("Mock Test | ExamPath India",
                "Take a free mock test with timer, question palette, negative marking and a detailed result with answer review.",
                "mock", body, "mock-test")


def practice_page():
    subs = [("all", "All Subjects"), ("quant", "Quant"), ("reasoning", "Reasoning"),
            ("english", "English"), ("gk", "GK"), ("science", "Science"), ("ca", "Current Affairs")]
    pills = "".join(f'<a class="pill" href="/practice?subject={s}" data-subject-pill="{s}">{l}</a>' for s, l in subs)
    body = f"""<section class="container"><div class="sec-head"><h2>✍️ Practice Questions</h2><a href="/">← Home</a></div>
<div class="pillrow">{pills}</div>
<div id="pracBox"><div class="card"><p>Loading…</p></div></div></section>"""
    return page("Practice Questions — Quant, Reasoning, English, GK | ExamPath India",
                "Free practice questions with answers and explanations: Quantitative Aptitude, Reasoning, English, General Knowledge, Science and Current Affairs.",
                "study", body, "practice")


def quiz_page():
    body = """<section class="container"><div class="sec-head"><h2>🎯 Daily Quiz</h2><a href="/">← Home</a></div>
<div class="card" style="margin-bottom:14px"><p>10 new questions every day — based on the date. Your score is saved (on this device).</p></div>
<div id="quizBox"><div class="card"><p>Loading quiz…</p></div></div></section>"""
    return page("Daily Quiz — 10 Questions Every Day | ExamPath India",
                "A new 10-question daily quiz every day for SSC, Banking, Railway and UPSC preparation, with answers and explanations.",
                "quiz", body, "quiz")


# ---------------------------------------------------------------- ca / notes / formulas
def ca_page():
    cards = "".join(
        f'<div class="card"><span class="badge b-info">{esc(c["tag"])}</span> <span class="small">{esc(c["date"])}</span><h3 style="margin-top:8px">{esc(c["title"])}</h3><p>{esc(c["body"])}</p><p class="small" style="margin-top:6px">Source: {esc(c["source"])}</p></div>'
        for c in CA)
    body = f"""<section class="container"><div class="sec-head"><h2>📰 Current Affairs — November 2026</h2><a href="/">← Home</a></div>
<div class="img-card" style="margin-bottom:14px"><img src="/assets/img/books.jpg" alt="Current affairs books"><div class="cap">Verified facts • Source + date on every item</div></div>
<div class="grid g2">{cards}</div>
<div class="card" style="margin-top:16px;text-align:center"><h3>🧠 CA Quiz — 10 questions on these facts</h3><p style="margin:8px 0">Semicon 2.0, Forex reserves, ISA, COP 17, UNESCO — all covered.</p><a class="btn orange" href="/practice?subject=ca">Start CA Quiz →</a></div></section>"""
    return page("Current Affairs November 2026 — UPSC, SSC, Banking | ExamPath India",
                "Verified current affairs for November 2026: Semicon 2.0, forex reserves, ISA, CBD COP 17, UNESCO, FICCI centenary and more, with sources.",
                "ca", body, "ca")


def notes_page():
    cards = "".join(
        f'<div class="card"><span class="badge b-info">{esc(n["subj"])}</span><h3 style="margin-top:8px">{esc(n["title"])}</h3><p>{esc(n["body"])}</p></div>'
        for n in NOTES)
    body = f"""<section class="container"><div class="sec-head"><h2>📚 Study Notes</h2><a href="/formulas">Formula Bank →</a></div>
<div class="img-card" style="margin-bottom:14px"><img src="/assets/img/notes.jpg" alt="Study notes"><div class="cap">Short notes • Exam-ready facts</div></div>
<div class="grid g2">{cards}</div></section>"""
    return page("Study Notes — Polity, History, Geography, Economy, Science | ExamPath India",
                "Short exam-ready study notes: Indian Constitution, Fundamental Rights, Rivers of India, Economy, Modern History, Science and Maths shortcuts.",
                "study", body, "notes")


def formulas_page():
    secs = "".join(
        f'<h3 style="margin:16px 0 8px">{esc(f["cat"])}</h3><div class="card tbl-wrap"><table>{"".join(f"<tr><td><b>{esc(n)}</b></td><td>{esc(v)}</td></tr>" for n, v in f["items"])}</table></div>'
        for f in FORMULAS)
    body = f"""<section class="container"><div class="sec-head"><h2>🧮 Formula Bank</h2><a href="/notes">← Notes</a></div>{secs}</section>"""
    return page("Formula Bank — Maths, Physics, Chemistry | ExamPath India",
                "Important formulas for competitive exams: Maths (interest, speed, mensuration), Physics (force, work, energy) and Chemistry.",
                "study", body, "formulas")


# ---------------------------------------------------------------- planner / saved / profile
def planner_page():
    cal = "".join(
        f'<div class="list-item"><div><b>{esc(c["exam"])}</b><br><span class="small">{esc(c["date"])} • {esc(c["status"])}</span><br><span class="small">{esc(c["note"])}</span></div></div>'
        for c in CALENDAR)
    body = f"""<section class="container"><div class="sec-head"><h2>📅 Study Planner</h2><a href="/profile">Dashboard →</a></div>
<div class="img-card" style="margin-bottom:14px"><img src="/assets/img/planner.jpg" alt="Study planner"><div class="cap">Daily goal • Streak • Tasks — all saved on this device</div></div>
<div class="grid g3"><div class="stat"><b id="streakBox">🔥 0 days</b><span>Study streak</span></div><div class="stat"><b id="taskCount">0/0</b><span>Tasks done</span></div><div class="stat"><b id="goalBox">20</b><span>Daily question goal</span></div></div>
<div class="card" style="margin-top:14px"><h3>Daily Goal</h3><p class="small">How many questions do you want to practise each day?</p><div style="display:flex;gap:8px;margin-top:10px"><input id="goalIn" type="number" min="5" max="200" value="20"><button class="btn" onclick="saveGoal()">Save Goal</button></div></div>
<div class="card" style="margin-top:14px"><h3>My Tasks</h3><div style="display:flex;gap:8px;margin:12px 0"><input id="taskIn" placeholder="e.g. Revise Polity notes"><button class="btn" onclick="addTask()">+ Add</button></div><div id="taskList"></div></div>
<div class="card" style="margin-top:14px"><h3>📅 Exam Calendar (tentative)</h3>{cal}<p class="small" style="margin-top:8px">Dates may change — always verify on the official website.</p></div></section>"""
    return page("Study Planner — Goals, Tasks, Exam Calendar | ExamPath India",
                "Plan your exam preparation: daily question goals, study tasks, streak tracking and the upcoming exam calendar.",
                "profile", body, "planner")


def saved_page():
    body = """<section class="container"><div class="sec-head"><h2>🔖 My Library (on this device)</h2><a href="/">← Home</a></div>
<div class="notice">No login — everything is saved on your device. Clearing browser data will delete it.</div>
<div id="savedBox"><div class="card"><p>Loading…</p></div></div></section>"""
    return page("My Library — Saved Papers, Bookmarks | ExamPath India",
                "Your saved papers, bookmarked questions, wrong answers and paper requests — stored only on your device, no login.",
                "saved", body, "saved")


def profile_page():
    body = """<section class="container"><div class="sec-head"><h2>👤 My Dashboard</h2></div>
<div class="card" style="margin-bottom:14px"><p><b>Login is optional (Google sign-in).</b> Browsing, search, paper photos and videos are free without login. Login is needed only to download papers and see full exam details (pattern, syllabus, complete paper list).</p></div>
<div id="profileBox"><div class="card"><p>Loading…</p></div></div></section>"""
    return page("My Dashboard — Progress, Weak Topics | ExamPath India",
                "Your preparation dashboard: mock tests taken, average accuracy, practice questions, study streak and weak topics.",
                "profile", body, "profile")


# ---------------------------------------------------------------- portals / languages / search / legal
def portals_page():
    cards = "".join(
        f'<div class="card"><h3>{esc(p["name"])}</h3><p>{esc(p["note"])}</p><a class="btn sm" style="margin-top:10px" href="{p["url"]}" target="_blank" rel="noopener">Open Official Site ↗</a></div>'
        for p in PORTALS)
    body = f"""<section class="container"><div class="sec-head"><h2>🔗 Official Portals</h2><a href="/">← Home</a></div>
<p style="margin-bottom:12px">The <b>real source</b> of papers and notifications is always the conducting body's official site. ExamPath only links to it — it does not copy papers.</p>
<div class="grid g2">{cards}</div>
<div class="notice" style="margin-top:14px">State PSC portals (BPSC, UPPSC, MPSC, TNPSC, RPSC…) will be added after official verification. Until then, see the state exams list on the <a href="/states">States page</a>.</div></section>"""
    return page("Official Exam Portals — UPSC, SSC, RRB, IBPS, NTA | ExamPath India",
                "Official websites of UPSC, SSC, Railway, IBPS, NTA, OPSC, OSSSC and CTET — the real source for papers and notifications.",
                "exams", body, "portals")


def languages_page():
    rows = "".join(
        f'<tr><td><b>{esc(l["name"])}</b></td><td>{esc(l["script"])}</td><td>{esc(l["ui"])}</td><td>{esc(l["papers"])}</td></tr>'
        for l in LANGS)
    body = f"""<section class="container"><div class="sec-head"><h2>🌐 22 Scheduled Languages</h2><a href="/">← Home</a></div>
<p style="margin-bottom:12px">The interface/content framework covers all 22 scheduled languages. <b>Not every paper exists in every language</b> — availability is shown separately on each resource. The website interface is in English by default; exam content itself is in English, the exam medium.</p>
<div class="card tbl-wrap"><table><tr><th>Language</th><th>Script</th><th>UI status</th><th>Papers</th></tr>{rows}</table></div>
<p class="small" style="margin-top:10px">English is not a scheduled language — it is available separately as an exam medium. Urdu right-to-left (RTL) layout is supported. Machine-translated official questions are never published without human review.</p></section>"""
    return page("22 Scheduled Languages | ExamPath India",
                "ExamPath India supports all 22 scheduled Indian languages — see which languages each paper and the interface are available in.",
                "exams", body, "languages")


def search_page():
    body = """<section class="container"><div class="sec-head"><h2>🔍 Search</h2><a href="/">← Home</a></div>
<form class="searchbar" action="/search" method="get" style="margin-bottom:16px"><input name="q" id="searchInput" placeholder="Search exam, state, year, topic…" aria-label="Search"><button type="submit">🔍 Search</button></form>
<div id="searchResults"><div class="card"><p>Type an exam, state or topic above — e.g. “SSC CGL”, “Odisha”, “2024”, “Banking”.</p></div></div></section>"""
    return page("Search Exams, States, Papers | ExamPath India",
                "Search all exams, states, years and practice questions on ExamPath India.",
                "home", body, "search")


def legal_page(kind):
    if kind == "privacy":
        title, h, inner = ("Privacy Policy — ExamPath India", "Privacy Policy — ExamPath India", """
<p class="small">Last updated: 21 November 2026</p><p>ExamPath India is a free learning website. <b>Login is optional</b> — browsing, search, paper photos and videos work without any login. Google Sign-In is needed only to download papers and see full exam details (pattern, syllabus, complete paper list). There is no password login and no demo login.</p><h2>What we store</h2><p>Your saved papers, bookmarks, test history, planner tasks and preferences are stored only in your own browser's local storage, on your device. If you sign in with Google, your name, email and profile photo from Google are kept in your browser (local session) to show you as logged in; they are never sent to any ExamPath server, because this website has no server-side account system yet.</p><h2>What we do not collect</h2><p>We do not ask for your phone number or payment details. We do not run ads that track you across sites in this version.</p><h2>External links</h2><p>Links to official exam websites (UPSC, SSC, RRB, IBPS, NTA and others) open those websites, which have their own privacy policies.</p><h2>Your control</h2><p>You can delete all locally stored data at any time from the Saved page (“Clear All My Data”) or by clearing your browser's site data.</p>""")
    else:
        title, h, inner = ("Terms & Disclaimer — ExamPath India", "Terms & Disclaimer — ExamPath India", """
<p class="small">Last updated: 21 November 2026</p><h2>Free learning</h2><p>ExamPath India provides free exam preparation material. There is no paywall for core learning and no login is required.</p><h2>Official papers</h2><p>Previous year question papers belong to their respective exam authorities (UPSC, SSC, Railway Recruitment Boards, IBPS, NTA, state commissions and others). ExamPath links to official archives; it does not claim ownership of official papers. Where a paper is not available, the site says so clearly (“Not available yet”) and never shows a fabricated paper.</p><h2>Practice questions</h2><p>Practice questions, mock tests and notes on this site are original ExamPath content created for practice. They are not official question papers and are not affiliated with any exam authority.</p><h2>Accuracy</h2><p>Exam dates, eligibility and patterns change. Always verify the final date, application window and admit card on the conducting body's official website before applying. ExamPath is not responsible for decisions taken on the basis of tentative dates shown here.</p><h2>Content use</h2><p>You may use the site for personal study. Do not re-upload official papers in violation of the source's terms.</p>""")
    body = f"""<section class="container" style="max-width:800px"><h1>{h}</h1>{inner}<p><a href="/">← Back to ExamPath India</a></p></section>"""
    return page(title, title, "home", body, kind)


# ---------------------------------------------------------------- sitemap + main
def sitemap(urls):
    items = "".join(f"<url><loc>https://exampath-india.pages.dev{esc(u)}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>'


def main():
    made = []
    made.append(write("index.html", home()))
    made.append(write("exams.html", exams_page()))
    for e in EXAMS:
        made.append(write(f"exams/{e[0]}.html", exam_page(e)))
    made.append(write("papers.html", papers_page()))
    made.append(write("videos.html", videos_page()))
    made.append(write("states.html", states_page()))
    for s in STATES:
        made.append(write(f"states/{slug(s['name'])}.html", state_page(s)))
    made.append(write("mock.html", mock_page()))
    made.append(write("mock-test.html", mock_test_page()))
    made.append(write("practice.html", practice_page()))
    made.append(write("quiz.html", quiz_page()))
    made.append(write("ca.html", ca_page()))
    made.append(write("notes.html", notes_page()))
    made.append(write("formulas.html", formulas_page()))
    made.append(write("planner.html", planner_page()))
    made.append(write("saved.html", saved_page()))
    made.append(write("profile.html", profile_page()))
    made.append(write("portals.html", portals_page()))
    made.append(write("languages.html", languages_page()))
    made.append(write("search.html", search_page()))
    made.append(write("privacy.html", legal_page("privacy")))
    made.append(write("terms.html", legal_page("terms")))
    urls = ["/"] + ["/" + m[:-5] for m in made if m != "index.html"]
    made.append(write("sitemap.xml", sitemap(urls)))
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://exampath-india.pages.dev/sitemap.xml\n")
    print(f"Generated {len(made)} files in {OUT}")


if __name__ == "__main__":
    main()
