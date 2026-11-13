p = '/mnt/user-data/outputs/trainer-app.html'
s = open(p, encoding='utf-8').read()
box = open('/home/claude/bodybox.js', encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:70], s.count(old))
    s = s.replace(old, new)

def cut(start_marker, end_marker, new):
    global s
    a = s.index(start_marker); b = s.index(end_marker, a)
    s = s[:a] + new + s[b:]

# bounding boxes of the four bodies
rep("</script>\n<script>\nconst $ = ", box + "</script>\n<script>\nconst $ = ")

# ---------- CSS ----------
css = r"""
.fbar{display:grid;grid-template-columns:minmax(150px,2fr) repeat(5,minmax(0,1fr));gap:8px;padding:0 clamp(16px,4vw,40px) 16px}
@media (max-width:1000px){.fbar{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:560px){.fbar{grid-template-columns:repeat(2,minmax(0,1fr))}}
.daytabs{display:flex;gap:2px;flex-wrap:wrap;border-bottom:1px solid var(--line);margin:4px 0 0}
.daytabs button{border:1px solid var(--line);border-bottom:0;border-radius:8px 8px 0 0;background:var(--soft);color:var(--mute);padding:8px 14px;margin-bottom:-1px}
.daytabs button[aria-selected='true']{background:var(--surface);color:var(--ink);font-weight:600;border-color:var(--line);border-top:3px solid var(--accent)}
.cnt{display:inline-block;min-width:20px;margin-left:8px;padding:0 6px;border-radius:999px;background:var(--line);color:var(--ink);font-size:.78rem;font-weight:600;text-align:center}
.tabpanel{border:1px solid var(--line);border-top:0;border-radius:0 0 10px 10px;padding:16px}
.dsum{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start;padding-bottom:14px;margin-bottom:14px;border-bottom:1px solid var(--line)}
.dsum .txt{flex:1 1 220px;min-width:0}
.figs{display:flex;gap:8px;align-items:flex-end}
.figs figure{margin:0;text-align:center;color:var(--mute);font-size:.8rem}
.figs svg{display:block}
.pthumb{display:flex;gap:2px;flex:none;align-items:center;justify-content:center;width:62px;height:64px}
.pexp{padding:6px 8px 16px}
.pexp .figs{justify-content:center;margin-bottom:12px}
#plSex button{min-width:0;padding:5px 10px;font-size:.85rem}
.ibtn.danger{color:var(--danger)}
[hidden]{display:none!important}"""
rep("\n[hidden]{display:none!important}", css)

# ---------- plan page markup ----------
a = s.index("<div id='pagePl' hidden>"); b = s.index("<footer>", a)
s = s[:a] + """<div id='pagePl' hidden>
  <div class='fbar'>
    <input id='plQ' type='search' placeholder='Search plans' aria-label='Search plans'>
    <select id='plFDays' aria-label='Training days'></select>
    <select id='plFMuscle' aria-label='Muscle'></select>
    <select id='plFBody' aria-label='Body part'></select>
    <select id='plFLevel' aria-label='Level'></select>
    <select id='plFGoal' aria-label='Goal'></select>
  </div>
  <div class='layout'>
    <section id='plEditor' class='panel det'></section>
    <aside class='panel'>
      <div class='ahead'><b>Plans</b><div id='plSex' class='seg' role='group' aria-label='Body model'><button data-sex='MALE'>Male</button><button data-sex='FEMALE'>Female</button></div><button id='plNew' class='link'>+ New plan</button></div>
      <p id='plCount' class='count'></p>
      <div id='plList'></div>
    </aside>
  </div>
</div>
""" + s[b:]

