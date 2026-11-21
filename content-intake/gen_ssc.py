#!/usr/bin/env python3
"""Generate ExamPath India SSC content-intake JSON files (verified 2026-11-21).
All URLs below were HTTP-checked (curl, 200) or returned by browser search on 2026-11-21.
Official papers: SSC publishes papers/answer keys via the candidate login window after
each tier; there is no public per-year PDF archive, so the official entry per year points
to the live official archive listing page (verified HTTP 200)."""
import json, os

OUT = os.path.expanduser("~/workspace/exampath-india/content-intake")
os.makedirs(OUT, exist_ok=True)
D = "2026-11-21"
SSC_ARCHIVE = "https://ssc.gov.in/candidate-corner/previousPaper"
SSC_HOME = "https://ssc.gov.in/"

def off(year, stage, exam_name):
    return {"year": year, "stage": stage, "title": f"{exam_name} {year} \u2014 Official Previous Papers & Answer Keys",
            "url": SSC_ARCHIVE, "source": "SSC \u2014 ssc.gov.in (Official)",
            "checked": D, "http": 200}

def un(year, stage, title, url, source):
    return {"year": year, "stage": stage, "title": title, "url": url,
            "source": source, "checked": D, "http": 200}

def build(exam_id, exam_name, years, off_stage, details, un_entries, videos, not_found, notes):
    data = {
        "exam_id": exam_id,
        "exam_name": exam_name,
        "official_papers": [off(y, off_stage, exam_name) for y in years],
        "unofficial_papers": un_entries,
        "details": details,
        "youtube": videos,
        "not_found_years": not_found,
        "notes": notes,
    }
    p = os.path.join(OUT, exam_id + ".json")
    with open(p, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(exam_id, "official:", len(data["official_papers"]),
          "unofficial:", len(data["unofficial_papers"]),
          "videos:", len(videos), "not_found:", not_found)

def det(elig, pattern, syllabus):
    return {"eligibility": elig, "pattern": pattern, "syllabus": syllabus,
            "official_page": SSC_HOME,
            "sources": [SSC_HOME, SSC_ARCHIVE]}

def yt(title, channel, url):
    return {"title": title, "channel": channel, "url": url}

# ---------------- SSC CGL ----------------
cgl_years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017]
cgl_un = []
for y in cgl_years:
    cgl_un.append(un(y, "Tier-I", f"SSC CGL {y} \u2014 Tier 1 & 2 Papers (shift-wise, with solutions)",
                    "https://testbook.com/ssc-cgl-exam/previous-year-papers", "Testbook"))
    cgl_un.append(un(y, "Tier-I", f"SSC CGL {y} \u2014 Tier 1 & 2 Practice Papers (with answer keys)",
                    "https://prepp.in/ssc-cgl-exam/practice-papers", "Prepp"))
build("ssc-cgl", "SSC CGL", cgl_years, "Tier-I",
    det("Graduation",
        "Tier-I: 100 Q, 200 marks, 60 min. Tier-II: Paper I (Maths+Reasoning+English+GK+Computer), Paper II/III as per post.",
        "Quantitative Aptitude, General Intelligence & Reasoning, English Comprehension, General Awareness, Computer Knowledge"),
    cgl_un,
    [yt("SSC CGL Marathon Class 2026 | SSC CGL Previous Year Solved Paper (2024-25) | SSC CGL Question Paper", "SSC Adda247", "https://www.youtube.com/watch?v=ARt6wa-UpyI"),
     yt("Lecture 15 | 13 Sep 2024 | Shift 3 | Maths Selection Series | SSC CGL, CHSL, MTS, CPO", "Unlocked SSC", "https://www.youtube.com/watch?v=lQT-RqXlEqk"),
     yt("How Abhinav Sir Cracked SSC CGL with AIR 27? | SSC CGL 2025 Strategy for Beginners | SSC Podcast", "Testbook", "https://www.youtube.com/watch?v=81G6_QCRdCg"),
     yt("SSC CGL 2026 | SSC CGL 2022 English Paper Solution All Shift | SSC CGL English Classes By Neha Mam", "English by Neha Vats", "https://www.youtube.com/watch?v=xPVIsnBUJ5o"),
     yt("SSC CGL & CHSL 2026 Static GK Marathon | SSC CGL/CHSL Static GK Most Important Topics | By Pawan Sir", "SSC Adda247", "https://www.youtube.com/watch?v=QjSlI3VA-2w")],
    [],
    "Official: SSC releases papers/answer keys via the candidate login window after each tier; no public per-year PDF archive exists, so each official entry links to the live official archive listing (HTTP 200 on 2026-11-21). Unofficial: Testbook non-AMP URLs used (the /amp/ variants returned HTTP 500 via curl on 2026-11-21; non-AMP equivalents verified 200). SSC CGL 2026 Tier-1 was held Sep 2026 (result awaited per site calendar); no verified upcoming dates published.")

