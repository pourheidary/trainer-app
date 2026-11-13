import fs from 'fs';
const base = '/home/claude/mm/MuscleMap-main/packages/assets/';
const mods = {
  MALE_FRONT: await import(base + 'src/male-front.ts'),
  MALE_BACK: await import(base + 'src/male-back.ts'),
  FEMALE_FRONT: await import(base + 'src/female-front.ts'),
  FEMALE_BACK: await import(base + 'src/female-back.ts'),
};
const out = { MALE: {}, FEMALE: {} }, img = { MALE: {}, FEMALE: {} };
for (const [k, m] of Object.entries(mods)) {
  const d = m[k];
  const [sex, view] = k.split('_');
  out[sex][view] = { viewBox: d.viewBox, centerX: d.centerX, outline: d.outline.map(o => ({ side: o.side, d: o.d })), muscles: d.muscles.map(x => ({ g: x.group, s: x.side, d: x.d })) };
  const file = base + 'bodies/' + sex.toLowerCase() + '-' + view.toLowerCase() + '.webp';
  img[sex][view] = 'data:image/webp;base64,' + fs.readFileSync(file).toString('base64');
  const groups = [...new Set(d.muscles.map(x => x.group))];
  console.log(k, d.viewBox, 'centerX', d.centerX, 'outline', d.outline.length, 'muscles', d.muscles.length, groups.join(','));
}
fs.writeFileSync('/home/claude/bodies.js', 'const BODIES = ' + JSON.stringify(out) + ';\nconst BODY_IMG = ' + JSON.stringify(img) + ';\n');
console.log('bytes', fs.statSync('/home/claude/bodies.js').size);
