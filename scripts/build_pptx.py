#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur du PPTX de soutenance Bloc 1 & 2 (RNCP40875).
20 slides imposees + annexes backup. Design premium minimaliste.
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

ROOT    = Path(__file__).resolve().parent.parent
ASSETS  = ROOT / "assets"
SCREENS = ASSETS / "screens"
OUT     = ROOT / "Soutenance_Bloc1-2_Adam_Emilien.pptx"

# ---- Palette premium (linear/vercel inspired, aucun branding ecole) ----
DARK     = RGBColor(0x0B, 0x11, 0x21)   # fond sombre titres
INK      = RGBColor(0x0F, 0x17, 0x2A)   # texte principal
SLATE    = RGBColor(0x64, 0x74, 0x8B)   # texte secondaire
SURF     = RGBColor(0xF8, 0xFA, 0xFF)   # surface carte
BORD     = RGBColor(0xE2, 0xE8, 0xF0)   # bordures
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

# Accents par section
BLEU     = RGBColor(0x1D, 0x4E, 0xD8)   # intro/conclusion + Urban
BLEU_D   = RGBColor(0x1E, 0x3A, 0x8A)
TEAL     = RGBColor(0x04, 0x78, 0x57)   # Maintenance (emeraude)
ROUGE    = RGBColor(0x7C, 0x3A, 0xED)   # IA Pero (violet)
TEXTE    = INK
GRIS     = SLATE
GRIS_CLR = SURF
GRIS_BORD = BORD
BLANC    = WHITE
VERT     = RGBColor(0x05, 0x96, 0x69)   # succes

FONT = "Calibri"

REPOS = {
    "urban":  "https://github.com/Adam-Blf/urban-data-explorer",
    "maint":  "https://github.com/Adam-Blf/maintenance-predictive-industrielle",
    "iapero": "https://github.com/Adam-Blf/ia-pero",
}
DEMO_URBAN = "https://urban.beloucif.com"

EMU_IN = 914400
SW, SH = 13.333, 7.5

prs = Presentation()
prs.slide_width  = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]


# ---------- helpers ----------
def slide():
    return prs.slides.add_slide(BLANK)


def bg(s, color):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = color


def _set_font(run, size, color, bold=False, italic=False, font=FONT):
    run.font.size    = Pt(size)
    run.font.color.rgb = color
    run.font.bold    = bold
    run.font.italic  = italic
    run.font.name    = font


def textbox(s, text, l, t, w, h, size=18, color=INK, bold=False, italic=False,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=FONT, line_spacing=1.0):
    tb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap          = True
    tf.vertical_anchor    = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment    = align
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    _set_font(r, size, color, bold, italic, font)
    return tb


def bullets(s, items, l, t, w, h, size=16, color=INK, gap=6, bullet_color=BLEU):
    tb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after  = Pt(gap)
        p.line_spacing = 1.05
        rb = p.add_run()
        rb.text = "▪  "
        _set_font(rb, size - 2, bullet_color, bold=True)
        if isinstance(it, tuple):
            lead, rest = it
            r1 = p.add_run(); r1.text = lead;  _set_font(r1, size, color, bold=True)
            r2 = p.add_run(); r2.text = rest;  _set_font(r2, size, color)
        else:
            r = p.add_run(); r.text = it; _set_font(r, size, color)
    return tb


def rect(s, l, t, w, h, fill=None, line=None, line_w=1.0,
         shape=MSO_SHAPE.RECTANGLE, round_=None):
    sp = s.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if round_ is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = round_
        except Exception:
            pass
    return sp


def shape_text(sp, text, size=14, color=WHITE, bold=True,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE):
    tf = sp.text_frame
    tf.word_wrap        = True
    tf.vertical_anchor  = anchor
    tf.margin_left = tf.margin_right = Pt(4)
    tf.margin_top  = tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    _set_font(r, size, color, bold)
    return sp


def header(s, kicker, title, color=BLEU):
    """Bandeau minimaliste : fine bande coloree + texte, pas de logo."""
    bg(s, WHITE)
    rect(s, 0, 0, SW, 0.09, fill=color)
    textbox(s, kicker.upper(), 0.55, 0.17, 11.0, 0.32,
            size=9, color=color, bold=True, font=FONT)
    textbox(s, title, 0.55, 0.45, 11.5, 0.65,
            size=25, color=INK, bold=True, font=FONT)
    rect(s, 0.55, 1.18, SW - 1.1, 0.015, fill=BORD)


def footer(s, idx, dark=False):
    c = RGBColor(0x88, 0x88, 0xAA) if dark else SLATE
    rect(s, 0.55, 7.1, SW - 1.1, 0.012, fill=BORD)
    textbox(s, "Adam Beloucif  &  Emilien Morice  ·  RNCP 40875",
            0.55, 7.15, 9.0, 0.28, size=9, color=c)
    textbox(s, f"{idx} / 20", 12.2, 7.15, 0.8, 0.28,
            size=9, color=c, align=PP_ALIGN.RIGHT)