# ---------------- SSC CHSL ----------------
chsl_years = [2024, 2023, 2022, 2021, 2020, 2019]
chsl_un = []
for y in chsl_years:
    chsl_un.append(un(y, "Tier-I", f"SSC CHSL {y} \u2014 Tier 1 & 2 Papers (shift-wise, with solutions)",
                    "https://testbook.com/ssc-chsl/previous-year-papers", "Testbook"))
    chsl_un.append(un(y, "Tier-I", f"SSC CHSL {y} \u2014 Previous Year Papers with Solutions",
                    "https://www.adda247.com/jobs/ssc-chsl-previous-year-question-paper/", "Adda247"))
build("ssc-chsl", "SSC CHSL", chsl_years, "Tier-I",
    det("12th pass",
        "Tier-I: 100 Q, 200 marks, 60 min. Tier-II: Maths, Reasoning, English, GK + Skill Test.",
        "Quant, Reasoning, English, General Awareness, Typing / Data Entry Skill Test"),
    chsl_un,
    [yt("SSC CHSL 2025 Maths PYQ | 12 Nov Paper Solution | 25 Questions", "Vitorr Classes", "https://www.youtube.com/watch?v=UOwGi3vmcqI"),
     yt("SSC CHSL 2025 TIER 2 | Maths Complete Solution | SSC CHSL Mains Maths Solution By Abhishek Ojha Sir", "Rankers Gurukul", "https://www.youtube.com/watch?v=oEIt9_xmUBA"),
     yt("SSC CHSL Previous Year Question Paper | 5 July 2019 Morning | Maths Paper Solved | SSC CHSL Maths", "PendulumEdu", "https://www.youtube.com/watch?v=R-CVYtiPp34"),
     yt("SSC CHSL Exam 2026 | Previous Year Paper | English MCQ Solution | Day 1", "Adda247 Bengali", "https://www.youtube.com/watch?v=zwEgcWWKb8M")],
    [],
    "Official: papers/answer keys via candidate login after each tier; archive listing linked per year (HTTP 200). Testbook non-AMP URL used (/amp/ returned HTTP 500 via curl). Important dates (SSC calendar, official): SSC CHSL 2026 Tier-1 scheduled 30 Nov \u2013 31 Dec 2026; verify admit card on ssc.gov.in.")

# ---------------- SSC GD ----------------
gd_years = [2024, 2023, 2022, 2021, 2019]
gd_un = []
for y in [2024, 2023, 2021]:
    gd_un.append(un(y, "CBT", f"SSC GD Constable {y} \u2014 CBT Papers (shift-wise, with solutions)",
                    "https://testbook.com/ssc-gd-constable/previous-year-papers", "Testbook"))
    gd_un.append(un(y, "CBT", f"SSC GD {y} Question Paper PDF (shift-wise, English & Hindi)",
                    "https://www.adda247.com/jobs/ssc-gd-previous-year-question-papers/", "Adda247"))
    gd_un.append(un(y, "CBT", f"SSC GD {y} CBT Previous Year Papers (shift-wise PDFs)",
                    "https://www.oliveboard.in/blog/ssc-gd-pyps/", "Oliveboard"))
gd_un.append(un(2022, "CBT", "SSC GD Constable 2022 \u2014 CBT Papers (shift-wise, with solutions)",
                "https://testbook.com/ssc-gd-constable/previous-year-papers", "Testbook"))
