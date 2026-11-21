# ExamPath India — Website Audit (Step 1: Website First)

Date: 21 Nov 2026. Auditor: website-first pass (Step 1 of user order: Website → Content → App → Admin LAST).
Live site: https://exampath-india.pages.dev/ (Cloudflare Pages project `exampath-india`).
Source: `~/workspace/exampath-india/` (generator `build_site.py` → `final-deploy/`).

## What was already good (v1, verified live)
- Home matches the poster layout: hero with 3 Indian students holding SSC / UPSC / JEE-NEET books
  (`/assets/img/hero-students.jpg`, verified visually — matches poster), search bar, 6 quick chips,
  9-category strip (SSC, Railway, UPSC, Banking, State Exams, Teaching, JEE, NEET, More),
  Explore by State (Odisha first, highlighted), PYQ banner, Popular Exams (6 tiles),
  Today's Current Affairs (3 items), Upcoming Exams with day pills, Daily Quiz card.
- Stats are HONEST real counts, not the poster's unverified numbers: 56 exams listed,
  80 practice questions, 8 study notes, 36 states & UTs, 22 languages. No fake
  "10 Lakh+ students / 10 Lakh+ questions" claims anywhere on the site.
- All pages return 200 live: home, exams, papers, mock, quiz, CA, notes, formulas, planner,
  saved, profile, portals, languages, search, 56 exam pages, 36 state pages, practice, mock-test.
- All images + sample PDF return 200 live (hero, books, mock, notes, planner, sample-practice-paper.pdf).
- No login anywhere; all personal data (saved papers, bookmarks, wrong answers, test history,
  planner, streak) in localStorage only. Default language English (EN/HI/OD switcher in header,
  English default).
- Question engine verified by code read: mock tests have timer, question palette, negative
  marking (+1/−0.25 SSC & Banking, −0.33 RRB), autosave + resume, auto-submit on timeout,
  results with correct/wrong/unattempted + answer review; wrong answers feed a revision mode;
  daily quiz is date-seeded (10 Q/day); practice has check-answer + explanations + bookmarks.
- PDF viewer: sample is an ExamPath ORIGINAL practice paper, clearly labelled "NOT an official PYQ".
- Languages page lists all 22 scheduled languages with script + UI status + paper availability,
  Urdu RTL note, and the rule that machine-translated official questions are never published.
- "Request this paper" action exists on exam pages and saves the request in localStorage
  (shown on the Saved page).

## Gaps found and FIXED in this pass (21 Nov 2026)
1. **12 broken links in `site.js`** — `href='/practice?subject=all">` (mismatched quotes) in the
   JS-generated HTML corrupted the DOM on: exam-page Practice link (after any year/stage switch),
   mock result screen (Retry / All Mocks / See Wrong Answers), practice empty state,
   quiz-complete screen, wrong-answers practice link, profile weak-topic links, profile
   "Take a Mock" link. All fixed to `href="..."`. (Static HTML from `build_site.py` was fine.)
2. **Live countdown missing** — `site.js` had countdown code for `#cd-d/#cd-h/#cd-m/#cd-s` but
   home had no such elements (dead code). Added a countdown strip on home for the next exam:
   SSC CHSL Tier-1, starts 30 Nov 2026 (verified — see portal table).
3. **"View All States (28)" was wrong** — site covers 28 states + 8 UTs = 36. Fixed to
   "View All States & UTs (36)".
4. **RRB overstated** — RRB exams were shown as "✓ Official archive" with "papers available
   shift-wise in the official archive". In reality RRB does NOT publish complete official
   question papers; it releases answer keys & response sheets per CEN on regional portals.
   Fixed: RRB portal note rewritten, RRB exam pages + paper rows now say
   "◐ Answer key on portal" / "Official Portal ↗" with an explicit explanation, and the
   Papers page heading changed to "Exams with an official source".
5. **RRB years were stale** — added verified years: RRB NTPC Graduate 2026 (CBT-1 held Mar 2026,
   CEN 06/2025), RRB NTPC Undergraduate 2026 (CBT-1 May–Jun 2026, CEN 07/2025),
   RRB ALP 2025 (CEN 09/2025). Year = years with at least one verified resource (answer key /
   response sheet on the official portal). No direct PDF URLs invented.
