/* Generateur PPTX soutenance Bloc 1 & 2 (RNCP40875).
   Pipeline : slide definie en HTML absolu (720x405 pt) → html2pptx parse le DOM
   → coordonnees pt injectees dans pptxgenjs → .pptx final.
   Les placeholders <div class="placeholder"> servent de points d'ancrage pour que
   la callback post() place images et boutons (API pptxgenjs) au bon endroit.
   20 slides + 3 annexes backup. Charte EFREI. Binome Adam & Emilien. */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');

const ROOT = __dirname;
const SLIDES = path.join(ROOT, 'slides');
const ASSETS = path.join(ROOT, 'assets');
const SCREENS = path.join(ASSETS, 'screens');
fs.mkdirSync(SLIDES, { recursive: true });

// ---- charte EFREI (extraite de efrei.fr) ----
// bleu #163767 primaire - rose #FF43B8 accent signature - navy #051832 fonds sombres - bleu logo #0C78B4
const C = {
  bleu: '#163767', bleuD: '#051832', rouge: '#FF43B8', teal: '#0C78B4',
  texte: '#212121', gris: '#5A6B82', grisclr: '#F4F4F4', bord: '#D7DEE8',
  vert: '#0C78B4', blanc: '#FFFFFF', bleuClair: '#E9EDF5', rougeClair: '#FDEEF7',
  tealClair: '#EAF4FB', bleuTxt: '#A9B8D6',
};
const hex = s => s.replace('#', '');

const LAUNCH = {
  urban: 'file:///C:/Users/adamb/soutenance-m1/demos/launch_urban.pyw',
  maint: 'file:///C:/Users/adamb/soutenance-m1/demos/launch_maintenance.pyw',
  iapero: 'file:///C:/Users/adamb/soutenance-m1/demos/launch_iapero.pyw',
};
const REPO = {
  urban: 'https://github.com/Adam-Blf/urban-data-explorer',
  maint: 'https://github.com/Adam-Blf/maintenance-predictive-industrielle',
  iapero: 'https://github.com/Adam-Blf/ia-pero',
};
// Dimensions source des images (px) : alimentent fit() pour preserver le ratio
// sans avoir a ouvrir le fichier au runtime (acces disque evite).
const DIMS = {
  'Logo-Efrei-Blanc.png': [3001, 1501],
  'correlation_matrix.png': [1000, 800], 'geocoding_integrity.png': [800, 450],
  'iapero-app-live.png': [1600, 900], 'iapero-recommendation-full.png': [1600, 900],
  'iapero-recommendation-live.png': [1600, 900], 'iapero-similarity-live.png': [1600, 900],
  'iapero-speakeasy-live.png': [1600, 900], 'infrastructures_stacked_bar.png': [1400, 700],
  'maintenance-dashboard-live.png': [1600, 900], 'maintenance-diagnostic-live.png': [1600, 900],
  'monthly_trends.png': [1200, 600], 'quality_completeness.png': [1000, 500],
  'ude-api.png': [1425, 1907], 'ude-dark.png': [1440, 900], 'ude-light.png': [1440, 900],
  'urban-dashboard-live.png': [1600, 900], 'urban-district-selected.png': [1600, 900],
};

