p = '/mnt/user-data/outputs/trainer-app.html'
s = open(p, encoding='utf-8').read()
av = open('/home/claude/avatars.js', encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)

# 1) embed the avatar images (same data script as the bodies)
rep("</script>\n<script>\nconst $ = ", av + "</script>\n<script>\nconst $ = ")

# 2) use them as the male / female symbols
rep("const MARS = '\\u{1F468}', VENUS = '\\u{1F469}';",
    "const MARS = `<img src='${AVATAR.Male}' alt=''>`, VENUS = `<img src='${AVATAR.Female}' alt=''>`;")

# 3) attribution
rep("Body figures from MuscleMap (MIT license).</footer>",
    "Body figures from MuscleMap (MIT license). Avatars: <a href='https://www.vecteezy.com' target='_blank' rel='noopener'>Vecteezy.com</a>.</footer>")

# 4) sets / reps / move buttons on one line
rep("</label></div>\n      <div class='r3'>", "</label>\n        <div class='r3'>")
rep(r"title='Remove'>\u2715</button></div>" + "\n    </div>`;", r"title='Remove'>\u2715</button></div></div>" + "\n    </div>`;")

# 5) CSS: compact widths, avatar images, pressed state
css = r"""
.stepper{max-width:160px}
.stepper button{width:40px}
.mini.sets{width:128px}
.mini.reps{width:80px}
.r3 button{min-width:40px;padding:0}
.dateRow input{flex:1;min-width:0}
.sx button{padding:0;min-width:52px}
.sx button img{width:36px;height:36px;border-radius:50%;display:block}
.seg.sx button[aria-pressed='true']{background:var(--soft);color:inherit;border-color:var(--accent);box-shadow:inset 0 0 0 2px var(--accent)}
.sx button[aria-pressed='false'] img{opacity:.5;filter:grayscale(.5)}
.av{padding:3px;overflow:hidden}
.av[data-st='']{background:var(--line)}
.av img{width:100%;height:100%;border-radius:50%;display:block}
[hidden]{display:none!important}"""
rep("\n[hidden]{display:none!important}", css)

open(p, 'w', encoding='utf-8').write(s)
print('patched', len(s))