def badge(s, code, label, l, t, fill=ROUGE):
    w  = 0.55 + 0.105 * len(label)
    sp = rect(s, l, t, min(w, 4.2), 0.38,
              fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, round_=0.5)
    tf = sp.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Pt(8)
    tf.margin_top  = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r1 = p.add_run(); r1.text = code + "  "; _set_font(r1, 11, WHITE, bold=True)
    r2 = p.add_run(); r2.text = label;       _set_font(r2, 10, WHITE)
    return sp


def badges_row(s, pairs, l, t, fill=ROUGE):
    x = l
    for code, label in pairs:
        sp = badge(s, code, label, x, t, fill=fill)
        x += sp.width / EMU_IN + 0.18


def button(s, text, url, l, t, w=2.7, h=0.52, fill=BLEU, fg=WHITE):
    sp = rect(s, l, t, w, h, fill=fill,
              shape=MSO_SHAPE.ROUNDED_RECTANGLE, round_=0.28)
    shape_text(sp, text, size=12, color=fg, bold=True)
    sp.click_action.hyperlink.address = url
    return sp


def image_fit(s, path, l, t, max_w, max_h, border=False):
    path = Path(path)
    if not path.exists():
        rect(s, l, t, max_w, max_h, fill=SURF, line=BORD)
        textbox(s, "[image]", l, t + max_h / 2 - 0.2, max_w, 0.4,
                size=12, color=SLATE, align=PP_ALIGN.CENTER)
        return
    if HAVE_PIL:
        with Image.open(path) as im:
            iw, ih = im.size
        ar = iw / ih; box_ar = max_w / max_h
        if ar > box_ar:
            w = max_w;  h = max_w / ar
        else:
            h = max_h;  w = max_h * ar
        l2 = l + (max_w - w) / 2
        t2 = t + (max_h - h) / 2
    else:
        w, h, l2, t2 = max_w, max_h, l, t
    if border:
        rect(s, l2 - 0.03, t2 - 0.03, w + 0.06, h + 0.06,
             fill=WHITE, line=BORD, line_w=1.0)
    s.shapes.add_picture(str(path), Inches(l2), Inches(t2), Inches(w), Inches(h))


def caption(s, text, l, t, w):
    textbox(s, text, l, t, w, 0.28, size=10, color=SLATE, italic=True,
            align=PP_ALIGN.CENTER)


# ============================================================
# SLIDE 1 - Titre (fond sombre, aucun logo ecole)
# ============================================================
s = slide(); bg(s, DARK)
rect(s, 0, 0, 0.18, SH, fill=BLEU)
# Accent line
rect(s, 0.55, 2.25, 5.0, 0.05, fill=BLEU)
textbox(s, "Soutenance de fin d'etudes  ·  M1 Data Engineering & IA",
        0.55, 1.4, 12.0, 0.55, size=15,
        color=RGBColor(0x93, 0xC5, 0xFD), bold=False)
textbox(s, "Bloc 1 & 2\nRNCPP 40875",
        0.55, 1.9, 12.0, 1.4, size=48, color=WHITE, bold=True, line_spacing=1.05)
textbox(s, "Expert en Ingenierie de Donnees  -  De la donnee brute a la decision",
        0.55, 3.4, 12.0, 0.5, size=17,
        color=RGBColor(0x93, 0xC5, 0xFD))
rect(s, 0.55, 4.1, 5.5, 0.04, fill=RGBColor(0x4F, 0x46, 0xE5))
textbox(s, "Adam Beloucif  &  Emilien Morice",
        0.55, 4.3, 12.0, 0.55, size=24, color=WHITE, bold=True)
textbox(s, "Session 2025-2026",
        0.55, 4.95, 12.0, 0.4, size=14,
        color=RGBColor(0x93, 0xC5, 0xFD))

# ============================================================
# SLIDE 2 - Contexte & problematique
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Introduction", "Contexte & problematique")
textbox(s, "Fil rouge  -  transformer la donnee en decision",
        0.55, 1.45, 12, 0.48, size=19, color=BLEU, bold=True)
textbox(s, "Trois projets, trois maillons complementaires d'une meme chaine de valeur data.",
        0.55, 1.98, 12, 0.38, size=14, color=SLATE)
maillons = [
    ("1  Data Engineering",
     "Construire l'architecture\nqui collecte, stocke et\nexpose la donnee.", BLEU),
    ("2  Data Science",
     "Modeliser pour predire\net outiller la decision\nmetier.", TEAL),
    ("3  IA Generative",
     "Comprendre le langage\nnaturel et generer une\nreponse personnalisee.", ROUGE),
]
x = 0.55
for titre, corps, col in maillons:
    rect(s, x, 2.65, 3.95, 2.75, fill=SURF, line=BORD)
    rect(s, x, 2.65, 3.95, 0.08, fill=col)
    textbox(s, titre, x + 0.25, 2.88, 3.5, 0.48, size=16, color=col, bold=True)
    textbox(s, corps, x + 0.25, 3.48, 3.5, 1.7, size=14, color=INK, line_spacing=1.15)
    x += 4.2
textbox(s, "Probleme commun : une donnee non exploitee n'a aucune valeur. "
           "Chaque projet repond a un besoin metier concret avec preuves techniques verifiables.",
        0.55, 5.7, 12.2, 0.8, size=13.5, color=SLATE, italic=True)
