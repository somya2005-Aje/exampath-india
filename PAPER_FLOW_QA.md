# Paper-flow QA — ExamPath India

Date: 21 Nov 2026 (evening IST). Live site: https://exampath-india.pages.dev/

## Required flow (user order)
Exam select → "Exam Papers" button → year choose → BOTH sections (Official + Unofficial) → photo cards → numbered list 1..N below → source link ONLY at bottom of each section + side "Source Website" box. All papers that actually happened that year; never invent a shift/paper; missing year = "Not available yet" + Request.

## Fixes applied in this run

1. **Numbered list unlocked (was hidden behind login).** The complete numbered list is now visible WITHOUT login on every exam page and /papers (generator `build_site.py` `_paper_section` + `site.js` `paperSection`). Only Download buttons and full pattern/syllabus stay login-gated, per the user rule. Verified live: 0 `data-lock="paperlist"` on any spot-checked page.
2. **"Official Archive ↗" button removed from the Official fallback.** It sat mid-section and broke the "source link only at bottom/side" rule. The fallback is now "Not available yet" + Request Paper; the portal link still appears in the combined "Source Website" box at the bottom (generator `paper_rows_static` + `site.js` `paperRows` + viewer help text updated). Verified live: 0 "Official Archive" on any spot-checked page.
3. **Round-2 intake merged into data.js** (13 exams): +78 papers (3 official / 75 unofficial), +38 videos. Stage values normalised to real exam stages (or "" = all stages) so no paper is orphaned; year lists extended for newly covered years (AFCAT 2026/2021, Agniveer 2026, BITSAT 2026, Coast Guard 2021, CUET 2025, KVS 2018, NIFT 2022, OSSSC 2026/2025/2021, RBI Asst 2025, SSC JE 2025/2020/2018). Dedupe by exam+year+URL: 0 duplicates added.
4. **6 NEET UG Testbook AMP duplicates removed** — identical title+source as the non-AMP entry for the same exam+year. 0 AMP NEET entries remain.
5. **Data integrity re-checked:** 0 orphan years, 0 orphan stages, 0 duplicate exam+year+URL. Only years with no papers anywhere: KVS 2019 (genuine absence — no cycle that year) and OSSSC 2022 (not found) — both correctly show "Not available yet".
6. **APK link fixed as a side effect of this redeploy:** the App agent had placed a real APK (5,989,535 bytes) in `final-deploy/` at 16:27; this redeploy published it. Live `/exampath.apk` now returns 200 with `application/vnd.android.package-archive` (was 11 KB of HTML before). If the App agent re-syncs www later, it should re-sync from this deploy.

## Final live counts (from live data.js, identical to local)
- Papers: **720** — 181 official + 539 unofficial (was 648 / 178 / 470)
- YouTube videos: **253** (was 215)
- Exams: 56 | Questions: 80 | Notes: 8 | States/UTs: 36
- Live: home 200, /papers 200, data.js 200 (323,055 B), /exampath.apk 200 (5,989,535 B)

## Per-exam QA table

