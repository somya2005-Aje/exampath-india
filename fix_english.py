#!/usr/bin/env python3
"""ExamPath: convert all default (new-user) UI text from Hinglish to English.
Hindi/Odia stay available ONLY via the header language selector (I18N dict).
Each pair must match exactly once; the script fails loudly otherwise."""
import sys

PATH = "final-deploy/app.js"
src = open(PATH, encoding="utf-8").read()

PAIRS = [
 # hero + home headings (now via T() so the selector translates them)
 ("SSC, Railway, UPSC, Banking, Defence, Teaching, NEET, JEE, CUET aur all 28 states + 8 UTs — year-wise previous papers, mock tests, notes aur current affairs. <b>100% free, bina login.</b>",
  "SSC, Railway, UPSC, Banking, Defence, Teaching, NEET, JEE, CUET and all 28 states + 8 UTs — year-wise previous papers, mock tests, notes and current affairs. <b>100% free, no login needed.</b>"),
 ('<h2>⏰ Next Exam Countdown</h2><p>Dates tentative hain — official site par verify karein</p>',
  '<h2>⏰ ${T("countdownH")}</h2><p>${T("countdownNote")}</p>'),
 ('<h2>📚 Exam Categories</h2><a href="#/exams">View all →</a>',
  '<h2>📚 ${T("catH")}</h2><a href="#/exams">${T("viewAll")}</a>'),
 ('<h2>🗺️ States &amp; UTs</h2><a href="#/states">All 36 →</a>',
  '<h2>🗺️ ${T("statesH")}</h2><a href="#/states">${T("viewAll")}</a>'),
 ('<h2>🎯 Aaj kya karein?</h2>', '<h2>🎯 ${T("todoH")}</h2>'),
 ('<h2>📰 Aaj ki Current Affairs (Nov 2026)</h2>',
  '<h2>📰 ${T("caH")}</h2>'),
 # home honesty + admin notes
 ("<b>⚠️ Honesty note:</b> ExamPath koi official paper copy nahi karta. Jo paper official archive me hai, uska <b>official link</b> diya gaya hai. Jo abhi available nahi hai, us par saaf likha hai <b>“Not available yet”</b> — fake PDF kabhi nahi. Practice questions ExamPath ke original hain, official PYQ nahi.",
  "<b>⚠️ Honesty note:</b> ExamPath does not copy official papers. Where a paper is in the official archive, its <b>official link</b> is given. Where it is not available yet, it clearly says <b>“Not available yet”</b> — never a fake PDF. Practice questions are original ExamPath questions, not official PYQs."),
 ("<h3>Admin panel alag se banega</h3><p>Yeh sirf <b>User App</b> hai (bina login). Admin dashboard — exam/paper/question management — alag project me banega, is app ke saath mix nahi.</p>",
  "<h3>The admin panel is built separately</h3><p>This is only the <b>User App</b> (no login). The admin dashboard — exam, paper and question management — will be a separate project, never mixed into this app.</p>"),
 # search / exams / states
 ('toast("Kuch likh kar search karein")', 'toast("Type something to search")'),
 ("Kuch nahi mila. Try karein: “SSC”, “Odisha”, “2024”, “Banking”.",
  "Nothing found. Try: “SSC”, “Odisha”, “2024”, “Banking”."),
 ("Year list data-driven hai — sirf wahi years dikhte hain jinme kam se kam ek verified resource hai. Kisi exam par click karke year → stage → paper dekhein.",
  "The year list is data-driven — only years with at least one verified resource are shown. Click any exam to see year → stage → paper."),
 ("Har state ke flagship exams list me hain. State papers official portal se verify karke add hote hain — bina verification ke koi paper “available” nahi dikhaya jata.",
  "Each state's flagship exams are listed. State papers are added only after verification on the official portal — no paper is shown as “available” without verification."),
 # exam detail
 ("<h2>Exam nahi mila</h2>", "<h2>Exam not found</h2>"),
 ("Official portal link verification me hai — Request se manga sakte hain.",
  "The official portal link is under verification — you can request it below."),
 ("<h3 style=\"margin:18px 0 8px\">📅 Year chunein (sirf available years)</h3>",
  "<h3 style=\"margin:18px 0 8px\">📅 Choose a year (available years only)</h3>"),
 ("Is exam ke papers official archive me shift-wise available hain — neeche Official Archive button se official site khulegi.",
  "Papers for this exam are available shift-wise in the official archive — the Official Archive button below opens the official site."),
 ("Is exam ke kuch saal official portal par available hain; baaki par “Not available yet” dikhega — Request karein, verify hote hi add hoga.",
  "Some years of this exam are available on the official portal; the rest show “Not available yet” — request them and they will be added after verification."),
 ("ExamPath Original Practice Paper — 20 questions, PDF viewer me khulta hai. <b>Yeh official PYQ nahi hai</b>, practice ke liye banaya gaya hai.",
  "ExamPath Original Practice Paper — 20 questions, opens in the PDF viewer. <b>This is not an official PYQ</b>; it was made for practice."),
 ("📄 Viewer me kholein", "📄 Open in Viewer"),
 ("<h3 style=\"margin:20px 0 8px\">📺 Sample Paper Viewer (kaam karta hai)</h3>",
  "<h3 style=\"margin:20px 0 8px\">📺 Sample Paper Viewer (working demo)</h3>"),
 ("<a class=\"btn green\" href=\"#/practice/all\">✍️ Practice Questions</a><a class=\"btn orange\" href=\"#/mock\">⏱️ Mock Test dein</a>",
  "<a class=\"btn green\" href=\"#/practice/all\">✍️ Practice Questions</a><a class=\"btn orange\" href=\"#/mock\">⏱️ Take a Mock Test</a>"),
 ("◐ Portal par check karein", "◐ Check on portal"),
 ("Official key, jahan release hui ho", "Official key, wherever released"),
 ('toast("Request save ho gayi ✓ — verify hote hi paper add hoga")',
  'toast("Request saved ✓ — the paper will be added after verification")'),
 # papers page + viewer
 ("Flow: <b>Category → State (agar ho) → Exam → Year → Stage → Shift/Set → Resource</b>. Year select karte hi sirf usi year ke resources dikhte hain.",
  "Flow: <b>Category → State (if any) → Exam → Year → Stage → Shift/Set → Resource</b>. Selecting a year shows only that year's resources."),
 ("✅ Official archive wale exams", "✅ Exams with an official archive"),
 ("ExamPath Original Practice Paper (20 Q) — viewer, zoom, fullscreen, download aur save sab kaam karte hain.",
  "ExamPath Original Practice Paper (20 Q) — the viewer, zoom, fullscreen, download and save all work."),
 ("📄 Viewer kholein", "📄 Open Viewer"),
 ("20 original practice questions • <b>Official PYQ NAHI hai</b> • Source: ExamPath India (original)",
  "20 original practice questions • <b>NOT an official PYQ</b> • Source: ExamPath India (original)"),
 ("Official papers ke liye exam page par <b>Official Archive</b> button se conducting body ki site khulti hai — wahi asli source hai.",
  "For official papers, the <b>Official Archive</b> button on the exam page opens the conducting body's own site — that is the real source."),
 ('onclick="closeModal()">Band karein</button>', 'onclick="closeModal()">Close</button>'),
 # mocks
 ("📊 Meri Test History", "📊 My Test History"),
 ("Abhi koi test nahi diya. Upar se ek mock start karein — result yahi save hoga (is device par, bina login).",
  "No test taken yet. Start a mock above — the result will be saved here (on this device, no login)."),
 ("Mock nahi mila. <a href=\"#/mock\">Wapas →</a>", "Mock not found. <a href=\"#/mock\">Back →</a>"),
 ("Answers autosave hote hain", "Answers are autosaved"),
 ("Wrong Answers dekhein", "See Wrong Answers"),
 ("🎉 Perfect! Sab sahi — koi galat answer nahi.", "🎉 Perfect! All correct — no wrong answers."),
 ('${auto?"⏰ Time khatam — auto-submitted!":"✅ Test Submitted!"}',
  '${auto?"⏰ Time\u2019s up — auto-submitted!":"✅ Test Submitted!"}'),
 # practice
 ("Is category me abhi koi question nahi hai. ${subj===\"wrong\"?\"Pehle ek mock dein — galat answers yahan aayenge.\":\"\"}",
  "There are no questions in this category yet. ${subj===\"wrong\"?\"Take a mock first — your wrong answers will appear here.\":\"\"}"),
 ('"✅ Sahi jawab!"', '"✅ Correct!"'),
 ('"❌ Galat — sahi jawab: "', '"❌ Wrong — correct answer: "'),
 # daily quiz
 ("Roz 10 naye questions — date ke hisaab se. Score save hota hai (is device par).",
  "10 new questions every day — based on the date. Your score is saved (on this device)."),
 ('"Good — roz practice se aur badhega."', '"Good — daily practice will improve it further."'),
 ('"Koi baat nahi — notes padhkar kal phir try karein."', '"No problem — read the notes and try again tomorrow."'),
 ("Practice karein →", "Practise →"),
 ('"❌ Sahi jawab: "', '"❌ Correct answer: "'),
 # CA page
 ("🧠 CA Quiz — inhi facts par 10 questions", "🧠 CA Quiz — 10 questions on these facts"),
 ("Semicon 2.0, Forex reserves, ISA, COP 17, UNESCO — sab cover hota hai.",
  "Semicon 2.0, Forex reserves, ISA, COP 17, UNESCO — all covered."),
 ("CA Quiz Start karein →", "Start CA Quiz →"),
 ("Verified facts • Source + date har item par", "Verified facts • Source + date on every item"),
 # planner
 ("Daily goal • Streak • Tasks — sab is device par save",
  "Daily goal • Streak • Tasks — all saved on this device"),
 ("Roz kitne questions practice karne hain?", "How many questions do you want to practise each day?"),
 ('placeholder="e.g. Polity notes revise karein"', 'placeholder="e.g. Revise Polity notes"'),
 ("Abhi koi task nahi. Upar se add karein.", "No tasks yet. Add one above."),
 ("Dates badal sakti hain — hamesha official website par verify karein.",
  "Dates may change — always verify on the official website."),
 ('toast("Daily goal save ho gaya ✓")', 'toast("Daily goal saved ✓")'),
 ('toast("Task likhein pehle")', 'toast("Write a task first")'),
 # saved
 ("🔖 My Library (is device par)", "🔖 My Library (on this device)"),
 ("Bina login — sab kuch aapke device par save hai. Browser data clear karne par yeh delete ho jayega.",
  "No login — everything is saved on your device. Clearing browser data will delete it."),
 ("Abhi kuch save nahi hai. Kisi exam page par <b>💾 Save</b> dabayein.",
  "Nothing saved yet. Tap <b>💾 Save</b> on any exam page."),
 ("Koi bookmark nahi. Practice me ☆ dabakar save karein.",
  "No bookmarks yet. Tap ☆ in Practice to save one."),
 ("Galat hue questions dobara practice karein:", "Practise the questions you got wrong again:"),
 ("Abhi koi wrong answer nahi — mock ya practice dekar dekhein.",
  "No wrong answers yet — take a mock or practise to see them here."),
 ("Koi request nahi.", "No requests yet."),
 ("if(confirm('Sab saved data delete karein?'))", "if(confirm('Delete all saved data?'))"),
 # profile
 ("👤 My Dashboard — Guest (bina login)", "👤 My Dashboard — Guest (no login)"),
 ("Guest user</b> — ExamPath me login nahi hota. Aapki progress, saved papers aur test history sirf is device par store hoti hai.",
  "Guest user</b> — ExamPath has no login. Your progress, saved papers and test history are stored only on this device."),
 ("Abhi koi weak topic nahi — mock dein aur analysis yahan dekhein.",
  "No weak topics yet — take a mock and the analysis will appear here."),
 ("Abhi koi test nahi diya.", "No test taken yet."),
 ("Mock dein →", "Take a Mock →"),
 ('toast("Data download ho gaya ✓")', 'toast("Data downloaded ✓")'),
 # portals + languages
 ("Papers aur notifications ka <b>asli source</b> hamesha conducting body ki official site hoti hai. ExamPath sirf link deta hai — paper copy nahi karta.",
  "The <b>real source</b> of papers and notifications is always the conducting body's official site. ExamPath only links to it — it does not copy papers."),
 ("State PSC portals (BPSC, UPPSC, MPSC, TNPSC, RPSC…) official verification ke baad add honge. Tab tak state exams ki list <a href=\"#/states\">States page</a> par dekhein.",
  "State PSC portals (BPSC, UPPSC, MPSC, TNPSC, RPSC…) will be added after official verification. Until then, see the state exams list on the <a href=\"#/states\">States page</a>."),
 ("Interface/content framework 22 scheduled languages ke liye hai. <b>Har paper har language me nahi hota</b> — availability har resource par alag se dikhai jati hai. UI abhi English + हिन्दी + ଓଡ଼ିଆ me hai (header se badlein).",
  "The interface/content framework covers all 22 scheduled languages. <b>Not every paper exists in every language</b> — availability is shown separately on each resource. The app language can be changed from the header (English, Hindi, Odia); exam content itself is in English, the exam medium."),
 ("English scheduled language nahi hai — woh exam medium ke roop me alag se available hai. Urdu right-to-left (RTL) layout supported hai. Machine-translated official questions bina human review ke publish nahi hote.",
  "English is not a scheduled language — it is available separately as an exam medium. Urdu right-to-left (RTL) layout is supported. Machine-translated official questions are never published without human review."),
]

missing = []
for old, new in PAIRS:
    n = src.count(old)
    if n == 0:
        missing.append(old[:70])
    elif n > 1:
        missing.append(f"MULTI({n}) {old[:70]}")
    else:
        src = src.replace(old, new)

if missing:
    print("FAILED — not found or ambiguous:")
    for m in missing:
        print(" -", m)
    sys.exit(1)

open(PATH, "w", encoding="utf-8").write(src)
print(f"OK — {len(PAIRS)} replacements applied")