footer(s, 2)

# ============================================================
# SLIDE 3 - Vue d'ensemble + boutons
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Introduction", "Vue d'ensemble des 3 projets")
cards = [
    ("Urban Data Explorer",  "Bloc 1  -  C1.1 - C2.4",
     "Plateforme data du logement parisien. 24 sources Open Data, architecture medaillon, "
     "PostgreSQL etoile, Cassandra, Kafka, API FastAPI securisee, dashboard MapLibre.",
     "urban", BLEU),
    ("Maintenance Predictive", "Bloc 2  -  C3.1 - C4.3",
     "Prediction de panne machine sous 24 h depuis capteurs IoT. 4 modeles compares (dont "
     "Deep Learning), mesure CO2 CodeCarbon, dashboard decisionnel Streamlit.",
     "maint", TEAL),
    ("L'IA Pero",             "Bloc 2  -  C5.1 - C5.3",
     "Recommandation de cocktails par IA semantique. SBERT 384 dims, similarite cosinus, "
     "guardrail 0.35, RAG + Gemini avec cache, interface Streamlit Speakeasy.",
     "iapero", ROUGE),
]
y = 1.48
for titre, comp, desc, key, col in cards:
    rect(s, 0.55, y, 12.25, 1.55, fill=SURF, line=BORD)
    rect(s, 0.55, y, 0.1, 1.55, fill=col)
    textbox(s, titre, 0.85, y + 0.12, 5.5, 0.44, size=18, color=col, bold=True)
    textbox(s, comp,  0.85, y + 0.58, 5.5, 0.32, size=11, color=SLATE, bold=True)
    textbox(s, desc,  0.85, y + 0.9, 8.7, 0.58, size=12, color=INK, line_spacing=1.05)
    button(s, "Ouvrir le repo  ->", REPOS[key], 10.05, y + 0.48, w=2.45, h=0.56, fill=col)
    y += 1.72
footer(s, 3)

# ============================================================
# SLIDE 4 - Contributions individuelles
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Introduction", "Contributions individuelles")
textbox(s, "Presentation collective, evaluation individualisee. Repartition par projet :",
        0.55, 1.42, 12, 0.38, size=13.5, color=SLATE)
rows = [
    ("Projet", "Adam Beloucif", "Emilien Morice"),
    ("Urban Data Explorer",
     "Architecture data, API securisee, modele PG/Cassandra, pipeline",
     "Sourcing & qualite des 24 sources, front cartographique, data prep"),
    ("Maintenance Predictive",
     "Modelisation 4 modeles, selection XGBoost, dashboard Streamlit",
     "EDA, preparation des donnees, analyse des correlations"),
    ("L'IA Pero",
     "Backend RAG/SBERT, guardrail semantique, cache, evaluation",
     "Referentiel cocktails, scenarios d'usage, tests des seuils"),
]
col_x = [0.55, 3.45, 8.15]
col_w = [2.9, 4.7, 4.65]
y = 1.98
rh = [0.5, 1.02, 1.02, 1.02]
for ri, row in enumerate(rows):
    is_head = ri == 0
    for ci, cell in enumerate(row):
        fill = BLEU if is_head else (SURF if ri % 2 else WHITE)
        sp = rect(s, col_x[ci], y, col_w[ci], rh[ri], fill=fill, line=BORD, line_w=0.75)
        tf = sp.text_frame; tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Pt(8)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = cell
        _set_font(r, 13 if is_head else 12,
                  WHITE if is_head else INK, bold=(is_head or ci == 0))
    y += rh[ri]
textbox(s, "Chaque membre porte au moins un choix technique et en connait les limites "
           "(critere d'individualisation du jury).",
        0.55, 6.5, 12, 0.48, size=12, color=SLATE, italic=True)
footer(s, 4)

# ============================================================
# P1 - SLIDE 5 - Besoin & architecture
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 1  -  Urban Data Explorer", "Besoin & architecture", BLEU)
bullets(s, [
    ("Besoin metier  ",
     "explorer le marche du logement parisien en croisant 24 sources Open Data heterogenes."),
    ("Architecture medaillon  ",
     "Bronze (brut Parquet) -> Silver (normalise, geocode) -> Gold (datamarts)."),
    ("Stockage dual  ",
     "PostgreSQL en etoile pour l'analytique, Cassandra query-first pour le streaming."),
    ("Exposition  ",
     "API FastAPI securisee -> dashboard React / MapLibre."),
], 0.55, 1.48, 5.9, 4.2, size=14.5, gap=10)
image_fit(s, SCREENS / "ude-light.png", 6.7, 1.5, 6.1, 4.35, border=True)
caption(s, "Dashboard Urban Data Explorer  -  choroplethe prix m2", 6.7, 5.9, 6.1)
button(s, "Demo live  ->", DEMO_URBAN, 0.55, 6.42, w=2.45, h=0.52, fill=BLEU)
button(s, "Repo GitHub  ->", REPOS["urban"], 3.2, 6.42, w=2.55, h=0.52, fill=INK)
footer(s, 5)

