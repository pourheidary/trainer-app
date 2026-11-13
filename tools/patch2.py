import re
p = '/mnt/user-data/outputs/trainer-app.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:70], s.count(old))
    s = s.replace(old, new)

def cut(start_marker, end_marker, new):
    global s
    a = s.index(start_marker); b = s.index(end_marker, a)
    s = s[:a] + new + s[b:]

# ---------- 1. header icon buttons ----------
ic = lambda d: f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
rep('<button id="folderBtn">Dataset folder</button>', f'<button id="folderBtn" class="ibtn" title="Dataset folder" aria-label="Dataset folder">{ic("<path d=\"M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\"/>")}</button>')
rep('<button id="exportBtn">Export backup</button>', f'<button id="exportBtn" class="ibtn" title="Export backup" aria-label="Export backup">{ic("<path d=\"M12 3v12m0 0-4-4m4 4 4-4M4 20h16\"/>")}</button>')
rep('<button id="importBtn">Import backup</button>', f'<button id="importBtn" class="ibtn" title="Import backup" aria-label="Import backup">{ic("<path d=\"M12 15V3m0 0L8 7m4-4 4 4M4 20h16\"/>")}</button>')

# ---------- 2. CSS ----------
css = r"""
.top{min-height:76px}
.top .acts{flex-wrap:nowrap}
.ibtn{width:40px;height:40px;padding:0;display:grid;place-items:center;flex:none}
.tabs button{height:36px}
.stack{display:grid;gap:16px;min-width:0}
.item small{display:block}
.av[data-st='ok']{background:#2e9e5b;color:#fff}
.av[data-st='soon']{background:#e8a317;color:#1a1200}
.av[data-st='late']{background:#d93a3f;color:#fff}
.fu{font-weight:600}
.fu[data-st='ok']{color:#2e9e5b}.fu[data-st='soon']{color:#b77f00}.fu[data-st='late']{color:#d93a3f}
.banner{margin:0 0 14px;padding:8px 14px;border-radius:8px;font-weight:600;max-width:560px}
.banner[data-st='ok']{background:rgba(46,158,91,.15);color:#2e9e5b}
.banner[data-st='soon']{background:rgba(232,163,23,.18);color:#b77f00}
.banner[data-st='late']{background:rgba(217,58,63,.15);color:#d93a3f}
.sform .fld{display:grid;gap:4px;font-size:.9rem;color:var(--mute)}
.bmi{padding:9px 0;color:var(--ink);font-weight:600}
.dateRow{display:flex;gap:8px}
.plhead2{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.plname{flex:1 1 220px;width:auto;font-size:1.25rem;font-weight:600}
.fl{display:grid;gap:4px;font-size:.9rem;color:var(--mute);margin-bottom:12px}
#plEditor .two{margin-bottom:0}
#plEditor .daytabs{margin:4px 0 14px}
.maps{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.mh{margin:0 0 10px;font-size:1.05rem}
[hidden]{display:none!important}"""
rep("\n[hidden]{display:none!important}", css, 1)

# ---------- 3. plan page markup ----------
a = s.index("<div id='pagePl' hidden>"); b = s.index("<footer>", a)
s = s[:a] + """<div id='pagePl' hidden>
  <div class='layout'>
    <div class='stack'>
      <section id='plEditor' class='panel det'></section>
      <section id='plMap' class='panel det' hidden></section>
    </div>
    <aside class='panel'>
      <div class='ahead'><b>Plans</b><button id='plNew' class='link'>+ New plan</button></div>
      <div class='filters'>
        <input id='plQ' type='search' placeholder='Search plans' aria-label='Search plans'>
        <select id='plFDays' aria-label='Training days'></select>
        <select id='plFMuscle' aria-label='Muscle'></select>
        <select id='plFBody' aria-label='Body part'></select>
        <select id='plFLevel' aria-label='Level'></select>
        <select id='plFGoal' aria-label='Goal'></select>
      </div>
      <p id='plCount' class='count'></p>
      <div id='plList'></div>
    </aside>
  </div>
</div>
""" + s[b:]