gd_un.append(un(2022, "CBT", "SSC GD Constable Previous Year Papers 2021\u20132025 (with solutions)",
                "https://www.sscadda.com/ssc-gd-constable-previous-year-paper/", "SSC Adda"))
build("ssc-gd", "SSC GD Constable", gd_years, "CBT",
    det("10th pass",
        "CBT: 80 Q, 160 marks, 60 min. Then PET/PST, medical.",
        "General Intelligence & Reasoning, GK & Awareness, Elementary Maths, English/Hindi"),
    gd_un,
    [yt("SSC GD 2025 Math solution 4th Feb Shift-3 Solved! 100% Real Questions in Bengali", "Curious Math by SS", "https://www.youtube.com/watch?v=eVGh0lwfVxI"),
     yt("SSC GD 2026: Maths 20/20 Target | SSC GD Previous Year Paper Solution | PYQ Set-1 | Ashok Sir", "A4 Academy", "https://www.youtube.com/watch?v=4tUJY1zRik8"),
     yt("SSC GD 2026 | SSC GD Maths PYQ | SSC Previous Year Paper Solution | By Aditya Patel Sir", "WiNNERS Institute", "https://www.youtube.com/watch?v=XpLNpNZHt54"),
     yt("SSC GD 2027 | Maths PYQ Set-10 | SSC GD Maths Previous Year Question Paper Solved by Vivek Sir", "Vidhya Manch", "https://www.youtube.com/watch?v=K2d2TL6JzUY")],
    [2019],
    "2019: no source found confirming a 2019 paper on 2026-11-21 (Adda247/Oliveboard list 2025, 2024, 2023, 2021; SSC Adda lists 2021\u20132025). Testbook's GD collection page is live (HTTP 200) but its per-year coverage for 2019 was not individually confirmed, so 2019 is recorded as not found rather than assumed. Official: papers via candidate login; archive listing linked per year (HTTP 200).")

# ---------------- SSC MTS ----------------
mts_years = [2024, 2023, 2022, 2021, 2019]
mts_un = []
for y in mts_years:
    mts_un.append(un(y, "Session 1", f"SSC MTS {y} Question Paper and Answer Key PDF (shift-wise, English & Hindi)",
                    "https://prepp.in/ssc-mts-exam/practice_papers", "Prepp"))
    mts_un.append(un(y, "Session 1", f"SSC MTS {y} \u2014 Previous Year Papers (shift-wise, with solutions)",
                    "https://testbook.com/ssc-mts/previous-year-papers", "Testbook"))
build("ssc-mts", "SSC MTS", mts_years, "Session 1",
    det("10th pass",
        "Session 1: Numerical & Mathematical Ability + Reasoning (no negative marking). Session 2: GK + English.",
        "Numerical Ability, Reasoning, General Awareness, English Language"),
    mts_un,
    [yt("SSC MTS PREVIOUS YEAR PAPER | SSC MTS 1 September 2023 / 3rd Shift / DETAIL SOLUTION | MTS GK PYQ 2023", "Study Point 11", "https://www.youtube.com/watch?v=b82WG4BQ99g"),
     yt("SSC MTS/SSC GD 2026 | GK GS Practice Set for SSC MTS/SSC GD Exams | MTS, GD GK GS By Ashutosh Sir", "SSC Adda247", "https://www.youtube.com/watch?v=-exrWi2OTgQ"),
     yt("SSC MTS Havaldar GK GS 2026 | GK GS MCQs | SSC MTS Havaldar 2026 GK GS | By Ashutosh Sir", "SSC Adda247", "https://www.youtube.com/watch?v=CF1lOt664t0"),
     yt("SSC MTS/GD 2026 | Reasoning Practice Set for SSC MTS/SSC GD Exams | Reasoning By Atul Awasthi Sir", "SSC Adda247", "https://www.youtube.com/watch?v=DJgSJA43gDM")],
    [],
    "Prepp year table verified in search results: 2024, 2023, 2022, 2021, 2020, 2019, 2017 with shift-wise PDFs. Testbook non-AMP URL used (/amp/ returned HTTP 500 via curl). Adda247 MTS PYQ page also live (HTTP 200): https://www.adda247.com/jobs/ssc-mts-previous-year-question-paper/ \u2014 not listed per year because its year coverage was not individually confirmed. Official: papers via candidate login; archive listing linked per year (HTTP 200).")