# ============================================================
# P1 - SLIDE 6 - Bases de donnees
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 1  -  Urban Data Explorer", "Bases de donnees  SQL vs NoSQL", BLEU)
badges_row(s, [("C1.1", "Relationnelle"), ("C1.2", "NoSQL")], 0.55, 1.32, fill=BLEU)
rect(s, 0.55, 1.95, 6.0, 4.2, fill=SURF, line=BORD)
rect(s, 0.55, 1.95, 6.0, 0.5, fill=BLEU)
textbox(s, "PostgreSQL  -  schema en etoile", 0.75, 2.03, 5.6, 0.38,
        size=15, color=WHITE, bold=True)
bullets(s, [
    "Fait + dimensions (arrondissement, temps), FK et cles composees",
    "Index sur les axes de requete -> p95 < 4 ms en jointure",
    "Contraintes NOT NULL / integrite referentielle",
    "Test de charge : scripts/test_load_postgres.py",
    "Besoin : agregats analytiques par arrondissement x mois",
], 0.8, 2.58, 5.5, 3.3, size=13, gap=8)
rect(s, 6.85, 1.95, 5.95, 4.2, fill=SURF, line=BORD)
rect(s, 6.85, 1.95, 5.95, 0.5, fill=TEAL)
textbox(s, "Cassandra  -  query-first", 7.05, 2.03, 5.6, 0.38,
        size=15, color=WHITE, bold=True)
bullets(s, [
    "Partition par event_type, clustering event_time DESC",
    "TTL 7 jours -> la donnee chaude expire seule",
    "Deux patterns d'acces : par type et par arrondissement",
    "Adapte aux evenements semi-structures a forte velocite",
    "PG aurait impose un schema rigide + purges manuelles",
], 7.1, 2.58, 5.5, 3.3, size=13, gap=8, bullet_color=TEAL)
footer(s, 6)

# ============================================================
# P1 - SLIDE 7 - Data Lake & streaming
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 1  -  Urban Data Explorer", "Data Lake & streaming temps reel", BLEU)
badges_row(s, [("C1.3", "Data Lake"), ("C2.2", "Streaming")], 0.55, 1.32, fill=BLEU)
bullets(s, [
    ("24 sources / 8 familles  ",
     "CSV, GeoJSON, API -> atterrissage Bronze en Parquet."),
    ("Silver  ",
     "normalisation des codes, geocodage point-in-polygon IRIS."),
    ("Gold  ",
     "datamarts dashboard & timeline, format colonnaire optimise."),
    ("Kafka  ",
     "producteur / consommateur temps reel evenement par evenement."),
    ("Micro-batch  ",
     "streaming/microbatch.py -> fenetres tumbling 10 s (count, moyenne)."),
], 0.55, 1.92, 6.0, 4.0, size=14, gap=9)
image_fit(s, SCREENS / "infrastructures_stacked_bar.png", 6.9, 1.95, 5.9, 3.0, border=True)
image_fit(s, SCREENS / "geocoding_integrity.png",        6.9, 5.1,  5.9, 1.6, border=True)
caption(s, "Repartition des sources + integrite du geocodage", 6.9, 6.72, 5.9)
footer(s, 7)

# ============================================================
# P1 - SLIDE 8 - API & securite + DEMO
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 1  -  Urban Data Explorer", "API & securite", BLEU)
badge(s, "C2.1", "API securisee", 0.55, 1.32, fill=BLEU)
sp_demo = rect(s, 9.55, 1.28, 3.25, 0.48, fill=ROUGE,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, round_=0.3)
shape_text(sp_demo, "DEMO LIVE  -  90 s", size=13, color=WHITE)
bullets(s, [
    ("JWT HS256  ",
     "secret en variable d'env (jamais commite), roles viewer / admin."),
    ("401 vs 403  ",
     "authentification et autorisation differenciees."),
    ("Quotas par IP  ",
     "120 anonyme / 600 authentifie req/min -> 429 si depassement."),
    ("Swagger  ",
     "documentation interactive live sur /docs."),
    ("CORS  ",
     "restreint a l'origine du front, donnees Open Data (RGPD by design)."),
], 0.55, 1.98, 6.0, 3.6, size=14, gap=8)
textbox(s, "Scenario demo", 0.55, 5.65, 6, 0.33, size=13, color=BLEU, bold=True)
textbox(s, "Dashboard -> clic 11e arr. -> comparaison 11e/16e -> /docs -> "
           "curl token -> 403 sans role admin.",
        0.55, 5.98, 6.2, 0.75, size=12, color=SLATE, italic=True)
image_fit(s, SCREENS / "ude-api.png", 6.9, 1.95, 5.9, 4.0, border=True)
button(s, "Ouvrir le repo  ->", REPOS["urban"], 6.9, 6.18, w=2.6, h=0.52, fill=BLEU)
button(s, "Demo live  ->",      DEMO_URBAN,      9.7, 6.18, w=2.5, h=0.52, fill=INK)
footer(s, 8)