// ---- HTML helpers (positionnement absolu, unites pt, canvas 720x405) ----
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function box(l, t, w, h, style = '') {
  return `<div style="position:absolute;left:${l}pt;top:${t}pt;width:${w}pt;height:${h}pt;${style}"></div>`;
}
function txt(l, t, w, h, html, o = {}) {
  const { size = 13, color = C.texte, bold = false, italic = false, align = 'left', lh = 1.15, tag = 'p' } = o;
  const st = `position:absolute;left:${l}pt;top:${t}pt;width:${w}pt;height:${h}pt;margin:0;`
    + `font-size:${size}pt;color:${color};font-weight:${bold ? 700 : 400};`
    + `font-style:${italic ? 'italic' : 'normal'};text-align:${align};line-height:${lh};`;
  return `<${tag} style="${st}">${html}</${tag}>`;
}
function bullets(l, t, w, h, items, o = {}) {
  const { size = 13, color = C.texte, gap = 7 } = o;
  const lis = items.map(it => {
    let inner;
    if (Array.isArray(it)) inner = `<b>${esc(it[0])}</b>${esc(it[1])}`;
    else inner = esc(it);
    return `<li style="margin:0 0 ${gap}pt 0;line-height:1.12;">${inner}</li>`;
  }).join('');
  const st = `position:absolute;left:${l}pt;top:${t}pt;width:${w}pt;height:${h}pt;margin:0;`
    + `padding-left:14pt;font-size:${size}pt;color:${color};`;
  return `<ul style="${st}">${lis}</ul>`;
}
function divbox(l, t, w, h, o = {}) {
  const { bg, border, bl, radius } = o;
  let s = `position:absolute;left:${l}pt;top:${t}pt;width:${w}pt;height:${h}pt;`;
  if (bg) s += `background:${bg};`;
  if (border) s += `border:1px solid ${border};`;
  if (bl) s += `border-left:${bl[1]}pt solid ${bl[0]};`;
  if (radius) s += `border-radius:${radius}pt;`;
  return `<div style="${s}"></div>`;
}
function ph(l, t, w, h, id) {
  return `<div class="placeholder" id="${id}" style="position:absolute;left:${l}pt;top:${t}pt;width:${w}pt;height:${h}pt;background:${C.grisclr};"></div>`;
}
function badge(l, t, code, label, fill = C.rouge) {
  const w = 30 + 5.4 * (code.length + label.length);
  return divbox(l, t, w, 20, { bg: fill, radius: 10 })
    + txt(l + 8, t + 4.5, w - 12, 14, `<b>${esc(code)}</b>&nbsp;&nbsp;${esc(label)}`, { size: 10.5, color: C.blanc });
}
function header(kicker, title, color = C.bleu) {
  return divbox(0, 0, 720, 56, { bg: color })
    + divbox(0, 56, 720, 3, { bg: C.rouge })
    + txt(28, 9, 560, 14, esc(kicker), { size: 11, color: C.blanc, bold: true })
    + txt(28, 24, 560, 24, esc(title), { size: 21, color: C.blanc, bold: true });
}
function footer(idx) {
  return txt(28, 391, 480, 12, 'Adam Beloucif &amp; Émilien Morice  -  RNCP40875  -  EFREI M1 DE&amp;IA', { size: 8.5, color: C.gris })
    + txt(640, 391, 60, 12, `${idx} / 20`, { size: 8.5, color: C.gris, align: 'right' });
}
// bande "preuve de competence" en bas de slide projet (formule guide : C.x demontree par <preuve>)
function proofbar(lead, proof, color, idx, hasBtn = false) {
  const tw = hasBtn ? 480 : 600;
  return divbox(0, 369, 720, 23, { bg: color })
    + txt(28, 374, tw, 14, `<b>✓ ${lead} -</b> ${proof}`, { size: 10.5, color: C.blanc })
    + txt(650, 374, 46, 14, `${idx} / 20`, { size: 10.5, color: C.blanc, bold: true, align: 'right' });
}
function wrap(inner, bodyBg = C.blanc) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  html{background:${bodyBg};} *{box-sizing:border-box;}
  body{width:720pt;height:405pt;margin:0;padding:0;background:${bodyBg};font-family:Arial,Helvetica,sans-serif;position:relative;display:flex;}
  ul{list-style:square;} li::marker{color:${C.rouge};}
  </style></head><body>${inner}</body></html>`;
}

// ---- definitions des slides ----
const slides = [];
function S(inner, bg, post) { slides.push({ html: wrap(inner, bg), post }); }

function fit(name, b) {
  const d = DIMS[name]; const ar = d[0] / d[1], bar = b.w / b.h;
  let w, h;
  if (ar > bar) { w = b.w; h = b.w / ar; } else { h = b.h; w = b.h * ar; }
  return { x: b.x + (b.w - w) / 2, y: b.y + (b.h - h) / 2, w, h };
}
function img(slide, name, b, border = true) {
  const f = fit(name, b);
  if (border) slide.addShape('rect', { x: f.x - 0.03, y: f.y - 0.03, w: f.w + 0.06, h: f.h + 0.06, fill: { color: 'FFFFFF' }, line: { color: hex(C.bord), width: 1 } });
  slide.addImage({ path: path.join(SCREENS, name), x: f.x, y: f.y, w: f.w, h: f.h });
}
let PPTX;
function btn(slide, text, url, x, y, w, h, fill, fg = C.blanc) {
  slide.addText(text, {
    x, y, w, h, shape: PPTX.shapes.ROUNDED_RECTANGLE, rectRadius: 0.07,
    fill: { color: hex(fill) }, color: hex(fg), bold: true, fontSize: 12,
    align: 'center', valign: 'middle', fontFace: 'Arial', hyperlink: { url },
  });
}
function caption(slide, t, x, y, w) {
  slide.addText(t, { x, y, w, h: 0.28, fontSize: 9, italic: true, color: hex(C.gris), align: 'center', fontFace: 'Arial' });
}
// bouton "Lancer la demo" loge dans la bande de preuve (slides de demo)
function bandBtn(slide, url, color) {
  slide.addText('▶  Lancer la démo', {
    x: 500 / 72, y: 370.5 / 72, w: 140 / 72, h: 19 / 72, shape: PPTX.shapes.ROUNDED_RECTANGLE,
    rectRadius: 0.06, fill: { color: 'FFFFFF' }, color: hex(color), bold: true, fontSize: 9.5,
    align: 'center', valign: 'middle', fontFace: 'Arial', hyperlink: { url },
  });
}
// badge "DEMO LIVE - 90 s" toujours positionne en haut-droite des slides de demo (8, 13, 16)
function demoBadge() {
  return divbox(540, 64, 152, 24, { bg: C.rouge, radius: 12 })
    + txt(540, 69, 152, 14, 'DÉMO LIVE - 90 s', { size: 11, color: C.blanc, bold: true, align: 'center' });
}

// ===== SLIDE 1 - Titre =====
{
  const inner = divbox(0, 0, 12, 405, { bg: C.rouge })
    + txt(50, 132, 600, 22, 'Soutenance de fin d’études', { size: 17, color: C.bleuTxt })
    + txt(48, 158, 640, 56, 'Bloc 1 &amp; 2  -  RNCP40875', { size: 38, color: C.blanc, bold: true })
    + txt(50, 224, 620, 20, 'Expert en Ingénierie de Données  -  de la donnée brute à la décision', { size: 14, color: C.bleuTxt })
    + divbox(50, 252, 230, 3, { bg: C.rouge })
    + txt(50, 268, 620, 28, 'Adam Beloucif  &amp;  Émilien Morice', { size: 20, color: C.blanc, bold: true })
    + txt(50, 300, 620, 18, 'M1 Data Engineering &amp; IA  -  EFREI Villejuif  -  Session 2026-2027', { size: 13, color: C.bleuTxt });
  S(inner, C.bleuD, null);
}

// ===== SLIDE 2 - Contexte =====
{
  let inner = header('INTRODUCTION', 'Contexte & problématique');
  inner += txt(28, 74, 660, 22, 'Fil rouge  -  transformer la donnée en décision', { size: 18, color: C.bleu, bold: true });
  inner += txt(28, 100, 660, 18, 'Trois projets, trois maillons complémentaires d’une même chaîne de valeur data.', { size: 13, color: C.gris });
  const cards = [
    ['1 - Data Engineering', 'Construire l’architecture qui collecte, stocke et expose la donnée.', C.bleu],
    ['2 - Data Science', 'Modéliser pour prédire et outiller la décision métier.', C.teal],
    ['3 - IA Générative', 'Comprendre le langage naturel et générer une réponse personnalisée.', C.rouge],
  ];
  let x = 28;
  for (const [t, d, col] of cards) {
    inner += divbox(x, 140, 210, 150, { bg: C.grisclr, border: C.bord });
    inner += divbox(x, 140, 210, 7, { bg: col });
    inner += txt(x + 14, 158, 184, 22, t, { size: 15, color: col, bold: true });
    inner += txt(x + 14, 190, 184, 90, d, { size: 13, color: C.texte, lh: 1.25 });
    x += 222;
  }
  inner += txt(28, 312, 664, 50, 'Problème commun  -  une donnée non exploitée n’a aucune valeur. Chaque projet répond à un besoin métier concret, avec des preuves techniques vérifiables.', { size: 13, color: C.texte, italic: true, lh: 1.25 });
  inner += footer(2);
  S(inner, C.blanc, null);
}

// ===== SLIDE 3 - Vue d'ensemble + boutons LANCER =====
{
  let inner = header('INTRODUCTION', 'Vue d’ensemble des 3 projets');
  const cards = [
    ['Urban Data Explorer', 'Bloc 1  -  C1.1 → C2.4', 'Plateforme data du logement parisien : 83 sources Open Data, architecture médaillon, PostgreSQL étoile, Cassandra, Kafka, API FastAPI sécurisée, dashboard MapLibre DSFR.', C.bleu],
    ['Maintenance Prédictive', 'Bloc 2  -  C3.1 → C4.3', 'Prédiction de panne machine sous 24 h depuis capteurs IoT : 4 modèles comparés (dont Deep Learning), mesure CO2 CodeCarbon, dashboard décisionnel Streamlit.', C.teal],
    ['L’IA Pero', 'Bloc 2  -  C5.1 → C5.3', 'Recommandation de cocktails par IA sémantique : SBERT 384 dims, similarité cosinus, guardrail 0.35, RAG + Gemini avec cache, interface Streamlit Speakeasy.', C.rouge],
  ];
  let y = 70;
  for (const [t, c, d, col] of cards) {
    inner += divbox(28, y, 664, 96, { bg: C.grisclr, border: C.bord });
    inner += divbox(28, y, 7, 96, { bg: col });
    inner += txt(44, y + 10, 360, 22, t, { size: 17, color: col, bold: true });
    inner += txt(44, y + 34, 360, 14, c, { size: 11, color: C.gris, bold: true });
    inner += txt(44, y + 52, 470, 40, d, { size: 11.5, color: C.texte, lh: 1.1 });
    inner += ph(540, y + 28, 138, 40, 'btn_' + col);
    y += 106;
  }
  inner += footer(3);
  S(inner, C.blanc, (slide, P) => {
    const cols = [[C.bleu, LAUNCH.urban, 70], [C.teal, LAUNCH.maint, 176], [C.rouge, LAUNCH.iapero, 282]];
    for (const [col, url, yy] of cols) {
      btn(slide, '▶  Lancer la démo', url, 540 / 72, (yy + 28) / 72, 138 / 72, 40 / 72, col);
    }
  });
}

// ===== SLIDE 4 - Contributions =====
{
  let inner = header('INTRODUCTION', 'Contributions individuelles');
  inner += txt(28, 68, 664, 16, 'Présentation collective, évaluation individualisée. Répartition par projet :', { size: 13, color: C.gris });
  const rows = [
    ['Projet', 'Adam Beloucif', 'Émilien Morice'],
    ['Urban Data Explorer', 'Architecture data, API sécurisée, modèle PG/Cassandra, pipeline', 'Sourcing & qualité des 83 sources, front cartographique, data prep'],
    ['Maintenance Prédictive', 'Modélisation 4 modèles, sélection XGBoost, dashboard Streamlit', 'EDA, préparation des données, analyse des corrélations'],
    ['L’IA Pero', 'Backend RAG/SBERT, guardrail sémantique, cache, évaluation', 'Référentiel cocktails, scénarios d’usage, tests des seuils'],
  ];
  const cx = [28, 188, 446]; const cw = [158, 256, 246];
  const rh = [26, 56, 56, 56]; let y = 92;
  rows.forEach((row, ri) => {
    const head = ri === 0;
    row.forEach((cell, ci) => {
      const bg = head ? C.bleu : (ri % 2 ? C.grisclr : C.blanc);
      inner += divbox(cx[ci], y, cw[ci], rh[ri], { bg, border: C.bord });
      inner += txt(cx[ci] + 8, y + (head ? 6 : 8), cw[ci] - 14, rh[ri] - 10,
        esc(cell), { size: head ? 12.5 : 11, color: head ? C.blanc : C.texte, bold: head || ci === 0, lh: 1.12 });
    });
    y += rh[ri];
  });
  inner += txt(28, 320, 664, 30, 'Chaque membre porte au moins un choix technique et en connaît les limites (critère d’individualisation du jury).', { size: 11.5, color: C.gris, italic: true });
  inner += footer(4);
  S(inner, C.blanc, null);
}

// ===== SLIDE 5 - P1 Besoin & archi =====
{
  let inner = header('PROJET 1 - URBAN DATA EXPLORER', 'Besoin & architecture', C.bleu);
  inner += bullets(28, 72, 300, 230, [
    ['Besoin métier : ', 'explorer le marché du logement parisien en croisant 83 sources Open Data.'],
    ['Architecture médaillon : ', 'Bronze (brut) → Silver (normalisé, géocodé) → Gold (datamarts).'],
    ['Stockage dual : ', 'PostgreSQL en étoile pour l’analytique, Cassandra query-first pour le streaming.'],
    ['Exposition : ', 'API FastAPI sécurisée → dashboard React / MapLibre charte DSFR.'],
  ], { size: 14, gap: 13 });
  inner += ph(338, 72, 356, 248, 'i');
  // Légende échelle choroplèthe EFREI bleu → rose (5 segments solides, html2pptx compat)
  const _scaleStops = ['#163767', '#0C78B4', '#5C31A0', '#C03890', '#FF43B8'];
  const _sw = 356 / _scaleStops.length;
  _scaleStops.forEach((col, i) => { inner += divbox(338 + i * _sw, 325, _sw, 14, { bg: col }); });
  inner += txt(338, 341, 178, 11, 'Bas - prix m²', { size: 7.5, color: C.gris });
  inner += txt(516, 341, 178, 11, 'Élevé - prix m²', { size: 7.5, color: C.gris, align: 'right' });
  inner += proofbar('C1.3 Data Lake démontrée', 'architecture médaillon Bronze → Silver → Gold en Parquet partitionné (etl/, data/)', C.bleu, 5);
  S(inner, C.blanc, (slide, P) => {
    const p = P.find(z => z.id === 'i');
    img(slide, 'ude-light.png', p);
    caption(slide, 'Dashboard Urban Data Explorer - choroplèthe prix m² - échelle EFREI bleu → rose', p.x, p.y + p.h + 0.02, p.w);
    // Gradient natif PPTX pour la légende
    const lx = p.x, ly = p.y + p.h + 0.08, lw = p.w, lh = 0.18;
    slide.addShape('rect', { x: lx, y: ly, w: lw, h: lh, fill: { type: 'gradient', stops: [{ position: 0, color: '163767' }, { position: 33, color: '0C78B4' }, { position: 66, color: '8B35B5' }, { position: 100, color: 'FF43B8' }], angle: 0 }, line: { color: 'D7DEE8', width: 0.5 } });
  });
}

// ===== SLIDE 6 - P1 Bases de donnees =====
{
  let inner = header('PROJET 1 - URBAN DATA EXPLORER', 'Bases de données - SQL vs NoSQL', C.bleu);
  inner += badge(28, 66, 'C1.1', 'Relationnelle', C.rouge) + badge(190, 66, 'C1.2', 'NoSQL', C.rouge);
  inner += divbox(28, 96, 322, 250, { bg: C.grisclr, border: C.bord }) + divbox(28, 96, 322, 28, { bg: C.bleu });
  inner += txt(40, 101, 300, 18, 'PostgreSQL - schéma en étoile', { size: 14, color: C.blanc, bold: true });
  inner += bullets(40, 132, 300, 205, [
    'Fait + dimensions (arrondissement, temps), FK et clés composées',
    'Index sur les axes de requête → p95 < 4 ms en jointure',
    'Contraintes NOT NULL, intégrité référentielle',
    'Test de charge : scripts/test_load_postgres.py',
    'Besoin : agrégats analytiques par arrondissement x mois',
  ], { size: 12.5, gap: 9 });
  inner += divbox(370, 96, 322, 250, { bg: C.grisclr, border: C.bord }) + divbox(370, 96, 322, 28, { bg: C.teal });
  inner += txt(382, 101, 300, 18, 'Cassandra - query-first', { size: 14, color: C.blanc, bold: true });
  inner += bullets(382, 132, 300, 205, [
    'Partition par event_type, clustering event_time DESC',
    'TTL 7 jours → la donnée chaude expire seule',
    'Deux patterns d’accès : par type et par arrondissement',
    'Adapté aux événements semi-structurés à forte vélocité',
    'PG aurait imposé un schéma rigide + des purges manuelles',
  ], { size: 12.5, gap: 9 });
  inner += proofbar('C1.1 & C1.2 démontrées', 'schéma étoile postgres/init.sql (+ test de charge) - modélisation query-first cassandra/schema.cql', C.bleu, 6);
  S(inner, C.blanc, null);
}

// ===== SLIDE 7 - P1 Data Lake & streaming =====
{
  let inner = header('PROJET 1 - URBAN DATA EXPLORER', 'Data Lake & streaming temps réel', C.bleu);
  inner += badge(28, 66, 'C1.3', 'Data Lake', C.rouge) + badge(170, 66, 'C2.2', 'Streaming', C.rouge);
  inner += bullets(28, 100, 320, 240, [
    ['83 sources / 4 familles : ', 'CSV, GeoJSON, API → atterrissage Bronze en Parquet.'],
    ['Silver : ', 'normalisation des codes, géocodage point-in-polygon IRIS.'],
    ['Gold : ', 'datamarts dashboard & timeline, format colonnaire optimisé.'],
    ['Kafka temps réel : ', 'flux public Vélib GBFS → consommateur Cassandra, événement par événement.'],
    ['Micro-batch : ', 'streaming/microbatch.py → fenêtres tumbling 10 s.'],
  ], { size: 13, gap: 11 });
  inner += ph(360, 70, 334, 150, 'a');
  inner += ph(360, 232, 334, 110, 'b');
  inner += proofbar('C1.3 - C2.2 - C2.3 démontrées', '83 sources Parquet - Kafka + micro-batch 10 s (streaming/) - fusion Polars DVF+INSEE réels (etl/)', C.bleu, 7);
  S(inner, C.blanc, (slide, P) => {
    img(slide, 'infrastructures_stacked_bar.png', P.find(z => z.id === 'a'));
    img(slide, 'geocoding_integrity.png', P.find(z => z.id === 'b'));
  });
}

// ===== SLIDE 8 - P1 API + DEMO =====
{
  let inner = header('PROJET 1 - URBAN DATA EXPLORER', 'API & sécurité', C.bleu);
  inner += badge(28, 66, 'C2.1', 'API sécurisée', C.rouge);
  inner += demoBadge();
  inner += bullets(28, 98, 300, 190, [
    ['JWT HS256 : ', 'secret en variable d’env, rôles viewer / admin.'],
    ['401 vs 403 : ', 'authentification et autorisation différenciées.'],
    ['Quotas par IP : ', '120 anonyme / 600 authentifié → 429 si dépassement.'],
    ['Swagger : ', 'documentation interactive live sur /docs.'],
    ['CORS + RGPD : ', 'restreint au front, Open Data uniquement.'],
  ], { size: 12.5, gap: 8 });
  inner += txt(28, 300, 300, 50, 'Scénario : dashboard → clic 11e arr. → comparaison 11e/16e → /docs → curl token → 403 sans rôle admin.', { size: 11, color: C.texte, italic: true, lh: 1.2 });
  inner += ph(360, 98, 334, 240, 'i');
  inner += proofbar('C2.1 démontrée', 'API FastAPI JWT + quotas 120/600 → 429 (api/security.py, démo curl 403)', C.bleu, 8, true);
  S(inner, C.blanc, (slide, P) => {
    img(slide, 'ude-api.png', P.find(z => z.id === 'i'));
    bandBtn(slide, LAUNCH.urban, C.bleu);
  });
}

// ===== SLIDE 9 - P1 Perf & resilience =====
{
  let inner = header('PROJET 1 - URBAN DATA EXPLORER', 'Performance, résilience & limites', C.bleu);
  inner += badge(28, 66, 'C1.4', 'Résilience', C.rouge) + badge(165, 66, 'C2.4', 'Perf pipelines', C.rouge);
  inner += bullets(28, 100, 664, 160, [
    ['Métriques pipeline : ', 'etl/metrics.py → durée, lignes, octets, lignes/sec exposés via GET /pipeline/metrics.'],
    ['Optimisations : ', 'Polars (Rust) vs pandas, Parquet colonnaire, lru_cache sur le géocodage inverse.'],
    ['Résilience testée : ', 'scripts/test_resilience.py : kill conteneur Postgres → fallback parquet → restart.'],
    ['Observabilité : ', 'prometheus_client + GET /metrics, dashboards Prometheus / Grafana (profil monitoring).'],
  ], { size: 14, gap: 11 });
  inner += divbox(28, 270, 664, 96, { bg: C.rougeClair, border: C.rouge });
  inner += txt(42, 280, 600, 18, 'Limites assumées & roadmap', { size: 15, color: C.rouge, bold: true });
  inner += txt(42, 304, 636, 54, 'Démo mono-nœud (replication_factor 1), pas de haute disponibilité réelle. Chemin documenté vers un cluster 3 nœuds + réplication Cassandra linéaire + API stateless réplicable.', { size: 13, color: C.texte, lh: 1.25 });
  inner += proofbar('C1.4 & C2.4 démontrées', 'résilience testée - observabilité Prometheus / Grafana - qualité de données (GET /pipeline/quality) - recherche pgvector', C.bleu, 9);
  S(inner, C.blanc, null);
}

// ===== SLIDE 10 - P2 Question metier =====
{
  let inner = header('PROJET 2 - MAINTENANCE PRÉDICTIVE', 'Question métier & stratégie IA', C.teal);
  inner += badge(28, 66, 'C4.1', 'Stratégie d’intégration IA', C.teal);
  inner += bullets(28, 100, 380, 180, [
    ['Problème : ', 'une panne non planifiée coûte 5 à 50 k€/h d’arrêt de ligne.'],
    ['Corrective : ', 'on répare après la casse → coût maximal, imprévu.'],
    ['Préventive : ', 'entretien calendaire → sur-maintenance, pièces gaspillées.'],
    ['Prédictive (cible) : ', 'prédire la panne sous 24 h → intervenir au bon moment.'],
  ], { size: 14, gap: 13 });
  inner += divbox(430, 100, 262, 210, { bg: C.grisclr, border: C.bord });
  inner += txt(444, 110, 234, 18, 'Feuille de route', { size: 14, color: C.teal, bold: true });
  inner += bullets(444, 136, 234, 165, [
    'Capteurs IoT existants → collecte',
    'Modèle prédictif + seuil de décision',
    'Alerte responsable maintenance',
    'Boucle de réentraînement périodique',
  ], { size: 13, gap: 14 });
  inner += txt(28, 300, 380, 20, 'Coût corrective ~100 €/h → prédictive ~20 €/h', { size: 14, color: C.teal, bold: true });
  inner += proofbar('C4.1 démontrée', 'stratégie d’intégration IA : du correctif au prédictif, feuille de route métier réalisable', C.teal, 10);
  S(inner, C.blanc, null);
}

// ===== SLIDE 11 - P2 Donnees & EDA =====
{
  let inner = header('PROJET 2 - MAINTENANCE PRÉDICTIVE', 'Données & analyse exploratoire', C.teal);
  inner += badge(28, 66, 'C3.1', 'Préparation', C.teal) + badge(165, 66, 'C3.3', 'EDA', C.teal);
  inner += bullets(28, 100, 326, 250, [
    ['Dataset : ', 'Kaggle industrial_machine_maintenance - 24 042 lignes x 15 variables.'],
    ['Cible : ', 'failure_within_24h (classe rare → déséquilibre).'],
    ['Nettoyage : ', 'imputation médiane (fit train), winsorisation des outliers capteurs.'],
    ['Insight clé : ', 'vibration_rms et temperature_motor sont les plus corrélées à la panne.'],
    ['Cohérence physique : ', 'l’usure mécanique génère vibration ET échauffement.'],
  ], { size: 13, gap: 10 });
  inner += ph(366, 70, 328, 268, 'i');
  inner += proofbar('C3.1 & C3.3 démontrées', 'préparation fit-train (imputation, scaling) - EDA distributions, corrélations, déséquilibre de classes', C.teal, 11);
  S(inner, C.blanc, (slide, P) => {
    const p = P.find(z => z.id === 'i'); img(slide, 'correlation_matrix.png', p);
    caption(slide, 'Matrice de corrélation des variables capteurs', p.x, p.y + p.h + 0.02, p.w);
  });
}

// ===== SLIDE 12 - P2 Modeles (table) =====
{
  let inner = header('PROJET 2 - MAINTENANCE PRÉDICTIVE', 'Modèles & évaluation comparative', C.teal);
  inner += badge(28, 66, 'C4.2', 'Modèles', C.teal) + badge(150, 66, 'C4.3', 'Éval + écoresponsabilité', C.teal);
  inner += ph(28, 96, 664, 132, 't');
  inner += bullets(28, 240, 664, 120, [
    ['Sélection : ', 'score = F1 − 0.5 x σ(F1 en cross-validation) → performance ET stabilité.'],
    ['Anti-leakage : ', 'pipeline sklearn fit sur train uniquement (ADR dédié).'],
    ['Écoresponsabilité : ', 'CodeCarbon - XGBoost 6.1 mg < RF 8.2 mg pour de meilleures perfs.'],
  ], { size: 12.5, gap: 7 });
  inner += proofbar('C4.2 & C4.3 démontrées', '4 modèles testés et justifiés - évaluation comparative + écoresponsabilité CodeCarbon', C.teal, 12);
  S(inner, C.blanc, (slide, P) => {
    const p = P.find(z => z.id === 't');
    const head = ['Modèle', 'F1', 'ROC-AUC', 'Temps', 'CO2'].map(t => ({ text: t, options: { fill: { color: hex(C.teal) }, color: 'FFFFFF', bold: true } }));
    const rows = [
      ['LogReg (baseline)', '0.747', '0.959', '3.2 s', '0.3 mg'],
      ['Random Forest', '0.863', '0.992', '45 s', '8.2 mg'],
      ['XGBoost (retenu)', '0.886', '0.995', '35 s', '6.1 mg'],
      ['MLP 64-32-16 (DL)', '0.836', '0.984', '18 s', '3.8 mg'],
    ];
    const body = rows.map((r, i) => r.map((c, ci) => {
      const ret = i === 2;
      return { text: c, options: { fill: { color: ret ? 'E5F3EF' : (i % 2 ? 'F6F6F6' : 'FFFFFF') }, color: ret ? hex(C.teal) : hex(C.texte), bold: ret || ci === 0 } };
    }));
    slide.addTable([head, ...body], { x: p.x, y: p.y, w: p.w, h: p.h, colW: [3.3, 1.3, 1.5, 1.3, 1.3], border: { pt: 0.75, color: 'DDDDDD' }, align: 'center', valign: 'middle', fontSize: 13, fontFace: 'Arial' });
  });
}

// ===== SLIDE 13 - P2 Dashboard + DEMO =====
{
  let inner = header('PROJET 2 - MAINTENANCE PRÉDICTIVE', 'Dashboard décisionnel', C.teal);
  inner += badge(28, 66, 'C3.2', 'Dashboard interactif', C.teal);
  inner += demoBadge();
  inner += bullets(28, 98, 300, 180, [
    ['Cible : ', 'responsable maintenance, pas le data scientist.'],
    ['Simulation : ', 'sliders capteurs → prédiction temps réel + probabilité.'],
    ['Explication : ', 'top variables influentes en langage métier.'],
    ['Distinct : ', 'des visuels EDA du rapport (consigne du sujet).'],
  ], { size: 13, gap: 10 });
  inner += txt(28, 296, 300, 48, 'Scénario : vibration haute + température haute → risque élevé → feature importance.', { size: 11, color: C.texte, italic: true, lh: 1.2 });
  inner += ph(360, 98, 334, 238, 'i');
  inner += proofbar('C3.2 démontrée', 'dashboard décisionnel interactif Streamlit : simulation scénario + prédiction temps réel', C.teal, 13, true);
  S(inner, C.blanc, (slide, P) => {
    img(slide, 'maintenance-dashboard-live.png', P.find(z => z.id === 'i'));
    bandBtn(slide, LAUNCH.maint, C.teal);
  });
}

// ===== SLIDE 14 - P2 Limites =====
{
  let inner = header('PROJET 2 - MAINTENANCE PRÉDICTIVE', 'Limites & bonus réalisés', C.teal);
  inner += divbox(28, 80, 322, 250, { bg: C.rougeClair, border: C.rouge });
  inner += txt(42, 90, 300, 18, 'Limites', { size: 16, color: C.rouge, bold: true });
  inner += bullets(42, 120, 300, 200, [
    'Données simulées (pas de bruit capteur réel)',
    'Pas de dimension temporelle exploitée',
    'Un LSTM sur séquences serait la suite logique',
    'Dérive en production → monitoring + réentraînement',
  ], { size: 13.5, gap: 15 });
  inner += divbox(370, 80, 322, 250, { bg: C.tealClair, border: C.teal });
  inner += txt(384, 90, 300, 18, 'Bonus déjà réalisés', { size: 16, color: C.teal, bold: true });
  inner += bullets(384, 120, 300, 200, [
    'Multiclass (type de panne) + régression RUL',
    'Prédiction conforme - garantie de couverture 90%',
    'Drift PSI + traçabilité MLflow',
    'Robustesse bruit capteur + calibration',
  ], { size: 13.5, gap: 15 });
  inner += proofbar('Recul professionnel', 'limites assumées (données simulées, pas de temporel) + bonus réalisés - valorisé par le jury', C.teal, 14);
  S(inner, C.blanc, null);
}

// ===== SLIDE 15 - P3 Cas d'usage =====
{
  let inner = header('PROJET 3 - L’IA PERO', 'Cas d’usage & architecture GenAI', C.rouge);
  inner += badge(28, 66, 'C5.1', 'Cas d’usage GenAI', C.bleu);
  inner += bullets(28, 100, 326, 180, [
    ['Besoin : ', 'recommander un cocktail depuis une envie en langage naturel.'],
    ['Pourquoi GenAI : ', 'les filtres échouent sur « frais, fruité, touche tropicale ».'],
    ['Comprendre + produire : ', 'sémantique (retrieval) ET génération (recette).'],
    ['Conformité : ', 'thématique alternative validée par l’Annexe I du sujet.'],
  ], { size: 13.5, gap: 12 });
  inner += txt(28, 296, 326, 16, 'Pipeline', { size: 13, color: C.rouge, bold: true });
  inner += txt(28, 314, 326, 40, 'Questionnaire → SBERT → cosinus → guardrail 0.35 → cache → Gemini (RAG)', { size: 12, color: C.texte, italic: true });
  inner += ph(366, 70, 328, 268, 'i');
  inner += proofbar('C5.1 démontrée', 'cas d’usage GenAI justifié : recommandation en langage naturel, thématique Annexe I validée', C.rouge, 15);
  S(inner, C.blanc, (slide, P) => {
    const p = P.find(z => z.id === 'i'); img(slide, 'iapero-speakeasy-live.png', p);
    caption(slide, 'Interface Speakeasy de L’IA Pero', p.x, p.y + p.h + 0.02, p.w);
  });
}

// ===== SLIDE 16 - P3 Solution + DEMO =====
{
  let inner = header('PROJET 3 - L’IA PERO', 'Solution & démonstration', C.rouge);
  inner += badge(28, 66, 'C5.2', 'Solution GenAI', C.bleu);
  inner += demoBadge();
  inner += bullets(28, 98, 300, 190, [
    ['SBERT all-MiniLM-L6-v2 : ', 'local, gratuit, 384 dims, suffisant pour des phrases courtes.'],
    ['Gemini free-tier : ', 'génération uniquement, bornée par le contexte RAG.'],
    ['Cache MD5 : ', '1 appel par génération → conforme au free-tier.'],
    ['Guardrail : ', 'similarité < 0.35 → refus des requêtes hors-domaine.'],
  ], { size: 12.5, gap: 9 });
  inner += txt(28, 300, 300, 48, 'Scénario : « quelque chose de frais et fruité » → Top-5 + radar ; « répare mon vélo » → refus guardrail.', { size: 11, color: C.texte, italic: true, lh: 1.2 });
  inner += ph(360, 98, 334, 238, 'i');
  inner += proofbar('C5.2 démontrée', 'solution GenAI fonctionnelle : SBERT + RAG Gemini + cache MD5 + guardrail sémantique', C.rouge, 16, true);
  S(inner, C.blanc, (slide, P) => {
    img(slide, 'iapero-recommendation-full.png', P.find(z => z.id === 'i'));
    bandBtn(slide, LAUNCH.iapero, C.rouge);
  });
}

// ===== SLIDE 17 - P3 Evaluation & risques =====
{
  let inner = header('PROJET 3 - L’IA PERO', 'Évaluation & risques', C.rouge);
  inner += badge(28, 66, 'C5.3', 'Évaluation qualité', C.bleu);
  inner += bullets(28, 100, 326, 170, [
    ['Guardrail testé : ', 'seuil 0.35 sur des jeux de requêtes hors-domaine.'],
    ['Tableau : ', 'requête → attendu → score de similarité → décision.'],
    ['Ajustements : ', 'seuil, Top-N, température Gemini, structure du prompt RAG.'],
    ['Objectif tenu : ', 'réponse < 3 s.'],
  ], { size: 13.5, gap: 12 });
  inner += divbox(28, 276, 326, 86, { bg: C.rougeClair, border: C.rouge });
  inner += txt(42, 284, 300, 16, 'Risques', { size: 13, color: C.rouge, bold: true });
  inner += txt(42, 304, 300, 54, 'Hallucination (mitigée RAG+cache) - dépendance API (fallback+cache) - biais dataset - usage responsable de l’alcool.', { size: 11.5, color: C.texte, lh: 1.2 });
  inner += ph(366, 70, 328, 268, 'i');
  inner += proofbar('C5.3 démontrée', 'évaluation qualité : seuil 0.35 testé, paramètres ajustés (température, prompt), limites identifiées', C.rouge, 17);
  S(inner, C.blanc, (slide, P) => {
    const p = P.find(z => z.id === 'i'); img(slide, 'iapero-similarity-live.png', p);
    caption(slide, 'Scores de similarité + décision du guardrail', p.x, p.y + p.h + 0.02, p.w);
  });
}

// ===== SLIDE 18 - Synthese competences =====
{
  let inner = header('CONCLUSION', 'Synthèse : compétences → preuves');
  const comps = [
    ['C1.1', 'Schéma étoile PG'], ['C1.2', 'Cassandra query-first'], ['C1.3', 'Médaillon Parquet'], ['C1.4', 'Résilience testée'],
    ['C2.1', 'API JWT + quotas'], ['C2.2', 'Kafka + micro-batch'], ['C2.3', 'Polars multi-sources'], ['C2.4', 'Métriques pipeline'],
    ['C3.1', 'Prép. fit-train'], ['C3.2', 'Dashboard Streamlit'], ['C3.3', 'EDA corrélations'], ['C4.1', 'Stratégie prédictive'],
    ['C4.2', '4 modèles testés'], ['C4.3', 'Éval + CO2'], ['C5.1', 'Cas d’usage NL'], ['C5.2', 'SBERT + RAG Gemini'],
    ['C5.3', 'Guardrail 0.35'],
  ];
  const cols = 4, cw = 162, chh = 52, gx = 7, gy = 9, x0 = 28, y0 = 72;
  comps.forEach((c, i) => {
    const r = Math.floor(i / cols), cc = i % cols;
    const x = x0 + cc * (cw + gx), y = y0 + r * (chh + gy);
    inner += divbox(x, y, cw, chh, { bg: C.grisclr, border: C.bord });
    inner += divbox(x, y, 5, chh, { bg: C.vert });
    inner += txt(x + 12, y + 7, cw - 16, 16, `<b>${c[0]}</b>`, { size: 14, color: C.bleu, bold: true });
    inner += txt(x + 12, y + 27, cw - 16, 18, esc(c[1]), { size: 11, color: C.texte });
  });
  inner += txt(28, 372, 664, 16, '17 compétences C1.1 → C5.3 couvertes, chacune avec une preuve dans le code.', { size: 11.5, color: C.vert, bold: true });
  inner += footer(18);
  S(inner, C.blanc, null);
}

// ===== SLIDE 19 - Limites transverses =====
{
  let inner = header('CONCLUSION', 'Limites & améliorations transverses');
  const items = [
    ['Haute disponibilité réelle', 'Passer du mono-nœud à un cluster 3 nœuds (PG + Cassandra).'],
    ['Dimension temporelle', 'LSTM sur séquences capteurs pour la maintenance.'],
    ['Base vectorielle', 'pgvector / FAISS au lieu d’une matrice en mémoire pour L’IA Pero.'],
    ['Monitoring & dérive', 'Détection de drift + réentraînement automatisé.'],
    ['CI/CD complet', 'Pipeline GitHub Actions (tests + build) sur les 3 repos.'],
  ];
  let y = 74;
  for (const [t, d] of items) {
    inner += divbox(28, y, 664, 50, { bg: C.grisclr, border: C.bord }) + divbox(28, y, 5, 50, { bg: C.bleu });
    inner += txt(44, y + 8, 220, 36, t, { size: 14, color: C.bleu, bold: true });
    inner += txt(270, y + 8, 410, 36, d, { size: 12.5, color: C.texte, lh: 1.15 });
    y += 56;
  }
  inner += footer(19);
  S(inner, C.blanc, null);
}

// ===== SLIDE 20 - Conclusion + LANCER =====
{
  let inner = divbox(0, 0, 12, 405, { bg: C.rouge })
    + txt(40, 30, 540, 34, 'Conclusion & apprentissages', { size: 28, color: C.blanc, bold: true })
    + divbox(42, 74, 200, 3, { bg: C.rouge })
    + bullets(42, 90, 620, 150, [
      'Brancher tests et métriques dès le jour 1, pas en consolidation',
      'Justifier chaque choix technique par un besoin métier',
      'Documenter les limites = posture professionnelle, pas un aveu',
      'Une chaîne complète : data engineering → data science → GenAI',
    ], { size: 16, color: C.blanc, gap: 13 })
    + txt(42, 250, 620, 16, 'Les 3 démos en un clic', { size: 14, color: C.bleuTxt, bold: true })
    + ph(42, 274, 200, 40, 'b1') + ph(262, 274, 200, 40, 'b2') + ph(482, 274, 200, 40, 'b3')
    + txt(42, 336, 620, 24, 'Merci de votre attention  -  Adam Beloucif & Émilien Morice', { size: 17, color: C.blanc, bold: true });
  S(inner, C.bleuD, (slide, P) => {
    btn(slide, '▶  Urban Data Explorer', LAUNCH.urban, 42 / 72, 274 / 72, 200 / 72, 40 / 72, C.blanc, C.bleu);
    btn(slide, '▶  Maintenance Prédictive', LAUNCH.maint, 262 / 72, 274 / 72, 200 / 72, 40 / 72, C.blanc, C.bleu);
    btn(slide, '▶  L’IA Pero', LAUNCH.iapero, 482 / 72, 274 / 72, 200 / 72, 40 / 72, C.blanc, C.bleu);
  });
}

// ===== ANNEXES =====
function annex(title, color, imgs, repoKey, launchKey) {
  let inner = header('ANNEXE - BACKUP DÉMO (hors décompte)', title, color);
  const n = imgs.length;
  const totalW = 664, gap = 12;
  const w = (totalW - gap * (n - 1)) / n;
  let x = 28;
  imgs.forEach((nm, i) => { inner += ph(x, 80, w, 250, 'a' + i); x += w + gap; });
  S(inner, C.blanc, (slide, P) => {
    imgs.forEach((nm, i) => img(slide, nm, P.find(z => z.id === 'a' + i)));
    btn(slide, '▶  Lancer la démo', LAUNCH[launchKey], 270 / 72, 345 / 72, 150 / 72, 26 / 72, color);
    btn(slide, 'Repo  ↗', REPO[repoKey], 432 / 72, 345 / 72, 100 / 72, 26 / 72, C.texte);
  });
}
annex('Urban Data Explorer - captures', C.bleu, ['urban-dashboard-live.png', 'urban-district-selected.png', 'ude-dark.png'], 'urban', 'urban');
annex('Maintenance - captures', C.teal, ['maintenance-diagnostic-live.png', 'monthly_trends.png', 'quality_completeness.png'], 'maint', 'maint');
annex('L’IA Pero - captures', C.rouge, ['iapero-app-live.png', 'iapero-recommendation-live.png'], 'iapero', 'iapero');

// ---- build ----
(async () => {
  PPTX = new pptxgen();
  PPTX.layout = 'LAYOUT_16x9';
  PPTX.author = 'Adam Beloucif';
  PPTX.title = 'Soutenance Bloc 1 & 2 - RNCP40875';
  for (let i = 0; i < slides.length; i++) {
    const f = path.join(SLIDES, `s${String(i + 1).padStart(2, '0')}.html`);
    fs.writeFileSync(f, slides[i].html, 'utf8');
    const { slide, placeholders } = await html2pptx(f, PPTX, { tmpDir: path.join(ROOT, '.tmp') });
    if (slides[i].post) slides[i].post(slide, placeholders, PPTX);
    const LOGO = path.join(ASSETS, 'Logo-Efrei-Blanc.png');
    let lg = { x: (720 - 88 - 22) / 72, y: 13 / 72, w: 88 / 72, h: 44 / 72 };
    if (i === 0) lg = { x: 48 / 72, y: 42 / 72, w: 150 / 72, h: 75 / 72 };
    if (i === 19) lg = { x: (720 - 120 - 28) / 72, y: 24 / 72, w: 120 / 72, h: 60 / 72 };
    slide.addImage({ path: LOGO, ...lg });
    process.stdout.write(`slide ${i + 1} ok\n`);
  }
  const out = path.join(ROOT, 'Soutenance_Bloc1-2_Adam_Emilien.pptx');
  try {
    await PPTX.writeFile({ fileName: out });
    console.log('SAVED ->', out);
  } catch (e) {
    const alt = path.join(ROOT, 'Soutenance_Bloc1-2_Adam_Emilien_NEW.pptx');
    await PPTX.writeFile({ fileName: alt });
    console.log('LOCKED, SAVED ->', alt, '(ferme le PPTX ouvert puis renomme)');
  }
})().catch(e => { console.error('BUILD ERROR:', e.message); process.exit(1); });