# ---------------- SSC CPO ----------------
cpo_years = [2024, 2023, 2022, 2021, 2020]
cpo_un = []
for y in [2024, 2023, 2022, 2020]:
    cpo_un.append(un(y, "Paper-I", f"SSC CPO {y} Paper 1 Question Paper and Answer Key PDF (shift-wise)",
                    "https://prepp.in/ssc-cpo-exam/practice_papers", "Prepp"))
    cpo_un.append(un(y, "Paper-I", f"SSC CPO {y} Previous Year Question Papers (shift-wise PDFs)",
                    "https://www.oliveboard.in/blog/ssc-cpo-paper-1-pyps/", "Oliveboard"))
cpo_un.append(un(2021, "Paper-II", "SSC CPO 2021 Tier 2 Question Paper PDF",
                "https://www.pw.live/ssc/exams/ssc-cpo-previous-year-papers", "PW.live"))
cpo_un.append(un(2021, "Paper-II", "SSC CPO 2021 Tier 2 Question Paper (with solutions)",
                "https://testbook.com/ssc-cpo/previous-year-papers", "Testbook"))
build("ssc-cpo", "SSC CPO (SI)", cpo_years, "Paper-I",
    det("Graduation",
        "Paper-I: 200 Q, 200 marks. Paper-II: English 200 Q. Then PET/PST.",
        "Quant, Reasoning, GK, English Comprehension"),
    cpo_un,
    [yt("SSC CPO 2026 | SSC CPO Reasoning Practice Paper | SSC CPO Reasoning Classes | By DK Sir", "SSC Adda247", "https://www.youtube.com/watch?v=g8nxNSfP0-4"),
     yt("SSC CPO 2026 | SSC CPO GK GS PYQs | SSC CPO GK GS Classes | SSC CPO GK GS By Somya Mam", "SSC Adda247", "https://www.youtube.com/watch?v=SGn1N3uxQyo"),
     yt("SSC CPO SI (Sub-Inspector) 2025 | English | PYPs | #40 Previous Year Paper Solution", "airGurukul", "https://www.youtube.com/watch?v=gJV4XIoQw7g"),
     yt("SSC CPO 2024 ALL 9 SHIFTS Reasoning Marathon | Complete Paper Solution | Best Concepts +450 PYQs", "Reasoning By Rakesh Yadav Sir", "https://www.youtube.com/watch?v=Z_kNc0b3UkY"),
     yt("SSC CPO 2026 GK PYQs | 2025 All Shifts GK Questions | by Dr. Vipan Goyal | EDU TERIA", "EDU TERIA COMPETITIVE EXAMS", "https://www.youtube.com/watch?v=PWVhvqVxIB8")],
    [],
    "2021 Paper-I: no source found listing a 2021 Paper-I paper (Prepp/Oliveboard/Testbook year lists skip 2021); 2021 Tier 2 papers ARE available (PW.live, Testbook), so 2021 is covered via Paper-II only. Testbook non-AMP URL used (/amp/ returned HTTP 500 via curl). Official: papers via candidate login; archive listing linked per year (HTTP 200).")

# ---------------- SSC Stenographer ----------------
steno_years = [2024, 2023, 2022, 2021, 2020]
steno_un = []
for y in [2024, 2023, 2022]:
    steno_un.append(un(y, "CBT", f"SSC Stenographer {y} Question Paper (shift-wise, English & Hindi)",
                    "https://testbook.com/ssc-stenographer/previous-year-papers", "Testbook"))
    steno_un.append(un(y, "CBT", f"SSC Stenographer {y} Question Paper with Answer Key PDF (shift-wise)",
                    "https://prepp.in/ssc-stenographer-exam/practice-papers", "Prepp"))
steno_un.append(un(2021, "CBT", "SSC Stenographer 2021 Question Paper (shift-wise PDFs)",
                    "https://www.careerpower.in/ssc-stenographer-previous-year-question-paper.html", "CareerPower"))