# ---------- 4. state, loader, import ----------
rep("let state = { over: {}, custom: {}, students: {}, plans: {} };", "let state = { over: {}, custom: {}, students: {}, plans: {}, planLib: {} };")
rep("if (s) state = { over: s.over || {}, custom: s.custom || {}, students: s.students || {}, plans: s.plans || {}, sex: s.sex };",
"""if (s) {
    state = { over: s.over || {}, custom: s.custom || {}, students: s.students || {}, plans: {}, planLib: s.planLib || {}, sex: s.sex };
    if (!s.planLib && s.plans) { let i = 0; for (const [k, lp] of Object.entries(s.plans)) if (lp.routines && lp.routines.some(r => r.length)) { const id = 'm' + k; state.planLib[id] = { id, name: 'Imported plan ' + (++i), days: lp.days || 3, level: 'Beginner', goal: 'General fitness', titles: lp.titles || [], routines: lp.routines }; } }
  }""")
rep("state.plans = { ...state.plans, ...(d.plans || {}) }; renderStudents(); renderStudentForm();",
    "state.planLib = { ...state.planLib, ...(d.planLib || {}) }; renderStudents(); renderStudentForm(); if (!$('#pagePl').hidden) renderPlan();")

# ---------- 5. students block ----------
cut("/* ---------- students page ---------- */", "function showPage(p) {", r"""/* ---------- students page ---------- */
let stSel = null;
const BLOOD = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
const BODY_TYPES = ['Ectomorph (slim)', 'Mesomorph (athletic)', 'Endomorph (stocky)', 'Overweight', 'Obese'];
const DURS = [[7, '1 week'], [14, '2 weeks'], [21, '3 weeks'], [30, '1 month'], [60, '2 months'], [90, '3 months']];
const today = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
function followUp(s) {
  if (!s.dur || !s.start) return null;
  const due = new Date(s.start + 'T00:00:00'); due.setDate(due.getDate() + +s.dur);
  const left = Math.round((due - today()) / 864e5);
  if (left < 0) return { st: 'late', text: `Follow-up overdue by ${-left} day${left === -1 ? '' : 's'}` };
  if (left === 0) return { st: 'late', text: 'Follow-up due today' };
  if (left <= 2) return { st: 'soon', text: `Follow-up in ${left} day${left === 1 ? '' : 's'}` };
  return { st: 'ok', text: `${left} days until follow-up` };
}
function bmiOf(h, w) { h = +h; w = +w; if (!(h > 0 && w > 0)) return null; const v = w / ((h / 100) ** 2); return { v: v.toFixed(1), cat: v < 18.5 ? 'Underweight' : v < 25 ? 'Normal' : v < 30 ? 'Overweight' : 'Obese' }; }
const bmiText = (h, w) => { const b = bmiOf(h, w); return b ? `${b.v} \u00b7 ${b.cat}` : 'Enter height and weight'; };
const initials = n => n.trim().split(/\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase() || '?';
const brief = s => [s.age && `${s.age} y`, s.height && `${s.height} cm`, s.weight && `${s.weight} kg`].filter(Boolean).join(' \u00b7 ');
const opts = (list, val, ph) => `<option value=''>${ph}</option>` + list.map(v => { const [value, label] = Array.isArray(v) ? v : [v, v]; return `<option value='${esc(value)}' ${String(value) === String(val) ? 'selected' : ''}>${esc(label)}</option>`; }).join('');
function renderStudents() {
  const q = $('#stQ').value.trim().toLowerCase(), pr = { late: 0, soon: 1 };
  const list = Object.values(state.students).filter(s => !q || s.name.toLowerCase().includes(q))
    .sort((a, b) => ((pr[(followUp(a) || {}).st] ?? 2) - (pr[(followUp(b) || {}).st] ?? 2)) || a.name.localeCompare(b.name));
  $('#stCount').textContent = `${list.length} student${list.length === 1 ? '' : 's'}`;
  $('#stList').innerHTML = list.map(s => { const f = followUp(s);
    return `<button class='item' data-id='${esc(s.id)}' ${s.id === stSel ? "aria-current='true'" : ''}><i class='av' data-st='${f ? f.st : ''}'>${esc(initials(s.name))}</i><span><b>${esc(s.name)}</b><small>${esc(brief(s))}</small>${f ? `<small class='fu' data-st='${f.st}'>${esc(f.text)}</small>` : ''}</span></button>`; }).join('')
    || `<p class='count'>No students yet. Use \u201cNew student\u201d to add the first one.</p>`;
}
function renderStudentForm() {
  const box = $('#stDetail');
  if (!stSel) { box.innerHTML = `<div class='empty'><div><b>Select a student</b>Choose a student from the list, or add a new one.</div></div>`; return; }
  const isNew = stSel === 'new';
  const s = isNew ? { name: '', sex: '', age: '', height: '', weight: '', blood: '', bodyType: '', dur: '', start: iso(today()), notes: '' } : state.students[stSel];
  const f = isNew ? null : followUp(s);
  box.innerHTML = `<h2 class='sth'>${isNew ? 'New student' : esc(s.name)}</h2>
  ${f ? `<p class='banner' data-st='${f.st}'>${esc(f.text)}</p>` : ''}
  <div class='sform'>
    <label>Name<input id='sName' value='${esc(s.name)}' autocomplete='off'></label>
    <div class='three'>
      <label>Sex<select id='sSex'>${opts(['Male', 'Female'], s.sex, 'Select')}</select></label>
      <label>Age<input id='sAge' type='number' min='1' max='120' inputmode='numeric' value='${esc(s.age)}'></label>
      <label>Blood type<select id='sBlood'>${opts(BLOOD, s.blood, 'Unknown')}</select></label>
    </div>
    <div class='three'>
      <label>Height (cm)<input id='sH' type='number' min='50' max='260' inputmode='decimal' value='${esc(s.height)}'></label>
      <label>Weight (kg)<input id='sW' type='number' min='20' max='400' step='0.1' inputmode='decimal' value='${esc(s.weight)}'></label>
      <div class='fld'><span>BMI</span><output id='sBmi' class='bmi'>${esc(bmiText(s.height, s.weight))}</output></div>
    </div>
    <label>Body type<select id='sBody'>${opts(BODY_TYPES, s.bodyType, 'Not set')}</select></label>
    <div class='two'>
      <label>Follow-up after<select id='sDur'>${opts(DURS, s.dur, 'No reminder')}</select></label>
      <label>Program given on<span class='dateRow'><input id='sStart' type='date' value='${esc(s.start || '')}'><button id='sToday' type='button'>Today</button></span></label>
    </div>
    <label>Notes<textarea id='sNotes' rows='5' placeholder='Goals, injuries, schedule, anything useful'>${esc(s.notes)}</textarea></label>
    <div class='acts'>${isNew ? '' : '<button id="sDel" class="danger left">Delete student</button>'}<button id='sSave' class='primary'>${isNew ? 'Add student' : 'Save changes'}</button></div>
  </div>`;
  $('#sSave').onclick = saveStudent;
  if (!isNew) $('#sDel').onclick = deleteStudent;
}
async function saveStudent() {
  const name = $('#sName').value.trim();
  if (!name) { $('#sName').focus(); return; }
  const id = stSel === 'new' ? 's' + Date.now() : stSel;
  state.students[id] = { id, name, sex: $('#sSex').value, age: $('#sAge').value, blood: $('#sBlood').value, height: $('#sH').value, weight: $('#sW').value,
    bodyType: $('#sBody').value, dur: $('#sDur').value ? +$('#sDur').value : '', start: $('#sStart').value, notes: $('#sNotes').value.trim() };
  stSel = id; await save(); renderStudents(); renderStudentForm();
}
async function deleteStudent() {
  if (!confirm('Delete this student?')) return;
  delete state.students[stSel]; stSel = null;
  await save(); renderStudents(); renderStudentForm();
}
$('#stDetail').addEventListener('input', ev => { if (ev.target.id === 'sH' || ev.target.id === 'sW') $('#sBmi').textContent = bmiText($('#sH').value, $('#sW').value); });
$('#stDetail').addEventListener('click', ev => { if (ev.target.id === 'sToday') $('#sStart').value = iso(today()); });
""")

