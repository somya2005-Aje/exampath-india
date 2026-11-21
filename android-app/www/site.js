/* ExamPath India — Website engine (proper multi-page site). No login.
   All personal data stays on the device (localStorage). Default language: English. */
"use strict";
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||"null");localStorage.setItem(k,JSON.stringify(v));return v}catch(e){return v===undefined?null:v}}
function toast(m){const t=$("#toast");if(!t)return;t.textContent=m;t.style.display="block";clearTimeout(t._h);t._h=setTimeout(()=>t.style.display="none",2600)}
function openModal(html,wide){const m=$("#modal"),b=$("#modalBox");if(!m)return;b.className="modal-box"+(wide?" wide":"");b.innerHTML=html;m.classList.add("open")}
function closeModal(){const m=$("#modal");if(m)m.classList.remove("open")}
const _modal=$("#modal");if(_modal)_modal.addEventListener("click",e=>{if(e.target.id==="modal")closeModal()});
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeModal()});
function seededShuffle(arr,seed){const a=[...arr];let s=seed>>>0||1;const rnd=()=>((s=(s*1664525+1013904223)>>>0)/4294967296);for(let i=a.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
const examById=id=>EP.exams.find(e=>e[0]===id);
const catById=id=>EP.categories.find(c=>c.id===id);
const portalOf=e=>e[6]===null?null:EP.portals[e[6]];
const examStatus=id=>EP.examStatus[id]||"partial";
const slug=s=>String(s).toLowerCase().replace(/&/g,"and").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
function savedPapers(){return store("ep_saved")||[]}
function bookmarks(){return store("ep_bookmarks")||[]}
function wrongIds(){return store("ep_wrong")||[]}
function history(){return store("ep_history")||[]}
function markActivity(){const t=new Date();const d=t.toISOString().slice(0,10);const st=store("ep_streak")||{last:null,count:0};if(st.last===d)return;const y=new Date(t);y.setDate(y.getDate()-1);st.count=(st.last===y.toISOString().slice(0,10))?st.count+1:1;st.last=d;store("ep_streak",st)}
function toggleSavePaper(key,label){let s=savedPapers();const i=s.findIndex(x=>x.key===key);if(i>=0){s.splice(i,1);toast("Removed from My Library")}else{s.push({key,label,at:new Date().toISOString().slice(0,10)});toast("Saved to My Library ✓")}store("ep_saved",s)}
function toggleBookmark(qid){let b=bookmarks();const i=b.indexOf(qid);if(i>=0){b.splice(i,1);toast("Bookmark removed")}else{b.push(qid);toast("Question bookmarked ✓")}store("ep_bookmarks",b)}
function shareLink(title,text){const url=location.href;if(navigator.share){navigator.share({title,text,url}).catch(()=>{})}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(()=>toast("Link copied ✓"))}else toast(url)}
function requestPaper(examId,y,stage,type){const r=store("ep_requests")||[];r.push({exam:examId,year:y,stage,type,at:new Date().toISOString().slice(0,10)});store("ep_requests",r);toast("Request saved ✓ — the paper will be added after verification")}

/* ---------- i18n (nav + hero only; every other string is English) ---------- */
const I18N={
 en:{home:"Home",exams:"Exams",papers:"Previous Papers",mock:"Mock Tests",study:"Study Material",ca:"Current Affairs",quiz:"Daily Quiz",saved:"Saved",profile:"Profile",tag:"One Nation. One Learning Platform.",searchPh:"Search exam, state, year, topic… e.g. SSC CGL, Odisha, 2024"},
 hi:{home:"होम",exams:"परीक्षाएँ",papers:"पिछले प्रश्न-पत्र",mock:"मॉक टेस्ट",study:"अध्ययन सामग्री",ca:"करेंट अफेयर्स",quiz:"डेली क्विज़",saved:"सेव्ड",profile:"प्रोफ़ाइल",tag:"एक राष्ट्र। एक शिक्षण मंच।",searchPh:"परीक्षा, राज्य, वर्ष, विषय खोजें… जैसे SSC CGL, ओडिशा, 2024"},
 od:{home:"ହୋମ",exams:"ପରୀକ୍ଷା",papers:"ପୁରୁଣା ପ୍ରଶ୍ନପତ୍ର",mock:"ମକ୍ ଟେଷ୍ଟ",study:"ଅଧ୍ୟୟନ ସାମଗ୍ରୀ",ca:"ସାମ୍ପ୍ରତିକ ଘଟଣା",quiz:"ଦୈନିକ କୁଇଜ୍",saved:"ସେଭ୍ କରାଯାଇଥିବା",profile:"ପ୍ରୋଫାଇଲ୍",tag:"ଗୋଟିଏ ରାଷ୍ଟ୍ର। ଗୋଟିଏ ଶିକ୍ଷା ମଞ୍ଚ।",searchPh:"ପରୀକ୍ଷା, ରାଜ୍ୟ, ବର୍ଷ, ବିଷୟ ଖୋଜନ୍ତୁ…"}};
let LANG=["en","hi","od"].includes(store("ep_lang"))?store("ep_lang"):"en";
const T=k=>(I18N[LANG]&&I18N[LANG][k])||I18N.en[k]||k;
function applyLang(){$$("[data-i18n]").forEach(el=>{el.textContent=T(el.getAttribute("data-i18n"))});$$("[data-i18n-ph]").forEach(el=>{el.placeholder=T(el.getAttribute("data-i18n-ph"))});const ls=$("#langsel");if(ls)ls.value=LANG}

/* ---------- header: theme, language, mobile menu ---------- */
const _themeBtn=$("#themeBtn");
if(_themeBtn)_themeBtn.addEventListener("click",()=>{const d=document.documentElement;const dark=d.getAttribute("data-theme")==="dark";d.setAttribute("data-theme",dark?"light":"dark");store("ep_theme",dark?"light":"dark");_themeBtn.textContent=dark?"🌙":"☀️"});
(function(){const th=store("ep_theme");if(th){document.documentElement.setAttribute("data-theme",th);if(_themeBtn)_themeBtn.textContent=th==="dark"?"☀️":"🌙"}})();
const _langsel=$("#langsel");
if(_langsel)_langsel.addEventListener("change",e=>{LANG=e.target.value;store("ep_lang",LANG);applyLang();toast(LANG==="en"?"Language: English":LANG==="hi"?"Language: Hindi":"Language: Odia")});
const _menuBtn=$("#menuBtn"), _mobileNav=$("#mobileNav");
if(_menuBtn&&_mobileNav){_menuBtn.addEventListener("click",()=>_mobileNav.classList.toggle("open"));_mobileNav.addEventListener("click",e=>{if(e.target.tagName==="A")_mobileNav.classList.remove("open")})}
applyLang();

/* ---------- countdown (home) ---------- */
(function(){const el=$("#cd-d");if(!el)return;const target=new Date("2026-11-30T09:00:00+05:30").getTime();const tick=()=>{let d=target-Date.now();if(d<0)d=0;$("#cd-d").textContent=Math.floor(d/86400000);$("#cd-h").textContent=String(Math.floor(d/3600000)%24).padStart(2,"0");$("#cd-m").textContent=String(Math.floor(d/60000)%60).padStart(2,"0");$("#cd-s").textContent=String(Math.floor(d/1000)%60).padStart(2,"0")};tick();setInterval(tick,1000)})();

/* ---------- search page ---------- */
function searchAll(q){q=q.toLowerCase();const ex=EP.exams.filter(e=>(e[2]+" "+e[4]+" "+e[5]+" "+e[8].join(" ")).toLowerCase().includes(q));const st=EP.states.filter(s=>(s.name+" "+s.exams.join(" ")).toLowerCase().includes(q));const qs=EP.questions.filter(x=>(x.q+" "+x.t).toLowerCase().includes(q));return{ex,st,qs}}
(function(){const box=$("#searchResults");if(!box)return;const q=new URLSearchParams(location.search).get("q")||"";const inp=$("#searchInput");if(inp)inp.value=q;if(!q.trim())return;const r=searchAll(q);
 box.innerHTML=`${r.ex.length?`<h3 style="margin:14px 0 8px">Exams (${r.ex.length})</h3><div class="grid g3">${r.ex.map(e=>`<div class="card cat-card" onclick="location.href='/exams/${e[0]}'"><h3>${esc(e[2])}</h3><p>${esc(e[5])} • ${esc(e[7])}</p><p class="small" style="margin-top:6px">Years: ${e[8].join(", ")}</p></div>`).join("")}</div>`:""}
 ${r.st.length?`<h3 style="margin:18px 0 8px">States (${r.st.length})</h3><div class="grid g3">${r.st.map(s=>`<div class="card cat-card" onclick="location.href='/states/${slug(s.name)}'"><h3>${esc(s.name)}</h3><p>${esc(s.exams.join(" • "))}</p></div>`).join("")}</div>`:""}
 ${r.qs.length?`<h3 style="margin:18px 0 8px">Practice questions (${r.qs.length})</h3><div class="card">${r.qs.slice(0,5).map(x=>`<p style="padding:8px 0;border-bottom:1px solid var(--border)">${esc(x.q)}</p>`).join("")}</div>`:""}
 ${!r.ex.length&&!r.st.length&&!r.qs.length?`<div class="card"><p>Nothing found. Try: “SSC”, “Odisha”, “2024”, “Banking”.</p></div>`:""}`})();

/* ---------- exams directory: category filter ---------- */
(function(){const grid=$("#examGrid");if(!grid)return;const pills=$$("[data-cat-filter]");const cat=new URLSearchParams(location.search).get("cat")||"all";
 const apply=c=>{pills.forEach(p=>p.classList.toggle("active",p.getAttribute("data-cat-filter")===c));$$(".exam-card").forEach(card=>{card.style.display=(c==="all"||card.getAttribute("data-cat")===c)?"":"none"})};
 pills.forEach(p=>p.addEventListener("click",()=>apply(p.getAttribute("data-cat-filter"))));apply(cat)})();

/* ---------- states page: region filter ---------- */
(function(){const grid=$("#stateGrid");if(!grid)return;const pills=$$("[data-region-filter]");
 const apply=r=>{pills.forEach(p=>p.classList.toggle("active",p.getAttribute("data-region-filter")===r));$$("#stateGrid .card").forEach(card=>{card.style.display=(r==="All"||card.getAttribute("data-region")===r)?"":"none"})};
 pills.forEach(p=>p.addEventListener("click",()=>apply(p.getAttribute("data-region-filter"))))})();

/* ---------- exam page: year/stage pills + paper rows ---------- */
function paperRows(e,y,sg){const st=examStatus(e[0]);const p=portalOf(e);const key=t=>`${e[0]}|${y}|${sg}|${t}`;const isSaved=k=>savedPapers().some(x=>x.key===k);
 const isRRB=p&&p.url.indexOf("rrbapply")>=0; /* RRB publishes answer keys/response sheets, not complete papers */
 const offBtn=p?`<a class="btn sm" href="${p.url}" target="_blank" rel="noopener">${isRRB?"Official Portal ↗":"Official Archive ↗"}</a>`:`<button class="btn sm" onclick="requestPaper('${e[0]}',${y},'${esc(sg)}','Question Paper')">Request Paper</button>`;
 const keyBtn=st==="official"&&p?`<a class="btn sm ghost" href="${p.url}" target="_blank" rel="noopener">${isRRB?"Official Portal ↗":"Official Key ↗"}</a>`:`<button class="btn sm ghost" onclick="requestPaper('${e[0]}',${y},'${esc(sg)}','Answer Key')">Request Key</button>`;
 const badge=isRRB?'<span class="badge b-part">◐ Answer key on portal</span>':st==="official"?'<span class="badge b-off">✓ Official</span>':p?'<span class="badge b-part">◐ Check on portal</span>':'<span class="badge b-none">Not available yet</span>';
 return `<tr><td><b>${esc(e[2])} ${y} — ${esc(sg)}</b><br><span class="small">Question Paper • Shift/Set as per official archive</span></td><td>${badge}</td><td style="white-space:nowrap">${offBtn} <button class="btn sm ${isSaved(key("paper"))?"green":"ghost"}" data-save-paper="${esc(key("paper"))}" data-save-label="${esc(e[2])} ${y} ${esc(sg)} Paper">${isSaved(key("paper"))?"✓ Saved":"💾 Save"}</button></td></tr>
 <tr><td><b>Answer Key — ${esc(sg)}</b><br><span class="small">Official key, wherever released</span></td><td>${badge}</td><td style="white-space:nowrap">${keyBtn}</td></tr>
 <tr><td><b>Solution &amp; Practice — ${esc(sg)}</b><br><span class="small">ExamPath original practice questions + explanations</span></td><td><span class="badge b-info">✍️ Practice</span></td><td><a class="btn sm purple" href="/practice?subject=all">Practice →</a></td></tr>`}
(function(){const sec=$("[data-exam]");if(!sec)return;const e=examById(sec.getAttribute("data-exam"));if(!e)return;let y=e[8][0], sg=e[9][0];
 const renderRows=()=>{const tb=$("#paperRows");if(tb)tb.innerHTML=paperRows(e,y,sg);const py=$("#paperYear");if(py)py.textContent=y};
 $$("#yearPills [data-year]").forEach(b=>b.addEventListener("click",()=>{y=parseInt(b.getAttribute("data-year"));$$("#yearPills [data-year]").forEach(x=>x.classList.toggle("active",x===b));renderRows()}));
 $$("#stagePills [data-stage]").forEach(b=>b.addEventListener("click",()=>{sg=b.getAttribute("data-stage");$$("#stagePills [data-stage]").forEach(x=>x.classList.toggle("active",x===b));renderRows()}))})();
document.addEventListener("click",e=>{const btn=e.target.closest("[data-save-paper]");if(!btn)return;const key=btn.getAttribute("data-save-paper"),label=btn.getAttribute("data-save-label");toggleSavePaper(key,label);const saved=savedPapers().some(x=>x.key===key);btn.textContent=saved?"✓ Saved":"💾 Save";btn.classList.toggle("green",saved);btn.classList.toggle("ghost",!saved)});

/* ---------- PDF viewer ---------- */
function openViewer(){openModal(`<h3>📄 ExamPath Original Practice Paper</h3><p class="small">20 original practice questions • <b>NOT an official PYQ</b> • Source: ExamPath India (original)</p>
 <div class="toolbar"><button class="btn sm" onclick="zoomViewer(1)">🔍+ Zoom In</button><button class="btn sm" onclick="zoomViewer(-1)">🔍− Zoom Out</button><button class="btn sm" onclick="fsViewer()">⛶ Full Screen</button><a class="btn sm green" href="/assets/sample-practice-paper.pdf" download>⬇️ Download PDF</a><button class="btn sm ghost" onclick="toggleSavePaper('sample|practice|paper','ExamPath Sample Practice Paper');closeModal()">💾 Save to Library</button></div>
 <div class="viewer" id="viewerBox"><iframe src="/assets/sample-practice-paper.pdf" title="Sample practice paper PDF"></iframe></div>
 <p class="small" style="margin-top:10px">For official papers, the <b>Official Archive</b> button on the exam page opens the conducting body's own site — that is the real source.</p>
 <button class="btn block" style="margin-top:12px" onclick="closeModal()">Close</button>`,true)}
let _zoom=1;function zoomViewer(d){_zoom=Math.min(1.8,Math.max(.6,_zoom+d*.2));const v=$("#viewerBox");if(v)v.style.zoom=_zoom}
function fsViewer(){const v=$("#viewerBox");if(v&&v.requestFullscreen)v.requestFullscreen()}

/* ---------- mock tests ---------- */
const MOCKS=[
 {id:"ssc",name:"SSC CGL Style Mock",desc:"25 Q • 30 min • +1 / −0.25 • Quant, Reasoning, English, GK",mins:30,neg:0.25,mix:{quant:7,reasoning:7,english:6,gk:5}},
 {id:"rrb",name:"RRB NTPC Style Mock",desc:"25 Q • 30 min • +1 / −0.33 • Maths, Reasoning, GK, Science",mins:30,neg:0.33,mix:{quant:7,reasoning:6,gk:7,science:5}},
 {id:"bank",name:"Banking (IBPS PO) Style Mock",desc:"25 Q • 30 min • +1 / −0.25 • Quant, Reasoning, English, GK",mins:30,neg:0.25,mix:{quant:8,reasoning:8,english:6,gk:3}},
];
function mockQuestions(def){const seed=[...def.id].reduce((s,c)=>s+c.charCodeAt(0),7);let out=[];Object.entries(def.mix).forEach(([s,n],i)=>{out=out.concat(seededShuffle(EP.questions.filter(q=>q.s===s),seed+i*13).slice(0,n))});return seededShuffle(out,seed+99)}
(function(){const box=$("#historyBox");if(!box)return;const h=history();
 box.innerHTML=h.length?`<div class="card tbl-wrap"><table><tr><th>Date</th><th>Mock</th><th>Score</th><th>Accuracy</th><th>Time</th></tr>${h.slice().reverse().map(x=>`<tr><td>${esc(x.date)}</td><td>${esc(x.mock)}</td><td><b>${x.score} / ${x.total}</b></td><td>${x.acc}%</td><td>${esc(x.time)}</td></tr>`).join("")}</table></div>`:`<div class="card"><p>No test taken yet. Start a mock above — the result will be saved here (on this device, no login).</p></div>`})();
let MK=null;
(function(){const box=$("#mockBox");if(!box)return;const id=new URLSearchParams(location.search).get("mock")||"ssc";const def=MOCKS.find(m=>m.id===id);if(!def){box.innerHTML=`<div class="card">Mock not found. <a href="/mock">Back →</a></div>`;return}
 const saved=store("ep_mock_current");
 if(saved&&saved.mockId===id&&saved.endTs>Date.now()){MK={def,qs:saved.qs.map(qid=>EP.questions.find(q=>q.id===qid)),idx:saved.idx||0,ans:saved.ans||{},marked:saved.marked||{},endTs:saved.endTs}}
 else{MK={def,qs:mockQuestions(def),idx:0,ans:{},marked:{},endTs:Date.now()+def.mins*60000}}
 drawMock();clearInterval(MK._t);MK._t=setInterval(()=>{if(!MK)return;const left=MK.endTs-Date.now();const el=$("#mkTimer");if(el){if(left<=0){clearInterval(MK._t);submitMock(true)}else{const m=Math.floor(left/60000),s=Math.floor(left/1000)%60;el.textContent=String(m).padStart(2,"0")+":"+String(s).padStart(2,"0")}}} ,1000)})();
function saveMock(){if(!MK)return;store("ep_mock_current",{mockId:MK.def.id,qs:MK.qs.map(q=>q.id),idx:MK.idx,ans:MK.ans,marked:MK.marked,endTs:MK.endTs})}
function drawMock(){const box=$("#mockBox");if(!box||!MK)return;const q=MK.qs[MK.idx];const total=MK.qs.length;const left=MK.endTs-Date.now();const mm=String(Math.max(0,Math.floor(left/60000))).padStart(2,"0"),ss=String(Math.max(0,Math.floor(left/1000)%60)).padStart(2,"0");
 box.innerHTML=`<div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><div><h2 style="font-size:20px">${esc(MK.def.name)}</h2><p class="small">Question ${MK.idx+1} of ${total} • +1 / −${MK.def.neg} • Answers are autosaved</p></div><div class="timer" id="mkTimer">${mm}:${ss}</div></div>
 <div class="progress" style="margin:12px 0"><i style="width:${((MK.idx+1)/total*100)}%"></i></div>
 <div class="grid" style="grid-template-columns:1fr 230px;gap:14px"><div class="qcard">
 <p><span class="badge b-info">${esc(q.s.toUpperCase())}</span> <span class="small">${esc(q.t)} • ${esc(q.d)}</span></p>
 <h3 style="margin:12px 0;font-size:18px">Q${MK.idx+1}. ${esc(q.q)}</h3>
 ${q.o.map((o,i)=>`<button class="opt ${MK.ans[MK.idx]===i?"sel":""}" onclick="answerMock(${i})">${String.fromCharCode(65+i)}. ${esc(o)}</button>`).join("")}
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px">
 <button class="btn ghost sm" onclick="prevQ()" ${MK.idx===0?"disabled":""}>← Previous</button>
 <button class="btn sm" onclick="nextQ()">${MK.idx===total-1?"Review →":"Next →"}</button>
 <button class="btn purple sm" onclick="markQ()">${MK.marked[MK.idx]?"★ Marked":"☆ Mark for Review"}</button>
 <button class="btn green sm" onclick="submitMock(false)">Submit Test</button></div></div>
 <div class="card"><h3>Question Palette</h3><div class="palette" style="margin-top:10px">${MK.qs.map((_,i)=>`<button class="pal ${MK.ans[i]!==undefined?"ans":""} ${MK.marked[i]?"mark":""} ${i===MK.idx?"cur":""}" onclick="gotoQ(${i})">${i+1}</button>`).join("")}</div>
 <p class="small" style="margin-top:10px">🟢 Answered • 🟣 Marked • 🟠 Current<br>Answered: ${Object.keys(MK.ans).length} / ${total}</p>
 <button class="btn red block" style="margin-top:10px" onclick="submitMock(false)">Submit Test</button></div></div>`;
 saveMock()}
function answerMock(i){MK.ans[MK.idx]=i;drawMock()}
function nextQ(){if(MK.idx<MK.qs.length-1){MK.idx++;drawMock()}}
function prevQ(){if(MK.idx>0){MK.idx--;drawMock()}}
function gotoQ(i){MK.idx=i;drawMock()}
function markQ(){MK.marked[MK.idx]=!MK.marked[MK.idx];drawMock()}
function submitMock(auto){if(!MK)return;clearInterval(MK._t);const total=MK.qs.length;let correct=0,wrong=0,un=0;const review=MK.qs.map((q,i)=>{const a=MK.ans[i];if(a===undefined){un++;return{q,a,ok:false}}if(a===q.a){correct++;return{q,a,ok:true}}wrong++;return{q,a,ok:false}});
 const score=Math.max(0,correct*1-wrong*MK.def.neg);const scoreStr=(Math.round(score*100)/100);const acc=total?Math.round(correct/total*100):0;const minsUsed=Math.round((MK.def.mins*60000-(MK.endTs-Date.now()))/60000);
 const h=history();h.push({mock:MK.def.name,score:scoreStr,total,acc,date:new Date().toISOString().slice(0,10),time:minsUsed+" min"});store("ep_history",h);
 const w=wrongIds();review.forEach(r=>{if(!r.ok&&r.a!==undefined&&!w.includes(r.q.id))w.push(r.q.id)});store("ep_wrong",w);
 store("ep_mock_current",null);markActivity();
 const box=$("#mockBox");const wrongQs=review.filter(r=>!r.ok);
 box.innerHTML=`<div class="card" style="text-align:center"><h2>${auto?"⏰ Time’s up — auto-submitted!":"✅ Test Submitted!"}</h2><p style="font-size:20px;margin:10px 0">Score: <b>${scoreStr} / ${total}</b> • Accuracy: <b>${acc}%</b></p>
 <div class="grid g4" style="margin:14px 0"><div class="stat"><b style="color:var(--green)">${correct}</b><span>Correct</span></div><div class="stat"><b style="color:var(--red)">${wrong}</b><span>Wrong</span></div><div class="stat"><b>${un}</b><span>Unattempted</span></div><div class="stat"><b>${minsUsed} min</b><span>Time used</span></div></div>
 <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap"><a class="btn" href="/mock-test?mock=${MK.def.id}">🔄 Retry Mock</a><a class="btn ghost" href="/mock">All Mocks</a><a class="btn purple" href="/saved">See Wrong Answers</a></div></div>
 <h3 style="margin:20px 0 10px">📝 Answer Review (wrong / unattempted)</h3>
 ${wrongQs.length?wrongQs.map(r=>`<div class="qcard" style="margin-bottom:12px"><p><span class="badge ${r.a===undefined?"b-grey":"b-none"}">${r.a===undefined?"Unattempted":"Wrong"}</span> <span class="small">${esc(r.q.s)} • ${esc(r.q.t)}</span></p><h3 style="margin:10px 0">${esc(r.q.q)}</h3>${r.q.o.map((o,i)=>`<div class="opt ${i===r.q.a?"right":i===r.a?"wrong":""}" style="cursor:default">${String.fromCharCode(65+i)}. ${esc(o)} ${i===r.q.a?"✓ Correct":""}</div>`).join("")}<p style="margin-top:8px"><b>Explanation:</b> ${esc(r.q.e)}</p></div>`).join(""):`<div class="card"><p>🎉 Perfect! All correct — no wrong answers.</p></div>`}`;
 MK=null;window.scrollTo(0,0)}

/* ---------- practice ---------- */
let PR=null;
(function(){const box=$("#pracBox");if(!box)return;const subj=new URLSearchParams(location.search).get("subject")||"all";
 $$("[data-subject-pill]").forEach(p=>p.classList.toggle("active",p.getAttribute("data-subject-pill")===subj));
 let list=subj==="all"?EP.questions:subj==="wrong"?EP.questions.filter(q=>wrongIds().includes(q.id)):EP.questions.filter(q=>q.s===subj);
 if(!list.length){box.innerHTML=`<div class="card"><p>There are no questions in this category yet. ${subj==="wrong"?"Take a mock first — your wrong answers will appear here.":""}</p><a class="btn" href="/practice?subject=all">All Practice →</a></div>`;return}
 const seed=[...subj].reduce((s,c)=>s+c.charCodeAt(0),11);list=seededShuffle(list,seed);
 PR={list,idx:0,checked:false,sel:null,correct:0,attempted:0};drawPractice()})();
function drawPractice(){const box=$("#pracBox");if(!box||!PR)return;const q=PR.list[PR.idx];const total=PR.list.length;const bm=bookmarks().includes(q.id);
 box.innerHTML=`<div class="qcard"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px"><p><span class="badge b-info">${esc(q.s.toUpperCase())}</span> <span class="small">${esc(q.t)} • ${esc(q.d)} • Q ${PR.idx+1}/${total}</span></p><button class="btn sm ${bm?"green":"ghost"}" onclick="toggleBookmark('${q.id}');drawPractice()">${bm?"★ Bookmarked":"☆ Bookmark"}</button></div>
 <div class="progress" style="margin:12px 0"><i style="width:${((PR.idx+1)/total*100)}%"></i></div>
 <h3 style="font-size:18px;margin:10px 0">${esc(q.q)}</h3>
 ${q.o.map((o,i)=>{let cls="";if(PR.checked){if(i===q.a)cls="right";else if(i===PR.sel)cls="wrong"}else if(PR.sel===i)cls="sel";return `<button class="opt ${cls}" onclick="pickPractice(${i})" ${PR.checked?"disabled":""}>${String.fromCharCode(65+i)}. ${esc(o)}</button>`}).join("")}
 ${PR.checked?`<div class="notice"><b>${PR.sel===q.a?"✅ Correct!":"❌ Wrong — correct answer: "+String.fromCharCode(65+q.a)}</b><br>${esc(q.e)}</div>`:""}
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
 ${!PR.checked?`<button class="btn" onclick="checkPractice()" ${PR.sel===null?"disabled":""}>Check Answer</button>`:`<button class="btn" onclick="nextPractice()">Next Question →</button>`}
 <span class="small" style="align-self:center">Session: ${PR.correct}/${PR.attempted} correct</span></div></div>`}
function pickPractice(i){PR.sel=i;drawPractice()}
function checkPractice(){if(PR.sel===null)return;PR.checked=true;PR.attempted++;const q=PR.list[PR.idx];if(PR.sel===q.a)PR.correct++;const st=store("ep_practice")||{attempted:0,correct:0};st.attempted++;if(PR.sel===q.a)st.correct++;store("ep_practice",st);if(PR.sel!==q.a){const w=wrongIds();if(!w.includes(q.id)){w.push(q.id);store("ep_wrong",w)}}markActivity();drawPractice()}
function nextPractice(){PR.idx=(PR.idx+1)%PR.list.length;PR.checked=false;PR.sel=null;drawPractice()}

/* ---------- daily quiz ---------- */
let DQ=null;
(function(){const box=$("#quizBox");if(!box)return;const d=new Date();const seed=d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate();DQ={list:seededShuffle(EP.questions,seed).slice(0,10),idx:0,checked:false,sel:null,score:0};drawQuiz()})();
function drawQuiz(){const box=$("#quizBox");if(!box||!DQ)return;if(DQ.idx>=DQ.list.length){const prev=store("ep_daily")||{};const key=new Date().toISOString().slice(0,10);prev[key]=DQ.score;store("ep_daily",prev);markActivity();box.innerHTML=`<div class="card" style="text-align:center"><h2>🎉 Quiz Complete!</h2><p style="font-size:22px;margin:12px 0">Score: <b>${DQ.score} / 10</b></p><p>${DQ.score>=8?"Excellent! 🔥":DQ.score>=5?"Good — daily practice will improve it further.":"No problem — read the notes and try again tomorrow."}</p><a class="btn" style="margin-top:12px" href="/practice?subject=all">Practise →</a> <a class="btn ghost" style="margin-top:12px" href="/ca">Current Affairs →</a></div>`;return}
 const q=DQ.list[DQ.idx];
 box.innerHTML=`<div class="qcard"><p><span class="badge b-info">${esc(q.s.toUpperCase())}</span> <span class="small">Q ${DQ.idx+1}/10 • Score: ${DQ.score}</span></p>
 <div class="progress" style="margin:12px 0"><i style="width:${(DQ.idx/10*100)}%"></i></div>
 <h3 style="font-size:18px;margin:10px 0">${esc(q.q)}</h3>
 ${q.o.map((o,i)=>{let cls="";if(DQ.checked){if(i===q.a)cls="right";else if(i===DQ.sel)cls="wrong"}else if(DQ.sel===i)cls="sel";return `<button class="opt ${cls}" onclick="pickQuiz(${i})" ${DQ.checked?"disabled":""}>${String.fromCharCode(65+i)}. ${esc(o)}</button>`}).join("")}
 ${DQ.checked?`<div class="notice"><b>${DQ.sel===q.a?"✅ Correct!":"❌ Correct answer: "+String.fromCharCode(65+q.a)}</b><br>${esc(q.e)}</div>`:""}
 <div style="margin-top:12px">${!DQ.checked?`<button class="btn" onclick="checkQuiz()" ${DQ.sel===null?"disabled":""}>Check Answer</button>`:`<button class="btn" onclick="nextQuiz()">Next →</button>`}</div></div>`}
function pickQuiz(i){DQ.sel=i;drawQuiz()}
function checkQuiz(){if(DQ.sel===null)return;DQ.checked=true;if(DQ.sel===DQ.list[DQ.idx].a)DQ.score++;drawQuiz()}
function nextQuiz(){DQ.idx++;DQ.checked=false;DQ.sel=null;drawQuiz()}

/* ---------- planner ---------- */
function renderPlanner(){const list=$("#taskList");if(!list)return;const plan=store("ep_plan")||{goal:20,tasks:[]};const st=store("ep_streak")||{count:0,last:null};const done=plan.tasks.filter(t=>t.done).length;
 const sb=$("#streakBox");if(sb)sb.textContent=`🔥 ${st.count} days`;const tc=$("#taskCount");if(tc)tc.textContent=`${done}/${plan.tasks.length}`;const gb=$("#goalBox");if(gb)gb.textContent=plan.goal;
 list.innerHTML=plan.tasks.length?plan.tasks.map((t,i)=>`<div class="list-item"><input type="checkbox" style="width:22px;height:22px;accent-color:var(--green)" ${t.done?"checked":""} onchange="toggleTask(${i})"><span style="${t.done?"text-decoration:line-through;color:var(--muted)":""};flex:1">${esc(t.t)}</span><button class="btn sm red" onclick="delTask(${i})">✕</button></div>`).join(""):`<p class="small">No tasks yet. Add one above.</p>`}
function saveGoal(){const v=parseInt($("#goalIn").value)||20;const p=store("ep_plan")||{goal:20,tasks:[]};p.goal=Math.min(200,Math.max(5,v));store("ep_plan",p);toast("Daily goal saved ✓");renderPlanner()}
function addTask(){const v=$("#taskIn").value.trim();if(!v)return toast("Write a task first");const p=store("ep_plan")||{goal:20,tasks:[]};p.tasks.push({t:v,done:false});store("ep_plan",p);$("#taskIn").value="";renderPlanner()}
function toggleTask(i){const p=store("ep_plan");p.tasks[i].done=!p.tasks[i].done;store("ep_plan",p);if(p.tasks[i].done)markActivity();renderPlanner()}
function delTask(i){const p=store("ep_plan");p.tasks.splice(i,1);store("ep_plan",p);renderPlanner()}
renderPlanner();

/* ---------- saved page ---------- */
function renderSaved(){const box=$("#savedBox");if(!box)return;const sp=savedPapers(),bm=bookmarks(),wr=wrongIds(),rq=store("ep_requests")||[];
 const qById=id=>EP.questions.find(q=>q.id===id);
 box.innerHTML=`
 <h3 style="margin:12px 0 8px">💾 Saved Papers (${sp.length})</h3>
 ${sp.length?`<div class="card">${sp.map((s,i)=>`<div class="list-item"><span style="flex:1"><b>${esc(s.label)}</b><br><span class="small">Saved: ${esc(s.at)}</span></span><button class="btn sm red" onclick="removeSaved(${i})">Remove</button></div>`).join("")}</div>`:`<div class="card"><p>Nothing saved yet. Tap <b>💾 Save</b> on any exam page.</p></div>`}
 <h3 style="margin:18px 0 8px">⭐ Bookmarked Questions (${bm.length})</h3>
 ${bm.length?`<div class="card">${bm.map(id=>{const q=qById(id);return q?`<div class="list-item"><span style="flex:1">${esc(q.q)}<br><span class="small">Answer: ${String.fromCharCode(65+q.a)}. ${esc(q.o[q.a])} • ${esc(q.s)}</span></span><button class="btn sm ghost" onclick="toggleBookmark('${id}');renderSaved()">Remove</button></div>`:""}).join("")}</div>`:`<div class="card"><p>No bookmarks yet. Tap ☆ in Practice to save one.</p></div>`}
 <h3 style="margin:18px 0 8px">❌ Wrong Answers — Revision (${wr.length})</h3>
 ${wr.length?`<div class="card"><p>Practise the questions you got wrong again:</p><a class="btn orange" style="margin-top:10px" href="/practice?subject=wrong">🔁 Wrong Answers Practice →</a><p class="small" style="margin-top:8px">${wr.slice(0,5).map(id=>{const q=qById(id);return q?esc(q.q):""}).filter(Boolean).join("<br>")}</p></div>`:`<div class="card"><p>No wrong answers yet — take a mock or practise to see them here.</p></div>`}
 <h3 style="margin:18px 0 8px">📩 Paper Requests (${rq.length})</h3>
 ${rq.length?`<div class="card">${rq.map(r=>`<p style="padding:6px 0;border-bottom:1px solid var(--border)">${esc(r.exam)} • ${r.year} • ${esc(r.stage)} • ${esc(r.type)} — <span class="small">${esc(r.at)}</span></p>`).join("")}</div>`:`<div class="card"><p>No requests yet.</p></div>`}
 <button class="btn red" style="margin-top:18px" onclick="askClearAll()">🗑️ Clear All My Data</button>`}
function removeSaved(i){const s=savedPapers();s.splice(i,1);store("ep_saved",s);renderSaved()}
function askClearAll(){openModal(`<h3>🗑️ Clear all my data?</h3><p>This deletes your saved papers, bookmarks, wrong answers, paper requests, test history and practice progress from this device. This cannot be undone.</p><div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap"><button class="btn red" onclick="clearAllData()">Yes, delete everything</button><button class="btn ghost" onclick="closeModal()">Cancel</button></div>`)}
function clearAllData(){["ep_saved","ep_bookmarks","ep_wrong","ep_requests","ep_history","ep_daily","ep_practice","ep_plan","ep_streak","ep_mock_current"].forEach(k=>localStorage.removeItem(k));closeModal();toast("All data cleared");renderSaved()}
renderSaved();

/* ---------- profile page ---------- */
(function(){const box=$("#profileBox");if(!box)return;const h=history();const pr=store("ep_practice")||{attempted:0,correct:0};const st=store("ep_streak")||{count:0};const acc=h.length?Math.round(h.reduce((s,x)=>s+x.acc,0)/h.length):(pr.attempted?Math.round(pr.correct/pr.attempted*100):0);
 const weak={};wrongIds().forEach(id=>{const q=EP.questions.find(x=>x.id===id);if(q)weak[q.s]=(weak[q.s]||0)+1});const weakList=Object.entries(weak).sort((a,b)=>b[1]-a[1]);
 box.innerHTML=`<div class="grid g4"><div class="stat"><b>${h.length}</b><span>Mock tests</span></div><div class="stat"><b>${acc}%</b><span>Avg accuracy</span></div><div class="stat"><b>${pr.attempted}</b><span>Practice Qs</span></div><div class="stat"><b>🔥 ${st.count}</b><span>Day streak</span></div></div>
 <div class="grid g2" style="margin-top:14px">
 <div class="card"><h3>🎯 Weak Topics</h3>${weakList.length?weakList.map(([s,n])=>`<p style="padding:6px 0;border-bottom:1px solid var(--border)">${esc(s.toUpperCase())} — ${n} wrong <a href="/practice?subject=${s}">Practice →</a></p>`).join(""):`<p class="small">No weak topics yet — take a mock and the analysis will appear here.</p>`}</div>
 <div class="card"><h3>📊 Test History</h3>${h.length?h.slice().reverse().slice(0,5).map(x=>`<p style="padding:6px 0;border-bottom:1px solid var(--border)">${esc(x.mock)} — <b>${x.score}/${x.total}</b> (${x.acc}%) • ${esc(x.date)}</p>`).join(""):`<p class="small">No test taken yet.</p>`}<a class="btn" style="margin-top:10px" href="/mock">Take a Mock →</a></div></div>
 <div class="card" style="margin-top:14px"><h3>💾 My Data</h3><p class="small">Saved papers: ${savedPapers().length} • Bookmarks: ${bookmarks().length} • Wrong answers: ${wrongIds().length}</p><div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap"><button class="btn ghost" onclick="exportData()">⬇️ Export My Data (JSON)</button><a class="btn ghost" href="/saved">My Library →</a></div></div>`})();
function exportData(){const data={saved:savedPapers(),bookmarks:bookmarks(),wrong:wrongIds(),history:history(),practice:store("ep_practice"),plan:store("ep_plan")};const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="exampath-my-data.json";a.click();toast("Data downloaded ✓")}

function shareApp(){const url="https://exampath-india.pages.dev/";const title="ExamPath India";const text="ExamPath India — free exam papers, mock tests, notes and current affairs. Get the app here:";if(navigator.share){navigator.share({title:title,text:text,url:url}).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){toast("Website link copied ✓ — share it, anyone opening it can download the app")})}else{toast(url)}}
if(window.Capacitor){document.querySelectorAll(".app-banner").forEach(function(b){b.style.display="none"})}
