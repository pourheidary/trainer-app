p = '/mnt/user-data/outputs/trainer-app.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)

def cut(start_marker, end_marker, new):
    global s
    a = s.index(start_marker); b = s.index(end_marker, a)
    s = s[:a] + new + s[b:]

# ---------- CSS ----------
rep("@media (max-width:480px){.three{grid-template-columns:1fr}}\n", "")
css = r"""
input[type=number]{-moz-appearance:textfield;appearance:textfield}
input[type=number]::-webkit-inner-spin-button,input[type=number]::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
.fld{display:grid;gap:4px;font-size:.9rem;color:var(--mute)}
.stepper{display:flex;align-items:stretch;width:100%}
.stepper input{text-align:center;border-radius:0;min-width:0;min-height:44px;flex:1 1 auto;width:100%}
.stepper button{flex:none;width:44px;min-height:44px;padding:0;font-size:1.3rem;line-height:1}
.stepper button:first-child{border-radius:8px 0 0 8px}
.stepper button:last-child{border-radius:0 8px 8px 0}
.mini.sets{width:150px}
.nameRow{display:flex;gap:12px;align-items:flex-end}
.nameRow .grow{flex:1 1 auto;min-width:0}
.sx button{min-width:48px;min-height:44px;padding:0;display:grid;place-items:center}
.plrow{display:grid;grid-template-columns:1fr 1fr auto;gap:12px;align-items:end;margin-bottom:16px}
@media (max-width:560px){.plrow{grid-template-columns:1fr 1fr}.plrow .fld{grid-column:1/-1}}
.av svg{width:26px;height:26px}
.phead{display:flex;align-items:center}
.phead .item{flex:1 1 auto;min-width:0;width:auto;margin-bottom:0}
.chev{flex:none;width:44px;height:44px;padding:0;border:0;background:none;display:grid;place-items:center;color:var(--mute)}
.chev svg{transition:transform .15s}
.chev[aria-expanded='true'] svg{transform:rotate(180deg)}
.pitem{margin-bottom:4px;border-radius:10px}
.pitem[data-open='true']{background:var(--soft)}
.mv button{min-width:40px;min-height:40px}
@media (pointer:coarse){.seg button{min-height:44px}.mv button{min-width:44px;min-height:44px}.ibtn{width:44px;height:44px}.link{padding:10px 0}}
[hidden]{display:none!important}"""
rep("\n[hidden]{display:none!important}", css)

# ---------- aside header: no sex toggle ----------
rep("<div id='plSex' class='seg' role='group' aria-label='Body model'><button data-sex='MALE'>Male</button><button data-sex='FEMALE'>Female</button></div>", "")

# ---------- students ----------
rep("let stSel = null;\n", """let stSel = null;
const MARS = `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><circle cx='10' cy='14' r='6'/><path d='M14.5 9.5 21 3m0 0h-5m5 0v5'/></svg>`;
const VENUS = `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><circle cx='12' cy='9' r='6'/><path d='M12 15v7M9 19h6'/></svg>`;
const SEXICON = { Male: MARS, Female: VENUS };
const stepper = (id, val, min, max, inc, attrs = '') => `<span class='stepper'><button type='button' class='stp' data-dir='-1' aria-label='Decrease'>\\u2212</button><input ${id ? `id='${id}'` : ''} type='number' min='${min}' max='${max}' step='any' data-inc='${inc}' inputmode='decimal' value='${esc(val)}' ${attrs}><button type='button' class='stp' data-dir='1' aria-label='Increase'>+</button></span>`;
""")
rep("<i class='av' data-st='${f ? f.st : ''}'>${esc(initials(s.name))}</i>", "<i class='av' data-st='${f ? f.st : ''}'>${SEXICON[s.sex === 'Female' ? 'Female' : 'Male']}</i>")
rep("{ name: '', sex: '', age: '',", "{ name: '', sex: 'Male', age: '',")

a = s.index("<label>Name<input id='sName'"); b = s.index("<div class='two'>\n      <label>Follow-up after", a)
s = s[:a] + """<div class='nameRow'>
      <label class='grow'>Name<input id='sName' value='${esc(s.name)}' autocomplete='off'></label>
      <div class='fld'><span>Sex</span><div id='sSex' class='seg sx' role='group' aria-label='Sex'>
        <button type='button' data-sx='Male' aria-pressed='${s.sex !== 'Female'}' aria-label='Male' title='Male'>${MARS}</button>
        <button type='button' data-sx='Female' aria-pressed='${s.sex === 'Female'}' aria-label='Female' title='Female'>${VENUS}</button>
      </div></div>
    </div>
    <div class='three'>
      <label>Age<input id='sAge' type='number' min='1' max='120' inputmode='numeric' value='${esc(s.age)}'></label>
      <label>Blood type<select id='sBlood'>${opts(BLOOD, s.blood, 'Unknown')}</select></label>
      <label>Body type<select id='sBody'>${opts(BODY_TYPES, s.bodyType, 'Not set')}</select></label>
    </div>
    <div class='three'>
      <div class='fld'><span>Height (cm)</span>${stepper('sH', s.height, 50, 260, 1, "aria-label='Height in centimeters'")}</div>
      <div class='fld'><span>Weight (kg)</span>${stepper('sW', s.weight, 20, 400, 0.5, "aria-label='Weight in kilograms'")}</div>
      <div class='fld'><span>BMI</span><output id='sBmi' class='bmi'>${esc(bmiText(s.height, s.weight))}</output></div>
    </div>
    """ + s[b:]