steno_un.append(un(2020, "CBT", "SSC Stenographer 2020 Question Paper (shift-wise PDFs)",
                    "https://www.careerpower.in/ssc-stenographer-previous-year-question-paper.html", "CareerPower"))
steno_un.append(un(2020, "CBT", "SSC Stenographer 2020 Question Paper with Answer Key PDF",
                    "https://prepp.in/ssc-stenographer-exam/practice-papers", "Prepp"))
build("ssc-steno", "SSC Stenographer", steno_years, "CBT",
    det("12th pass",
        "CBT: 200 Q, 200 marks. Skill Test: shorthand (100/80 wpm).",
        "General Intelligence & Reasoning, General Awareness, English Language"),
    steno_un,
    [yt("SSC Stenographer 2026 | SSC Stenographer Reasoning Practice Set #04 | SSC Steno Reasoning by DK Sir", "SSC Adda247", "https://www.youtube.com/watch?v=zUEmBMcYA4s"),
     yt("SSC Stenographer 2026 | SSC Stenographer GK GS Classes | Polity Practice Set #11 | By Somya Mam", "SSC Adda247", "https://www.youtube.com/watch?v=Epa2WysIUaY"),
     yt("SSC Stenographer 2026 | SSC Steno Reasoning Previous Year Question Paper | Garima Ma'am | Testbook", "Testbook", "https://www.youtube.com/watch?v=9-WuFhZWAUs"),
     yt("SSC Stenographer 2025 | SSC Stenographer English Most Important Questions | Parneet Ma'am | TESTBOOK", "Testbook", "https://www.youtube.com/watch?v=R8nUu9LwUjw"),
     yt("SSC Stenographer 2026 | SSC Stenographer Reasoning Practice Set #01 | SSC Steno Reasoning by DK Sir", "SSC Adda247", "https://www.youtube.com/watch?v=EkitkXcC-68")],
    [],
    "2021: only CareerPower's year list confirms 2021 (Prepp/Testbook/Oliveboard lists skip 2021). Oliveboard Steno PYQ page also live (HTTP 200) covering 2022\u20132025: https://www.oliveboard.in/blog/ssc-stenographer-pyps/ . Testbook non-AMP URL used (/amp/ returned HTTP 500 via curl). Official: papers via candidate login; archive listing linked per year (HTTP 200).")

# ---------------- SSC JE ----------------
je_years = [2024, 2023, 2022, 2021, 2019]
je_un = []
for y in [2024, 2023, 2022, 2019]:
    je_un.append(un(y, "Paper-I", f"SSC JE {y} Previous Year Papers (Civil, Mechanical, Electrical; Paper-I & Paper-II)",
                    "https://testbook.com/ssc-je/previous-year-papers", "Testbook"))
    je_un.append(un(y, "Paper-I", f"SSC JE {y} Question Paper and Answer Key PDF (Paper 1 & Paper 2, all branches)",
                    "https://prepp.in/ssc-je-exam/practice_papers", "Prepp"))
je_un.append(un(2021, "Paper-I", "SSC JE 2021 Previous Year Papers (Civil, Mechanical, Electrical; with solutions)",
                "https://testbook.com/ssc-je/previous-year-papers", "Testbook"))
je_un.append(un(2021, "Paper-I", "SSC JE 2021 Previous Year Question Papers with Solution PDF",
                "https://www.tutorialsduniya.com/exams/ssc-je-previous-year-question-papers/", "TutorialsDuniya"))