# ============================================================
# P1 - SLIDE 9 - Perf, resilience, limites
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 1  -  Urban Data Explorer", "Performance, resilience & limites", BLEU)
badges_row(s, [("C1.4", "Resilience"), ("C2.4", "Perf pipelines")], 0.55, 1.32, fill=BLEU)
bullets(s, [
    ("Metriques pipeline  ",
     "etl/metrics.py -> duree, lignes, octets, lignes/sec exposes via GET /pipeline/metrics."),
    ("Optimisations  ",
     "Polars (Rust) vs pandas, Parquet colonnaire, lru_cache sur le geocodage inverse."),
    ("Resilience testee  ",
     "scripts/test_resilience.py : kill conteneur Postgres -> fallback parquet -> restart."),
    ("Compose  ",
     "healthchecks, restart unless-stopped, depends_on service_healthy."),
], 0.55, 1.92, 12.2, 2.6, size=14, gap=9)
rect(s, 0.55, 4.72, 12.25, 1.75,
     fill=RGBColor(0xFE, 0xF2, 0xF2), line=RGBColor(0xFC, 0xA5, 0xA5), line_w=1.0)
textbox(s, "Limites assumees  &  roadmap",
        0.8, 4.88, 11, 0.38, size=15,
        color=RGBColor(0xB9, 0x1C, 0x1C), bold=True)
textbox(s, "Demo mono-noeud (replication_factor 1), pas de haute disponibilite reelle. "
           "Chemin documente vers un cluster 3 noeuds + replication Cassandra lineaire "
           "+ API stateless replicable.",
        0.8, 5.3, 11.8, 1.0, size=13.5, color=INK, line_spacing=1.1)
footer(s, 9)

# ============================================================
# P2 - SLIDE 10 - Question metier
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 2  -  Maintenance Predictive", "Question metier & strategie IA", TEAL)
badge(s, "C4.1", "Strategie d'integration IA", 0.55, 1.32, fill=TEAL)
bullets(s, [
    ("Probleme  ",
     "une panne non planifiee coute 5 a 50 k EUR/h d'arret de ligne."),
    ("Corrective  ",
     "on repare apres la casse -> cout maximal, imprevu."),
    ("Preventive  ",
     "entretien calendaire -> sur-maintenance, pieces gaspillees."),
    ("Predictive (cible)  ",
     "predire la panne sous 24 h -> intervenir au bon moment."),
], 0.55, 1.95, 7.0, 3.0, size=14.5, gap=10)
rect(s, 8.0, 1.95, 4.8, 3.8, fill=SURF, line=BORD)
textbox(s, "Feuille de route", 8.25, 2.1, 4.3, 0.38,
        size=15, color=TEAL, bold=True)
bullets(s, [
    "Capteurs IoT existants -> collecte",
    "Modele predictif + seuil de decision",
    "Alerte responsable maintenance",
    "Boucle de reentrainement periodique",
], 8.25, 2.6, 4.4, 3.0, size=13, gap=10, bullet_color=TEAL)
textbox(s, "Cout corrective ~100 EUR/h  ->  predictive ~20 EUR/h",
        0.55, 5.38, 7, 0.4, size=14, color=TEAL, bold=True)
footer(s, 10)

# ============================================================
# P2 - SLIDE 11 - Donnees & EDA
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 2  -  Maintenance Predictive", "Donnees & analyse exploratoire", TEAL)
badges_row(s, [("C3.1", "Preparation"), ("C3.3", "EDA")], 0.55, 1.32, fill=TEAL)
bullets(s, [
    ("Dataset  ",
     "Kaggle industrial_machine_maintenance  -  24 042 lignes x 15 variables."),
    ("Cible  ",
     "failure_within_24h (classe rare -> desequilibre)."),
    ("Nettoyage  ",
     "imputation mediane (fit train), winsorisation outliers capteurs."),
    ("Insight cle  ",
     "vibration_rms et temperature_motor sont les plus correlees a la panne."),
    ("Coherence physique  ",
     "l'usure mecanique genere vibration ET echauffement."),
], 0.55, 1.92, 6.1, 4.0, size=14, gap=8, bullet_color=TEAL)
image_fit(s, SCREENS / "correlation_matrix.png", 6.9, 1.92, 5.9, 4.5, border=True)
caption(s, "Matrice de correlation des variables capteurs", 6.9, 6.45, 5.9)
footer(s, 11)

# ============================================================
# P2 - SLIDE 12 - Modeles & comparaison
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 2  -  Maintenance Predictive", "Modeles & evaluation comparative", TEAL)
badges_row(s, [("C4.2", "Modeles"), ("C4.3", "Eval + ecoresponsabilite")], 0.55, 1.32, fill=TEAL)
data = [
    ["Modele",              "F1",    "ROC-AUC", "Temps", "CO2"],
    ["LogReg (baseline)",   "0.865", "0.914",   "3.2 s", "0.3 mg"],
    ["Random Forest",       "0.910", "0.952",   "45 s",  "8.2 mg"],
    ["XGBoost (retenu)",    "0.928", "0.964",   "35 s",  "6.1 mg"],
    ["MLP 64-32-16 (DL)",   "0.896", "0.936",   "18 s",  "3.8 mg"],
]
cx = [0.55, 4.55, 6.15, 8.05, 9.65]
cw = [4.0,  1.6,  1.9,  1.6,  1.7]
ty = 1.98; rh = 0.6
for ri, row in enumerate(data):
    retained = ri == 3
    for ci, cell in enumerate(row):
        if ri == 0:
            fill = TEAL
        elif retained:
            fill = RGBColor(0xD1, 0xFA, 0xE5)
        else:
            fill = SURF if ri % 2 else WHITE
        sp = rect(s, cx[ci], ty, cw[ci], rh, fill=fill, line=BORD, line_w=0.75)
        tf = sp.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Pt(8)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
        r = p.add_run(); r.text = cell
        c = WHITE if ri == 0 else (TEAL if retained else INK)
        _set_font(r, 12.5, c, bold=(ri == 0 or retained))
    ty += rh
