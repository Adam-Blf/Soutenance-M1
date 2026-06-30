# -*- coding: utf-8 -*-
"""
Generateur PDF Q&A - Soutenance Bloc 1 & 2 RNCP40875
EFREI M1 Data Engineering & IA - Adam Beloucif & Emilien Morice
"""

from fpdf import FPDF
import os

# ─── couleurs EFREI ───────────────────────────────────────────────────────────
NAVY    = (5, 24, 50)        # #051832
BLUE    = (22, 55, 103)      # #163767
LBLUE   = (12, 120, 180)     # #0C78B4
PINK    = (255, 67, 184)     # #FF43B8
WHITE   = (255, 255, 255)
GRAY    = (50, 50, 50)
LGRAY   = (245, 246, 248)
MGRAY   = (150, 150, 150)

def clean(txt):
    """Remplace mediopoint et tirets longs."""
    return (txt
            .replace('·', '-')
            .replace('×', 'x')
            .replace('→', '->')
            .replace('—', ' - ')
            .replace('–', ' - ')
            .replace('×', 'x')
            .replace('â', ' - ')
            .replace('â', ' - ')
            .replace('⋅', '-')
            .replace('·', ' - ')
            .replace('—', ' - ')
            .replace('–', ' - ')
            .replace('’', "'")
            .replace('‘', "'")
            .replace('“', '"')
            .replace('”', '"'))


class SoutenancePDF(FPDF):

    def header(self):
        # Barre navy en haut
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 18, 'F')
        # Accent magenta
        self.set_fill_color(*PINK)
        self.rect(0, 18, 210, 2, 'F')
        # Texte gauche
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 9)
        self.set_xy(12, 5)
        self.cell(100, 6, 'EFREI - M1 Data Engineering & IA', border=0)
        # Texte droite
        self.set_font('Helvetica', '', 8)
        self.set_xy(110, 5)
        self.cell(90, 6, 'Soutenance Bloc 1 & 2 - RNCP40875', border=0, align='R')
        self.ln(14)

    def footer(self):
        self.set_y(-14)
        self.set_fill_color(*NAVY)
        self.rect(0, 283, 210, 14, 'F')
        self.set_fill_color(*PINK)
        self.rect(0, 283, 210, 1.5, 'F')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', '', 7.5)
        self.set_xy(12, 286)
        self.cell(130, 5, 'Adam Beloucif & Emilien Morice - Session 2026-2027')
        self.set_font('Helvetica', 'B', 8)
        self.set_xy(150, 286)
        self.cell(50, 5, f'Page {self.page_no()}', align='R')

    # ── helpers ──────────────────────────────────────────────────────────────

    def section_title(self, title, color=BLUE):
        self.ln(4)
        self.set_fill_color(*color)
        self.rect(self.l_margin, self.get_y(), 4, 9, 'F')
        self.set_x(self.l_margin + 7)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*color)
        self.cell(0, 9, clean(title), ln=True)
        self.set_draw_color(*color)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)
        self.set_text_color(*GRAY)

    def subsection(self, title):
        self.ln(3)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*LBLUE)
        self.set_x(self.l_margin)
        self.cell(0, 7, clean(title), ln=True)
        self.set_draw_color(*LBLUE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.l_margin + 80, self.get_y())
        self.ln(3)
        self.set_text_color(*GRAY)

    def qa(self, question, answer, badge=None):
        """Paire question - reponse."""
        # Verification saut de page
        if self.get_y() > 250:
            self.add_page()

        q = clean(question)
        a = clean(answer)

        # Badge de competence optionnel
        if badge:
            self.set_fill_color(*PINK)
            self.set_text_color(*WHITE)
            self.set_font('Helvetica', 'B', 7)
            self.set_x(self.l_margin)
            self.cell(len(badge) * 3.5 + 4, 5, badge, fill=True, border=0)
            self.ln(5)

        # Question
        self.set_fill_color(*BLUE)
        self.rect(self.l_margin, self.get_y(), 2.5, 6.5, 'F')
        self.set_x(self.l_margin + 5)
        self.set_font('Helvetica', 'B', 10.5)
        self.set_text_color(*BLUE)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 5, 6.5, q)
        self.ln(1)

        # Reponse (fond gris clair)
        x = self.l_margin + 5
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin - 5

        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(*GRAY)

        # On calcule la hauteur approximative du texte
        nb_lines = self.get_string_width(a) / (w - 4) + a.count('\n') + 1
        h_approx = max(int(nb_lines) + 2, 3) * 5.5 + 6

        # Fond gris
        self.set_fill_color(*LGRAY)
        self.rect(x - 2, y, w + 2, h_approx, 'F')

        self.set_xy(x, y + 2)
        self.multi_cell(w - 2, 5.5, a)
        self.ln(6)

    def info_box(self, text, color=PINK):
        """Boite d'information."""
        if self.get_y() > 255:
            self.add_page()
        x = self.l_margin
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        self.set_fill_color(*(tuple(min(c + 200, 255) for c in color)))
        self.set_draw_color(*color)
        self.set_line_width(0.6)
        self.rect(x, y, w, 12, 'FD')
        self.set_fill_color(*color)
        self.rect(x, y, 3, 12, 'F')
        self.set_font('Helvetica', 'BI', 9)
        self.set_text_color(*NAVY)
        self.set_xy(x + 6, y + 3)
        self.multi_cell(w - 8, 5, clean(text))
        self.ln(4)
        self.set_text_color(*GRAY)

    def table_row(self, cols, widths, bold=False, header=False):
        """Ligne de tableau simple."""
        if header:
            self.set_fill_color(*NAVY)
            self.set_text_color(*WHITE)
            self.set_font('Helvetica', 'B', 8.5)
        elif bold:
            self.set_fill_color(*LGRAY)
            self.set_text_color(*BLUE)
            self.set_font('Helvetica', 'B', 8.5)
        else:
            self.set_fill_color(*WHITE)
            self.set_text_color(*GRAY)
            self.set_font('Helvetica', '', 8.5)
        x = self.l_margin
        y = self.get_y()
        for col, w in zip(cols, widths):
            self.rect(x, y, w, 7, 'FD' if header or bold else 'D')
            self.set_xy(x + 1, y + 1)
            self.cell(w - 2, 5, clean(str(col)), border=0)
            x += w
        self.ln(7)
        self.set_text_color(*GRAY)

    def cover_page(self):
        """Page de couverture."""
        # Fond navy haut
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 80, 'F')
        # Bande rose
        self.set_fill_color(*PINK)
        self.rect(0, 80, 210, 4, 'F')

        # Logo textuel EFREI
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 32)
        self.set_xy(20, 18)
        self.cell(0, 14, 'EFREI', align='L')
        self.set_font('Helvetica', '', 11)
        self.set_xy(20, 33)
        self.cell(0, 6, 'Ecole d\'Ingenieur du Numerique', align='L')
        self.set_xy(20, 40)
        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 5, 'M1 Data Engineering & IA - Session 2026-2027', align='L')

        # Accent bleu ciel
        self.set_fill_color(*LBLUE)
        self.rect(150, 18, 3, 40, 'F')

        # Titre principal
        self.set_text_color(*NAVY)
        self.set_font('Helvetica', 'B', 22)
        self.set_xy(20, 98)
        self.cell(170, 12, 'Guide de Preparation', align='C', ln=True)
        self.set_font('Helvetica', 'B', 18)
        self.set_xy(20, self.get_y())
        self.cell(170, 10, 'Questions Jury - 20 Minutes d\'Echange', align='C', ln=True)

        # Ligne decorative
        self.set_draw_color(*LBLUE)
        self.set_line_width(1.2)
        self.line(40, self.get_y() + 4, 170, self.get_y() + 4)
        self.ln(16)

        # Sous-titre
        self.set_font('Helvetica', '', 12)
        self.set_text_color(*GRAY)
        self.set_x(20)
        self.cell(170, 7, 'Soutenance Bloc 1 & 2 - RNCP40875', align='C', ln=True)
        self.ln(10)

        # Auteurs
        self.set_fill_color(*BLUE)
        self.rect(50, self.get_y(), 110, 16, 'F')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 12)
        self.set_xy(50, self.get_y() + 2)
        self.cell(110, 6, 'Adam Beloucif & Emilien Morice', align='C', ln=True)
        self.set_font('Helvetica', '', 9)
        self.set_xy(50, self.get_y())
        self.cell(110, 5, 'Villejuif, 2026', align='C', ln=True)
        self.ln(12)

        # 3 projets
        self.set_draw_color(*BLUE)
        self.set_line_width(0.3)
        cols = ['Projet 1', 'Projet 2', 'Projet 3']
        subs = ['Urban Data Explorer', 'Maintenance Predictive', 'L\'IA Pero']
        blocs = ['Bloc 1 - C1.1 > C2.4', 'Bloc 2 DS - C3.1 > C4.3', 'Bloc 2 GenAI - C5.1 > C5.3']
        colors_proj = [LBLUE, BLUE, PINK]
        x0 = 18
        for i, (col, sub, bloc, col_c) in enumerate(zip(cols, subs, blocs, colors_proj)):
            bx = x0 + i * 58
            self.set_fill_color(*col_c)
            self.rect(bx, self.get_y(), 56, 26, 'F')
            self.set_text_color(*WHITE)
            self.set_font('Helvetica', 'B', 10)
            self.set_xy(bx + 2, self.get_y() + 3)
            self.cell(52, 6, col, align='C', ln=False)
            self.set_xy(bx + 2, self.get_y() + 9)
            self.set_font('Helvetica', 'B', 8.5)
            self.cell(52, 5, sub, align='C', ln=False)
            self.set_xy(bx + 2, self.get_y() + 15)
            self.set_font('Helvetica', '', 7)
            self.cell(52, 4, bloc, align='C', ln=False)
        self.ln(36)

        # Note de bas de couverture
        self.set_font('Helvetica', 'I', 8.5)
        self.set_text_color(*MGRAY)
        self.set_x(20)
        self.cell(170, 5, 'Document confidentiel - Preparation interne - Ne pas distribuer', align='C')


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENU Q&A
# ═══════════════════════════════════════════════════════════════════════════════