build("ssc-je", "SSC JE", je_years, "Paper-I",
    det("Diploma / B.E. (Engg)",
        "Paper-I: 200 Q (GK, Reasoning + Engineering). Paper-II: Engineering (300 marks).",
        "Civil / Electrical / Mechanical Engineering, GK, Reasoning"),
    je_un,
    [yt("Power Plant | SSC JE Previous Year Question Paper | Mechanical Engineering | SSC JE 2023", "Engineers Wallah (Physics Wallah)", "https://www.youtube.com/watch?v=harh9ta5Q4Q"),
     yt("SSC JE CBT-1 2026 | SSC JE Exam Preparation & Expected Questions | SSC JE Electrical Engineering", "Engineers Wallah (Physics Wallah)", "https://www.youtube.com/watch?v=rIrNnwB7xwg")],
    [],
    "2021: Prepp's year list skips 2021 (2025, 2024, 2023, 2022, 2020, 2019...); TutorialsDuniya lists 2021 explicitly. Adda247 JE page also live (HTTP 200): https://www.adda247.com/engineering-jobs/ssc-je-previous-year-question-papers/ and CareerPower JE page live (HTTP 200): https://www.careerpower.in/ssc-je-previous-year-question-papers.html \u2014 year coverage not individually confirmed, so not listed per year. Guidely JE page also live (HTTP 200): https://guidely.in/previous-year-papers/ssc-je (shift-wise Paper 1 2019\u20132025, Paper 2). YouTube: only 2 JE videos were returned by search on 2026-11-21, so only 2 recorded (max is 6, not a minimum). Testbook non-AMP URL used (/amp/ returned HTTP 500 via curl). Official: papers via candidate login; archive listing linked per year (HTTP 200).")

# ---------------- SSC Selection Post ----------------
sp_years = [2024, 2023, 2022, 2021]
sp_un = []
for y in [2024, 2023]:
    sp_un.append(un(y, "CBT", f"SSC Selection Post {y} Question Paper with Answer Key PDF (Matriculation / Higher Secondary / Graduation levels)",
                    "https://prepp.in/ssc-selection-post-exam/question-paper", "Prepp"))
    sp_un.append(un(y, "CBT", f"SSC Selection Post {y} Question Paper PDF (level-wise, English & Hindi)",
                    "https://www.adda247.com/jobs/ssc-selection-post-previous-year-question-paper/", "Adda247"))
sp_un.append(un(2022, "CBT", "SSC Selection Post 2022 Question Paper with Answer Key PDF (level-wise)",
                "https://prepp.in/ssc-selection-post-exam/question-paper", "Prepp"))
sp_un.append(un(2022, "CBT", "SSC Selection Post Phase 9 (2022) Previous Year Question Papers (shift-wise PDFs)",
                "https://www.oliveboard.in/blog/ssc-selection-post-pyps/", "Oliveboard"))
sp_un.append(un(2021, "CBT", "SSC Selection Post 2021 Question Paper with Answer Key PDF (level-wise)",
                "https://prepp.in/ssc-selection-post-exam/question-paper", "Prepp"))
build("ssc-sp", "SSC Selection Post", sp_years, "CBT",
    det("10th / 12th / Graduation",
        "CBT: 100 Q, 200 marks, 60 min (level-wise syllabus).",
        "GK, Reasoning, Quant, English (level-wise)"),
    sp_un,
    [yt("SSC Selection Post Phase 14 Complete Maths Solution | 25 Sept Shift 1 | Best Approach SSC CGL 2026", "SSC JIVI", "https://www.youtube.com/watch?v=WebhyhcOovA"),
     yt("SSC Phase 14 Reasoning Classes | SSC Selection Post Reasoning Practice Set #1 | Reasoning By DK Sir", "SSC Adda247", "https://www.youtube.com/watch?v=FoS32WOJOyU"),
     yt("SSC Phase 14 Maths Classes 2026 | SSC Selection Post Maths PYQ | Number System #2 | By Ashish Sir", "SSC Adda247", "https://www.youtube.com/watch?v=rmlerChogWU"),
     yt("SSC Phase 14 GK GS Classes | SSC Selection Post GK GS PYQ | Science & Technology | By Somya Mam", "SSC Adda247", "https://www.youtube.com/watch?v=00bvKnvezhU"),
     yt("SSC Phase 14 GK GS Classes | SSC Selection Post GK GS PYQ | International & National | By Somya Mam", "SSC Adda247", "https://www.youtube.com/watch?v=N1CLcgPJUro")],
    [],
    "Prepp year list verified: 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018 (level-wise). 2021: only Prepp confirms 2021; Adda247/Oliveboard lists cover 2022\u20132025. Testbook Selection Post collection page also live (HTTP 200): https://testbook.com/ssc-selection-post/previous-year-papers \u2014 year coverage not individually confirmed. Prepp's /practice-papers slug for this exam returned 404; the working slug is /question-paper (verified 200). Official: papers via candidate login; archive listing linked per year (HTTP 200).")