# ---------- 6. plan logic block ----------
cut("const CROP = '180 30 664 1510'", "function openPicker() {", r"""const CROP = '180 30 664 1510';
const BLUE = { p: '#1f7aff', s: '#8cc4ff' }, RED = { p: '#e5484d', s: '#f5a3a6' };
const LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Elite'];
const GOALS = ['Muscle building', 'Fat loss', 'Strength', 'Endurance', 'General fitness', 'Competition prep'];
const curSex = () => state.sex === 'FEMALE' ? 'FEMALE' : 'MALE';
const shade = (hex, a) => { const v = parseInt(hex.slice(1), 16), t = a < 0 ? 0 : 255, q = Math.abs(a); return '#' + [v >> 16, (v >> 8) & 255, v & 255].map(c => Math.round(c + (t - c) * q).toString(16).padStart(2, '0')).join(''); };
function figure(sex, view, lv, pal, tag) {
  const d = BODIES[sex][view], id = `f${tag}${sex[0]}${view[0]}`, mir = `matrix(-1 0 0 1 ${2 * d.centerX} 0)`;
  const outline = d.outline.map(o => `<path d='${o.d}'/>` + (o.side === 'LEFT' ? `<path d='${o.d}' transform='${mir}'/>` : '')).join('');
  const grad = (n, c) => `<linearGradient id='${id}${n}' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='${shade(c, .22)}'/><stop offset='.55' stop-color='${c}'/><stop offset='1' stop-color='${shade(c, -.28)}'/></linearGradient>`;
  const muscles = d.muscles.map(m => {
    const l = lv[m.g]; if (!l) return '';
    const a = `<path d='${m.d}' fill='url(#${id}${l})' stroke='rgba(6,10,18,.55)' stroke-width='1'`;
    return `${a}/>` + (m.s === 'LEFT' ? `${a} transform='${mir}'/>` : '');
  }).join('');
  return `<svg viewBox='${CROP}' role='img' aria-label='${sex === 'MALE' ? 'Male' : 'Female'} ${view.toLowerCase()} view'><defs><clipPath id='${id}c'>${outline}</clipPath>${grad('p', pal.p)}${grad('s', pal.s)}</defs><image href='${BODY_IMG[sex][view]}' x='0' y='0' width='1024' height='1536' preserveAspectRatio='none' clip-path='url(#${id}c)' style='filter:grayscale(1)'/>${muscles}</svg>`;
}
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
  const list = filteredPlans(), total = Object.keys(state.planLib).length;
  $('#plCount').textContent = `${list.length} of ${total} plan${total === 1 ? '' : 's'}`;
  $('#plList').innerHTML = list.map(p => `<button class='item' data-id='${esc(p.id)}' ${p.id === plSel ? "aria-current='true'" : ''}><i class='av'>${p.days}d</i><span><b>${esc(p.name || 'Untitled plan')}</b><small>${p.days} day${p.days === 1 ? '' : 's'} \u00b7 ${esc(p.level)} \u00b7 ${esc(p.goal)}</small></span></button>`).join('')
    || `<p class='count'>${total ? 'No plan matches your filters.' : 'No plans yet. Use \u201cNew plan\u201d to create the first one.'}</p>`;
}
function renderPlan() {
  const dsel = $('#plFDays');
  if (!dsel.options.length) dsel.innerHTML = `<option value=''>Any number of days</option>` + [1, 2, 3, 4, 5, 6, 7].map(n => `<option value='${n}'>${n} day${n > 1 ? 's' : ''}</option>`).join('');
  fillOpts($('#plFLevel'), 'All levels', LEVELS); fillOpts($('#plFGoal'), 'All goals', GOALS);
  fillOpts($('#plFMuscle'), 'All muscles', Object.keys(KEYGROUPS).sort());
  const bps = [...new Set([...all.map(e => e.body_part), ...Object.values(state.planLib).flatMap(p => p.routines.flat().map(x => x.b))].filter(Boolean))].sort();
  fillOpts($('#plFBody'), 'All body parts', bps);
  renderPlanList(); renderEditor();
}
function renderEditor() {
  const p = getPlan(), box = $('#plEditor');
  if (!p) { box.innerHTML = `<div class='empty'><div><b>Select a plan</b>Choose a plan from the library, or create a new one.</div></div>`; $('#plMap').hidden = true; return; }
  plDay = Math.min(plDay, p.days - 1);
  const sel = (list, v) => list.map(o => `<option ${o === v ? 'selected' : ''}>${esc(o)}</option>`).join('');
  box.innerHTML = `<div class='plhead2'><input id='plName' class='plname' value='${esc(p.name)}' placeholder='Plan name' aria-label='Plan name' autocomplete='off'>
      <div class='acts'><button id='plDup'>Duplicate</button><button id='plDel' class='danger'>Delete</button></div></div>
    <div class='two' style='margin-bottom:12px'><label class='fl' style='margin:0'>Level<select id='plLevel'>${sel(LEVELS, p.level)}</select></label><label class='fl' style='margin:0'>Goal<select id='plGoal'>${sel(GOALS, p.goal)}</select></label></div>
    <div class='fl'><span>Training days per week</span><div class='seg' role='group' aria-label='Training days per week'>${[1, 2, 3, 4, 5, 6, 7].map(n => `<button data-n='${n}' aria-pressed='${p.days === n}'>${n}</button>`).join('')}</div></div>
    <div id='plTabs' class='daytabs' role='tablist' aria-label='Training days'></div>
    <div id='plDay'></div>`;
  renderTabs(); renderDay(); renderMaps();
}
function renderTabs() {
  const p = getPlan();
  $('#plTabs').innerHTML = Array.from({ length: p.days }, (_, i) => `<button data-d='${i}' role='tab' aria-selected='${i === plDay}'>Day ${i + 1}${p.titles[i] ? ': ' + esc(p.titles[i]) : ''}</button>`).join('');
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
  $('#plDay').innerHTML = `<label class='dtitle'>Day ${plDay + 1} title<input id='plTitle' value='${esc(p.titles[plDay] || '')}' placeholder='Optional, for example Chest and triceps'></label>${rows}
    <p class='plfoot'><button id='plAdd' class='primary'>Add exercise</button><span class='count'>${r.length} exercise${r.length === 1 ? '' : 's'} \u00b7 ${sets} sets</span></p>`;
}
function renderMaps() {
  const p = getPlan(), box = $('#plMap'); if (!p) return;
  box.hidden = false;
  const sx = curSex(), dayA = analyse(p.routines[plDay]), rows = activeRows(p);
  const figs = (a, pal, tag) => `<div class='fig'><figure>${figure(sx, 'FRONT', a.glv, pal, tag)}<figcaption>Front</figcaption></figure><figure>${figure(sx, 'BACK', a.glv, pal, tag)}<figcaption>Back</figcaption></figure></div>`;
  const dayBlock = p.routines[plDay].length
    ? `<div><h3 class='mh'>Day ${plDay + 1}${p.titles[plDay] ? ': ' + esc(p.titles[plDay]) : ''}</h3>${figs(dayA, BLUE, 'd')}${legend(dayA, BLUE)}</div>`
    : `<div><h3 class='mh'>Day ${plDay + 1}</h3><p class='count'>Add exercises to this day to see which muscles it works.</p></div>`;
  let planBlock = '';
  if (p.days > 1) {
    const planA = analyse(rows);
    planBlock = rows.length ? `<div><h3 class='mh'>Whole plan (${p.days} days)</h3>${figs(planA, RED, 'w')}${legend(planA, RED)}</div>` : '';
  }
  box.innerHTML = `<div class='ahead'><h2 class='sth' style='margin:0'>Muscle maps</h2><div class='seg' role='group' aria-label='Body model'><button data-sex='MALE' aria-pressed='${sx === 'MALE'}'>Male</button><button data-sex='FEMALE' aria-pressed='${sx === 'FEMALE'}'>Female</button></div></div>
    <div class='maps'>${dayBlock}${planBlock}</div>`;
}
""")

