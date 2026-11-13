p = '/mnt/user-data/outputs/trainer-app.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)

def cut(start_marker, end_marker, new):
    global s
    a = s.index(start_marker); assert s.count(start_marker) == 1, start_marker
    b = s.index(end_marker, a)
    s = s[:a] + new + s[b:]

# ---------- CSS ----------
css = r"""
:root{--ctl:44px}
input:not([type='file']),select,button{min-height:var(--ctl)}
input:not([type='file']),select{height:var(--ctl)}
.tabs button{min-height:36px;height:36px}
.seg button{height:var(--ctl);padding:0 14px}
.ibtn{width:var(--ctl);height:var(--ctl)}
.stepper input,.stepper button{height:var(--ctl)}
.mini input{padding:0 8px}
.mini.reps{width:110px}
.clr .x{min-height:0;height:36px}
.sx button{font-size:1.5rem;line-height:1;padding:0}
.av{font-size:1.5rem;line-height:1}
.row{display:grid;gap:10px;padding:14px 0;border-bottom:1px solid var(--line)}
.r1{display:flex;gap:12px;align-items:center}
.r2{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap}
.r3{display:flex;gap:8px}
.r3 button{min-width:var(--ctl);padding:0 12px}
.pitem[data-open='true']{background:var(--soft);box-shadow:inset 3px 0 0 var(--accent);border-radius:10px}
.pitem .item{align-items:center;margin-bottom:0}
.pitem[data-open='true'] .item{align-items:flex-start}
.pitem .item:hover{background:none}
.cv{margin-left:auto;flex:none;display:grid;place-items:center;width:32px;height:32px;color:var(--mute)}
.cv svg{transition:transform .15s}
.pitem[data-open='true'] .cv svg{transform:rotate(180deg)}
.prow{display:flex;align-items:center;border-radius:10px;margin-bottom:2px}
.prow .item{flex:1 1 auto;min-width:0;width:auto;margin:0}
.prow[data-n]:not([data-n='0']){background:var(--soft);box-shadow:inset 3px 0 0 var(--accent)}
.pctl{display:flex;align-items:center;gap:4px;flex:none;padding-right:4px}
.pctl button{width:var(--ctl);padding:0;font-size:1.3rem;line-height:1}
.pn{min-width:24px;text-align:center}
[hidden]{display:none!important}"""
rep("\n[hidden]{display:none!important}", css)

# ---------- face icons ----------
cut("const MARS = ", "const stepper = ", "const MARS = '\\u{1F468}', VENUS = '\\u{1F469}';\nconst SEXICON = { Male: MARS, Female: VENUS };\n")

# ---------- selection == maximized ----------
rep("let plSel = null, plOpen = null, plDay = 0, saveT;", "let plSel = null, plDay = 0, saveT;")
cut("function renderPlanList() {", "function renderPlan() {", r"""function renderPlanList() {
  const list = filteredPlans(), total = Object.keys(state.planLib).length;
  $('#plCount').textContent = `${list.length} of ${total} plan${total === 1 ? '' : 's'}`;
  $('#plList').innerHTML = list.map(p => {
    const rows = activeRows(p), a = analyse(rows), sx = planSex(p), open = p.id === plSel;
    return `<div class='pitem' data-open='${open}'><button class='item' data-id='${esc(p.id)}' aria-expanded='${open}'>${open ? '' : thumb(a, sx)}<span><b>${esc(p.name || 'Untitled plan')}</b><small>${p.days} day${p.days === 1 ? '' : 's'} \u00b7 ${esc(p.level)} \u00b7 ${esc(p.goal)}</small></span><span class='cv' aria-hidden='true'>${ICON("<path d='M6 9l6 6 6-6'/>")}</span></button>`
      + (open ? `<div class='pexp'>${rows.length ? figs(a, 'red', 280, sx) + legend(a, RED) : `<p class='count'>This plan has no exercises yet.</p>`}</div>` : '') + `</div>`;
  }).join('') || `<p class='count'>${total ? 'No plan matches your filters.' : 'No plans yet. Use \u201cNew plan\u201d to create the first one.'}</p>`;
}
""")
rep("plSel = id; plOpen = id; plDay = 0; saveSoon();\n  for (const sid", "plSel = id; plDay = 0; saveSoon();\n  for (const sid")
cut("$('#plList').addEventListener('click', ev => {", "for (const sid of ['#plQ'", r"""$('#plList').addEventListener('click', ev => {
  const b = ev.target.closest('.item'); if (!b) return;
  plSel = plSel === b.dataset.id ? null : b.dataset.id; plDay = 0; renderPlanList(); renderEditor();
});
""")
rep("state.planLib[id] = copy; plSel = id; plOpen = id; saveSoon(); renderPlan(); return;", "state.planLib[id] = copy; plSel = id; saveSoon(); renderPlan(); return;")
rep("delete state.planLib[plSel]; if (plOpen === plSel) plOpen = null; plSel = null; saveSoon(); renderPlan(); return;", "delete state.planLib[plSel]; plSel = null; saveSoon(); renderPlan(); return;")

