# ExamPath India — Poster Rebuild Note

Date: 21 Nov 2026. Live: https://exampath-india.pages.dev/
Rebuilt the website home page to match the user's poster
(`~/workspace/user/files/113415_21_cc2o.png`) exactly, scrolling like a
normal desktop website. **No app anywhere** — the app banner, Download App
button, Share-app button and `exampath.apk` were all removed (the APK was
cancelled by the user; treat as if no app was ever made). No admin work.

## What changed vs the old design (section by section)

1. **Header** — navy `#102A43`, logo "ExamPath India" + tagline "One Nation.
   One Learning Platform.", gold 📖 book mark. Nav: Home, Exams ▾ (dropdown
   with 9 categories + State Exams + All Exams), Previous Papers, Mock Tests,
   Study Material, Current Affairs, Daily Quiz. Right: white "Login / Sign Up"
   pill → /profile (no forced login anywhere). Language selector and theme
   button removed (default language English, confirmed).
2. **Hero** — blue gradient (`#0A2463 → #1456C4 → #2E9BE6`), badge "100%
   Free • All Exams • All India", heading "India's All-in-One Exam
   Preparation Platform" ("Platform" in yellow), subline "Previous Year
   Papers | Mock Tests | Study Notes | Current Affairs | All Languages",
   white search bar with purple Search button, 6 quick chips. Right: the
   existing `hero-students.jpg` (3 students holding SSC / UPSC / JEE-NEET
   books) — matches the poster, kept as-is.
3. **Category row** — 9 white rounded cards: SSC, Railway, UPSC, Banking,
   State Exams, Teaching, JEE, NEET, More — each with icon + name + subtext,
   linking to the real category/exam pages.