# ---------- plan logic ----------
cut("const CROP = '180 30 664 1510';", "function openPicker() {", r"""const BLUE = { p: '#1f7aff', s: '#8cc4ff' }, RED = { p: '#e5484d', s: '#f5a3a6' }, PAL = { blue: BLUE, red: RED };
const LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Elite'];
const GOALS = ['Muscle building', 'Fat loss', 'Strength', 'Endurance', 'General fitness', 'Competition prep'];
const curSex = () => state.sex === 'FEMALE' ? 'FEMALE' : 'MALE';
const shade = (hex, a) => { const v = parseInt(hex.slice(1), 16), t = a < 0 ? 0 : 255, q = Math.abs(a); return '#' + [v >> 16, (v >> 8) & 255, v & 255].map(c => Math.round(c + (t - c) * q).toString(16).padStart(2, '0')).join(''); };
(function initDefs() {
  let h = '';
  for (const sex of ['MALE', 'FEMALE']) for (const view of ['FRONT', 'BACK']) {
    const k = sex + view, d = BODIES[sex][view];
    h += `<image id='img-${k}' href='${BODY_IMG[sex][view]}' x='0' y='0' width='1024' height='1536' preserveAspectRatio='none'/>`;
    h += `<clipPath id='clip-${k}'>${d.outline.map(o => `<path d='${o.d}'/>`).join('')}</clipPath>`;
    d.muscles.forEach((m, i) => { h += `<path id='mp-${k}-${i}' d='${m.d}'/>`; });
  }
  for (const [n, pal] of Object.entries(PAL)) for (const l of ['p', 's']) {
    const c = pal[l];
    h += `<linearGradient id='g-${n}-${l}' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='${shade(c, .22)}'/><stop offset='.55' stop-color='${c}'/><stop offset='1' stop-color='${shade(c, -.28)}'/></linearGradient>`;
  }
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true'); svg.style.position = 'absolute';
  svg.innerHTML = `<defs>${h}</defs>`; document.body.prepend(svg);
})();
function figure(sex, view, lv, pal, h) {
  const k = sex + view, d = BODIES[sex][view], [x0, y0, x1, y1] = BODY_BOX[sex][view], pad = Math.round((y1 - y0) * .02);
  const vw = x1 - x0 + 2 * pad, vh = y1 - y0 + 2 * pad, w = Math.round(h * vw / vh), mir = `matrix(-1 0 0 1 ${2 * d.centerX} 0)`;
  const muscles = d.muscles.map((m, i) => {
    const l = lv[m.g]; if (!l) return '';
    const a = `<use href='#mp-${k}-${i}' fill='url(#g-${pal}-${l})' stroke='rgba(6,10,18,.55)' stroke-width='1'`;
    return `${a}/>` + (m.s === 'LEFT' ? `${a} transform='${mir}'/>` : '');
  }).join('');
  return `<svg viewBox='${x0 - pad} ${y0 - pad} ${vw} ${vh}' width='${w}' height='${h}' role='img' aria-label='${sex === 'MALE' ? 'Male' : 'Female'} ${view.toLowerCase()} view'><use href='#img-${k}' clip-path='url(#clip-${k})' style='filter:grayscale(1)'/>${muscles}</svg>`;
}
const figs = (a, pal, h) => `<div class='figs'><figure>${figure(curSex(), 'FRONT', a.glv, pal, h)}<figcaption>Front</figcaption></figure><figure>${figure(curSex(), 'BACK', a.glv, pal, h)}<figcaption>Back</figcaption></figure></div>`;
const thumb = a => `<span class='pthumb'>${figure(curSex(), 'FRONT', a.glv, 'red', 64)}${figure(curSex(), 'BACK', a.glv, 'red', 64)}</span>`;
let plSel = null, plDay = 0, saveT;
const saveSoon = () => { clearTimeout(saveT); saveT = setTimeout(save, 400); };
const resolve = x => all.find(e => e.id === x.id) || { name: x.n, target: x.t, secondary: x.s, image: '', body_part: x.b || '' };
const getPlan = () => state.planLib[plSel] || null;
const activeRows = p => p.routines.slice(0, p.days).flat();
function analyse(rows) {
  const prim = {}, sec = new Set(), other = new Set(), bparts = new Set();
  for (const x of rows) {
    const e = resolve(x), k = muscleKey(e.target), n = +x.sets || 0;
    if (k) prim[k] = (prim[k] || 0) + n; else if (e.target) other.add(e.target);
    for (const t of String(e.secondary || '').split(',')) { const sk = muscleKey(t); if (sk) sec.add(sk); else if (t.trim()) other.add(t.trim()); }
    if (e.body_part) bparts.add(e.body_part);
  }
  for (const k in prim) sec.delete(k);
  const lv = {}; for (const k of sec) lv[k] = 's'; for (const k in prim) lv[k] = 'p';
  const glv = {}; for (const [k, l] of Object.entries(lv)) for (const g of KEYGROUPS[k] || []) if (glv[g] !== 'p') glv[g] = l;
  return { prim, sec, other, glv, bparts };
}
function legend(a, pal) {
  const names = Object.entries(a.prim).sort((x, y) => y[1] - x[1]).map(([k, n]) => `${cap(k)} (${n} sets)`);
  return `<p class='mgrp'><span class='sw' style='background:${pal.p}'></span><b>Primary:</b> ${esc(names.join(', ') || 'none')}</p>
    <p class='mgrp'><span class='sw' style='background:${pal.s}'></span><b>Secondary:</b> ${esc([...a.sec].map(cap).join(', ') || 'none')}</p>
    ${a.other.size ? `<p class='mgrp count'>Not drawn on the figure: ${esc([...a.other].join(', '))}</p>` : ''}`;
}
const fillOpts = (sel, label, vals) => { const cur = sel.value; sel.innerHTML = `<option value=''>${label}</option>` + vals.map(v => `<option value='${esc(v)}'>${esc(cap(String(v)))}</option>`).join(''); sel.value = vals.map(String).includes(cur) ? cur : ''; };
function filteredPlans() {
  const q = $('#plQ').value.trim().toLowerCase(), d = $('#plFDays').value, lv = $('#plFLevel').value, g = $('#plFGoal').value, m = $('#plFMuscle').value, bp = $('#plFBody').value;
  return Object.values(state.planLib).filter(p => {
    if (q && !(p.name || '').toLowerCase().includes(q)) return false;
    if (d && p.days !== +d) return false;
    if (lv && p.level !== lv) return false;
    if (g && p.goal !== g) return false;
    if (m || bp) { const a = analyse(activeRows(p)); if (m && !(a.prim[m] || a.sec.has(m))) return false; if (bp && !a.bparts.has(bp)) return false; }
    return true;
  }).sort((a, b) => (a.name || '').localeCompare(b.name || ''));
}
function renderPlanList() {
  for (const b of $('#plSex').children) b.setAttribute('aria-pressed', String(b.dataset.sex === curSex()));
  const list = filteredPlans(), total = Object.keys(state.planLib).length;
  $('#plCount').textContent = `${list.length} of ${total} plan${total === 1 ? '' : 's'}`;
  $('#plList').innerHTML = list.map(p => {
    const rows = activeRows(p), a = analyse(rows), on = p.id === plSel;
    return `<button class='item' data-id='${esc(p.id)}' ${on ? "aria-current='true'" : ''}>${on ? '' : thumb(a)}<span><b>${esc(p.name || 'Untitled plan')}</b><small>${p.days} day${p.days === 1 ? '' : 's'} \u00b7 ${esc(p.level)} \u00b7 ${esc(p.goal)}</small></span></button>`
      + (on ? `<div class='pexp'>${rows.length ? figs(a, 'red', 280) + legend(a, RED) : `<p class='count'>This plan has no exercises yet.</p>`}</div>` : '');
  }).join('') || `<p class='count'>${total ? 'No plan matches your filters.' : 'No plans yet. Use \u201cNew plan\u201d to create the first one.'}</p>`;
}
function renderPlan() {
  const dsel = $('#plFDays');
  if (!dsel.options.length) dsel.innerHTML = `<option value=''>Any days</option>` + [1, 2, 3, 4, 5, 6, 7].map(n => `<option value='${n}'>${n} day${n > 1 ? 's' : ''}</option>`).join('');
  fillOpts($('#plFLevel'), 'All levels', LEVELS); fillOpts($('#plFGoal'), 'All goals', GOALS);
  fillOpts($('#plFMuscle'), 'All muscles', Object.keys(KEYGROUPS).sort());
  const bps = [...new Set([...all.map(e => e.body_part), ...Object.values(state.planLib).flatMap(p => p.routines.flat().map(x => x.b))].filter(Boolean))].sort();
  fillOpts($('#plFBody'), 'All body parts', bps);
  renderPlanList(); renderEditor();
}
const ICON = d => `<svg width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'>${d}</svg>`;
function renderEditor() {
  const p = getPlan(), box = $('#plEditor');
  if (!p) { box.innerHTML = `<div class='empty'><div><b>Select a plan</b>Choose a plan from the library, or create a new one.</div></div>`; return; }
  plDay = Math.min(plDay, p.days - 1);
  const sel = (list, v) => list.map(o => `<option ${o === v ? 'selected' : ''}>${esc(o)}</option>`).join('');
  box.innerHTML = `<div class='plhead2'><input id='plName' class='plname' value='${esc(p.name)}' placeholder='Plan name' aria-label='Plan name' autocomplete='off'>
      <button id='plDup' class='ibtn' title='Duplicate plan' aria-label='Duplicate plan'>${ICON("<rect x='9' y='9' width='11' height='11' rx='2'/><path d='M5 15V6a2 2 0 0 1 2-2h9'/>")}</button>
      <button id='plDel' class='ibtn danger' title='Delete plan' aria-label='Delete plan'>${ICON("<path d='M4 7h16M10 11v6M14 11v6M6 7l1 12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-12M9 7V4h6v3'/>")}</button></div>
    <div class='fl'><span>Training days per week</span><div class='seg' role='group' aria-label='Training days per week'>${[1, 2, 3, 4, 5, 6, 7].map(n => `<button data-n='${n}' aria-pressed='${p.days === n}'>${n}</button>`).join('')}</div></div>
    <div class='two' style='margin-bottom:16px'><label class='fl' style='margin:0'>Level<select id='plLevel'>${sel(LEVELS, p.level)}</select></label><label class='fl' style='margin:0'>Goal<select id='plGoal'>${sel(GOALS, p.goal)}</select></label></div>
    <div id='plTabs' class='daytabs' role='tablist' aria-label='Training days'></div>
    <div id='plDay'></div>`;
  renderTabs(); renderDay();
}
function renderTabs() {
  const p = getPlan(); if (!p) return;
  $('#plTabs').innerHTML = Array.from({ length: p.days }, (_, i) => `<button data-d='${i}' role='tab' aria-selected='${i === plDay}'>Day ${i + 1}${p.titles[i] ? ': ' + esc(p.titles[i]) : ''}<span class='cnt'>${p.routines[i].length}</span></button>`).join('');
}
function renderSummary() {
  const p = getPlan(), box = $('#plSum'); if (!p || !box) return;
  const r = p.routines[plDay], a = analyse(r);
  box.innerHTML = r.length ? `${figs(a, 'blue', 120)}<div class='txt'><h3 class='mh'>Muscles worked on day ${plDay + 1}</h3>${legend(a, BLUE)}</div>`
    : `<p class='count' style='margin:0'>Add exercises to see which muscles this day works.</p>`;
}
function renderDay() {
  const p = getPlan(), r = p.routines[plDay], sets = r.reduce((a, x) => a + (+x.sets || 0), 0);
  const rows = r.map((x, i) => {
    const e = resolve(x), u = fileUrl(e.image);
    return `<div class='row'>${u ? `<img src='${esc(u)}' alt=''>` : `<span class='ph'></span>`}<span class='rn'>${esc(e.name)}</span>
      <label class='mini'>Sets<input data-i='${i}' data-f='sets' type='number' min='1' max='20' inputmode='numeric' value='${esc(x.sets)}'></label>
      <label class='mini'>Reps<input data-i='${i}' data-f='reps' value='${esc(x.reps)}'></label>
      <span class='mv'><button data-i='${i}' data-act='up' aria-label='Move up'>\u2191</button><button data-i='${i}' data-act='down' aria-label='Move down'>\u2193</button><button data-i='${i}' data-act='del' class='danger' aria-label='Remove exercise'>\u2715</button></span></div>`;
  }).join('') || `<p class='count'>No exercises yet. Add the first one for this day.</p>`;
  $('#plDay').innerHTML = `<div class='tabpanel' role='tabpanel'><div id='plSum' class='dsum'></div>
    <label class='dtitle'>Day ${plDay + 1} title<input id='plTitle' value='${esc(p.titles[plDay] || '')}' placeholder='Optional, for example Chest and triceps'></label>${rows}
    <p class='plfoot'><button id='plAdd' class='primary'>Add exercise</button><span class='count'>${r.length} exercise${r.length === 1 ? '' : 's'} \u00b7 ${sets} sets</span></p></div>`;
  renderSummary();
}
""")