bullets(s, [
    ("Selection  ",
     "score = F1 - 0.5 * s(F1 en cross-val) -> performance ET stabilite."),
    ("Anti-leakage  ",
     "pipeline sklearn fit sur train uniquement (ADR dedie)."),
    ("Ecoresponsabilite  ",
     "CodeCarbon : XGBoost 6.1 mg < RF 8.2 mg pour de meilleures perfs."),
], 0.55, 5.25, 12.2, 1.72, size=13, gap=6, bullet_color=TEAL)
footer(s, 12)

# ============================================================
# P2 - SLIDE 13 - Dashboard + DEMO
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 2  -  Maintenance Predictive", "Dashboard decisionnel", TEAL)
badge(s, "C3.2", "Dashboard interactif", 0.55, 1.32, fill=TEAL)
sp_demo2 = rect(s, 9.55, 1.28, 3.25, 0.48, fill=ROUGE,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE, round_=0.3)
shape_text(sp_demo2, "DEMO LIVE  -  90 s", size=13, color=WHITE)
bullets(s, [
    ("Cible  ",   "responsable maintenance, pas le data scientist."),
    ("Simulation  ", "sliders capteurs -> prediction temps reel + probabilite."),
    ("Explication  ", "top variables influentes en langage metier."),
    ("Distinct  ",  "des visuels EDA du rapport (consigne du sujet)."),
], 0.55, 1.98, 5.9, 3.2, size=14, gap=9, bullet_color=TEAL)
textbox(s, "Scenario : vibration haute + temperature haute -> risque eleve -> "
           "feature importance.",
        0.55, 5.3, 6.0, 0.8, size=12, color=SLATE, italic=True)
image_fit(s, SCREENS / "maintenance-dashboard-live.png", 6.9, 1.95, 5.9, 4.0, border=True)
button(s, "Ouvrir le repo  ->", REPOS["maint"], 6.9, 6.18, w=5.9, h=0.52, fill=TEAL)
footer(s, 13)

# ============================================================
# P2 - SLIDE 14 - Limites
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 2  -  Maintenance Predictive", "Limites & bonus realises", TEAL)
rect(s, 0.55, 1.55, 6.0, 4.65,
     fill=RGBColor(0xFE, 0xF2, 0xF2), line=RGBColor(0xFC, 0xA5, 0xA5))
textbox(s, "Limites", 0.8, 1.7, 5.5, 0.4,
        size=17, color=RGBColor(0xB9, 0x1C, 0x1C), bold=True)
bullets(s, [
    "Donnees simulees (pas de bruit capteur reel)",
    "Pas de dimension temporelle exploitee",
    "Un LSTM sur sequences serait la suite logique",
    "Derive en production -> monitoring + reentrainement",
], 0.8, 2.22, 5.5, 3.75, size=14, gap=12,
    bullet_color=RGBColor(0xB9, 0x1C, 0x1C))
rect(s, 6.85, 1.55, 5.95, 4.65,
     fill=RGBColor(0xD1, 0xFA, 0xE5), line=TEAL)
textbox(s, "Bonus deja realises", 7.1, 1.7, 5.5, 0.4,
        size=17, color=TEAL, bold=True)
bullets(s, [
    "Multiclass : type de panne predit",
    "Regression : RUL (duree de vie restante)",
    "Calibration des probabilites",
    "Tuning des hyperparametres justifie",
], 7.1, 2.22, 5.5, 3.75, size=14, gap=12, bullet_color=TEAL)
footer(s, 14)

# ============================================================
# P3 - SLIDE 15 - Cas d'usage & archi
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 3  -  L'IA Pero", "Cas d'usage & architecture GenAI", ROUGE)
badge(s, "C5.1", "Cas d'usage GenAI", 0.55, 1.32, fill=BLEU)
bullets(s, [
    ("Besoin  ",       "recommander un cocktail depuis une envie en langage naturel."),
    ("Pourquoi GenAI  ", "les filtres echouent sur « frais, fruite, touche tropicale »."),
    ("Comprendre + produire  ",
     "semantique (retrieval) ET generation (recette)."),
    ("Conformite  ",
     "thematique alternative validee par l'Annexe I du sujet."),
], 0.55, 1.95, 6.1, 3.2, size=14, gap=9, bullet_color=BLEU)
textbox(s, "Pipeline",
        0.55, 5.2, 6, 0.33, size=14, color=ROUGE, bold=True)
