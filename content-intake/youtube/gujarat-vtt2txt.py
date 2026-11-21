import re, sys

def parse(path):
    cues = []
    cur_t = None
    cur = []
    for line in open(path, encoding='utf-8', errors='ignore'):
        line = line.rstrip('\n')
        m = re.match(r'(\d+:\d\d:\d\d\.\d+) --> ', line)
        if m:
            if cur_t and cur:
                cues.append((cur_t, ' '.join(cur)))
            cur_t = m.group(1)
            cur = []
            continue
        s = line.strip()
        if not s or s.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE')) or re.match(r'^\d+$', s):
            continue
        t = re.sub(r'<[^>]+>', ' ', line)
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            cur.append(t)
    if cur_t and cur:
        cues.append((cur_t, ' '.join(cur)))
    out = []
    for t, x in cues:
        if out and out[-1][1] == x:
            continue
        out.append((t, x))
    return out

def tosec(s):
    p = s.split(':')
    if len(p) == 3:
        h, m, sec = p
    else:
        h = '0'
        m, sec = p
    return int(h) * 3600 + int(m) * 60 + float(sec)

def fmt(sec):
    return f"{int(sec // 60):02d}:{int(sec % 60):02d}"

for path in sys.argv[1:]:
    cues = parse(path)
    print(f"### {path} cues={len(cues)} dur~{fmt(tosec(cues[-1][0])) if cues else '?'}")
    for t, x in cues:
        print(f"[{fmt(tosec(t))}] {x}")
