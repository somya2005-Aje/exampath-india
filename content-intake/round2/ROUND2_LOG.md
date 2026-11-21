# ExamPath India — Content Intake Round 2 Log

Date: 2026-11-21. Intake folder: `~/workspace/exampath-india/content-intake/round2/`
Purpose: fill the thin spots flagged in the round-1 log (56/56 exams, 167 Official + 439 Unofficial papers, 215 YouTube videos) and deepen coverage. Method: 4 parallel group workers; every link fetched/opened on 2026-11-21 before inclusion. No invented URLs. Nothing found = recorded in `not_found_years`, never fabricated. Nothing in `final-deploy/`, `data.js`, `build_site.py`, admin, or APK work was touched — intake only, links + metadata only.

## Validated totals (counted from the files themselves, not worker reports)

- Files: **13** (one per exam worked on)
- New official papers: **3**
- New unofficial papers: **75**
- New YouTube videos: **38**
- Worker reports matched the file counts exactly (A: 0/13/6, B: 0/19/14, C: 2/39/12, D: 1/4/6).

Validation run by coordinator: all 13 files parse as JSON, required keys present (`exam_id`, `exam_name`, `official_papers`, `unofficial_papers`, `youtube`, `not_found_years`, `notes`), every paper URL starts with http, every paper entry carries `checked` + `http`, every YouTube URL is a real `youtube.com/watch?v=` link.

## Per-exam counts (new official / unofficial / videos / not-found)

| Exam | Official | Unofficial | Videos | Not found |
|---|---|---|---|---|
| WBCS | 0 | 6 | 3 | 2024, 2023, 2022 (official only — unofficial now found for all three) |
| OSSSC RI/ARI/PEO | 0 | 7 | 3 | 2022 |
| NIFT | 0 | 11 | 9 | — |
| CLAT | 0 | 8 | 5 | — |
| SSC JE | 1 | 10 | 3 | — |
| CUET UG | 1 | 8 | 6 | — |
| Coast Guard | 0 | 3 | 3 | 2022 |
| BITSAT | 0 | 6 | 0 | — |
| AFCAT | 0 | 6 | 0 | — |
| Agniveer | 0 | 6 | 0 | — |
| SSC GD Constable | 0 | 3 | 1 | — (2019 now FOUND) |
| KVS | 0 | 1 | 2 | 2019 |
| RBI Assistant | 1 | 0 | 3 | 2024 |

## What was found (highlights)