textbox(s, "Questionnaire -> SBERT -> cosinus -> guardrail 0.35 -> "
           "cache -> Gemini (RAG)",
        0.55, 5.52, 6.2, 0.8, size=13, color=SLATE, italic=True)
image_fit(s, SCREENS / "iapero-speakeasy-live.png", 6.9, 1.95, 5.9, 4.35, border=True)
caption(s, "Interface Speakeasy de L'IA Pero", 6.9, 6.35, 5.9)
footer(s, 15)

# ============================================================
# P3 - SLIDE 16 - Solution + DEMO
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 3  -  L'IA Pero", "Solution & demonstration", ROUGE)
badge(s, "C5.2", "Solution GenAI", 0.55, 1.32, fill=BLEU)
sp_demo3 = rect(s, 9.55, 1.28, 3.25, 0.48, fill=ROUGE,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE, round_=0.3)
shape_text(sp_demo3, "DEMO LIVE  -  90 s", size=13, color=WHITE)
bullets(s, [
    ("SBERT all-MiniLM-L6-v2  ",
     "local, gratuit, 384 dims, suffisant pour des phrases courtes."),
    ("Gemini free-tier  ",
     "generation uniquement, bornee par le contexte RAG."),
    ("Cache MD5  ",
     "1 appel par generation -> conforme a la contrainte free-tier."),
    ("Guardrail  ",
     "similarite < 0.35 -> refus des requetes hors-domaine."),
], 0.55, 1.98, 6.0, 3.3, size=14, gap=8, bullet_color=ROUGE)
textbox(s, "Scenario : « quelque chose de frais et fruite » -> Top-5 + radar ; "
           "« repare mon velo » -> refus guardrail.",
        0.55, 5.32, 6.1, 0.9, size=12, color=SLATE, italic=True)
image_fit(s, SCREENS / "iapero-recommendation-full.png", 6.9, 1.95, 5.9, 4.0, border=True)
button(s, "Ouvrir le repo  ->", REPOS["iapero"], 6.9, 6.18, w=5.9, h=0.52, fill=ROUGE)
footer(s, 16)

# ============================================================
# P3 - SLIDE 17 - Evaluation & risques
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Projet 3  -  L'IA Pero", "Evaluation & risques", ROUGE)
badge(s, "C5.3", "Evaluation qualite", 0.55, 1.32, fill=BLEU)
bullets(s, [
    ("Guardrail teste  ",
     "seuil 0.35 sur des jeux de requetes hors-domaine."),
    ("Tableau  ",
     "requete -> attendu -> score de similarite -> decision."),
    ("Ajustements  ",
     "seuil, Top-N, temperature Gemini, structure du prompt RAG."),
    ("Objectif tenu  ",
     "reponse < 3 s."),
], 0.55, 1.95, 6.1, 3.2, size=14, gap=9, bullet_color=ROUGE)
rect(s, 0.55, 5.18, 6.1, 1.55,
     fill=RGBColor(0xFE, 0xF2, 0xF2), line=RGBColor(0xFC, 0xA5, 0xA5))
textbox(s, "Risques", 0.8, 5.3, 5, 0.33, size=14,
        color=RGBColor(0xB9, 0x1C, 0x1C), bold=True)
textbox(s, "Hallucination (mitigee RAG+cache)  -  dependance API (fallback+cache)  -  "
           "biais dataset  -  usage responsable de l'alcool.",
        0.8, 5.65, 5.7, 1.0, size=12.5, color=INK, line_spacing=1.1)
image_fit(s, SCREENS / "iapero-similarity-live.png", 6.9, 1.95, 5.9, 4.5, border=True)
caption(s, "Scores de similarite + decision du guardrail", 6.9, 6.5, 5.9)
footer(s, 17)

# ============================================================
# SLIDE 18 - Synthese competences
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Conclusion", "Synthese : competences -> preuves")
comps = [
    ("C1.1", "Schema etoile PG"),     ("C1.2", "Cassandra query-first"),
    ("C1.3", "Medaillon Parquet"),     ("C1.4", "Resilience testee"),
    ("C2.1", "API JWT + quotas"),      ("C2.2", "Kafka + micro-batch"),
    ("C2.3", "Polars multi-sources"),  ("C2.4", "Metriques pipeline"),
    ("C3.1", "Prep fit-train"),        ("C3.2", "Dashboard Streamlit"),
    ("C3.3", "EDA correlations"),      ("C4.1", "Strategie predictive"),
    ("C4.2", "4 modeles testes"),      ("C4.3", "Eval + CO2"),
    ("C5.1", "Cas d'usage NL"),        ("C5.2", "SBERT + RAG Gemini"),
    ("C5.3", "Guardrail 0.35"),
]
cols = 4
cw = 3.05; chh = 0.92; gx = 0.12; gy = 0.14
x0, y0 = 0.55, 1.5
for i, (code, proof) in enumerate(comps):
    r_i = i // cols; c_i = i % cols
    x = x0 + c_i * (cw + gx); y = y0 + r_i * (chh + gy)
    sp = rect(s, x, y, cw, chh, fill=SURF, line=BORD)
    rect(s, x, y, 0.08, chh, fill=VERT)
    textbox(s, code,  x + 0.2, y + 0.1,  cw - 0.3, 0.34, size=15, color=BLEU, bold=True)
    textbox(s, proof, x + 0.2, y + 0.46, cw - 0.3, 0.38, size=12, color=INK)
