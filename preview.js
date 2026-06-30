/* Apercu FIDELE au PPTX : reproduit img()/fit() du build (image ajustee + fin lisere,
   fond de slide visible autour). Permet de juger le placement reel des captures. */
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const SCREENS = path.join(__dirname, 'assets', 'screens').replace(/\\/g, '/');
const DIMS = {
  'correlation_matrix.png': [1000, 800], 'geocoding_integrity.png': [800, 450],
  'iapero-app-live.png': [1600, 900], 'iapero-recommendation-full.png': [1600, 900],
  'iapero-recommendation-live.png': [1600, 900], 'iapero-similarity-live.png': [1600, 900],
  'iapero-speakeasy-live.png': [1600, 900], 'infrastructures_stacked_bar.png': [1400, 700],
  'maintenance-dashboard-live.png': [1600, 900], 'maintenance-diagnostic-live.png': [1600, 900],
  'monthly_trends.png': [1200, 600], 'quality_completeness.png': [1000, 500],
  'ude-api.png': [1425, 1907], 'ude-dark.png': [1440, 900], 'ude-light.png': [1440, 900],
  'urban-dashboard-live.png': [1600, 900], 'urban-district-selected.png': [1600, 900],
};
const MAP = {
  's05': { i: 'ude-light.png' },
  's07': { a: 'infrastructures_stacked_bar.png', b: 'geocoding_integrity.png' },
  's08': { i: 'ude-api.png' }, 's11': { i: 'correlation_matrix.png' },
  's13': { i: 'maintenance-dashboard-live.png' }, 's15': { i: 'iapero-speakeasy-live.png' },
  's16': { i: 'iapero-recommendation-full.png' }, 's17': { i: 'iapero-similarity-live.png' },
  's21': { a0: 'urban-dashboard-live.png', a1: 'urban-district-selected.png', a2: 'ude-dark.png' },
  's22': { a0: 'maintenance-diagnostic-live.png', a1: 'monthly_trends.png', a2: 'quality_completeness.png' },
  's23': { a0: 'iapero-app-live.png', a1: 'iapero-recommendation-live.png' },
};
function fit(name, b) {
  const d = DIMS[name], ar = d[0] / d[1], bar = b.w / b.h; let w, h;
  if (ar > bar) { w = b.w; h = b.w / ar; } else { h = b.h; w = b.h * ar; }
  return { x: b.x + (b.w - w) / 2, y: b.y + (b.h - h) / 2, w, h };
}
function inject(html, map) {
  return html.replace(/<div class="placeholder" id="([^"]+)" style="([^"]+)"><\/div>/g, (m, id, style) => {
    const img = map[id]; if (!img) return m;
    const g = s => parseFloat((style.match(new RegExp(s + ':([0-9.]+)pt')) || [])[1]);
    const b = { x: g('left'), y: g('top'), w: g('width'), h: g('height') };
    const f = fit(img, b);
    return `<img src="file:///${SCREENS}/${img}" style="position:absolute;left:${f.x}pt;top:${f.y}pt;width:${f.w}pt;height:${f.h}pt;border:1px solid #ddd;box-sizing:border-box;">`;
  });
}
(async () => {
  const dir = path.join(__dirname, 'slides');
  const out = path.join(__dirname, '.preview'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 1.5 });
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html')).sort()) {
    const key = f.replace('.html', '');
    let html = fs.readFileSync(path.join(dir, f), 'utf8');
    if (MAP[key]) html = inject(html, MAP[key]);
    const tmp = path.join(out, f); fs.writeFileSync(tmp, html);
    await pg.goto('file:///' + tmp.replace(/\\/g, '/'));
    await pg.screenshot({ path: path.join(out, key + '.png') });
  }
  await b.close(); console.log('preview done');
})();