| Exam ID | Exam | Result | Papers (off/unoff) | Videos | Checked how | Notes |
|---|---|---|---|---|---|---|
| ssc-cgl | SSC CGL | PASS | 32 (8 off / 24 unoff) | 5 | live fetch | All listed years have papers |
| ssc-chsl | SSC CHSL | PASS | 25 (6 off / 19 unoff) | 4 | live fetch | All listed years have papers |
| ssc-gd | SSC GD Constable | PASS | 19 (5 off / 14 unoff) | 5 | local gen + data check | All listed years have papers |
| ssc-mts | SSC MTS | PASS | 15 (5 off / 10 unoff) | 4 | local gen + data check | All listed years have papers |
| ssc-cpo | SSC CPO (SI) | PASS | 15 (5 off / 10 unoff) | 5 | local gen + data check | All listed years have papers |
| ssc-steno | SSC Stenographer | PASS | 14 (5 off / 9 unoff) | 5 | local gen + data check | All listed years have papers |
| ssc-je | SSC JE | PASS | 26 (6 off / 20 unoff) | 5 | local gen + data check | All listed years have papers |
| ssc-sp | SSC Selection Post | PASS | 11 (4 off / 7 unoff) | 5 | local gen + data check | All listed years have papers |
| rrb-ntpc-g | RRB NTPC Graduate | PASS | 16 (0 off / 16 unoff) | 5 | live fetch | All listed years have papers |
| rrb-ntpc-ug | RRB NTPC Undergraduate | PASS | 8 (0 off / 8 unoff) | 4 | local gen + data check | All listed years have papers |
| rrb-groupd | RRB Group D (Level 1) | PASS | 5 (0 off / 5 unoff) | 5 | local gen + data check | All listed years have papers |
| rrb-alp | RRB ALP | PASS | 8 (0 off / 8 unoff) | 5 | local gen + data check | All listed years have papers |
| rrb-je | RRB JE | PASS | 9 (0 off / 9 unoff) | 4 | local gen + data check | All listed years have papers |
| rrb-tech | RRB Technician | PASS | 5 (0 off / 5 unoff) | 4 | local gen + data check | All listed years have papers |
| rrb-rpf-c | RPF Constable | PASS | 5 (0 off / 5 unoff) | 4 | local gen + data check | All listed years have papers |
| rrb-rpf-si | RPF Sub-Inspector | PASS | 4 (0 off / 4 unoff) | 3 | local gen + data check | All listed years have papers |
| upsc-cse | UPSC Civil Services (IAS/IPS) | PASS | 24 (8 off / 16 unoff) | 3 | live fetch | All listed years have papers |
| upsc-nda | UPSC NDA | PASS | 15 (5 off / 10 unoff) | 3 | local gen + data check | All listed years have papers |
| upsc-cds | UPSC CDS | PASS | 12 (4 off / 8 unoff) | 4 | local gen + data check | All listed years have papers |
| upsc-capf | UPSC CAPF AC | PASS | 12 (4 off / 8 unoff) | 3 | local gen + data check | All listed years have papers |
| upsc-ese | UPSC ESE (IES) | PASS | 12 (4 off / 8 unoff) | 4 | local gen + data check | All listed years have papers |
| upsc-cms | UPSC CMS | PASS | 12 (4 off / 8 unoff) | 4 | local gen + data check | All listed years have papers |
| ibps-po | IBPS PO | PASS | 19 (7 off / 12 unoff) | 3 | live fetch | All listed years have papers |
| ibps-clerk | IBPS Clerk | PASS | 17 (4 off / 13 unoff) | 3 | local gen + data check | All listed years have papers |
| ibps-rrb | IBPS RRB (Office Assistant & Officer) | PASS | 15 (4 off / 11 unoff) | 4 | local gen + data check | All listed years have papers |
| sbi-po | SBI PO | PASS | 16 (4 off / 12 unoff) | 4 | local gen + data check | All listed years have papers |
| sbi-clerk | SBI Clerk (Junior Associate) | PASS | 16 (4 off / 12 unoff) | 4 | local gen + data check | All listed years have papers |
| rbi-b | RBI Grade B | PASS | 12 (3 off / 9 unoff) | 4 | local gen + data check | All listed years have papers |
| rbi-asst | RBI Assistant | PASS | 10 (4 off / 6 unoff) | 7 | local gen + data check | All listed years have papers |
| afcat | AFCAT | PASS | 14 (0 off / 14 unoff) | 4 | local gen + data check | All listed years have papers |
| agniveer | Agniveer (Army / Navy / Air Force) | PASS | 12 (0 off / 12 unoff) | 4 | local gen + data check | All listed years have papers |
| coast-guard | Indian Coast Guard (Navik / DB) | PASS | 9 (0 off / 9 unoff) | 5 | local gen + data check | All listed years have papers |
| ctet | CTET | PASS | 12 (4 off / 8 unoff) | 5 | live fetch | All listed years have papers |
| ugc-net | UGC NET | PASS | 12 (3 off / 9 unoff) | 6 | local gen + data check | All listed years have papers |
| csir-net | CSIR NET | PASS | 9 (3 off / 6 unoff) | 6 | local gen + data check | All listed years have papers |
| kvs | KVS (PRT / TGT / PGT) | PASS | 8 (2 off / 6 unoff) | 6 | live fetch | Years with no verified paper (shows "Not available yet"): 2019 |
| dsssb | DSSSB (TGT / PGT / LDC) | PASS | 9 (3 off / 6 unoff) | 6 | local gen + data check | All listed years have papers |
| neet-ug | NEET UG | PASS | 24 (12 off / 12 unoff) | 4 | live fetch | All listed years have papers |
| jee-main | JEE Main | PASS | 16 (8 off / 8 unoff) | 4 | live fetch | All listed years have papers |
| jee-adv | JEE Advanced | PASS | 12 (4 off / 8 unoff) | 4 | local gen + data check | All listed years have papers |
| bitsat | BITSAT | PASS | 12 (0 off / 12 unoff) | 4 | local gen + data check | All listed years have papers |
| cuet-ug | CUET UG | PASS | 18 (4 off / 14 unoff) | 8 | local gen + data check | All listed years have papers |
| gate | GATE | PASS | 9 (3 off / 6 unoff) | 4 | local gen + data check | All listed years have papers |
| cat | CAT | PASS | 9 (3 off / 6 unoff) | 4 | local gen + data check | All listed years have papers |
| clat | CLAT | PASS | 17 (3 off / 14 unoff) | 8 | local gen + data check | All listed years have papers |
| nift | NIFT Entrance | PASS | 17 (0 off / 17 unoff) | 9 | live fetch | All listed years have papers |
| cbse-10 | CBSE Class 10 | PASS | 9 (3 off / 6 unoff) | 4 | local gen + data check | All listed years have papers |
| cbse-12 | CBSE Class 12 | PASS | 9 (3 off / 6 unoff) | 3 | local gen + data check | All listed years have papers |
| opsc-ocs | OPSC OCS (Odisha Civil Services) | PASS | 12 (4 off / 8 unoff) | 3 | local gen + data check | All listed years have papers |
| osssc | OSSSC RI / ARI / PEO | PASS | 10 (1 off / 9 unoff) | 6 | live fetch | Years with no verified paper (shows "Not available yet"): 2022 |
| bpsc | BPSC 70th CCE (Bihar) | PASS | 10 (3 off / 7 unoff) | 4 | local gen + data check | All listed years have papers |
| uppsc | UPPSC PCS | PASS | 9 (3 off / 6 unoff) | 4 | local gen + data check | All listed years have papers |
| mpsc | MPSC Rajyaseva (Maharashtra) | PASS | 6 (3 off / 3 unoff) | 3 | local gen + data check | All listed years have papers |
| tnpsc | TNPSC Group 2 / 2A | PASS | 9 (3 off / 6 unoff) | 3 | local gen + data check | All listed years have papers |
| rpsc-ras | RPSC RAS (Rajasthan) | PASS | 9 (3 off / 6 unoff) | 4 | local gen + data check | All listed years have papers |
| wbcs | WBCS (West Bengal) | PASS | 9 (0 off / 9 unoff) | 6 | live fetch | All listed years have papers |