# ---------- 7. plan events block ----------
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
$('#plEditor').addEventListener('input', ev => {
  const t = ev.target, p = getPlan(); if (!p) return;
  if (t.id === 'plName') { p.name = t.value; saveSoon(); renderPlanList(); return; }
  if (t.id === 'plLevel') { p.level = t.value; saveSoon(); renderPlanList(); return; }
  if (t.id === 'plGoal') { p.goal = t.value; saveSoon(); renderPlanList(); return; }
  if (t.id === 'plTitle') {
    p.titles[plDay] = t.value; saveSoon();
    const tb = $('#plTabs').children[plDay]; if (tb) tb.textContent = 'Day ' + (plDay + 1) + (t.value.trim() ? ': ' + t.value.trim() : '');
    return;
  }
  if (t.dataset.f) {
    const x = p.routines[plDay][+t.dataset.i]; if (!x) return;
    x[t.dataset.f] = t.dataset.f === 'sets' ? Math.max(1, Math.min(20, parseInt(t.value) || 1)) : t.value;
    saveSoon(); renderMaps();
  }
});
$('#plEditor').addEventListener('click', ev => {
  const b = ev.target.closest('button'), p = getPlan(); if (!b || !p) return;
  if (b.dataset.n) { p.days = +b.dataset.n; saveSoon(); renderPlanList(); renderEditor(); return; }
  if (b.dataset.d) { plDay = +b.dataset.d; renderTabs(); renderDay(); renderMaps(); return; }
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
  saveSoon(); renderDay(); renderMaps(); renderPlanList();
});
$('#plMap').addEventListener('click', ev => { const b = ev.target.closest('[data-sex]'); if (!b) return; state.sex = b.dataset.sex; saveSoon(); renderMaps(); });
""")

# picker adds body part and uses new render fns; remove the old sex handler
rep("getPlan().routines[plDay].push({ id: e.id, n: e.name, t: e.target, s: e.secondary, sets: 3, reps: '10' });\n  saveSoon(); renderDay(); renderMap();",
    "getPlan().routines[plDay].push({ id: e.id, n: e.name, t: e.target, s: e.secondary, b: e.body_part, sets: 3, reps: '10' });\n  saveSoon(); renderDay(); renderMaps(); renderPlanList();")
rep("$('#plMap').addEventListener('click', ev => { const b = ev.target.closest('[data-sex]'); if (!b) return; state.sex = b.dataset.sex; saveSoon(); renderMap(); });\n", "")

# ---------- 8. clear button on every search box ----------
rep("$('#pQ').addEventListener('input', () =>", r"""function enhanceSearch(el) {
  el.type = 'text'; el.autocomplete = 'off';
  const wrap = document.createElement('div'); wrap.className = 'clr';
  const x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.setAttribute('aria-label', 'Clear search'); x.textContent = '\u2715'; x.hidden = !el.value;
  el.parentNode.insertBefore(wrap, el); wrap.append(el, x);
  el.addEventListener('input', () => { x.hidden = !el.value; });
  x.onclick = () => { el.value = ''; x.hidden = true; el.dispatchEvent(new Event('input', { bubbles: true })); el.focus(); };
}
['#q', '#stQ', '#plQ'].forEach(id => enhanceSearch($(id)));
$('#pQ').addEventListener('input', () =>""")

open(p, 'w', encoding='utf-8').write(s)
print('patched', len(s))