# ---------- exercise rows: three lines ----------
cut("const rows = r.map((x, i) => {", "  $('#plDay').innerHTML = `<div class='tabpanel' role='tabpanel'>", r"""const rows = r.map((x, i) => {
    const e = resolve(x), u = fileUrl(e.image);
    return `<div class='row'>
      <div class='r1'>${u ? `<img src='${esc(u)}' alt=''>` : `<span class='ph'></span>`}<span class='rn'>${esc(e.name)}</span></div>
      <div class='r2'><div class='mini sets'><span>Sets</span>${stepper('', x.sets, 1, 20, 1, `data-i='${i}' data-f='sets' aria-label='Sets'`)}</div>
        <label class='mini reps'>Reps<input data-i='${i}' data-f='reps' value='${esc(x.reps)}'></label></div>
      <div class='r3'><button data-i='${i}' data-act='up' aria-label='Move up' title='Move up'>\u2191</button><button data-i='${i}' data-act='down' aria-label='Move down' title='Move down'>\u2193</button><button data-i='${i}' data-act='del' class='danger' aria-label='Remove exercise' title='Remove'>\u2715</button></div>
    </div>`;
  }).join('') || `<p class='count'>No exercises yet. Add the first one for this day.</p>`;
""")

# ---------- picker: selected rows, remove, add several ----------
cut("function renderPick() {", "$('#tabPl').onclick = () => showPage('pl');", r"""function renderPick() {
  const q = $('#pQ').value.trim().toLowerCase(), t = $('#pT').value, eq = $('#pE').value, bp = $('#pB').value;
  const p = getPlan(), cur = p ? p.routines[plDay] : [], box = $('#pList'), keep = box.scrollTop;
  const list = all.filter(e => (!q || e.name.toLowerCase().includes(q)) && (!t || e.target === t) && (!eq || e.equipment === eq) && (!bp || e.body_part === bp)).slice(0, 80);
  box.innerHTML = list.map(e => {
    const n = cur.filter(x => x.id === e.id).length;
    return `<div class='prow' data-id='${esc(e.id)}' data-n='${n}'><button class='item' aria-label='Add ${esc(e.name)}'><img src='${esc(fileUrl(e.image))}' alt='' loading='lazy'><span><b>${esc(e.name)}</b><small>${esc(e.target)}</small></span></button>
      <span class='pctl'>${n ? `<button type='button' data-padd='-1' aria-label='Remove one ${esc(e.name)}'>\u2212</button><b class='pn'>${n}</b>` : ''}<button type='button' data-padd='1' aria-label='Add one more ${esc(e.name)}'>+</button></span></div>`;
  }).join('') || `<p class='count'>No exercise matches.</p>`;
  box.scrollTop = keep;
}
""")
cut("$('#pList').addEventListener('click', ev => {", "document.addEventListener('click', ev => {\n  const b = ev.target.closest('.stp');", r"""$('#pList').addEventListener('click', ev => {
  const row = ev.target.closest('.prow'); if (!row) return;
  const e = all.find(x => x.id === row.dataset.id), p = getPlan(); if (!e || !p) return;
  const m = ev.target.closest('[data-padd]'), r = p.routines[plDay];
  if (m && +m.dataset.padd < 0) {
    for (let i = r.length - 1; i >= 0; i--) if (r[i].id === e.id) { r.splice(i, 1); break; }
    $('#pMsg').textContent = `Removed one ${e.name}.`;
  } else {
    r.push({ id: e.id, n: e.name, t: e.target, s: e.secondary, b: e.body_part, sets: 3, reps: '10' });
    $('#pMsg').textContent = `Added ${e.name} (3 sets of 10). Change sets and reps in the day list.`;
  }
  saveSoon(); renderTabs(); renderDay(); renderPlanList(); renderPick();
});
""")

open(p, 'w', encoding='utf-8').write(s)
print('patched', len(s))
