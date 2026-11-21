# ExamPath India — Content Integration Note (21 Nov 2026)

Live: https://exampath-india.pages.dev/ — redeployed 21 Nov 2026 (117 files).
Source of intake: `content-intake/` (56 JSON files + VERIFICATION_LOG.md). Merge script: `/tmp/merge_intake.py`
(re-runnable; data source of truth is `final-deploy/data.js`, generator `build_site.py`).

## Final counts (verified from LIVE data.js)
- Papers: **648** — Official **178**, Unofficial **470**
- YouTube videos: **215** (55 of 56 exams; NIFT has 0 videos)
- Exams covered: **56 / 56**
- Intake totals were 167 official / 439 unofficial / 215 videos; the merge added 496 new
  entries and skipped 110 duplicates (same exam + year + URL). Existing entries added
  11 extra official + 31 extra unofficial beyond the intake (e.g. OSSSC official-site entry).
- Details refreshed conservatively (only where intake clearly extends existing text):
  eligibility 19 exams, pattern 8, syllabus 14.

## Paper flow (user's new design, live on exam pages + Papers page)
- Exam page: **"📄 Exam Papers — Choose Year"** button → year pills → stage pills →
  Official + Unofficial sections. Same flow on `/papers` (exam dropdown + same button).
- Papers are **photo-style cards** (CSS paper-page tiles: masthead, big year, exam name,
  stage, "Question Paper", ruled lines). No paper photos are downloaded/hosted.
  Clicking a card opens the actual verified paper (source PDF/page) in a new tab.
- Each section has: card gallery → **numbered list 1..N** (each number linked to its paper)
  → **Source Website box** at the bottom (source homepage links only). The source-website
  link is never the card's main action. A combined "Source Websites — {year}" box sits
  below both sections. Nothing verified = "Not available yet" + Request button.
- Counts are per-year from the intake — e.g. **SSC CGL 2024 shows 4 paper cards**
  (1 official + 3 unofficial). No shift/paper was invented.

## Login gate (new, `auth.js`)
- **Free without login:** home, search, exam overview, paper photo-cards (view), YouTube.
- **Login-gated:** ⬇️ Download buttons (every paper card + sample PDF + viewer),
  full exam pattern, full syllabus, complete numbered paper list (locked teaser + login button).
  Clicking a gated item opens the login box ("Sign in with Google").
- **No fake login:** `auth.js` waits for `window.FIREBASE_CONFIG`. No config is set yet
  (Firebase setup runs separately), so the button reads "Google sign-in setup ho raha hai —
  thodi der me check karein" and clicking it says so honestly; no session is ever created.
  When the config arrives, real Google Sign-In (Firebase `signInWithPopup`) runs and only
  then is a session flag written to localStorage. After login the header shows the user's
  name/photo + Logout. No demo login, no local password login.
- `auth.js` source: `~/workspace/exampath-india/auth.js` (copy in `final-deploy/auth.js`).

## Exclusions / special labels
- **NIFT AglaSem + CLAT AglaSem** (http null / http 0 in the sweep): re-checked live via
  browser fetch on 21 Nov 2026 — BOTH open with real content (NIFT page updated 18 Nov 2026;
  CLAT page updated 1 Nov 2026; curl returns 403 = site bot protection). INCLUDED, with a
  note "Page opens in a browser; curl returns 403 (site bot protection)".
- **3 dead IBPS PO PDF links removed** (Oliveboard `IBPS-PO-2023/2021/2020-Shift-1-Prelims-PYP.pdf`,
  404 per the sweep); the corrected slugs (without `-Shift-1`, verified 200) are in.
  The 2025 `-Shift-1` PDF is live (200) and kept.
- **OSSSC's 2 unofficial PDFs** are LI / Forester / Forest Guard papers — labelled with their
  real post names + note "not RI/ARI/PEO", never as RI/ARI/PEO papers.
- **BITSAT / NIFT / AFCAT / Agniveer / Coast Guard:** no official papers exist; unofficial
  entries are labelled "Memory-based (unofficial)" (NIFT 2024–2025 are actual NTA papers per
  the intake note; only the 2023 NIFT paper is memory-based — labelled as such).
- **CLAT official papers are PAID** (Rs 500 via candidate login) — labelled on every CLAT
  official entry; no free PDF is linked.
- **RRB: 0 official papers** (answer keys/response sheets only; portal link + note).
- **Not found (8 years):** SSC GD 2019, KVS 2019, OSSSC 2023/2022, RBI Assistant 2024,
  WBCS 2024/2023/2022 — shown as "Not available yet", never fabricated.
- **WBCS:** 0 official, 3 unofficial; wbpsc.gov.in unreachable from this server.

## YouTube
- `/videos` page (215 videos grouped by exam) + "🎬 Watch & Learn (YouTube)" section on
  every exam page with videos. All links are real `youtube.com/watch?v=` URLs from the
  intake; none invented. UGC NET video PJKfIeQ3lew: watch page fetched 200 (oEmbed Forbidden
  noted in intake).

## Still not found / not done
- No hosted official PDFs — papers open on their source sites (official archives + third-party
  pages). No Firebase backend/config yet (auth shows setup-in-progress honestly). No APK work
  (per order). No admin work (per order). The login box cannot be tested end-to-end until
  `window.FIREBASE_CONFIG` is provided.
- RRB / OSSSC / WBPSC official portals were unreachable from this server (curl 000);
  their links are kept with limitation notes and need a browser re-check.
