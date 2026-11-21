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
<div class="stat"><b>{len(EXAMS)}+</b><span>Exams Listed</span></div>
<div class="stat"><b>{len(EP["questions"])}</b><span>Practice Questions</span></div>
<div class="stat"><b>{len(NOTES)}</b><span>Study Notes</span></div>
<div class="stat"><b>36</b><span>States &amp; UTs</span></div>
<div class="stat"><b>22</b><span>Indian Languages</span></div>
</div></section>
<section class="container"><div class="notice"><b>⚠️ Honesty note:</b> ExamPath does not copy official papers. Where a paper is in the official archive, its <b>official link</b> is given. Where it is not available yet, it clearly says <b>“Not available yet”</b> — never a fake PDF. Practice questions are original ExamPath questions, not official PYQs. All numbers on this page are real — exams listed, questions and notes actually on this website.</div>
<div class="card" style="text-align:center"><h3>The admin panel is built separately</h3><p>This is only the <b>User Website</b> (no login). The admin dashboard — exam, paper and question management — will be a separate project, never mixed into this website.</p></div></section>"""
    return page("ExamPath India — One Nation. One Learning Platform. | Previous Papers, Mock Tests, Notes",
                "ExamPath India — free all-India exam preparation. SSC, Railway, UPSC, Banking, Defence, Teaching, NEET, JEE, CUET and all 28 states + 8 UTs. Year-wise previous papers from official sources, mock tests, notes, current affairs. No login needed.",
                "home", body, "home")