## Spot-check detail (live fetch, 21 Nov 2026 evening)

All 12 fetched pages: HTTP 200, Exam Papers button present, both section headings present, photo cards present, numbered list visible and NOT locked, 0 "Official Archive" buttons.

| Page | HTTP | Button | Official sec | Unofficial sec | Photo cards | Numlists | Locked lists | Archive btn |
|---|---|---|---|---|---|---|---|---|
| SSC CGL | 200 | yes | yes | yes | 4 | 2 | 0 | 0 |
| SSC CHSL | 200 | yes | yes | yes | 4 | 2 | 0 | 0 |
| UPSC CSE | 200 | yes | yes | yes | 3 | 2 | 0 | 0 |
| RRB NTPC Graduate | 200 | yes | yes | yes | 2 | 1 | 0 | 0 |
| IBPS PO | 200 | yes | yes | yes | 3 | 2 | 0 | 0 |
| NEET UG | 200 | yes | yes | yes | 4 | 2 | 0 | 0 |
| JEE Main | 200 | yes | yes | yes | 4 | 2 | 0 | 0 |
| CTET | 200 | yes | yes | yes | 3 | 2 | 0 | 0 |
| WBCS | 200 | yes | yes | yes | 4 | 1 | 0 | 0 |
| OSSSC RI/ARI/PEO | 200 | yes | yes | yes | 1 | 1 | 0 | 0 |
| NIFT | 200 | yes | yes | yes | 8 | 1 | 0 | 0 |
| KVS | 200 | yes | yes | yes | 4 | 2 | 0 | 0 |
| /papers | 200 | yes (exam select + button) | — | — | — | 2 | 0 | 0 |

Note: "Numlists 1" on RRB/WBCS/OSSSC/NIFT = the static first year+stage has papers in only one section (e.g. RRB has 0 official papers by design — RRB publishes answer keys/response sheets only; WBCS/OSSSC 0 official for the shown year). Both section headings are still rendered; the empty one shows "Not available yet" + Request. Card/numlist counts above are for the static first year+stage only — other years/stages render via the same JS on pill click.

## Still missing / not done
- **Firebase login still blocked** (no project — deleted projects count against the 5-project quota until ~21 Dec 2026; awaiting user choice: limit increase / wait / other account). Login gate honestly says "Google sign-in setup ho raha hai"; Download + pattern/syllabus stay gated. Photos, videos and the numbered list are free without login.
- 5 duplicate video URLs exist in data.js, all CROSS-exam shares (same video relevant to two exams: 3 shared NTPC Graduate/UG, 2 shared RPF Constable/SI). Each exam shows the video once; left as-is deliberately.
- Round-2 intake files were NOT edited; only data.js + generator + site.js changed. Redeploy published the App agent's APK from final-deploy/ (see fix 6).