# ---------- events ----------
cut("$('#tabPl').onclick = () => showPage('pl');", "$('#pList').addEventListener('click', ev => {", r"""$('#tabPl').onclick = () => showPage('pl');
$('#plNew').onclick = () => {
  const id = 'p' + Date.now();
  state.planLib[id] = { id, name: 'New plan', days: 3, level: 'Beginner', goal: 'Muscle building', titles: [], routines: Array.from({ length: 7 }, () => []) };
  plSel = id; plDay = 0; saveSoon();
  for (const sid of ['#plFDays', '#plFLevel', '#plFGoal', '#plFMuscle', '#plFBody']) $(sid).value = '';
  $('#plQ').value = ''; $('#plQ').dispatchEvent(new Event('input', { bubbles: true }));
  renderPlan(); const n = $('#plName'); n.focus(); n.select();
};
$('#plList').addEventListener('click', ev => { const b = ev.target.closest('.item'); if (!b) return; plSel = b.dataset.id; plDay = 0; renderPlanList(); renderEditor(); });
for (const sid of ['#plQ', '#plFDays', '#plFLevel', '#plFGoal', '#plFMuscle', '#plFBody']) $(sid).addEventListener('input', renderPlanList);
$('#plSex').addEventListener('click', ev => { const b = ev.target.closest('[data-sex]'); if (!b) return; state.sex = b.dataset.sex; saveSoon(); renderPlanList(); renderSummary(); });
$('#plEditor').addEventListener('input', ev => {
  const t = ev.target, p = getPlan(); if (!p) return;
  if (t.id === 'plName') { p.name = t.value; saveSoon(); renderPlanList(); return; }
  if (t.id === 'plLevel') { p.level = t.value; saveSoon(); renderPlanList(); return; }
  if (t.id === 'plGoal') { p.goal = t.value; saveSoon(); renderPlanList(); return; }
  if (t.id === 'plTitle') { p.titles[plDay] = t.value; saveSoon(); renderTabs(); return; }
  if (t.dataset.f) {
    const x = p.routines[plDay][+t.dataset.i]; if (!x) return;
    x[t.dataset.f] = t.dataset.f === 'sets' ? Math.max(1, Math.min(20, parseInt(t.value) || 1)) : t.value;
    saveSoon(); renderSummary(); renderPlanList();
  }
});
$('#plEditor').addEventListener('click', ev => {
  const b = ev.target.closest('button'), p = getPlan(); if (!b || !p) return;
  if (b.dataset.n) { p.days = +b.dataset.n; saveSoon(); renderPlanList(); renderEditor(); return; }
  if (b.dataset.d) { plDay = +b.dataset.d; renderTabs(); renderDay(); return; }
  if (b.id === 'plAdd') { openPicker(); return; }
  if (b.id === 'plDup') {
    const id = 'p' + Date.now(), copy = JSON.parse(JSON.stringify(p)); copy.id = id; copy.name = (p.name || 'Plan') + ' (copy)';
    state.planLib[id] = copy; plSel = id; saveSoon(); renderPlan(); return;
  }
  if (b.id === 'plDel') { if (!confirm('Delete this plan?')) return; delete state.planLib[plSel]; plSel = null; saveSoon(); renderPlan(); return; }
  const r = p.routines[plDay], i = +b.dataset.i, a = b.dataset.act;
  if (a === 'del') r.splice(i, 1);
  else if (a === 'up' && i > 0) { const t = r[i - 1]; r[i - 1] = r[i]; r[i] = t; }
  else if (a === 'down' && i < r.length - 1) { const t = r[i + 1]; r[i + 1] = r[i]; r[i] = t; }
  else return;
  saveSoon(); renderTabs(); renderDay(); renderPlanList();
});
""")

rep("saveSoon(); renderDay(); renderMaps(); renderPlanList();", "saveSoon(); renderTabs(); renderDay(); renderPlanList();")

open(p, 'w', encoding='utf-8').write(s)
print('patched', len(s))