# age uses a stepper too (replace the plain input just written)
rep("<label>Age<input id='sAge' type='number' min='1' max='120' inputmode='numeric' value='${esc(s.age)}'></label>",
    "<div class='fld'><span>Age</span>${stepper('sAge', s.age, 1, 120, 1, \"aria-label='Age in years'\")}</div>")
rep("sex: $('#sSex').value,", "sex: (($('#sSex [aria-pressed=true]') || {}).dataset || {}).sx || 'Male',")
rep("$('#stDetail').addEventListener('click', ev => { if (ev.target.id === 'sToday') $('#sStart').value = iso(today()); });",
    "$('#stDetail').addEventListener('click', ev => {\n  if (ev.target.id === 'sToday') $('#sStart').value = iso(today());\n  const b = ev.target.closest('[data-sx]'); if (b) for (const x of $('#sSex').children) x.setAttribute('aria-pressed', String(x === b));\n});")

# ---------- plan page: figures without captions, per-plan sex ----------
rep("const figs = (a, pal, h) => `<div class='figs'><figure>${figure(curSex(), 'FRONT', a.glv, pal, h)}<figcaption>Front</figcaption></figure><figure>${figure(curSex(), 'BACK', a.glv, pal, h)}<figcaption>Back</figcaption></figure></div>`;",
    "const figs = (a, pal, h, sex) => `<div class='figs'>${figure(sex, 'FRONT', a.glv, pal, h)}${figure(sex, 'BACK', a.glv, pal, h)}</div>`;")
rep("const thumb = a => `<span class='pthumb'>${figure(curSex(), 'FRONT', a.glv, 'red', 64)}${figure(curSex(), 'BACK', a.glv, 'red', 64)}</span>`;",
    "const thumb = (a, sex) => `<span class='pthumb'>${figure(sex, 'FRONT', a.glv, 'red', 64)}${figure(sex, 'BACK', a.glv, 'red', 64)}</span>`;")
rep("let plSel = null, plDay = 0, saveT;", "let plSel = null, plOpen = null, plDay = 0, saveT;\nconst planSex = p => p.sex === 'FEMALE' ? 'FEMALE' : p.sex === 'MALE' ? 'MALE' : (state.sex === 'FEMALE' ? 'FEMALE' : 'MALE');")

cut("function renderPlanList() {", "function renderPlan() {", r"""function renderPlanList() {
  const list = filteredPlans(), total = Object.keys(state.planLib).length;
  $('#plCount').textContent = `${list.length} of ${total} plan${total === 1 ? '' : 's'}`;
  $('#plList').innerHTML = list.map(p => {
    const rows = activeRows(p), a = analyse(rows), sx = planSex(p), open = p.id === plOpen;
    return `<div class='pitem' data-open='${open}'><div class='phead'><button class='item' data-id='${esc(p.id)}' ${p.id === plSel ? "aria-current='true'" : ''}>${open ? '' : thumb(a, sx)}<span><b>${esc(p.name || 'Untitled plan')}</b><small>${p.days} day${p.days === 1 ? '' : 's'} \u00b7 ${esc(p.level)} \u00b7 ${esc(p.goal)}</small></span></button>
      <button class='chev' data-toggle='${esc(p.id)}' aria-expanded='${open}' aria-label='${open ? 'Collapse' : 'Expand'} plan'>${ICON("<path d='M6 9l6 6 6-6'/>")}</button></div>`
      + (open ? `<div class='pexp'>${rows.length ? figs(a, 'red', 280, sx) + legend(a, RED) : `<p class='count'>This plan has no exercises yet.</p>`}</div>` : '') + `</div>`;
  }).join('') || `<p class='count'>${total ? 'No plan matches your filters.' : 'No plans yet. Use \u201cNew plan\u201d to create the first one.'}</p>`;
}
""")