6. **9th official portal added** — RRB Regional Portals (rrb.indianrailways.gov.in), home of all
   21 regional RRBs (CEN notices, answer keys, results, mock-test links).
7. **No PWA manifest** — `manifest.json` added and linked in every page head. (Offline
   service-worker caching is still NOT implemented — `service-worker.js` only removes the old
   app's worker. Installability/offline is a known gap, see below.)

## Official portal verification (21 Nov 2026, verify-first rule)
| Portal | URL | Result | Note |
|---|---|---|---|
| UPSC | https://upsc.gov.in/examinations/previous-question-papers | VERIFIED (live page fetch) | curl returned 404 (site blocks non-browser clients) but the live page was fetched and lists CSE Mains/Prelims 2026, NDA, CDS, CAPF, CMS, ESE papers with file sizes. URL kept. |
| SSC | https://ssc.gov.in/candidate-corner/previousPaper | 200 | OK |
| RRB (apply) | https://www.rrbapply.gov.in/ | UNREACHABLE from this server | curl 000 (DNS/timeout) + browser fetch failed (network error). Link retained as the blueprint's official application URL; labelled with the RRB limitation note. Re-check in a browser. |
| RRB (regional) | https://rrb.indianrailways.gov.in/ | UNREACHABLE from this server (curl 000) | Confirmed as the official RRB portal home by two independent search sources (21 Nov 2026). Added as 9th portal. Re-check in a browser. |
| IBPS | https://www.ibps.in/ | 200 | OK |
| NTA | https://nta.ac.in/ | 200 | OK |
| OPSC | https://opsc.gov.in/ | 200 | OK |
| OSSSC | https://www.osssc.gov.in/ | 200 (retry) | First probe returned 000 (transient); retry returned 200. OK |
| CTET | https://ctet.nic.in/ | 200 | OK |

Also verified by search (21 Nov 2026): SSC CHSL 2026 Tier-1, 30 Nov–31 Dec 2026
(SSC notice dated 1 Oct 2026; 2,536 vacancies) — countdown + calendar entry are correct and
labelled Tentative. RRB NTPC Graduate CBT-1 Mar 2026 / UG CBT-1 May–Jun 2026 / ALP CEN 09/2025
confirmed via two sources.

## Still honestly missing / NOT claimed
- No Firebase backend yet: no server sync, no admin, no user accounts. Data is local only.
- No real user/student counts, no real download counts — stats show only real on-site counts.
- No direct official PDF files hosted: papers are linked to official archives only; anything
  unverified shows "Not available yet" + Request.
- PWA: manifest added, but no offline caching service worker yet (app-shell caching pending).
- Exam calendar: RRB NTPC Graduate CBT-1 "22 Dec 2026–15 Jan 2027" and IBPS PO / UPSC CSE 2027
  dates are Tentative (exam-tracker dates, labelled as such) — verify on official sites.
- Admin app: NOT started — per user order it comes LAST, after the App/APK step.
- APK: NOT rebuilt in this pass — per user order, App comes after the website step.

## Smoke test (this pass)
- `node --check` site.js + data.js: PASS. `build_site.py` parses + regenerates 112 files: PASS.
- Generated HTML checks: countdown `#cd-d` present (1), states label "(36)" present,
  manifest linked, RRB honesty text on RRB exam page, 2026 year on RRB NTPC pages,
  0 remaining broken `href='` links in site.js: PASS.
- Live curl (before this redeploy): 17/17 pages 200.
- AFTER redeploy (21 Nov 2026, deploy exit 0, 115 files uploaded): 7/7 spot-check pages 200
  (home, SSC CGL, RRB NTPC, Odisha, papers, portals, manifest.json). Live home contains
  countdown `#cd-d`, "View All States & UTs (36)" and manifest link; live RRB NTPC page
  contains the RRB honesty text (2×) and "Answer key on portal" (2×). PASS.
