# ExamPath India — User App (Phase 1) — Step-by-step Plan

User order (2026-11-21): PDF blueprint pehle padho → step-by-step banao → **Admin app USER app ke saath mat banao (alag hoga)** → **pehle USER app website, BINA LOGIN** → online available sab kuch jaha chahiye waha add karo (photo etc.) → achhe se banao, koi mistake na karo.

## Phase 1 — USER APP (yeh build)
1. Design system — PDF §1 palette (navy #102A43, blue #246BCE, cyan #16B8C4, purple #7257D5, orange #F59E0B, green #159A72), mobile-first, 44px targets, light/dark.
2. Home — hero photo, search, countdown (SSC CHSL Tier-1, 30 Nov 2026), categories, states, trending, current affairs.
3. Exam directory — 9 categories, 60+ exams, 28 states + 8 UTs (region filter). Data-driven, admin-ready structure (abhi local data, baad me admin se manage hoga).
4. Year-wise PYQ flow (§3) — Category → State → Exam → Year → Stage → Shift/Set → Resource. Sirf wahi year dikhe jisme resource hai; baaki par "Not available yet" + Request.
5. Official sources (§4) — sirf verified portals: UPSC, SSC, RRB, IBPS, NTA, OPSC, OSSSC, CTET. Koi fake paper/PDF nahi. Jo paper official archive me hai uska link; jo nahi hai wo "Not available yet".
6. PDF viewer (§5) — in-app viewer (iframe + zoom/download/save/share/report). Sample ke liye ek REAL generated practice PDF (ExamPath Original Practice Paper — official PYQ nahi, clearly labelled).
7. Question bank + Mock tests (§6) — 80 original practice questions (Quant/Reasoning/English/GK/Science/CA) + 3 full mocks (SSC/RRB/Banking style) — timer, palette, negative marking, autosave, results, wrong-answer revision. Sab localStorage (bina login).
8. Study toolkit (§7) — Syllabus, Notes, Formula Bank, Current Affairs (Nov 2026 verified), Daily Quiz, Planner, Countdown, Dashboard (progress/accuracy/streak — local).
9. Languages (§8) — 22 scheduled languages list + availability labels; UI switch EN / HI / OD (Roman + Devanagari/Odia key strings); Urdu RTL note.
10. Saved / Profile — My Library, bookmarks, wrong answers, test history — sab device par (localStorage), koi login nahi, koi server nahi.
11. PWA + Android-ready — manifest, service worker (app shell cache), installable, WebView-friendly.
12. Policies — Privacy, Terms, Disclaimer, Sources page. Koi paid wall nahi.

## Phase 2 — ADMIN APP (ALAG, baad me — is build me NAHI)
Separate project: secure dashboard, exam/state management, PDF upload + year/shift metadata, question bank, bulk import, mock config, moderation, roles, audit logs. Backend/Firebase rules ke saath.

## Honesty rules (PDF §14)
- Accuracy before quantity. Fake paper/shift/key kabhi nahi.
- Year first-class filter hai.
- Save ≠ Download.
- Language availability hamesha dikhao.
- Free core learning, no paywall.

## Deploy
- Source: ~/workspace/exampath-india/ ; Deploy: Cloudflare Pages project `exampath-india` → https://exampath-india.pages.dev/
- Deploy script: ~/workspace/exampath-india/deploy_pages.py (DailyTools pattern)
