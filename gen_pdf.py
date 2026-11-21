#!/usr/bin/env python3
"""Generate ExamPath Sample Practice Paper PDF (pure stdlib, no deps).
20 original ExamPath practice questions. Clearly labelled NOT an official PYQ."""
import zlib

QUESTIONS = [
 ("Quantitative Aptitude", [
  ("1. 15% of 240 is: (a) 30 (b) 36 (c) 42 (d) 48  -- Answer: (b) 36",),
  ("2. Simple interest on Rs.12,000 at 8% p.a. for 3 years is:", "    (a) Rs.2,400 (b) Rs.2,880 (c) Rs.3,200 (d) Rs.2,000  -- Answer: (b)"),
  ("3. 72 km/h expressed in m/s is: (a) 18 (b) 20 (c) 24 (d) 25  -- Answer: (b) 20 m/s",),
  ("4. The HCF of 24 and 36 is: (a) 6 (b) 8 (c) 12 (d) 18  -- Answer: (c) 12",),
  ("5. A book bought for Rs.500 is sold for Rs.650. Profit % is:", "    (a) 20% (b) 25% (c) 30% (d) 35%  -- Answer: (c) 30%",),
 ]),
 ("General Intelligence & Reasoning", [
  ("6. Odd one out: Apple, Mango, Banana, Potato -- Answer: Potato (vegetable)",),
  ("7. Series: 2, 4, 8, 16, 32, ?  (a) 48 (b) 56 (c) 64 (d) 96  -- Answer: (c) 64",),
  ("8. If CAT is coded as DBU, DOG is coded as: (a) EPH (b) DPH (c) EOH (d) FOH", "    -- Answer: (a) EPH (each letter +1)",),
  ("9. Book is to Read as Pen is to: (a) Ink (b) Paper (c) Write (d) Draw", "    -- Answer: (c) Write",),
  ("10. 5, 11, 23, 47, ?  (a) 85 (b) 91 (c) 95 (d) 99  -- Answer: (c) 95 (x2+1)",),
 ]),
 ("English Language", [
  ("11. Synonym of 'Brave': (a) Cowardly (b) Courageous (c) Timid (d) Weak", "     -- Answer: (b) Courageous",),
  ("12. Antonym of 'Ancient': (a) Old (b) Modern (c) Antique (d) Historic", "     -- Answer: (b) Modern",),
  ("13. Correctly spelt word: (a) Recieve (b) Receive (c) Riceive (d) Receeve", "     -- Answer: (b) Receive",),
  ("14. Idiom 'To bite the dust' means: (a) To eat dust (b) To be defeated", "     (c) To work hard (d) To hide  -- Answer: (b) To be defeated",),
  ("15. Fill in: She has been working here ___ 2019. (a) for (b) from (c) since (d) by", "     -- Answer: (c) since",),
 ]),
 ("General Awareness", [
  ("16. The Indian Constitution was adopted on: (a) 26 Jan 1950 (b) 26 Nov 1949", "     (c) 15 Aug 1947 (d) 2 Oct 1949  -- Answer: (b) 26 November 1949",),
  ("17. The first President of India was: (a) S. Radhakrishnan", "     (b) Dr. Rajendra Prasad (c) Dr. A.P.J. Abdul Kalam (d) Giani Zail Singh", "     -- Answer: (b) Dr. Rajendra Prasad",),
  ("18. The longest river in India is: (a) Yamuna (b) Godavari (c) Ganga (d) Brahmaputra", "     -- Answer: (c) Ganga",),
  ("19. The Reserve Bank of India was established in: (a) 1935 (b) 1947 (c) 1950 (d) 1969", "     -- Answer: (a) 1935",),
  ("20. The capital of Australia is: (a) Sydney (b) Melbourne (c) Canberra (d) Perth", "     -- Answer: (c) Canberra",),
 ]),
]

def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").replace("Rs.", "Rs.")

lines = []
lines.append("ExamPath India -- Sample Practice Paper")
lines.append("20 Original Practice Questions  |  Time: 30 minutes  |  Each question: 1 mark")
lines.append("IMPORTANT: This is an ORIGINAL ExamPath practice paper.")
lines.append("It is NOT an official previous year question paper (PYQ).")
lines.append("Official papers are linked from their conducting body's website.")
lines.append("")
for sec, qs in QUESTIONS:
    lines.append(sec)
    lines.append("-" * 60)
    for q in qs:
        for part in q:
            lines.append(part)
    lines.append("")

PER_PAGE = 42
pages = [lines[i:i+PER_PAGE] for i in range(0, len(lines), PER_PAGE)]

def content_stream(page_lines, pageno, total):
    out = ["BT /F1 13 Tf 56 760 Td 15 TL"]
    out.append(f"(ExamPath India  |  Sample Practice Paper  |  Page {pageno}/{total}) Tj T*")
    out.append("0.2 0.4 0.8 rg")
    out.append("( ) Tj T*")
    out.append("0 0 0 rg")
    out.append("/F1 11 Tf 12 TL")
    for ln in page_lines:
        if not ln:
            out.append("T*")
        else:
            out.append(f"({esc(ln)}) Tj T*")
    out.append("ET")
    return "\n".join(out).encode("latin-1", "replace")

objects = []
# 1 catalog, 2 pages, then per page: page obj + content obj, font obj last
font_id = 3 + 2 * len(pages)
objs = {}
objs[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
kids = " ".join(f"{3+i*2} 0 R" for i in range(len(pages)))
objs[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode()
for i, pl in enumerate(pages):
    pid = 3 + i * 2
    cid = pid + 1
    stream = content_stream(pl, i + 1, len(pages))
    comp = zlib.compress(stream)
    objs[pid] = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {cid} 0 R >>".encode()
    objs[cid] = b"<< /Length " + str(len(comp)).encode() + b" /Filter /FlateDecode >>\nstream\n" + comp + b"\nendstream"
objs[font_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"

out = bytearray(b"%PDF-1.4\n")
offsets = {}
for oid in sorted(objs):
    offsets[oid] = len(out)
    out += f"{oid} 0 obj\n".encode() + objs[oid] + b"\nendobj\n"
xref_pos = len(out)
n = max(objs) + 1
out += f"xref\n0 {n}\n".encode()
out += b"0000000000 65535 f \n"
for oid in range(1, n):
    out += f"{offsets.get(oid,0):010d} 00000 n \n".encode()
out += f"trailer\n<< /Size {n} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode()

with open("final-deploy/assets/sample-practice-paper.pdf", "wb") as f:
    f.write(out)
print("PDF written:", len(out), "bytes,", len(pages), "pages")