cut("function renderEditor() {", "function renderTabs() {", r"""function renderEditor() {
  const p = getPlan(), box = $('#plEditor');
  if (!p) { box.innerHTML = `<div class='empty'><div><b>Select a plan</b>Choose a plan from the library, or create a new one.</div></div>`; return; }
  plDay = Math.min(plDay, p.days - 1);
  const sel = (list, v) => list.map(o => `<option ${o === v ? 'selected' : ''}>${esc(o)}</option>`).join(''), sx = planSex(p);
  box.innerHTML = `<div class='plhead2'><input id='plName' class='plname' value='${esc(p.name)}' placeholder='Plan name' aria-label='Plan name' autocomplete='off'>
      <button id='plDup' class='ibtn' title='Duplicate plan' aria-label='Duplicate plan'>${ICON("<rect x='9' y='9' width='11' height='11' rx='2'/><path d='M5 15V6a2 2 0 0 1 2-2h9'/>")}</button>
      <button id='plDel' class='ibtn danger' title='Delete plan' aria-label='Delete plan'>${ICON("<path d='M4 7h16M10 11v6M14 11v6M6 7l1 12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-12M9 7V4h6v3'/>")}</button></div>
    <div class='fl'><span>Training days per week</span><div class='seg' role='group' aria-label='Training days per week'>${[1, 2, 3, 4, 5, 6, 7].map(n => `<button data-n='${n}' aria-pressed='${p.days === n}'>${n}</button>`).join('')}</div></div>
    <div class='plrow'><label class='fl' style='margin:0'>Level<select id='plLevel'>${sel(LEVELS, p.level)}</select></label><label class='fl' style='margin:0'>Goal<select id='plGoal'>${sel(GOALS, p.goal)}</select></label>
      <div class='fld'><span>Body model</span><div class='seg sx' role='group' aria-label='Body model'><button type='button' data-psx='MALE' aria-pressed='${sx === 'MALE'}' aria-label='Male' title='Male'>${MARS}</button><button type='button' data-psx='FEMALE' aria-pressed='${sx === 'FEMALE'}' aria-label='Female' title='Female'>${VENUS}</button></div></div></div>
    <div id='plTabs' class='daytabs' role='tablist' aria-label='Training days'></div>
    <div id='plDay'></div>`;
  renderTabs(); renderDay();
}
""")

cut("function renderSummary() {", "function renderDay() {", r"""function renderSummary() {
  const p = getPlan(), box = $('#plSum'); if (!p || !box) return;
  const r = p.routines[plDay], a = analyse(r);
  box.innerHTML = r.length ? `${figs(a, 'blue', 120, planSex(p))}<div class='txt'><h3 class='mh'>Muscles worked on day ${plDay + 1}</h3>${legend(a, BLUE)}</div>`
    : `<p class='count' style='margin:0'>Add exercises to see which muscles this day works.</p>`;
}
""")

rep("<label class='mini'>Sets<input data-i='${i}' data-f='sets' type='number' min='1' max='20' inputmode='numeric' value='${esc(x.sets)}'></label>",
    "<div class='mini sets'><span>Sets</span>${stepper('', x.sets, 1, 20, 1, `data-i='${i}' data-f='sets' aria-label='Sets'`)}</div>")

# ---------- plan events ----------
rep("plSel = id; plDay = 0; saveSoon();\n  for (const sid", "plSel = id; plOpen = id; plDay = 0; saveSoon();\n  for (const sid")
rep("$('#plList').addEventListener('click', ev => { const b = ev.target.closest('.item'); if (!b) return; plSel = b.dataset.id; plDay = 0; renderPlanList(); renderEditor(); });",
    "$('#plList').addEventListener('click', ev => {\n  const t = ev.target.closest('.chev');\n  if (t) { plOpen = plOpen === t.dataset.toggle ? null : t.dataset.toggle; renderPlanList(); return; }\n  const b = ev.target.closest('.item'); if (!b) return;\n  plSel = b.dataset.id; plOpen = b.dataset.id; plDay = 0; renderPlanList(); renderEditor();\n});")
rep("$('#plSex').addEventListener('click', ev => { const b = ev.target.closest('[data-sex]'); if (!b) return; state.sex = b.dataset.sex; saveSoon(); renderPlanList(); renderSummary(); });\n", "")
rep("  if (b.dataset.n) { p.days = +b.dataset.n;", "  if (b.dataset.psx) { p.sex = b.dataset.psx; saveSoon(); renderEditor(); renderPlanList(); return; }\n  if (b.dataset.n) { p.days = +b.dataset.n;")
rep("state.planLib[id] = copy; plSel = id; saveSoon(); renderPlan(); return;", "state.planLib[id] = copy; plSel = id; plOpen = id; saveSoon(); renderPlan(); return;")
rep("delete state.planLib[plSel]; plSel = null; saveSoon(); renderPlan(); return;", "delete state.planLib[plSel]; if (plOpen === plSel) plOpen = null; plSel = null; saveSoon(); renderPlan(); return;")

# ---------- stepper handler ----------
rep("function enhanceSearch(el) {", r"""document.addEventListener('click', ev => {
  const b = ev.target.closest('.stp'); if (!b) return;
  const inp = b.parentElement.querySelector('input'), inc = +inp.dataset.inc || 1, dir = +b.dataset.dir;
  const min = inp.min === '' ? -Infinity : +inp.min, max = inp.max === '' ? Infinity : +inp.max, cur = parseFloat(inp.value);
  let v = isNaN(cur) ? (isFinite(min) && min > 0 ? min : 0) : cur + inc * dir;
  v = Math.round(Math.min(max, Math.max(min, v)) * 100) / 100;
  inp.value = v; inp.dispatchEvent(new Event('input', { bubbles: true }));
});
function enhanceSearch(el) {""")

open(p, 'w', encoding='utf-8').write(s)
print('patched', len(s))
