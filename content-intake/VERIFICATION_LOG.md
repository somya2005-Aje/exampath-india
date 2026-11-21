# ExamPath India — Content Intake Verification Log

Date: 2026-11-21. Intake folder: `~/workspace/exampath-india/content-intake/`
Method: 6 parallel group agents collected papers/details/YouTube per exam; every link checked reachable on 2026-11-21 (curl / browser fetch / search-result confirmation) before inclusion. No invented URLs. Nothing found = recorded in `not_found_years`, never fabricated. Validation run by coordinator: all 56 files parse as JSON, required keys present, all paper URLs start with http, all YouTube URLs are `youtube.com/watch?v=` links. **Validated totals below are the counts actually in the files** (they override any worker's reported subtotal where they differ).

## Validated totals
- Exams covered: **56 / 56**
- Official papers: **167**
- Unofficial papers: **439**
- YouTube videos: **215**
- Not-found years: **8**

## Per-exam counts (official / unofficial / videos / not-found years)

| Exam | Official | Unofficial | Videos | Not found |
|---|---|---|---|---|
| SSC CGL | 8 | 16 | 5 | — |
| SSC CHSL | 6 | 12 | 4 | — |
| SSC GD Constable | 5 | 11 | 4 | 2019 |
| SSC MTS | 5 | 10 | 4 | — |
| SSC CPO SI | 5 | 10 | 5 | — |
| SSC Stenographer | 5 | 9 | 5 | — |
| SSC JE | 5 | 10 | 2 | — |
| SSC Selection Post | 4 | 7 | 5 | — |
| RRB NTPC Graduate | 0 | 11 | 5 | — |
| RRB NTPC Undergraduate | 0 | 4 | 4 | — |
| RRB Group D | 0 | 5 | 5 | — |
| RRB ALP | 0 | 8 | 5 | — |
| RRB JE | 0 | 9 | 4 | — |
| RRB Technician | 0 | 5 | 4 | — |
| RPF Constable | 0 | 5 | 4 | — |
| RPF Sub-Inspector | 0 | 4 | 3 | — |
| UPSC CSE | 8 | 16 | 3 | — |
| UPSC NDA | 5 | 10 | 3 | — |
| UPSC CDS | 4 | 8 | 4 | — |
| UPSC CAPF | 4 | 8 | 3 | — |
| UPSC ESE | 4 | 8 | 4 | — |
| UPSC CMS | 4 | 8 | 4 | — |
| OPSC OCS | 4 | 8 | 3 | — |
| OSSSC RI/ARI/PEO | 0 | 2 | 3 | 2023, 2022 |
| BPSC 70th CCE | 3 | 7 | 4 | — |
| UPPSC PCS | 3 | 6 | 4 | — |
| MPSC Rajyaseva | 3 | 3 | 3 | — |
| TNPSC Group 2/2A | 3 | 6 | 3 | — |
| RPSC RAS | 3 | 6 | 4 | — |
| WBCS | 0 | 3 | 3 | 2024, 2023, 2022 |
| IBPS PO | 7 | 11 | 3 | — |
| IBPS Clerk | 4 | 13 | 3 | — |
| IBPS RRB | 4 | 11 | 4 | — |
| SBI PO | 4 | 12 | 4 | — |
| SBI Clerk | 4 | 12 | 4 | — |
| RBI Grade B | 3 | 9 | 4 | — |
| RBI Assistant | 3 | 6 | 4 | 2024 |
| CTET | 4 | 8 | 5 | — |
| UGC NET | 3 | 9 | 6 | — |
| CSIR NET | 3 | 6 | 6 | — |
| KVS | 2 | 5 | 4 | 2019 |
| DSSSB | 3 | 6 | 6 | — |
| NEET UG | 6 | 12 | 4 | — |
| JEE Main | 4 | 8 | 4 | — |
| JEE Advanced | 4 | 8 | 4 | — |
| BITSAT | 0 | 6 | 4 | — |
| CUET UG | 3 | 6 | 2 | — |
| GATE | 3 | 6 | 4 | — |
| CAT | 3 | 6 | 4 | — |
| CLAT | 3 | 6 | 3 | — |
| NIFT | 0 | 6 | 0 | — |
| CBSE Class 10 | 3 | 6 | 4 | — |
| CBSE Class 12 | 3 | 6 | 3 | — |
| AFCAT | 0 | 8 | 4 | — |
| Agniveer | 0 | 6 | 4 | — |
| Indian Coast Guard | 0 | 6 | 2 | — |

## Group totals (validated)
- SSC: 43 official / 85 unofficial / 34 videos
- Railway/RRB: 0 / 51 / 34
- UPSC + State PSCs: 48 / 99 / 48
- Banking: 29 / 74 / 26
- Teaching: 15 / 34 / 27
- Medical/Engineering/Entrance + Boards + Defence: 32 / 96 / 46

## Important caveats (read before integrating)
1. **"Official" usually means the official archive/listing page**, not a per-year PDF. SSC, UPSC, NTA, IBPS, SBI and RBI serve papers/keys from one archive page or a candidate-login window; per-year entries point at that verified listing. No entry claims a direct per-paper PDF that was not found.
2. **Some bodies publish no papers at all**: RRB (answer keys/response sheets only), IBPS/SBI/RBI (notifications/keys only), BITSAT, NIFT, AFCAT, Agniveer, Coast Guard (memory-based exams only). Their `official_papers` are empty (or keys/notifications only) by design, and unofficial memory-based papers are labelled as such.
3. **SSC worker's reported subtotal (48 official) does not match its files (43)** — validated file count (43) is used everywhere in this log.
4. **Two entries have weak http values** (Med group): NIFT AglaSem entry `"http": null` (search-result confirmation only), CLAT AglaSem entry `"http": 0` (curl failed, search-confirmed). Re-check before publishing those two links.
5. **UGC NET video PJKfIeQ3lew** (Adda247): oEmbed "Forbidden" but watch page fetched 200; flagged in `ugc-net.json`.
6. **KVS 2022 = KVS 2023 papers**: Advt 15/2022 cycle exam held 07 Feb–11 Mar 2023; both years list the same verified pages (noted in `kvs.json`).
7. **TNPSC 2023**: no Group 2 Prelims held in 2023; the 2023 entry points to the Mains papers collection (noted in `tnpsc.json`).
8. **Group D year mapping**: the 2022 exam was the CEN 02/2018 cycle; a verified 2026-cycle paper exists but data.js has no 2026 year for Group D — noted in `rrb-groupd.json`, not listed as a year entry. Same for JE 2026 cycle.
9. **CLAT official papers are paid** (Rs 500 via candidate login, consortiumofnlus.ac.in).
10. **NEET 2026** (3 May) was cancelled after a leak; re-exam 21 June 2026 (noted in `neet-ug.json`).

## Sources that FAILED verification (excluded, not used)
- **Unreachable from this VM (curl 000 / fetch failed)**: rrbapply.gov.in, rrb.indianrailways.gov.in, rrbcdg.gov.in, osssc.gov.in, wbpsc.gov.in, bpsc.bih.nic.in (used bpsc.bihar.gov.in instead, 200), joinindiannavy.gov.in.
- **Testbook `/amp/` URLs**: HTTP 500 via curl across groups (bot protection); non-AMP equivalents used where they returned 200; AMP pages included only where a browser fetch returned 200 (noted per file).
- **Prepp.in**: HTTP 403 to curl (loads 200 via browser fetch); recorded as 200 with caveat. Prepp 404s excluded: `rrb-group-d-exam/practice_papers`, `rrb-technician-exam/practice_papers`, `ssc-steno-exam/practice-papers` (working slug `ssc-stenographer-exam`), `ssc-selection-post-exam/practice-papers` (working slug `/question-paper`).
- **Oliveboard 410s**: `ssc-cpo-pyps/`, `ssc-je-pyps/` (replaced by `ssc-cpo-paper-1-pyps/` / Prepp-Testbook pages). **Oliveboard 404s**: IBPS PO PDFs `IBPS-PO-2023/2021/2020-Shift-1-Prelims-PYP.pdf` (corrected slugs without `-Shift-1` verified 200 and used).
- **404s**: jeeadv.ac.in `/archives/past-question-papers.html`, exams.nta.ac.in/cuet-ug/, cbseacademic.nic.in/question_papers.html, Testbook CAT/NIFT/Agniveer pages, Adda247 Coast Guard page, all careers360.com `/exams/<exam>/question-papers` URLs, guessed Adda247/CareerPower/JagranJosh slugs for SSC exams.
- **403 (bot protection, curl only)**: Shiksha UGC NET page (excluded), Shiksha pages (Med group), AglaSem pages (verified via browser fetch where used).
- **500**: Testbook NEET AMP, Testbook Agniveer AMP, Testbook DSSSB AMP (main + TGT; PGT AMP 200 used).
- **503**: beta4.collegedunia.com JEE Advanced page.
- **SBI careers moved**: sbi.co.in/careers 302 → sbi.bank.in/web/careers (200); files use the final URL.
- **UPSC direct curl returns 404** (bot protection); archive verified via browser fetch (crawled 2026-11-18).

## Not-found years (8)
- SSC GD 2019; KVS 2019; OSSSC 2023, 2022; RBI Assistant 2024 (no recruitment cycle in 2024); WBCS 2024, 2023, 2022.

## Thin coverage (little or nothing verified)
- **WBCS**: 0 official, 3 unofficial, all 3 years not found (wbpsc.gov.in unreachable).
- **OSSSC**: 0 official, 2 unofficial (and those 2 are LI/Forester/Forest Guard PDFs, not RI/ARI/PEO — flagged in file), 2023/2022 not found.
- **RRB (all 8 exams)**: 0 official — portals unreachable from this VM; needs a browser re-check before any official RRB link is published.
- **NIFT**: 0 official, 0 YouTube videos (no watch URL found in two searches).
- **BITSAT / AFCAT / Agniveer / Coast Guard**: 0 official (bodies publish no papers).
- **SSC JE YouTube**: only 2 videos found; CUET/Coast Guard: 2 each; CBSE-12/CLAT: 3 each.

## Files
All 56 intake files in `~/workspace/exampath-india/content-intake/<exam-id>.json` + this log. A generator script `gen_ssc.py` (SSC group) also sits in the intake folder — it is a build helper, not intake data.