def build_pdf():
    pdf = SoutenancePDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(18, 22, 18)
    pdf.set_auto_page_break(auto=True, margin=18)

    # ─── PAGE DE COUVERTURE ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.cover_page()

    # ─── SECTION 0 : VUE D'ENSEMBLE ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('Vue d\'ensemble - Les 3 projets')

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.5, clean(
        'La soutenance dure 50 minutes : 30 min de presentation/demo + 20 min d\'echange jury. '
        'L\'evaluation est collective en presentation mais individualisee en notation. '
        'Structure imposee : besoin metier -> choix techniques -> realisation -> preuve -> resultats -> limites.'
    ))
    pdf.ln(4)

    # Tableau des 3 projets
    pdf.table_row(['Projet', 'Stack', 'Competences', 'Chiffres cles'], [42, 60, 38, 36], header=True)
    pdf.table_row(['Urban Data Explorer',
                   'Polars, PostgreSQL, Cassandra, Kafka, FastAPI, React',
                   'C1.1 a C2.4',
                   '24 sources, 102 tests'], [42, 60, 38, 36])
    pdf.table_row(['Maintenance Predictive',
                   'sklearn, XGBoost, MLP, Streamlit, CodeCarbon',
                   'C3.1 a C4.3',
                   'F1=0.886, AUC=0.995'], [42, 60, 38, 36], bold=True)
    pdf.table_row(['L\'IA Pero (GenAI)',
                   'SBERT all-MiniLM-L6-v2, Gemini, Streamlit',
                   'C5.1 a C5.3',
                   '384 dims, seuil 0.35'], [42, 60, 38, 36])
    pdf.ln(4)

    # Tableau metriques maintenance
    pdf.subsection('Metriques Maintenance Predictive - a retenir par coeur')
    pdf.table_row(['Modele', 'F1', 'ROC-AUC', 'CV F1', 'Score sel.', 'CO2'],
                  [52, 22, 24, 22, 28, 20], header=True)
    pdf.table_row(['LogReg (baseline)', '0.747', '0.959', '0.750', '0.746', '0.3 mg'],
                  [52, 22, 24, 22, 28, 20])
    pdf.table_row(['Random Forest', '0.863', '0.992', '0.844', '0.839', '8.2 mg'],
                  [52, 22, 24, 22, 28, 20])
    pdf.table_row(['XGBoost (RETENU)', '0.886', '0.995', '0.886', '0.880', '6.1 mg'],
                  [52, 22, 24, 22, 28, 20], bold=True)
    pdf.table_row(['MLP 64-32-16 (DL)', '0.836', '0.984', '0.795', '0.790', '3.8 mg'],
                  [52, 22, 24, 22, 28, 20])
    pdf.ln(4)

    pdf.info_box(
        'CONSEIL GENERAL : Toujours citer le code de competence (C1.1, C4.3...) quand vous repondez. '
        'Structure de reponse en 30-45 s : Choix -> Justification -> Preuve dans le code -> Limite.',
        BLUE
    )

    pdf.subsection('5 erreurs fatales a eviter')
    errors = [
        '1. Presenter sans relier aux competences -> toujours citer C×.×.',
        '2. Resultats sans justification -> chaque choix a un "parce que".',
        '3. Oublier les limites -> en donner a chaque projet (recul pro = points).',
        '4. Demo trop longue -> 90 s max chacune, scenariee.',
        '5. Individualisation non preparee -> reponses personnelles, pas "on a fait".',
    ]
    for e in errors:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*GRAY)
        pdf.set_x(pdf.l_margin + 2)
        pdf.cell(0, 6, clean(e), ln=True)
    pdf.ln(3)

    # ─── SECTION 1 : BLOC 1 - URBAN DATA EXPLORER ────────────────────────────
    pdf.add_page()
    pdf.section_title('Bloc 1 - Urban Data Explorer', LBLUE)

    pdf.info_box(
        'Pitch : Plateforme data complete d\'exploration du logement parisien - '
        '24 sources Open Data, architecture medaillon Bronze/Silver/Gold en Polars, '
        'PostgreSQL en etoile, Cassandra pour le streaming, Kafka, '
        'API FastAPI securisee JWT + quotas, dashboard React/MapLibre charte DSFR.',
        LBLUE
    )

    pdf.subsection('Questions issues des QA_JURY.md (deja preparees)')

    pdf.qa(
        'Pourquoi PostgreSQL ?',
        'Besoin analytique structure (agregats par arrondissement x mois) -> schema en etoile classique, '
        'integrite referentielle (FK dim_arrondissement), index sur les axes de requete. '
        'Teste en charge : scripts/test_load_postgres.py mesure p95 reel sur les jointures fact/dim.',
        'C1.1'
    )

    pdf.qa(
        'Comment avez-vous garanti l\'integrite des donnees ?',
        'Contraintes NOT NULL + FK + cles primaires composees cote PG. Drapeau data_source (real/reference) '
        'sur chaque ligne Gold pour la tracabilite. Validation des codes arrondissement par regex normalisee '
        '(_normalize_code). Tests pytest sur les transformations.',
        'C1.1'
    )

    pdf.qa(
        'Pourquoi Cassandra en NoSQL ?',
        'Donnees d\'evenements semi-structurees a forte velocite (flux urbains). Modelisation query-first : '
        'partition par event_type, clustering event_time DESC, TTL 7 jours (la donnee chaude expire seule). '
        'Deux patterns d\'acces : par type et par arrondissement. '
        'PG aurait impose un schema rigide et des purges manuelles.',
        'C1.2'
    )

    pdf.qa(
        'Comment le Data Lake integre-t-il des sources variees ?',
        '24 sources / 8 familles (CSV, GeoJSON, API) atterrissent en Bronze (brut Parquet), '
        'normalisees en Silver (codes, geocodage point-in-polygon IRIS), '
        'agregees en Gold (datamarts dashboard/timeline). '
        'Le format colonnaire Parquet aligne lecture analytique et cout stockage.',
        'C1.3'
    )

    pdf.qa(
        'Quelles contraintes de securite ?',
        'JWT HS256 (secret env var, jamais commite), roles viewer/admin, 401/403 differencies. '
        'Quotas par IP fenetre glissante 120 anonyme / 600 authentifie -> 429. '
        'CORS restreint a l\'origine du front. '
        'Donnees Open Data uniquement, pas de donnee personnelle (RGPD by design).',
        'C2.1'
    )

    pdf.qa(
        'Comment l\'architecture est-elle scalable ?',
        'Stateless API -> replicable horizontalement. Kafka decouple producteurs/consommateurs. '
        'Cassandra scale lineairement par ajout de noeuds. Parquet partitionne par date. '
        'Limite assumee : demo mono-noeud (replication_factor 1), '
        'on documente le chemin vers un cluster 3 noeuds.',
        'C1.4'
    )

    pdf.qa(
        'Comment avez-vous teste la resilience ?',
        'scripts/test_resilience.py : kill du conteneur Postgres -> l\'API bascule en fallback parquet local '
        '(reponse degradee mais 200) -> restart -> mesure du temps de recuperation. '
        'Healthchecks + restart: unless-stopped + depends_on: service_healthy dans le compose.',
        'C1.4'
    )

    pdf.qa(
        'Comment mesurez-vous la performance des pipelines ?',
        'etl/metrics.py persiste par etape : duree, lignes, octets, lignes/sec dans un parquet de metriques, '
        'expose via GET /pipeline/metrics. Optimisations : lru_cache sur le geocodage inverse, '
        'Polars (Rust) plutot que pandas, Parquet colonnaire.',
        'C2.4'
    )

    pdf.qa(
        'Micro-batch vs temps reel ?',
        'Les deux : consumer temps reel evenement par evenement -> Cassandra. '
        'streaming/microbatch.py agrege en fenetres tumbling 10 s '
        '(count, moyenne par type x arrondissement). '
        'Le micro-batch lisse la charge d\'ecriture et fournit des agregats prets a servir.',
        'C2.2'
    )

    pdf.subsection('Questions supplementaires possibles')

    pdf.qa(
        'Pourquoi Polars plutot que pandas ?',
        'Polars est ecrit en Rust avec execution lazy et parallelisme automatique. '
        'Sur nos volumes (24 sources, fichiers jusqu\'a quelques centaines de Mo), '
        'Polars est environ 10x plus rapide que pandas sur les jointures et agregations. '
        'Sans cluster Spark (cout zero), c\'est le meilleur rapport perf/complexite pour un ETL local ou Docker.',
        'C2.3'
    )

    pdf.qa(
        'Pourquoi FastAPI et pas Flask ou Django ?',
        'FastAPI genere le Swagger automatiquement (exigence C2.1 demontrable en demo live), '
        'supporte l\'async natif (utile pour les appels externes aux APIs ville), '
        'valide les schemas avec Pydantic (moins de code de validation manuel). '
        'Flask est trop bas niveau pour une API avec auth + quotas. '
        'Django est sur-specifie pour une API pure sans ORM metier.',
        'C2.1'
    )

    pdf.qa(
        'Quelle est la difference entre Bronze, Silver et Gold dans votre Data Lake ?',
        'Bronze : donnees brutes telles que recues (CSV, GeoJSON, JSON API), '
        'sans transformation, partitionnees par date d\'ingestion. '
        'Silver : donnees normalisees (codes arrondissement standardises, geocodage IRIS resolu, '
        'valeurs manquantes imputees), pret pour la jointure. '
        'Gold : agregats metier (prix m2 median/arrondissement/mois, flux urbains par heure) '
        'directement consommables par le dashboard et l\'API.',
        'C1.3'
    )

    pdf.qa(
        'Comment avez-vous gere les 24 sources heterogenes ?',
        'Chaque source a un connecteur dedie dans etl/external.py '
        '(CSV DVF, GeoJSON arrondissements, API Etalab). '
        'Le pipeline Bronze ne transforme pas, il enregistre fidelement. '
        'La couche Silver applique une normalisation commune : '
        'code arrondissement sur 2 chiffres, timestamp ISO 8601, geometrie WGS84. '
        'Un drapeau data_source tracabilite quelle source a produit chaque enregistrement.',
        'C2.3'
    )

    pdf.qa(
        'Comment fonctionne votre systeme de quotas exactement ?',
        'Fenetre glissante par adresse IP sur 60 s : '
        '120 requetes max pour les appels non authentifies, 600 pour les appels avec JWT valide. '
        'Un token bucket en memoire (dict IP -> compteur + horodatage reset) '
        'renvoie 429 Too Many Requests avec l\'entete Retry-After quand le seuil est depasse. '
        'Limite : pas persistant entre redemarrages -> Redis en production.',
        'C2.1'
    )

    pdf.qa(
        'Quelles sont les limites de votre architecture en production ?',
        'Mono-noeud : Cassandra avec replication_factor 1, '
        'PostgreSQL sans replica standby, Kafka mono-broker. '
        'Pas de HA reelle -> une panne du noeud coupe tout. '
        'Roadmap documentee : cluster Cassandra 3 noeuds (RF=3), '
        'PG avec streaming replication + pgBouncer, Kafka 3 brokers + Schema Registry. '
        'Par design pour la demo : ressources limitees, objectif de demontrer les patterns, pas la scalabilite reelle.',
        'C1.4'
    )

    # ─── SECTION 2 : BLOC 2 - MAINTENANCE PREDICTIVE ─────────────────────────
    pdf.add_page()
    pdf.section_title('Bloc 2 Data Science - Maintenance Predictive Industrielle', BLUE)

    pdf.info_box(
        'Pitch : Systeme intelligent multi-modeles predisant la panne machine sous 24 h '
        'a partir de capteurs IoT (vibration, temperature, RPM, pression). '
        '4 modeles compares dont 1 Deep Learning. Dashboard decisonnel Streamlit. '
        'API FastAPI. Mesure CO2 CodeCarbon. Dataset : Kaggle - 24 042 lignes x 15 variables.',
        BLUE
    )

    pdf.subsection('Questions issues de QA_JURY.md')

    pdf.qa(
        'Quelles donnees ? Quels problemes de qualite ?',
        'Kaggle industrial_machine_maintenance : 24 042 lignes, 15 variables capteurs '
        '(vibration_rms, temperature_motor, rpm, pressure_level, operating_mode). '
        'Problemes : valeurs manquantes (imputation mediane fit sur train uniquement), '
        'classes desequilibrees (panne 24 h rare), '
        'outliers capteurs (winsorisation justifiee par l\'EDA).',
        'C3.1'
    )

    pdf.qa(
        'Pourquoi ces variables ?',
        'EDA -> vibration et temperature moteur sont les plus correlees a la panne '
        '(confirme ensuite par feature importance : coherence physique, '
        'l\'usure mecanique genere vibration et echauffement). '
        'On garde les variables redondantes sous surveillance multicolinearite '
        'plutot que de supprimer mecaniquement.',
        'C3.3'
    )

    pdf.qa(
        'Comment avez-vous traite le desequilibre des classes ?',
        'Stratified split pour preserver les proportions. '
        'class_weight="balanced" sur LogReg et Random Forest. '
        'scale_pos_weight sur XGBoost. '
        'Metriques adaptees : F1, PR-AUC, Recall prioritaire '
        '(un faux negatif = panne non detectee = cout maximal). '
        'Ajustement du seuil de decision (models/optimal_threshold.json) : '
        'par defaut 0.5 mais optimise empiriquement sur la courbe Precision/Recall.',
        'C3.1'
    )

    pdf.qa(
        'Quels modeles ? Pourquoi XGBoost en final ?',
        '4 modeles : LogReg (baseline interpretable), Random Forest, XGBoost, MLP 64-32-16 (DL impose). '
        'XGBoost retenu : F1 0.886, ROC-AUC 0.995, '
        'mais surtout score de selection = F1 - 0.5 x sigma(F1 CV) -> '
        'meilleur compromis performance/stabilite. '
        'Le MLP fait moins bien : dataset tabulaire de taille moyenne, '
        'le gradient boosting reste l\'etat de l\'art.',
        'C4.2'
    )

    pdf.qa(
        'Comment avez-vous evite le surapprentissage ?',
        'Pipelines sklearn : preprocessing fit uniquement sur train (ADR anti-data-leakage dedie). '
        'Cross-validation 5 folds stratifiee. '
        'Early stopping MLP (patience=10 sur val_loss). '
        'Regularisation : alpha MLP, subsample/colsample XGBoost. '
        'Comparaison systematique train/test scores pour detecter l\'overfit.',
        'C4.2'
    )

    pdf.qa(
        'Et l\'ecoresponsabilite ? (explicite dans C4.3)',
        'CodeCarbon mesure le CO2 par entrainement : '
        'XGBoost 6.1 mg vs RF 8.2 mg pour de meilleures perfs -> '
        'retenu aussi sur ce critere. '
        'La LogReg a 0.3 mg reste pertinente si la contrainte carbone domine. '
        'C\'est explicitement dans le referentiel C4.3 : a mentionner devant le jury.',
        'C4.3'
    )

    pdf.qa(
        'A qui s\'adresse le dashboard ?',
        'Responsable maintenance : KPI flotte, simulation de scenario machine (sliders capteurs), '
        'prediction temps reel avec probabilite, '
        'top variables influentes en langage metier '
        '("vibration au-dessus de X -> risque eleve"). '
        'Distinct des visuels EDA du rapport (consigne explicite du sujet).',
        'C3.2'
    )

    pdf.qa(
        'Limites du modele ?',
        'Donnees simulees (pas de bruit capteur reel). '
        'Pas de dimension temporelle exploitee (un LSTM sur sequences serait la suite). '
        'Derive possible en production -> monitoring et reentrainement periodique necessaires. '
        'Un seul dataset Kaggle : generalisation non validee sur d\'autres types de machines.',
        'C4.3'
    )

    pdf.subsection('Questions supplementaires possibles')

    pdf.qa(
        'Pourquoi avoir choisi ce dataset Kaggle ?',
        'Criteres : donnees de capteurs industriels reels (format IoT typique), '
        'suffisamment grand (24 042 lignes, pas de sur-ajustement trivial), '
        'variable cible claire (failure_within_24h binaire), '
        'desequilibre de classes present (realiste, force l\'apprentissage des techniques adaptees). '
        'Dataset open source, reproductible par le jury.',
        'C3.1'
    )

    pdf.qa(
        'Expliquez votre pipeline sklearn et pourquoi le preprocessing est fit uniquement sur le train set.',
        'Pipeline sklearn encapsule : Imputer (mediane) -> StandardScaler -> modele. '
        'Le fit() est appele une seule fois sur X_train. '
        'Lors du predict(), le transform() utilise les parametres appris sur train. '
        'Si on faisait fit sur tout le dataset, '
        'les statistiques de normalisation incorporeraient de l\'information du jeu de test '
        '(data leakage) et les metriques seraient optimistes. '
        'Documente dans notre ADR anti-data-leakage.',
        'C3.1'
    )

    pdf.qa(
        'Qu\'est-ce que l\'early stopping et pourquoi l\'avez-vous utilise sur le MLP ?',
        'L\'early stopping interrompt l\'entrainement quand la perte sur le jeu de validation '
        'ne s\'ameliore plus pendant N epochs (patience=10 ici). '
        'Sans early stopping, le MLP continuerait a apprendre le bruit du train set '
        '(overfit) et degraderait ses performances sur les donnees inedites. '
        'C\'est une forme de regularisation implicite, complementaire a la regularisation L2 (alpha).',
        'C4.2'
    )

    pdf.qa(
        'Comment CodeCarbon mesure-t-il les emissions CO2 ?',
        'CodeCarbon echantillonne la consommation CPU/GPU/RAM en temps reel via les APIs systeme '
        '(Intel RAPL, NVIDIA NVML). Il multiplie l\'energie consommee (kWh) '
        'par le facteur d\'emission carbone du reseau electrique local (gCO2eq/kWh), '
        'recupere via un mapping pays/region. '
        'Notre mesure (0.3 a 8.2 mg selon le modele) est une estimation : '
        'la machine de calcul n\'etait pas dediee, la mesure inclut le fond de l\'OS.',
        'C4.3'
    )

    pdf.qa(
        'Pourquoi avoir choisi F1 - 0.5*sigma(F1_CV) comme score de selection ?',
        'F1 seul ne capture pas la stabilite entre les folds. '
        'Un modele avec F1=0.90 mais sigma=0.15 est moins fiable '
        'qu\'un modele F1=0.88 avec sigma=0.02. '
        'La penalite 0.5*sigma est un compromis : '
        'elle penalise la variance sans ignorer la performance moyenne. '
        'XGBoost ressort gagnant sur les deux criteres (F1 et stabilite), '
        'ce qui renforce la confiance dans le choix.',
        'C4.3'
    )

    pdf.qa(
        'Quelle est la difference entre ROC-AUC et PR-AUC ? Quand preferer l\'une ou l\'autre ?',
        'ROC-AUC mesure la capacite a distinguer les classes sur toutes les paires '
        '(taux vrai positif vs taux faux positif). Elle est optimiste en cas de desequilibre '
        'car le grand nombre de vrais negatifs tire le TPR vers le haut. '
        'PR-AUC (Precision-Recall AUC) est plus severe : elle mesure la precision '
        'a chaque seuil de rappel, penalisant les faux positifs sur la classe minoritaire. '
        'En maintenance predictive avec classes desequilibrees, '
        'PR-AUC est le critere principal : on veut detecter les pannes sans noyer '
        'le technicien sous les fausses alarmes.',
        'C4.3'
    )

    pdf.qa(
        'Comment detecteriez-vous une derive du modele en production ?',
        'Deux types de derive : derive des donnees (data drift) et derive des predictions. '
        'Pour la data drift : monitorer les distributions des capteurs '
        '(test KS ou PSI entre la fenetre courante et la distribution d\'entrainement). '
        'Pour la derive des predictions : mesurer le taux de pannes predites vs pannes reelles '
        'sur une fenetre glissante. '
        'Outil : Evidently AI ou Great Expectations. '
        'Seuil de reentrainement : quand le PSI > 0.2 ou le F1 glissant chute de 5 points.',
        'C4.3'
    )

    pdf.qa(
        'Comment avez-vous evite le data leakage ?',
        'Pipeline sklearn : fit uniquement sur X_train, jamais sur X_val ou X_test. '
        'Pas de feature engineering dependant de la cible (pas de target encoding naif). '
        'Split chronologique envisage mais non applique : '
        'le dataset est simule (pas de dimension temporelle reelle). '
        'Documente dans l\'ADR anti-data-leakage du repo.',
        'C3.1'
    )

    # ─── SECTION 3 : BLOC 2 IA GENERATIVE ────────────────────────────────────
    pdf.add_page()
    pdf.section_title('Bloc 2 IA Generative - L\'IA Pero (Cocktails)', PINK)

    pdf.info_box(
        'Pitch : Moteur de recommandation de cocktails par IA semantique. '
        'SBERT all-MiniLM-L6-v2 (embeddings 384 dims), similarite cosinus, '
        'guardrail semantique seuil 0.35, RAG + Google Gemini avec cache MD5. '
        'Interface Streamlit Speakeasy. Thematique alternative validee par l\'Annexe I du sujet.',
        PINK
    )

    pdf.subsection('Questions issues de QA_JURY.md')

    pdf.qa(
        'Pourquoi ce cas d\'usage ?',
        'Recommandation par preferences exprimees en langage naturel : '
        'les filtres classiques echouent sur "frais et fruite avec une touche tropicale". '
        'Thematique alternative validee par l\'Annexe I du sujet. '
        'La GenAI est adaptee car il faut comprendre (semantique) '
        'ET produire (recette personnalisee).',
        'C5.1'
    )

    pdf.qa(
        'Quel modele ? Pourquoi ?',
        'SBERT all-MiniLM-L6-v2 local : gratuit, rapide, 384 dims, '
        'suffisant pour la similarite de phrases courtes, '
        'pas besoin d\'un gros modele pour le retrieval. '
        'Gemini free-tier pour la generation uniquement '
        '(RAG : le contexte recupere borne la generation).',
        'C5.2'
    )

    pdf.qa(
        'Comment evaluez-vous la qualite des reponses ?',
        'Trois niveaux : '
        '(1) guardrail semantique seuil 0.35 teste sur jeux de requetes hors-domaine, '
        '(2) tableau requete -> attendu -> score de similarite -> decision, '
        '(3) revue humaine des generations (coherence ingredients/recette). '
        'Performances dans le rapport (objectif < 3 s de reponse tenu).',
        'C5.3'
    )

    pdf.qa(
        'Quels parametres avez-vous ajustes ?',
        'Seuil de pertinence du guardrail (0.35 : arbitrage faux rejets / hors-sujets). '
        'Nombre de resultats Top-N. '
        'Temperature de generation Gemini. '
        'Structure du prompt RAG (contexte ingredients + profil gustatif injectes).',
        'C5.3'
    )

    pdf.qa(
        'Quels risques ?',
        'Hallucinations (mitigue par RAG + cache). '
        'Dependance API externe (mitigue par fallback et cache MD5). '
        'Biais du dataset cocktails. '
        'Usage responsable de l\'alcool mentionne comme limite ethique. '
        'Cout : appels strictement limites + caching = conforme a la contrainte free-tier du sujet.',
        'C5.3'
    )

    pdf.qa(
        'Comment l\'industrialiser ?',
        'DB vectorielle (pgvector/FAISS) au lieu de la matrice en memoire. '
        'Fine-tuning SBERT sur le domaine. '
        'Monitoring des prompts/reponses. '
        'Journalisation des appels GenAI. '
        'Validation humaine en boucle.',
        'C5.2'
    )

    pdf.qa(
        'Pourquoi SBERT et pas un embedding proprietaire (OpenAI, Cohere) ?',
        'Choix cout/autonomie : SBERT all-MiniLM-L6-v2 tourne en local, '
        'aucun appel reseau sur le retrieval, 0 latence API, 0 cout par token. '
        'Pour la similarite de phrases courtes sur un referentiel ferme (cocktails), '
        '384 dims suffisent : verifie empiriquement (Top-5 coherents sur les requetes de test). '
        'Un embedding proprietaire aurait cree une dependance externe sur le chemin critique du retrieval.',
        'C5.2'
    )

    pdf.qa(
        'Que se passe-t-il quand un utilisateur demande hors-domaine ?',
        'Le guardrail calcule la similarite cosinus entre la requete et l\'ensemble du referentiel cocktails. '
        'Si le max est inferieur a 0.35, la requete est rejetee proprement '
        'avec un message explicite avant tout appel Gemini. '
        'Teste sur : "repare mon velo", requetes vides, injections de prompt -> '
        'tous tombent sous le seuil. '
        'Risque residuel : une requete semantiquement proche d\'un cocktail par accident peut passer '
        '-> limite documentee.',
        'C5.3'
    )

    pdf.qa(
        'Pourquoi le seuil a 0.35 precisement ?',
        'Calibration empirique sur 30 requetes labelisees manuellement '
        '(15 in-domain, 15 hors-domain). '
        'Courbe Recall/Precision du guardrail en variant le seuil de 0.1 a 0.6. '
        'A 0.35 on maximise le F1 du guardrail '
        '(rejeter le hors-domaine sans bloquer le in-domain). '
        'Documente dans le rapport, reproductible via le script d\'evaluation.',
        'C5.3'
    )

    pdf.subsection('Questions supplementaires possibles')

    pdf.qa(
        'Qu\'est-ce qu\'un embedding vectoriel et pourquoi SBERT ?',
        'Un embedding est une representation d\'un texte sous forme de vecteur numerique '
        'dans un espace semantique (ici 384 dimensions). '
        'Deux textes semantiquement proches ont des vecteurs proches (cosinus eleve). '
        'SBERT (Sentence-BERT) est un modele transformer fine-tune pour produire '
        'des embeddings de phrases complets (pas juste des tokens), '
        'ce qui le rend bien adapte a la comparaison de descriptions de cocktails.',
        'C5.2'
    )

    pdf.qa(
        'Expliquez la similarite cosinus avec un exemple concret.',
        'La similarite cosinus mesure l\'angle entre deux vecteurs, independamment de leur norme. '
        'Exemple : vecteur("frais et fruity") et vecteur("Mojito : menthe, citron vert, sucre") '
        'ont un angle faible (similaires) -> cosinus proche de 1. '
        'vecteur("repare mon velo") et vecteur("Mojito") ont un angle eleve -> cosinus proche de 0. '
        'Formule : cos(theta) = (A.B) / (||A|| x ||B||). '
        'Avantage : insensible a la longueur des textes, '
        'ce qui compte c\'est la direction semantique.',
        'C5.2'
    )

    pdf.qa(
        'Qu\'est-ce que le RAG et pourquoi l\'avez-vous utilise ?',
        'RAG = Retrieval-Augmented Generation. '
        'Au lieu de laisser le LLM generer librement (risque d\'hallucination), '
        'on recupere (retrieval) les cocktails les plus pertinents via SBERT + cosinus, '
        'on les injecte dans le prompt (augmented context), '
        'puis le LLM (Gemini) genere une reponse ancree dans ce contexte. '
        'Avantages : moins d\'hallucinations, reponses factuelles, '
        'pas besoin de fine-tuner le LLM sur notre domaine.',
        'C5.2'
    )

    pdf.qa(
        'Comment fonctionne votre cache MD5 ?',
        'A chaque appel Gemini, on calcule un hash MD5 '
        'de la requete normalisee + contexte recupere. '
        'Si ce hash existe dans le cache (fichier JSON local), '
        'on retourne la reponse deja generee sans appel API. '
        'Avantages : cout zero sur les requetes repetees, '
        'latence < 100 ms au lieu de 2-3 s, '
        'conforme a la contrainte free-tier (quotas Gemini). '
        'Limite : le cache ne prend pas en compte le contexte utilisateur precedent.',
        'C5.2'
    )

    pdf.qa(
        'Quels biais votre systeme peut-il introduire ?',
        'Biais de dataset : le referentiel de cocktails (cocktails.csv) '
        'sur-represente les cocktails anglo-saxons et sous-represente les boissons non-alcoolisees. '
        'Biais de representation : SBERT a ete entraine sur un corpus anglais general, '
        'pas sur la terminologie de la mixologie. '
        'Biais de confirmation : le cache peut retourner une vieille reponse '
        'si le referentiel a ete mis a jour. '
        'Biais ethique : le systeme ne verifie pas l\'age de l\'utilisateur (limite documentee).',
        'C5.3'
    )

    pdf.qa(
        'Comment passeriez-vous en production ce systeme ?',
        'Infrastructure : conteneuriser l\'app Streamlit + modele SBERT via Docker. '
        'Remplacement de la matrice en memoire par FAISS ou pgvector pour le retrieval scalable. '
        'Cache Redis au lieu du fichier JSON local. '
        'Monitoring : journalisation des requetes/reponses dans une DB '
        'pour detecter les derives et alimenter le fine-tuning. '
        'CI/CD : tests automatiques du guardrail a chaque mise a jour du referentiel. '
        'Conformite : filtre d\'age RGPD, '
        'disclaimer usage responsable de l\'alcool.',
        'C5.2'
    )

    # ─── SECTION 4 : INDIVIDUALISATION ───────────────────────────────────────
    pdf.add_page()
    pdf.section_title('Questions d\'individualisation - Adam Beloucif', NAVY)

    pdf.info_box(
        'IMPORTANT : L\'evaluation est individualisee. Repondez a la premiere personne. '
        'Jamais "on a fait", toujours "j\'ai concu", "j\'ai implemente", "j\'ai choisi".',
        NAVY
    )

    pdf.qa(
        'Quelle est votre contribution principale sur ce projet ?',
        'Sur Urban Data Explorer : j\'ai concu et implemente l\'architecture data de bout en bout '
        '(pipeline medaillon Polars, schema etoile PostgreSQL avec FK et index, '
        'modelisation Cassandra query-first, API FastAPI avec JWT et quotas). '
        'Sur Maintenance Predictive : j\'ai implemente les modeles XGBoost et MLP, '
        'le pipeline sklearn anti-leakage, la selection de modele par score composite '
        'et le dashboard Streamlit. '
        'Sur l\'IA Pero : j\'ai concu le pipeline SBERT, le guardrail semantique, '
        'le cache MD5 et l\'integration Gemini RAG.',
        None
    )

    pdf.qa(
        'Quelle est la competence que vous maitrisez le mieux ?',
        'C2.1 (API securisee) et C4.3 (evaluation comparative). '
        'Sur C2.1 : j\'ai implemente de A a Z le systeme JWT avec roles, '
        'les quotas par fenetre glissante et les codes d\'erreur differencies '
        '-> demonstrable live en 30 secondes. '
        'Sur C4.3 : j\'ai concu le score de selection F1 - 0.5*sigma, '
        'mesure le CO2 avec CodeCarbon et produit le tableau comparatif des 4 modeles.',
        None
    )

    pdf.qa(
        'Quel choix technique avez-vous personnellement porte et pourquoi ?',
        'J\'ai choisi Polars plutot que pandas/Spark pour l\'ETL Urban Data Explorer. '
        'Justification : moteur Rust, parallelisme automatique, '
        '10x plus rapide sur nos volumes sans le cout operationnel d\'un cluster Spark. '
        'J\'ai valide ce choix avec un benchmark rapide sur les 24 sources '
        'avant de l\'integrer dans le pipeline medaillon.',
        None
    )

    pdf.qa(
        'Quelle difficulte avez-vous rencontree et comment l\'avez-vous resolue ?',
        'Deux difficultes majeures. '
        'Premierement, la jointure spatiale IRIS (point-in-polygon) etait trop lente '
        '(> 30 s par fichier DVF) -> solution : cache LRU sur les resultats de geocodage '
        'et arrondi des coordonnees a 4 decimales (precision 11 m, suffisante pour IRIS). '
        'Deuxiemement, le desequilibre de classes en maintenance predictive '
        '(pannes rares) rendait l\'accuracy trompeuse -> '
        'solution : class_weight, PR-AUC, ajustement du seuil de decision.',
        None
    )

    pdf.qa(
        'Que referiez-vous differemment ?',
        'J\'integrerais les metriques de pipeline (rows/sec, duree par etape) '
        'des le premier commit, pas en consolidation finale. '
        'J\'ecrirais les tests unitaires en meme temps que le code (TDD), '
        'pas en fin de sprint. '
        'Sur le MLP, j\'experimentrais une architecture avec BatchNorm '
        'pour voir si les resultats s\'ameliorent. '
        'Sur l\'IA Pero, j\'utiliserais FAISS des le debut '
        'plutot qu\'une matrice en memoire.',
        None
    )

    pdf.qa(
        'Reponse si le jury souleve le binome ia-pero (Amina vs Emilien)',
        '"Le projet IA generative a ete mene dans un binome different, avec Amina Medjdoub. '
        'Emilien et moi presentons nos projets respectifs en commun '
        'car nos Blocs 1 et 2 sont lies. '
        'Sur l\'IA Pero, j\'ai personnellement concu et implemente '
        'le pipeline SBERT, le guardrail semantique, le cache MD5, '
        'l\'integration Gemini et l\'evaluation. '
        'Je peux repondre a toutes les questions techniques sur ce projet." '
        '-> Ne pas hesiter, ne pas s\'excuser. L\'evaluation est individualisee.',
        None
    )

    # ─── SECTION 5 : QUESTIONS PIEGES ────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('Questions pieges et rares', BLUE)

    pdf.qa(
        'Pourquoi avoir simule les donnees plutot que d\'utiliser des donnees reelles ?',
        'Le dataset Kaggle industrial_machine_maintenance est base sur des capteurs reels '
        'mais anonymises et legerement biaises par le createur pour le partage public. '
        'En contexte pedagogique, l\'objectif est de maitriser la methode, pas de resoudre un probleme industriel reel. '
        'En production, on utiliserait des donnees de l\'OPCUA du systeme SCADA de la machine, '
        'avec horodatage et historique de maintenance.',
        None
    )

    pdf.qa(
        'Votre modele est-il reproductible ?',
        'Oui. Chaque notebook fixe la graine aleatoire (random_state=42) pour sklearn et numpy. '
        'Le dataset Kaggle est versionne et le lien de telechargement est dans le README. '
        'requirements.txt fixe les versions exactes (sklearn==1.4.0, xgboost==2.0.3). '
        'Les metriques sont sauvegardees dans reports/03/metrics_summary.json '
        'et peuvent etre regenerees avec : python scripts/03_train_models.py.',
        None
    )

    pdf.qa(
        'Comment avez-vous gere la vie privee dans Urban Data Explorer ?',
        'RGPD by design : uniquement des donnees Open Data (DVF, INSEE Filosofi, APIs Etalab). '
        'Pas de donnee personnelle : DVF ne contient que des adresses et prix (agregats), '
        'pas d\'identite d\'acheteur. '
        'Les logs API ne conservent pas l\'adresse IP au-dela de la fenetre de quota (60 s). '
        'Pas de cookie de tracking cote front.',
        None
    )

    pdf.qa(
        'Quel serait le cout de votre solution en production ?',
        'Urban Data Explorer : infrastructure Docker sur un VPS 4 vCPU / 8 Go RAM '
        'suffisant pour la demo -> ~25 EUR/mois (Hetzner CX31). '
        'En scalabilite : cluster Kubernetes managee (GKE Autopilot) -> '
        'proportionnel a la charge, ~100-300 EUR/mois. '
        'IA Pero : SBERT local = 0 EUR/token. Gemini free-tier = 0 EUR '
        'sous les quotas. En prod : Gemini Flash 8B -> ~0.0375 USD/M tokens d\'entree.',
        None
    )

    pdf.qa(
        'Qu\'est-ce que le principe de moindre privilege et comment l\'appliquez-vous ?',
        'Donner a chaque composant uniquement les permissions dont il a besoin, pas plus. '
        'Applications dans notre projet : '
        'role viewer = lecture seule (GET uniquement), '
        'role admin = lecture + ecriture (GET + POST /pipeline/run). '
        'L\'API ne tourne pas en root dans le conteneur (USER appuser). '
        'Le secret JWT est injecte via variable d\'environnement, '
        'jamais hardcode dans le code.',
        None
    )

    pdf.qa(
        'Comment votre systeme se comporte-t-il en cas d\'indisponibilite d\'une source externe ?',
        'Urban Data Explorer : chaque ETL a un try/except par source. '
        'En cas d\'echec, la source est marquee en erreur dans les metriques '
        'et les donnees existantes en Bronze sont conservees (pas d\'ecrasement). '
        'L\'API repond avec les donnees Gold existantes (qui peuvent etre perimees) '
        'et expose un champ last_updated pour indiquer la fraicheur. '
        'IA Pero : si Gemini est indisponible, retour du Top-5 SBERT seul '
        '(recommendation sans generation).',
        None
    )

    pdf.qa(
        'Quelle est la difference entre overfitting et underfitting ? Comment les diagnostiquer ?',
        'Overfitting : le modele a appris le bruit du training set, '
        'son score train est nettement superieur au score test. '
        'Diagnostic : courbe d\'apprentissage (train score vs val score en fonction de la taille du train). '
        'Underfitting : le modele est trop simple, '
        'scores train et test tous les deux bas. '
        'Sur notre projet : XGBoost test F1=0.886 vs train F1=0.91 '
        '-> leger overfit acceptable, controle par CV (ecart-type faible).',
        None
    )

    # ─── ANNEXE : CHIFFRES CLE ────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('Annexe - Chiffres a retenir par coeur', NAVY)

    pdf.subsection('Urban Data Explorer')
    data_ude = [
        ['Metrique', 'Valeur'],
        ['Nombre de sources', '24 sources / 8 familles'],
        ['Tests pytest', '102 tests (branche feat/bloc1-hardening)'],
        ['Quotas API', '120 req/min anonyme - 600 req/min authentifie'],
        ['Niveaux cartographiques', '5 niveaux (ville -> batiment)'],
        ['Micro-batch fenetre', '10 secondes (fenetres tumbling)'],
        ['Tech stack', 'Polars, PostgreSQL, Cassandra, Kafka, FastAPI, React, MapLibre'],
    ]
    for i, row in enumerate(data_ude):
        if i == 0:
            pdf.table_row(row, [60, 116], header=True)
        else:
            pdf.table_row(row, [60, 116])
    pdf.ln(4)

    pdf.subsection('Maintenance Predictive Industrielle')
    pdf.table_row(['Modele', 'F1', 'ROC-AUC', 'PR-AUC', 'Score sel.', 'CO2'],
                  [46, 22, 24, 24, 24, 20], header=True)
    pdf.table_row(['LogReg (baseline)', '0.747', '0.959', '0.712', '0.746', '0.3 mg'], [46, 22, 24, 24, 24, 20])
    pdf.table_row(['Random Forest', '0.863', '0.992', '0.881', '0.839', '8.2 mg'], [46, 22, 24, 24, 24, 20])
    pdf.table_row(['XGBoost (RETENU)', '0.886', '0.995', '0.921', '0.880', '6.1 mg'], [46, 22, 24, 24, 24, 20], bold=True)
    pdf.table_row(['MLP 64-32-16', '0.836', '0.984', '0.857', '0.790', '3.8 mg'], [46, 22, 24, 24, 24, 20])
    pdf.ln(4)

    pdf.subsection('L\'IA Pero - Parametres cles')
    data_iapero = [
        ['Parametre', 'Valeur'],
        ['Modele embedding', 'SBERT all-MiniLM-L6-v2 (local)'],
        ['Dimension embedding', '384 dimensions'],
        ['Seuil guardrail', '0.35 (calibre sur 30 requetes)'],
        ['Metrique guardrail', 'Similarite cosinus max sur tout le referentiel'],
        ['Generation LLM', 'Google Gemini free-tier (RAG)'],
        ['Cache', 'MD5 (requete + contexte) - JSON local'],
        ['Latence cible', '< 3 secondes de reponse'],
        ['Top-N recommandations', '5 cocktails par requete'],
    ]
    for i, row in enumerate(data_iapero):
        if i == 0:
            pdf.table_row(row, [60, 116], header=True)
        else:
            pdf.table_row(row, [60, 116])
    pdf.ln(4)

    pdf.subsection('Mapping competences RNCP40875')
    pdf.table_row(['Competence', 'Projet', 'Preuve cle'], [25, 50, 101], header=True)
    comps = [
        ('C1.1', 'Urban Data Explorer', 'postgres/init.sql - schema etoile, FK, index'),
        ('C1.2', 'Urban Data Explorer', 'cassandra/schema.cql - query-first, TTL, 2 patterns'),
        ('C1.3', 'Urban Data Explorer', 'data/ Bronze/Silver/Gold, etl/metrics.py'),
        ('C1.4', 'Urban Data Explorer', 'docker-compose.yml healthchecks, scripts/test_resilience.py'),
        ('C2.1', 'Urban Data Explorer', 'api/security.py - JWT, roles, quotas 120/600, 429'),
        ('C2.2', 'Urban Data Explorer', 'streaming/producer.py, consumer.py, microbatch.py'),
        ('C2.3', 'Urban Data Explorer', 'etl/processing.py - Polars, jointure IRIS, fusion DVF+INSEE'),
        ('C2.4', 'Urban Data Explorer', 'etl/metrics.py, lru_cache geocodage, Parquet colonnaire'),
        ('C3.1', 'Maintenance Predictive', 'src/preprocessing.py - pipeline sklearn fit-train-only'),
        ('C3.2', 'Maintenance Predictive', 'dashboard/app.py - Streamlit KPI + simulation'),
        ('C3.3', 'Maintenance Predictive', 'scripts/02_eda.py - distributions, correlations, desequilibre'),
        ('C4.1', 'Maintenance Predictive', 'RAPPORT.md strategie IA : cout corrective -> predictive'),
        ('C4.2', 'Maintenance Predictive', 'scripts/03_train_models.py - 4 modeles, hyperparams justifies'),
        ('C4.3', 'Maintenance Predictive', 'reports/03/metrics_summary.json - tableau + CO2 CodeCarbon'),
        ('C5.1', 'L\'IA Pero', 'RAPPORT_FINAL.md - personas, scenarios, justification GenAI'),
        ('C5.2', 'L\'IA Pero', 'src/recommender.py - SBERT, cosinus, guardrail, cache, Gemini'),
        ('C5.3', 'L\'IA Pero', 'tests/test_guardrail.py - tableau requetes/scores/decisions'),
    ]
    for comp, projet, preuve in comps:
        pdf.table_row([comp, projet, preuve], [25, 50, 101])

    return pdf


if __name__ == '__main__':
    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(out_dir, 'QA_JURY_COMPLET.pdf')

    pdf = build_pdf()
    pdf.output(out_path)
    print(f'PDF genere : {out_path}')
    size_kb = os.path.getsize(out_path) // 1024
    print(f'Taille     : {size_kb} Ko')
    print(f'Pages      : {pdf.page}')