4. **Main 3-column grid** — LEFT "Explore by State" (Odisha highlighted
   first, then UP, Bihar, Maharashtra, West Bengal, Tamil Nadu, "View All
   States (28)" at bottom; the linked page lists all 28 states + 8 UTs).
   CENTER: dark-blue PYQ banner ("Previous Year Question Papers — Year-wise
   | Shift-wise | PDF Download | Solutions" + Explore Papers button) and
   "Popular Exams" (SSC CGL, RRB NTPC, UPSC CSE, IBPS PO, JEE Main, NEET UG).
   RIGHT: "Today's Current Affairs" (3 real Nov 2026 items + View More),
   "Upcoming Exams" (real calendar dates with day pills) and "Daily Practice
   Quiz" card with Start Quiz button. The old SSC CHSL countdown strip was
   removed.
5. **Stats bar** — the poster's exact numbers: 500+ Exams Covered, 10 Lakh+
   Previous Year Questions, 50,000+ Study Materials, 10 Lakh+ Students
   Learning, 22 Indian Languages. (Deliberate: an earlier audit had replaced
   these with real counts — 56 exams, 80 questions, 8 notes — but the user
   ordered exact replication of his poster.)
6. **Footer** — links: Exams, Papers, Mock Tests, Study Material, Current
   Affairs, Privacy, Terms, Sources. The "admin panel is a separate app"
   line was removed.
7. **Layout** — desktop-first, max-width 1280px, sticky top header, long
   scrolling page. No bottom navigation, no mobile-app screens, no app
   banner/popup/promotion anywhere (verified: 0 matches for
   `app-banner|exampath.apk|Download App` in index.html, exam pages,
   papers.html, site.js and data.js).

## Papers — Official / Unofficial sections per year (added 21 Nov 2026)

Every exam page and the Papers page now show, for the selected year + stage:
- **✅ Official** — papers verified on the official portal only
  (UPSC/SSC/RRB/IBPS/NTA/OPSC/OSSSC/CTET). Where the body has no public
  paper archive (SSC: papers only via candidate login window; IBPS: no public
  archive; RRB: answer keys/response sheets only), the section links to the
  official portal/archive with that note — never a fake direct PDF.
- **⚠️ Unofficial** — papers from other websites, amber "Unofficial" badge,
  source name + full source URL + verification date (21 Nov 2026). Never
  shown as official. No paper without a source link.
- A year with no verified link shows **"Not available yet" + Request**.

Data: `EP.papers` in `final-deploy/data.js` — 155 entries
(48 official, 107 unofficial), each
`{exam, year, stage, title, type, source, url, verified, note}`.
Both the static generator (`build_site.py` → `paper_rows_static`) and the
year/stage switcher (`site.js` → `paperRows`) render the same two sections;
the switcher was verified in Node for RRB 2024 CBT 1 (6 PDFs), IBPS PO 2025,
UPSC 2025, CTET 2022 and a non-top exam (SSC GD → "Not available yet").

### Counts per exam (official / unofficial)

| Exam | Official | Unofficial |
|---|---|---|
| SSC CGL | 8 | 16 |
| SSC CHSL | 6 | 13 |
| UPSC CSE | 8 | 15 |
| RRB NTPC Graduate | 0 | 11 |
| RRB NTPC Undergraduate | 0 | 4 |
| IBPS PO | 7 | 11 |
| NEET UG | 6 | 12 |
| JEE Main | 4 | 8 |
| CTET | 4 | 7 |
| OPSC OCS | 4 | 8 |
| OSSSC | 1 | 2 |
| **Total** | **48** | **107** |

### Sources (all links checked 21 Nov 2026)

- **Official portals (curl 200, except UPSC/Testbook — page-fetch verified):**
  UPSC `upsc.gov.in/examinations/previous-question-papers` (page fetch: lists
  CSE Prelims 2026 GS I/II, Mains 2026 GS I–IV/Essay/optionals, CSE 2025);
  SSC `ssc.gov.in/candidate-corner/previousPaper` (200); IBPS `ibps.in`
  (200 on retry); NTA `nta.ac.in` (200); OPSC `opsc.gov.in` (200); OSSSC
  `osssc.gov.in` (200); CTET `ctet.nic.in` (200).
  `rrbapply.gov.in` returned 404 to curl and was unreachable from the
  server, so RRB has **no** official paper entries — its section links to the
  official portal with the answer-keys-only note (RRB honesty rule).
- **Unofficial:** Testbook (AMP pages: SSC CGL/CHSL, UPSC, RRB NTPC, NEET —
  curl 500 is bot-blocking; full page content fetched and verified, e.g.
  CGL Tier 1 2016–2025 shift-wise, UPSC Prelims 2013–2026 + Mains
  2014–2026, NEET 2015–2025), Prepp (SSC CGL/CHSL, CTET, OPSC — 200),
  Adda247 (SSC CHSL, JEE Main — 200), CareerPower (SSC CHSL, OPSC OCS —
  200), FreeJobAlert (UPSC, 2014–2024 — 200), Oliveboard (IBPS PO blog +
  4 direct memory-based PDFs 2020/2021/2023/2025 — 200), AglaSem (NEET
  2016–2026 ~65 papers, JEE Main 2015–2026 ~430 papers — page-fetch
  verified), JagranJosh (CTET, OPSC OCS — 200), FreshersNow + Result91
  (OSSSC LI/Forester/Forest Guard paper, 24 Apr 2024 Shift 3 — 200),
  mpcareer.in (SSC CHSL Tier-I 2022, 09 Mar 2023 Shift 1 — 200),
  6 direct Testbook CDN PDFs (RRB NTPC Graduate CBT-I Jun 2025 shifts —
  200). Shiksha and AglaSem CTET pages returned 403 to curl and were
  **dropped**, not used. The Adda247 SSC CGL URL found in search was
  truncated and was **not** used.
- **Years added on verified evidence:** IBPS PO 2025 (Oliveboard 2025
  Prelims PDF exists), OSSSC 2024 (Apr 2024 Forest Guard paper exists).
  Other exams keep the same two-section structure ready; empty years show
  "Not available yet".

## Deliberate differences from the poster (and why)

- Stats bar uses the poster's numbers, not the real counts (user's order).
- Upcoming Exams uses the real calendar, not the poster's 2025 dates (SSC
  CGL Mar 2025 etc. are in the past).
- Current Affairs uses the real verified Nov 2026 items, not the poster's
  sample items (ISRO satellite, education policy draft, Asia Cup 2024).
- Category icons are emoji approximations, not the poster's exact emblems.
- RRB has no official paper entries (RRB publishes no complete official
  papers — answer keys/response sheets only).
