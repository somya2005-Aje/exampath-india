# ExamPath India — Content Intake Round 3 Log

Date: 2026-11-21. Intake folder: `~/workspace/exampath-india/content-intake/round3/`
Purpose: the user ordered — don't stop at 3–4 papers per year; find out for every exam+year how many papers actually happened, add ALL of them, mark what doesn't exist as "Not available". Method: 6 parallel group workers (SSC / Railway / UPSC+Defence / Banking+Teaching / Entrance / State PSC); every link fetched/opened on 2026-11-21 before inclusion. No invented URLs. Nothing found = recorded in `not_found_years`, never fabricated. Merged into `final-deploy/data.js` by `/tmp/merge_round3.py`.

## Validated totals (counted from live data.js, not worker reports)
- Files: **56** (one per exam) — all parse as JSON, required keys present, every paper URL http, every paper entry carries `checked` + `http`.
- Intake found: **316 papers (27 official / 289 unofficial)**. Merged: **309 papers (26 official / 283 unofficial)**. **7 skipped as exact duplicates** already in data.js (exam+year+URL) — mostly JEE Main hub URLs already present from round 1.
- Live totals after merge: **1,029 papers — 207 official + 822 unofficial** (was 720 / 181 / 539); **253 videos** (unchanged — no new videos in round 3); **56 exams**.
- Validation on merged data.js: **0 orphan years, 0 orphan stages, 0 duplicate exam+year+URL.**
- 19 stage values normalised to "" (unknown stage strings like "Prelims/Mains" / "Paper I & II" — those papers now show under all stages, never orphaned).

## Per-exam merged counts (official / unofficial / years added)
| Exam | Off | Unoff | Years added |
|---|---|---|---|
| ssc-cgl | 2 | 7 | 2026, 2025, 2024, 2023 |
| ssc-chsl | 2 | 4 | 2026, 2025 |
| ssc-gd | 1 | 9 | 2025 |
| ssc-mts | 1 | 5 | 2026, 2024 |
| ssc-cpo | 1 | 5 | 2025 |
| ssc-steno | 1 | 5 | 2025 |
| ssc-je | 0 | 4 | 2020, 2018 |
| ssc-sp | 1 | 5 | 2025 |
| rrb-ntpc-g | 0 | 8 | 2026, 2025 |
| rrb-ntpc-ug | 0 | 6 | 2026, 2025 |
| rrb-groupd | 0 | 7 | 2026, 2025 |
| rrb-alp | 0 | 5 | 2026, 2025 |
| rrb-je | 0 | 5 | 2026, 2025 |
| rrb-tech | 0 | 3 | 2026, 2024 |
| rrb-rpf-c | 0 | 6 | 2025 |
| rrb-rpf-si | 0 | 4 | 2024 |
| upsc-cse | 1 | 6 | 2026 |
| upsc-nda | 1 | 7 | 2026 |
| upsc-cds | 1 | 5 | 2026 |
| upsc-capf | 1 | 4 | 2026 |
| upsc-ese | 1 | 6 | 2026 |
| upsc-cms | 1 | 3 | 2026 |
| ibps-po | 0 | 8 | 2025 |
| ibps-clerk | 0 | 2 | 2025 |
| ibps-rrb | 0 | 2 | 2025 |
| sbi-po | 0 | 2 | 2025 |
| sbi-clerk | 0 | 4 | 2025 |
| rbi-b | 0 | 3 | 2025 |
| rbi-asst | 0 | 2 | 2023 |
| afcat | 0 | 9 | 2026, 2021 |
| agniveer | 0 | 9 | 2025, 2024, 2023, 2022 |
| coast-guard | 0 | 3 | 2025, 2022 |
| ctet | 0 | 2 | 2024 |
| ugc-net | 0 | 4 | 2025 |
| csir-net | 0 | 5 | 2025 |
| kvs | 0 | 2 | 2026 |
| dsssb | 0 | 7 | 2025 |
| neet-ug | 1 | 6 | 2026, 2025 |
| jee-main | 1 | 6 | 2026, 2025 |
| jee-adv | 2 | 5 | 2026, 2025 |
| bitsat | 0 | 8 | 2026, 2025 |
| cuet-ug | 1 | 5 | 2026, 2025 |
| gate | 1 | 10 | 2026, 2025 |
| cat | 1 | 4 | 2025 |
| clat | 1 | 4 | 2026 |
| nift | 1 | 4 | 2026 |
| cbse-10 | 1 | 1 | 2026 |
| cbse-12 | 1 | 1 | 2026 |
| opsc-ocs | 0 | 8 | 2025, 2024 |
| osssc | 0 | 3 | 2022 |
| bpsc | 0 | 10 | 2025 |
| uppsc | 0 | 5 | 2025 |
| mpsc | 0 | 5 | 2025 |
| tnpsc | 0 | 6 | 2025 |
| rpsc-ras | 0 | 5 | 2025 |
| wbcs | 0 | 4 | 2025, 2021 |

