"""Build the public page (index.html) from the design source (src/frontier-1905.html).

The public build:
- wraps the page in a full HTML document with a viewport tag and sharing metadata
- removes the colour editor (a design-time tool) and keeps the light-quanta branch hidden
- embeds the fonts when src/fonts/*.woff2 exist, so the page needs nothing from outside

Run: python3 build.py
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'src', 'frontier-1905.html'), encoding='utf-8').read()

def cut(s, start, end, keep_end=True):
    a = s.index(start)
    b = s.index(end, a)
    return s[:a] + (s[b:] if keep_end else s[b + len(end):])

# 1. colour editor: markup, toolbar button and script
s = cut(src, '    <form class="cpop clock" id="clock"', '    <div class="focus" id="focus"')
s = re.sub(r'\s*<button id="cOpen".*?</button>', '', s, count=1, flags=re.S)
s = cut(s, '/* ---------- colour editor ---------- */', '/* ---------- connection filter ---------- */')
s = s.replace("try{showBranch=localStorage.getItem('f1905-branch')==='1';}catch(e){}", '')
for probe in ('id="cpop"', 'id="clock"', 'id="cOpen"', 'PASS_HASH'):
    assert probe not in s, probe

# 2. fonts: embed if present
fdir = os.path.join(ROOT, 'src', 'fonts')
FACES = [  # family, file, weight, style
    ('Libre Caslon Text', 'libre-caslon-text.woff2', '400 700', 'normal'),
    ('Libre Caslon Text', 'libre-caslon-text-italic.woff2', '400 700', 'italic'),
    ('IBM Plex Sans Condensed', 'plex-sans-condensed-400.woff2', '400', 'normal'),
    ('IBM Plex Sans Condensed', 'plex-sans-condensed-500.woff2', '500', 'normal'),
    ('IBM Plex Sans Condensed', 'plex-sans-condensed-600.woff2', '600', 'normal'),
    ('IBM Plex Mono', 'plex-mono-400.woff2', '400', 'normal'),
    ('IBM Plex Mono', 'plex-mono-500.woff2', '500', 'normal'),
]
if all(os.path.exists(os.path.join(fdir, f)) for _, f, _, _ in FACES):
    css = ''.join(
        "@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%s;font-style:%s;font-display:swap}\n"
        % (fam, base64.b64encode(open(os.path.join(fdir, f), 'rb').read()).decode(), w, st)
        for fam, f, w, st in FACES)
    s = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\s*', '', s)
    s = s.replace('<style>', '<style>\n' + css, 1)
    print('fonts embedded')
else:
    print('fonts loaded from Google Fonts (src/fonts not found)')

# 3. full document (head.html carries the title and sharing tags)
s = s.replace('<title>Frontier 1905</title>', '', 1)
head_end = s.index('</style>') + len('</style>')
head, body = s[:head_end], s[head_end:]
meta = open(os.path.join(ROOT, 'src', 'head.html'), encoding='utf-8').read()
out = ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + meta + head + '\n</head>\n<body>' + body + '\n</body>\n</html>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(out)
print('index.html', len(out) // 1024, 'KB')