textbox(s, "17 competences C1.1 -> C5.3 couvertes, chacune avec une preuve dans le code.",
        0.55, 6.92, 12, 0.3, size=12, color=VERT, bold=True)
footer(s, 18)

# ============================================================
# SLIDE 19 - Limites & ameliorations transverses
# ============================================================
s = slide(); bg(s, WHITE)
header(s, "Conclusion", "Limites & ameliorations transverses")
items = [
    ("Haute disponibilite reelle",
     "Passer du mono-noeud a un cluster 3 noeuds (PG + Cassandra)."),
    ("Dimension temporelle",
     "LSTM sur sequences capteurs pour la maintenance."),
    ("Base vectorielle",
     "pgvector / FAISS au lieu d'une matrice en memoire pour L'IA Pero."),
    ("Monitoring & derive",
     "Detection de drift + reentrainement automatise."),
    ("CI/CD complet",
     "Pipeline GitHub Actions (tests + build) sur les 3 repos."),
]
y = 1.55
for titre, corps in items:
    rect(s, 0.55, y, 12.25, 0.94, fill=SURF, line=BORD)
    rect(s, 0.55, y, 0.08, 0.94, fill=BLEU)
    textbox(s, titre, 0.82, y + 0.12, 4.2, 0.7, size=15, color=BLEU, bold=True,
            anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, corps, 5.18, y + 0.12, 7.4, 0.7, size=13.5, color=INK,
            anchor=MSO_ANCHOR.MIDDLE)
    y += 1.04
footer(s, 19)

# ============================================================
# SLIDE 20 - Conclusion (fond sombre premium)
# ============================================================
s = slide(); bg(s, DARK)
rect(s, 0, 0, 0.18, SH, fill=BLEU)
textbox(s, "Conclusion & apprentissages",
        0.9, 0.65, 11, 0.75, size=30, color=WHITE, bold=True)
rect(s, 0.95, 1.55, 4.5, 0.04, fill=RGBColor(0x4F, 0x46, 0xE5))
bullets(s, [
    "Brancher tests et metriques des le jour 1, pas en consolidation",
    "Justifier chaque choix technique par un besoin metier",
    "Documenter les limites = posture professionnelle, pas un aveu",
    "Une chaine complete : data engineering -> data science -> GenAI",
], 0.95, 1.85, 11.5, 2.65, size=17, color=WHITE, gap=12,
    bullet_color=RGBColor(0x93, 0xC5, 0xFD))
textbox(s, "Les 3 projets en un clic",
        0.95, 4.72, 11, 0.38, size=14,
        color=RGBColor(0x93, 0xC5, 0xFD), bold=True)
button(s, "Urban Data Explorer  ->",    REPOS["urban"],  0.95, 5.18, w=3.85, h=0.68,
       fill=WHITE, fg=BLEU)
button(s, "Maintenance Predictive  ->", REPOS["maint"],  4.95, 5.18, w=3.85, h=0.68,
       fill=WHITE, fg=TEAL)
button(s, "L'IA Pero  ->",              REPOS["iapero"], 8.95, 5.18, w=3.85, h=0.68,
       fill=WHITE, fg=ROUGE)
textbox(s, "Merci de votre attention  -  Adam Beloucif & Emilien Morice",
        0.95, 6.32, 11.5, 0.48, size=18, color=WHITE, bold=True)

# ============================================================
# ANNEXES backup (hors decompte)
# ============================================================
def annexe(title, imgs, key, col):
    s = slide(); bg(s, WHITE)
    header(s, "Annexe  -  Backup demo (hors decompte)", title, col)
    n = len(imgs)
    if n == 1:
        image_fit(s, imgs[0], 1.5, 1.45, 10.3, 5.25, border=True)
    else:
        w = (12.25 - 0.4 * (n - 1)) / n
        x = 0.55
        for img in imgs:
            image_fit(s, img, x, 1.55, w, 4.85, border=True)
            x += w + 0.4
    button(s, "Ouvrir le repo  ->", REPOS[key], 5.35, 6.7, w=2.7, h=0.48, fill=col)


annexe("Urban Data Explorer  -  captures",
       [SCREENS / "urban-dashboard-live.png",
        SCREENS / "urban-district-selected.png",
        SCREENS / "ude-dark.png"],
       "urban", BLEU)
annexe("Maintenance  -  captures",
       [SCREENS / "maintenance-diagnostic-live.png",
        SCREENS / "monthly_trends.png",
        SCREENS / "quality_completeness.png"],
       "maint", TEAL)
annexe("L'IA Pero  -  captures",
       [SCREENS / "iapero-app-live.png",
        SCREENS / "iapero-recommendation-live.png"],
       "iapero", ROUGE)

prs.save(str(OUT))
print("OK ->", OUT)
print("slides:", len(prs.slides._sldIdLst))