## What was found (highlights)
- **2025 + 2026 cycles now covered for nearly every exam** that held one: SSC CGL/CHSL/GD/CPO/Steno/SP 2025, RRB NTPC/Group D/ALP/JE 2025–2026, IBPS/SBI/RBI 2025, UPSC all six 2026, NEET/JEE/CUET/GATE 2026, BPSC 71st CCE, UPPSC/MPSC/TNPSC/RPSC 2025, DSSSB 2025.
- **2026 was held, not "upcoming":** the briefs wrongly told workers that NEET 2026 / JEE Adv 2026 / CUET 2026 / UPSC 2026 were "not held yet". It is 21 Nov 2026 — all were held May–Sep 2026 and are published. Workers verified live and added them; kept.
- **NEET UG 2026:** held 3 May 2026, **cancelled 12 May 2026 after a paper leak**, re-exam 21 June 2026 (codes 50/60/70/80), result 16 July 2026. Both sittings covered.
- **Previously not-found years now FOUND:** OSSSC 2022 (CRE 2021 paper held 30 Jan 2022), Coast Guard 2022 (Navik GD memory-based + Asst Commandant), SSC GD 2019 was round 2.
- **Genuine absences (still "Not available yet", verified):** KVS 2019 (no teaching cycle), CTET 2025 (CBSE conducted NO CTET in 2025 — first year without one since 2011; the Dec 2025 session was held 8 Feb 2026), RBI Assistant 2024 (no recruitment cycle), RRB Technician 2025 (no exam held; Dec 2024 → Mar 2026 gap), SSC CPO Paper-II 2025 (scheduled 28 Nov 2026, not yet held), SSC Steno Skill Test (live dictation, no PDF exists for any year), RBI Assistant 2025-cycle Prelims (11 & 13 Apr 2026, not yet held at check time — not added).
- **Held-date rule:** papers are recorded under the year the exam was HELD (e.g. SSC CGL Tier-II of the 2025 cycle, held Jan 2026, is under 2026; RPF Constable 2024-cycle CBT held Mar 2025 is under 2025; KVS 2025-cycle Tier-1 held Jan 2026 is under 2026). Titles state the cycle so the year is never misleading. Round 1 used CEN/notification year in a few places — the same hub may therefore appear under two adjacent years across rounds; that follows the existing one-entry-per-year-per-hub convention and is not double-counting distinct papers.
- **Bodies that publish NO official papers** (memory-based/unofficial only, all labelled): RRB, IBPS, SBI, RBI (papers), BITSAT, AFCAT, Agniveer, Coast Guard, NIFT, CLAT (free route; official is paid ₹500 via login).

## UI change (this round)
- Every exam page and the /papers page now show a **per-year paper count on each year pill**: e.g. "2025 — 6 papers", "2026 — 1 paper", "2019 — 0 papers". Implemented in `build_site.py` (`_paper_count` / `_paper_count_label`, exam page + papers page) and `final-deploy/site.js` (dynamic pill rebuild on /papers). Count = all verified papers for that exam+year across all stages. Years with 0 papers still show the pill and open "Not available yet" + Request.

## Caveats
- Browser-verified, curl-blocked URLs are recorded as http 200 with a note ("browser-verified, curl 403 bot-block" etc.) — same convention as rounds 1–2. Counts: SSC 5, Banking/Teaching several (Testbook AMP curl 500, AglaSem/YourMockTest curl 403), UPSC+Defence 5, Entrance 11 (mostly Shiksha/AglaSem), State PSC 3.
- UPSC official entries point at the archive hub (as in round 1): upsc.gov.in is a JS-rendered app; per-paper PDF hrefs are not extractable via curl, so no individual official PDF URLs could be verified. Archive content itself was verified via browser fetch.
- WBCS 2025: hub listings only — no direct PDF of the 7 Sep 2025 Prelims paper was found anywhere; wbpsc.gov.in / psc.wb.gov.in still unreachable.
- One PW MPSC URL carrying a user auth token was found in search and deliberately NOT used.
- Firebase config (`window.FIREBASE_CONFIG`, projectId `exampath-india`) was already wired into `build_site.py` FOOTER by the parent before this round's regeneration; verified present in regenerated HTML before redeploy.