- **WBCS:** 0 official — wbpsc.gov.in still unreachable (curl 000, both www/non-www) and psc.wb.gov.in also unreachable, so nothing recorded as official. 6 unofficial, all HTTP 200: Prelims 2024 (UnlockIAS direct PDF, Prepp full 200-Q paper, PYQSathi), Mains 2023 (compulsory + optional, PYQSathi), Prelims 2023 + 2022 (AptiPlus collection 2015–2024). 3 videos (2024 paper analysis / answer keys).
- **OSSSC — first REAL RI/ARI/PEO papers:** PEO & JA 2023 official paper (09 Jul 2023, CRE-2023, Adda247, 7.9 MB) + solved SET-B/SET-D PDFs; RI/ARI CRE 2023-IV Prelims 08 Oct 2025 Shift 3 (Testbook CDN, 15.8 MB) and 19 Oct 2025 Shift 3 (Result91); Mains 26 Apr 2026 Shift 1 (Result91); Adda247 RI/ARI collection incl. Revenue Inspector 2021 Paper 1 & 2. Note: the "2023 cycle" RI/ARI prelims were held Oct–Nov 2025, so they are recorded under 2025/2026 by exam-held date. Round 1's two LI/Forester/Forest Guard PDFs were NOT re-listed (wrong posts). osssc.gov.in itself is flaky (curl 200 once, then 000; browser fetch failed) — no papers retrieved from it.
- **NIFT:** 0 official — NIFT/NTA publishes no exam papers for any year; `nift.ac.in/samplequestion` is 404 and the homepage shows no sample-paper link. 11 unofficial incl. two direct PDFs from ACS (B.Des 2025 CAT & GAT, PG 2024 GAT, both HTTP 200 with real paper content), Shiksha hub (2025 + 2024 B.Des + Situation Test 2011–2019), Careers360 B.FTech 2025 memory-based + Situation Test PYQs, GetMyUni, PW.live. **9 videos — from 0 in round 1** (Situation Test PYQ, crack strategy, 2026 guide, exam-day guidelines, etc., all oEmbed-verified).
- **CLAT:** 0 new official (paid ₹500 route already in round 1; no free official PDF exists). 8 unofficial: Prepp hub (2025/2024/2023, Sets A–D + keys), Careers360 Law hub, FindMyCollege direct PDF of CLAT 2025 UG Set A with provisional key (~616 KB, HTTP 200). 5 videos (2025 live solving, 5-year PYQ reasoning topics, legal-reasoning analysis, mock solutions, 2026 guide).
- **AglaSem verdicts — BOTH KEPT:** NIFT hub (`admission.aglasem.com/nift-admission-question-papers/`) and CLAT hub (`admission.aglasem.com/clat-previous-year-question-papers-answers/`) both open live with real content (browser-crawled 2026-11-21 16:09 UTC); curl 403 is bot-block only. Both were already in round 1, so not duplicated in round 2.
- **SSC JE:** 1 official (2025, ssc.gov.in portal) + 10 unofficial (Adda247 2025 memory-based + 2016–2024, Guidely, CareerPower, ExamSaga, JagranJosh, Testbook/Prepp 2025) + 3 videos (oEmbed-verified).
- **CUET UG:** 1 official (2025, NTA portal) + 8 unofficial (Adda247 2025/2024, CareerPower 2024/2023, Zollege direct PDFs, Careers360 History 2025) + 6 videos. 2025 now covered.
- **Coast Guard:** 0 official (none exist) + 3 unofficial, all 2021, all labelled "Memory-based (unofficial)" + 3 videos (sample-paper Maths, Science PYQs, Physics PYQs).
- **BITSAT / AFCAT / Agniveer:** 0 official (bodies publish none). 6 memory-based unofficial each, all labelled: BITSAT (Prepp 2025/2024/2023, Adda247 2024/2023, Careers360 2026 memory-based); AFCAT (Prepp 2026/2025/2024/2023/2022/2021 — adds new years 2026 and 2021); Agniveer (Testbook GD 2026/2025/2024/2023 + Tradesman 2026/2024). No new videos (round 1 already has 4 each).
- **SSC GD 2019 — FOUND:** 3 unofficial (Testbook `next.testbook.com` full shift-wise 2019 table ~40 shifts, JagranJosh 6 Mar & 12 Feb 2019 with solutions, EduRev 06 Mar 2019 Shift 2), all HTTP 200 + 1 video. `not_found_years` now empty.
- **KVS 2019 — genuine absence:** no teaching cycle that year (JagranJosh/Testbook/LeverageEdu list only 2018/2017/2016; ctet.co.in "2019-20" page is model papers). 1 new unofficial is the 2018-cycle paper (exam held Feb 2019), recorded as year 2018, explicitly NOT 2019. 2 videos.
- **RBI Assistant 2024 — genuine absence:** no recruitment cycle in 2024. Official rbi.org.in page (Id=4946, fetched) shows the cycle after 2023 is Panel Year 2025 (650 posts, applications 16 Feb–8 Mar 2026, Prelims 11 & 13 Apr 2026, Mains 7 Jun 2026), corroborated by PracticeMock and the RBI notification PDF; sites claiming a 2024 cycle contradict each other and copy 2023 dates verbatim. 1 new official entry = the Panel Year 2025 cycle page + 3 videos. Caveat: round 1's official opportunities-portal URL now returns RBI's "file not available or misspelled" error — the Id=4946 page is the verified official replacement (noted in rbi-asst.json).

## Duplicates vs round 1 — skip at integration (5 entries, same exam + URL)

These are hub/listing URLs already in round 1, not distinct new papers; the integration step dedupes by exam+year+URL and should skip them:
- `cuet-ug` — https://cuet.nta.nic.in/
- `nift` — https://design.careers360.com/articles/nift-previous-year-question-papers-with-solutions-pdf-check-here
- `ssc-je` — https://ssc.gov.in/candidate-corner/previousPaper
- `ssc-je` — https://testbook.com/ssc-je/previous-year-papers
- `ssc-je` — https://prepp.in/ssc-je-exam/practice_papers

## Still not found

- **WBCS official papers 2024/2023/2022** — official host unreachable from this server; unofficial papers now exist for all three years. Needs a browser re-check of wbpsc.gov.in.
- **OSSSC RI/ARI/PEO calendar year 2022** — no paper found anywhere.
- **Coast Guard 2022** — no 2022 paper found on any new source.
- **KVS 2019 and RBI Assistant 2024** — confirmed genuine absences (no exam/cycle those years), not search failures.
- **NIFT official papers** — NIFT publishes none for any year (all papers unofficial/memory-based).
- **CLAT free official PDFs** — none exist; official route is paid ₹500 via candidate login.
- **BITSAT / AFCAT / Agniveer / Coast Guard official papers** — bodies publish none; memory-based only.
- **NIFT videos before round 2: 0 → now 9.** SSC JE / CUET / Coast Guard videos: 2 each → 5 / 8 / 5 total with round 1.

## Excluded per verify-first rule

- CUET video `n4Qn3sXU2TI` (oEmbed Forbidden, channel unconfirmable); guessed Adda247 CUET URL (404); PW.live Coast Guard page (auth/token params, no clean link); CUET PG videos (out of scope); IndCareer NIFT page (download links point only to generic NTA domain, no specific file); UnlockIAS 2023/2022 PDFs at the same URL pattern (404); Shiksha/AglaSem 403s where the page could not be opened live; Testbook `/amp/` URLs (500 via curl, non-AMP used where 200).
- Prepp BITSAT/AFCAT pages: curl 403 (bot-block) but read in full via browser fetch — recorded as http 200 with that note in each entry.
- One KVS video channel recorded as "Unknown" (channel name not exposed by the YouTube page crawl) rather than guessed.
