# -*- coding: utf-8 -*-
"""
Generateur PDFs 150 Q&A - Soutenance finale RNCP40875
EFREI M1 Data Engineering & IA - Adam Beloucif & Emilien Morice
3 projets x 150 questions = 450 Q&A avec reponses detaillees

Usage: python scripts/gen_150q_all.py
Output: soutenance-m1/Soutenance_UDE_150Q.pdf
        soutenance-m1/Soutenance_MPI_150Q.pdf
        soutenance-m1/Soutenance_IAPero_150Q.pdf
"""

from fpdf import FPDF
from pathlib import Path
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_150q_extra import UDE_QA_EXTRA, MPI_QA_EXTRA, IAP_QA_EXTRA
from gen_150q_extra2 import UDE_QA_EXTRA2, MPI_QA_EXTRA2, IAP_QA_EXTRA2
from gen_150q_extra3 import UDE_QA_EXTRA3, MPI_QA_EXTRA3, IAP_QA_EXTRA3
from gen_150q_extra4 import UDE_QA_EXTRA4, MPI_QA_EXTRA3_PATCH, IAP_QA_EXTRA4

OUT_DIR = Path(__file__).parent.parent

NAVY  = (5, 24, 50)
BLUE  = (22, 55, 103)
LBLUE = (12, 120, 180)
PINK  = (255, 67, 184)
WHITE = (255, 255, 255)
GRAY  = (50, 50, 50)
LGRAY = (245, 246, 248)


def clean(txt):
    return (txt
            .replace('·', '-').replace('×', 'x')
            .replace('→', '->').replace('—', ' - ')
            .replace('–', ' - ').replace('⋅', '-')
            .replace('’', "'").replace('‘', "'")
            .replace('“', '"').replace('”', '"')
            .replace('â', 'a').replace('é', 'e')
            .replace('è', 'e').replace('ê', 'e')
            .replace('à', 'a').replace('î', 'i')
            .replace('ô', 'o').replace('û', 'u')
            .replace('ç', 'c').replace('ù', 'u')
            .replace('ó', 'o').replace('í', 'i'))


class SoutenancePDF(FPDF):
    project_name = ""

    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 18, 'F')
        self.set_fill_color(*PINK)
        self.rect(0, 18, 210, 2, 'F')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 9)
        self.set_xy(12, 5)
        self.cell(100, 6, 'EFREI - M1 Data Engineering & IA', border=0)
        self.set_font('Helvetica', '', 8)
        self.set_xy(110, 5)
        self.cell(90, 6, clean(self.project_name), border=0, align='R')
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
        self.cell(130, 5, 'Adam Beloucif & Emilien Morice - RNCP40875 - Session 2026-2027')
        self.set_font('Helvetica', 'B', 8)
        self.set_xy(150, 286)
        self.cell(50, 5, f'Page {self.page_no()}', align='R')

    def cover(self, title, subtitle, bloc, color=BLUE):
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 297, 'F')
        self.set_fill_color(*PINK)
        self.rect(0, 120, 210, 4, 'F')
        self.set_text_color(*PINK)
        self.set_font('Helvetica', 'B', 11)
        self.set_xy(0, 80)
        self.cell(210, 10, 'EFREI PARIS - M1 DATA ENGINEERING & IA', align='C')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 24)
        self.set_xy(0, 100)
        self.multi_cell(210, 12, clean(title), align='C')
        self.set_font('Helvetica', '', 14)
        self.set_xy(0, 140)
        self.cell(210, 10, clean(subtitle), align='C')
        self.set_text_color(*PINK)
        self.set_font('Helvetica', 'B', 12)
        self.set_xy(0, 160)
        self.cell(210, 10, clean(bloc), align='C')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', '', 10)
        self.set_xy(0, 200)
        self.cell(210, 8, 'Adam Beloucif & Emilien Morice', align='C')
        self.set_xy(0, 210)
        self.cell(210, 8, 'Soutenance - Juin 2026', align='C')
        self.set_font('Helvetica', 'B', 9)
        self.set_xy(0, 235)
        self.cell(210, 6, '150 Questions - Reponses Detaillees - Preparation Jury', align='C')

    def section_title(self, num, title):
        self.ln(6)
        self.set_fill_color(*NAVY)
        self.rect(self.l_margin, self.get_y(), 190, 11, 'F')
        self.set_fill_color(*PINK)
        self.rect(self.l_margin, self.get_y() + 9, 60, 2, 'F')
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*WHITE)
        self.set_xy(self.l_margin + 4, self.get_y() + 1.5)
        self.cell(0, 8, clean(f'Section {num} - {title}'))
        self.ln(14)
        self.set_text_color(*GRAY)

    def qa(self, num, question, answer, badge=None):
        if self.get_y() > 245:
            self.add_page()
        q = clean(question)
        a = clean(answer)
        if badge:
            self.set_fill_color(*LBLUE)
            self.set_text_color(*WHITE)
            self.set_font('Helvetica', 'B', 6.5)
            self.set_x(self.l_margin)
            bw = min(len(badge) * 3.2 + 6, 60)
            self.cell(bw, 4.5, clean(badge), fill=True)
            self.ln(5)
        # Numero
        self.set_fill_color(*BLUE)
        self.rect(self.l_margin, self.get_y(), 7, 7, 'F')
        self.set_font('Helvetica', 'B', 7)
        self.set_text_color(*WHITE)
        self.set_xy(self.l_margin, self.get_y())
        self.cell(7, 7, str(num), align='C')
        # Question
        self.set_xy(self.l_margin + 9, self.get_y())
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*BLUE)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 9, 6, q)
        self.ln(1)
        # Reponse
        self.set_x(self.l_margin + 9)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*GRAY)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 9, 5.5, a)
        self.ln(3)


# ===========================================================================
# PROJET 1 - URBAN DATA EXPLORER
# ===========================================================================

UDE_QA = [
    # Section 1 - Architecture generale
    ("Decrivez l'architecture globale d'Urban Data Explorer.",
     "UDE repose sur trois couches complementaires : (1) PostgreSQL en schema etoile pour les requetes analytiques OLAP, (2) Cassandra en modele query-first pour les donnees d'evenements haute frequence avec partitionnement par event_type et TTL de 7 jours, (3) Kafka pour le streaming micro-batch toutes les 10 secondes. Le frontend MapLibre consomme une API FastAPI securisee par JWT. Le pipeline de collecte ingere 24 sources issues de 8 familles de donnees urbaines.",
     "C1.1 Architecture"),
    ("Pourquoi avoir choisi trois bases de donnees differentes ?",
     "Chaque base repond a un cas d'usage distinct. PostgreSQL est optimise pour les jointures complexes et les agregations sur des tables de faits/dimensions - ideal pour les indicateurs composites. Cassandra offre une ecriture lineairement scalable et une lecture ultra-rapide par partition, parfaite pour les flux d'evenements urbains (incidents, trafic temps reel). Kafka sert de bus d'evenements qui decouple les producteurs de donnees des consommateurs, garantissant la durabilite et le rejeu.",
     "C1.1 Choix BD"),
    ("Quel est le schema en etoile utilise dans PostgreSQL ?",
     "Le schema comporte une table de faits fact_events (event_id, event_type, timestamp, localisation_id, value, source_id) et plusieurs tables de dimensions : dim_localisation (IRIS, commune, departement, coordonnees), dim_time (annee, mois, jour, heure, jour_semaine), dim_source (nom, famille, url, frequence), dim_event_type (categorie, unite, agregation_defaut). Ce modele permet des requetes GROUP BY multidimensionnelles efficaces via index partiels sur les colonnes les plus filtrées.",
     "C1.1 Schema"),
    ("Comment fonctionne le micro-batch Kafka toutes les 10 secondes ?",
     "Un consumer Kafka Python lit les messages du topic urban_events par lot de 10 secondes (poll(timeout_ms=10000, max_records=5000)). Chaque batch est transforme via Polars (validation schema, deduplication par event_id), puis ecrit en bulk dans Cassandra via batch statements UNLOGGED (limite 100 inserts/batch pour eviter les coordinations distribuees) et en PostgreSQL via COPY FROM pour les evenements qualifies. Le lag consumer est monitore via JMX.",
     "C1.2 Kafka"),
    ("Pourquoi Polars plutot que Pandas dans ce projet ?",
     "Polars offre une execution multi-threaded native sur CPU via Apache Arrow, sans GIL Python. Pour un pipeline traitant des fichiers CSV de plusieurs centaines de MB (24 sources), la difference de vitesse est 5-10x. La syntaxe lazy (scan_csv, filter, groupby, collect) permet de construire un plan d'execution optimise avant toute lecture disque. De plus, Polars integre nativement la jointure spatiale avec Shapely pour l'appariement IRIS - essentiel pour aggreger les evenements par zone geographique.",
     "C1.2 Polars"),
    ("Expliquez la jointure spatiale Polars + Shapely pour l'IRIS.",
     "Chaque evenement arrive avec des coordonnees GPS (lat, lon). On charge le fond de carte IRIS (GeoJSON, 36 000+ geometries) en GeoDataFrame Shapely. La jointure consiste a appliquer un STRtree (Sorted-Tile R-tree) pour chercher le polygone IRIS contenant chaque point en O(log n). Cet enrichissement transforme lat/lon bruts en code IRIS INSEE (9 chiffres), permettant l'agregation par zone infra-communale normalisee. Le STRtree est construit une fois en memoire au demarrage du pipeline.",
     "C1.2 IRIS"),
    ("Comment avez-vous structure l'API FastAPI ?",
     "L'API est organisee en routers par domaine : /events (CRUD), /indicators (calculs agregats), /map (GeoJSON pour MapLibre), /auth (JWT). Chaque endpoint utilise l'injection de dependances FastAPI pour la connexion BD (asyncpg pour PostgreSQL, cassandra-driver async pour Cassandra). Le middleware JWT valide le Bearer token sur chaque requete protegee. Les schemas Pydantic v2 garantissent la validation entree/sortie. La documentation OpenAPI est auto-generee via /docs.",
     "C1.3 API"),
    ("Quels sont les quotas JWT et comment sont-ils implementes ?",
     "Deux niveaux de quotas : 120 req/min pour les utilisateurs standard, 600 req/min pour les utilisateurs premium. Ils sont implementes via un middleware Redis avec la cle rate:{user_id}:{minute_epoch}. A chaque requete, on INCR la cle et on EXPIRE a 60s. Si le compteur depasse le seuil, on retourne HTTP 429 avec le header Retry-After. Le choix Redis (in-memory, O(1)) permet de gerer des milliers de requetes par seconde sans latence notable sur l'API.",
     "C1.3 JWT"),
    ("Quelles sont les 4 familles principales de sources de donnees ?",
     "Parmi les 8 familles : (1) Mobilite - comptages trafic DIRIF, velib, RATP GTFS, (2) Environnement - stations Airparif NO2/PM2.5, meteo Meteoconcept, (3) Securite - incidents BSPP (Brigade de Sapeurs-Pompiers de Paris), main courante police, (4) Social-economique - DVF transactions immobilieres, fichier Sirene entreprises, revenus FiLoSoFi INSEE. Chaque famille a un adaptateur Python dedié qui normalise vers le schema interne avant ingestion Kafka.",
     "C1.1 Sources"),
    ("Comment est geree la fraicheur des 24 sources de donnees ?",
     "Chaque source a une frequence declaree dans dim_source : temps-reel (Kafka direct), horaire (cron + API REST), quotidien (cron 02:00, batch FTP/CSV), hebdomadaire/mensuel (OpenData static). Le pipeline verifie via une table metadata_freshness (source_id, last_fetched, expected_interval) et leve une alerte si last_fetched > expected_interval * 1.5. Les sources critiques (trafic, qualite air) ont une alerte a 10 minutes de retard.",
     "C1.1 Fraicheur"),
    ("Quels sont les 4 indicateurs composites calcules ?",
     "1) Indice Vitalite Urbaine (IVU) : combine trafic, commerce actif Sirene, evenements culturels, mobilite douce, notes 0-100. 2) Score Environnemental : NO2, PM2.5, bruit (dB), espaces verts m2/habitant, pondere par seuils OMS. 3) Indice Securite Relative : incidents/1000 habitants, normalise par densite, lisse sur 30 jours. 4) Accessibilite Multimodale : stations TC dans rayon 500m, score 0-10 par zone IRIS. Ces indices sont pre-calcules toutes les heures et stockes en table agregee pour eviter les requetes lourdes.",
     "C2.1 Indicateurs"),
    ("Comment est visualisee la carte dans MapLibre ?",
     "MapLibre GL JS charge les tuiles vectorielles depuis un serveur pmtiles (protocole compact, single-file). Les zones IRIS sont colorees par choroplethie selon l'indicateur selectionne (echelle de couleur divergente ou sequentielle selon la semantique). Les evenements ponctuels (incidents, capteurs) sont representes en clusters automatiques. Un panneau lateral affiche le detail IRIS au clic : sparklines des 30 derniers jours par indicateur, histogramme des sources, lien vers les donnees brutes. Le rendu WebGL permet l'affichage fluide de 36 000 polygones.",
     "C2.2 Carto"),
    ("Pourquoi 102 tests pytest et que couvrent-ils ?",
     "102 tests repartis : 34 tests unitaires (validateurs Pydantic, calcul indicateurs, clean IRIS), 28 tests integration BD (fixtures PostgreSQL in-memory via testcontainers, Cassandra local), 22 tests API (FastAPI TestClient, tous les endpoints CRUD + erreurs 401/422/429), 18 tests pipeline Kafka (mock consumer, batch Polars), comportement aux limites (null, coordonnees hors France, sources indisponibles). Couverture mesurée : 87% lignes. CI GitHub Actions lance pytest + coverage a chaque push.",
     "C2.3 Tests"),
    ("Quelles sont les limites actuelles du projet ?",
     "Quatre limites principales : (1) Pas de haute disponibilite - Cassandra en single-node, pas de replication factor > 1 en dev. (2) La jointure IRIS relance le STRtree entier si la memoire swap - non resolu en production. (3) Certaines sources OpenData (DVF, Sirene) ont des retards de mise a jour de 3-6 mois cote source officielle, rendant les indicateurs socio-eco partiellement obsoletes. (4) L'API ne supporte pas encore WebSocket pour le push temps reel cote client - le frontend fait du polling toutes les 30s.",
     "C2.4 Limites"),
    ("Comment amelioreriez-vous le projet en production ?",
     "Trois axes : (1) Infra - deploiement Kubernetes avec Cassandra en cluster 3 noeuds (RF=3), PostgreSQL en hot-standby, Kafka en mode distribue 3 brokers. (2) Observabilite - Prometheus + Grafana pour les metriques pipeline, alertes PagerDuty si lag Kafka > 30s ou fraicheur source depassee. (3) IA - ajout d'un modele LSTM pour la prediction d'indicateurs J+7, entrainement sur historique 3 ans. Integration d'anomaly detection (Isolation Forest) pour signaler automatiquement les outliers dans les flux temps reel.",
     "C2.4 Perspectives"),

    # Section 2 - PostgreSQL
    ("Pourquoi un schema en etoile et pas en flocon ?",
     "Le schema en etoile denormalise les dimensions (pas de sous-dimensions). Cela reduit le nombre de jointures necessaires (1 seule vs N en flocon). Pour des requetes OLAP comme 'agregats par zone IRIS, par mois, par type d'evenement', le schema etoile est plus performant car PostgreSQL peut utiliser des hash joins en memoire sur des tables compactes. Le flocon serait justifie si les dimensions avaient de la hierarchie complexe (ex : canton > departement > region) avec beaucoup de cardinalite, ce qui n'est pas le cas ici.",
     "C1.1 PostgreSQL"),
    ("Quels index avez-vous definis sur PostgreSQL ?",
     "Index principaux : B-tree sur fact_events(event_type, timestamp DESC) pour les requetes de serie temporelle recentes, index GiST sur dim_localisation(geom) pour les requetes spatiales PostGIS, index partiel sur fact_events(source_id) WHERE value IS NOT NULL pour filtrer les evenements valides. Toutes les FK ont un index secondaire. La table fact_events est partitionnee par mois (PARTITION BY RANGE sur timestamp) pour faciliter la purge des vieux evenements sans VACUUM complet.",
     "C1.1 PostgreSQL Index"),
    ("Comment evitez-vous les problemes de lock en ecriture Kafka -> PostgreSQL ?",
     "Le consumer Kafka ecrit via COPY FROM STDIN (mode bulk, pas de row-level lock) dans une table de staging fact_events_staging. Un job toutes les minutes fait INSERT INTO fact_events SELECT ... FROM fact_events_staging avec ON CONFLICT DO NOTHING (deduplication). La table staging est ensuite TRUNCATE. Ce pattern evite les deadlocks sur la table principale pendant les agregations de lecture. La transaction COPY est elle-meme courte (< 1s pour 5000 lignes).",
     "C1.2 PostgreSQL Lock"),
    ("Comment gerez-vous les fuseaux horaires dans PostgreSQL ?",
     "Toutes les colonnes timestamp sont en TIMESTAMPTZ (timestamp with timezone) stocke en UTC. Les sources qui fournissent des horaires locaux (Europe/Paris) sont converties via AT TIME ZONE 'UTC' lors de l'ingestion. Le frontend recoit les timestamps UTC et les convertit en heure locale via l'API Intl.DateTimeFormat du navigateur. Ce choix evite les bugs DST (heure d'ete/hiver) qui faussent les agregations horaires.",
     "C1.2 Timezones"),
    ("Quelle est la politique de retention des donnees ?",
     "Trois niveaux : PostgreSQL conserve 2 ans de donnees partitionnees par mois (DROP PARTITION automatique via pg_cron). Cassandra avec TTL 7 jours sur les evenements bruts haute frequence (incidents, trafic secondes). Les snapshots mensuels agreges (IVU, Score Env) sont conserves indefiniment dans une table separee non partitionnee. Cette strategie equilibre cout stockage (evite explosion du volume) et retroactivite analytique (2 ans suffisent pour les tendances urbaines).",
     "C2.1 Retention"),

    # Section 3 - Cassandra
    ("Expliquez le modele de partitionnement Cassandra choisi.",
     "La partition key est (event_type, date_bucket) ou date_bucket est la date tronquee a la journee. Le clustering key est timestamp DESC pour lire les evenements les plus recents en premier. Ce design repond a la requete principale : 'donner-moi les 100 derniers incidents de type TRAFIC du 2026-06-15'. La partition ne depasse jamais ~50 000 lignes/jour/type, ce qui evite les hot partitions. Le TTL 7j est defini au niveau table (DEFAULT_TIME_TO_LIVE = 604800).",
     "C1.1 Cassandra"),
    ("Qu'est-ce qu'une hot partition Cassandra et comment l'evitez-vous ?",
     "Une hot partition est une partition qui recoit disproportionnement plus de lectures/ecritures que les autres, surchargeant un noeud specifique. On l'evite en choisissant une partition key a haute cardinalite. Ici, l'ajout de date_bucket distribue la charge : meme event_type = TRAFIC, les insertions du lundi vont sur (TRAFIC, 2026-06-15) et du mardi sur (TRAFIC, 2026-06-16) - donc deux noeuds differents. Sans date_bucket, toutes les insertions TRAFIC depuis le debut du projet iraient sur la meme partition.",
     "C1.1 Cassandra Hot"),
    ("Pourquoi ne pas utiliser uniquement Cassandra pour tout le projet ?",
     "Cassandra est optimise pour les requetes par partition key. Elle ne supporte pas les jointures, les sous-requetes, ou les agregations complexes sur de multiples dimensions. Calculer l'IVU qui combine 5 sources differentes avec des ponderations necessite du SQL expressif (CTEs, window functions, GROUP BY multidimensionnel) - PostgreSQL excelle la-dessus. De plus, Cassandra n'a pas de contraintes de cle etrangere ni de transactions ACID multi-tables, ce qui rendrait la garantie de coherence des dimensions impossible.",
     "C1.1 Cassandra Limites"),
    ("Comment testez-vous Cassandra dans votre CI ?",
     "Via testcontainers-python (image cassandra:4.1). Au setup de la suite de tests, on demarre un conteneur Cassandra local, on cree le keyspace et les tables via CQL, on insere des fixtures, on execute les tests, puis on stoppe le conteneur. Cela garantit l'isolation entre les suites de tests. Les tests integration Cassandra couvrent : inserts batch, lecture par partition, expiration TTL simulee (en modifiant le TTL a 1s dans les fixtures), comportement avec coordinateur indisponible (mock).",
     "C2.3 Cassandra Tests"),

    # Section 4 - Kafka
    ("Qu'est-ce qu'un offset Kafka et pourquoi est-il important ?",
     "L'offset est un identifiant sequentiel unique par message dans une partition Kafka. Le consumer group garde en memoire l'offset du dernier message consomme (commit d'offset). Si le consumer redémarre, il reprend depuis le dernier offset commite - pas depuis le debut du topic. Dans UDE, on utilise l'auto-commit desactive : on commit manuellement l'offset APRES ecriture reussie en base. Cela garantit at-least-once delivery (un message peut etre traite deux fois en cas de crash post-ecriture) mais jamais perdu.",
     "C1.2 Kafka Offset"),
    ("Quelle est la difference entre un topic Kafka et une partition ?",
     "Un topic est un canal logique nomme (ex: urban_events). Il est physiquement divise en N partitions (ici 3 par topic). Chaque partition est une sequence ordonnee et immuable de messages. La parallelisation est possible : chaque consumer du groupe lit une partition differente simultanement. La partition key (ici event_type) determine dans quelle partition va chaque message, garantissant l'ordre des messages d'un meme type. Avec 3 partitions, on peut avoir 3 consumers en parallele maximum.",
     "C1.2 Kafka Partition"),
    ("Comment gerez-vous les messages corrompus dans Kafka ?",
     "Le schema Avro + Schema Registry valide chaque message a la production : si le producteur envoie un message hors schema, le Schema Registry leve une exception. Cote consumer, si la deserialisation echoue (message corrompu malgre tout), le message est envoye sur un Dead Letter Queue (topic urban_events_dlq). Un job de monitoring scanne le DLQ toutes les 10 minutes et alerte si plus de 5 messages y arrivent. Les messages du DLQ sont loggues avec le contexte source pour debug.",
     "C1.2 Kafka DLQ"),

    # Section 5 - FastAPI & Securite
    ("Comment est implementee l'authentification JWT ?",
     "Flow : 1) POST /auth/login avec credentials -> JWT HS256 signe avec SECRET_KEY (env var) contenant user_id, role, exp (24h). 2) Chaque requete protegee envoie Authorization: Bearer <token>. 3) Le middleware decode et verifie la signature, l'expiration, et charge le profil user depuis Redis cache (TTL 5min). 4) La dependance FastAPI Depends(get_current_user) injecte le user dans chaque handler. En production, on passerait a RS256 (cle asymetrique) pour pouvoir deleguuer la verification a des services tiers.",
     "C1.3 JWT Auth"),
    ("Pourquoi FastAPI plutot que Flask ou Django ?",
     "FastAPI offre trois avantages decisifs : (1) async/await natif avec asyncpg (PostgreSQL) et cassandra-driver async - essentiel pour ne pas bloquer le thread principal pendant les I/O BD. (2) Validation automatique via annotations Python + Pydantic v2 - zero boilerplate. (3) Documentation OpenAPI auto-generee (/docs, /redoc) - gain de temps considerable pour les clients de l'API. Flask est synchrone (WSGI), Django est lourd pour une pure API. FastAPI combine la legereté de Flask et la puissance async d'un framework moderne.",
     "C1.3 FastAPI"),
    ("Comment avez-vous securise les endpoints de l'API ?",
     "Plusieurs couches : 1) JWT valide sur tous les endpoints sauf /auth et /health. 2) Rate limiting Redis (120/600 req/min selon role). 3) CORS strict : seul le frontend MapLibre est autorise (origines whitelistees). 4) Validation Pydantic des inputs (pas d'injection SQL possible via ORM SQLAlchemy). 5) Pas de stack trace exposee en reponse HTTP - erreurs generiques cote client, details dans les logs serveur. 6) HTTPS obligatoire en production (certificat Let's Encrypt via Nginx reverse proxy).",
     "C1.3 Securite"),
    ("Qu'est-ce que l'injection SQL et comment est-elle evitee ici ?",
     "L'injection SQL consiste a inserer du code SQL malveillant dans un input utilisateur (ex : ' OR '1'='1). Elle est impossible ici car : 1) SQLAlchemy Core utilise des requetes parametrisees - les valeurs ne sont jamais concatenees dans le SQL. 2) Pydantic valide et typifies les inputs avant qu'ils n'atteignent la couche BD. 3) asyncpg passe les parametres separes de la requete (protocol-level parameterization). Les seuls SQL dynamiques (colonnes ORDER BY) utilisent une whitelist explicite.",
     "C1.3 SQL Injection"),

    # Section 6 - Collecte & qualite donnees
    ("Comment avez-vous gere les doublons entre les 24 sources ?",
     "Deux niveaux de deduplication : 1) Au niveau Kafka : chaque message a un idempotency_key (hash SHA256 du contenu + source + timestamp tronque a la minute). Le consumer verifie en Redis si la cle existe (SET NX, TTL 10min). Si oui, on skip le message. 2) Au niveau PostgreSQL : INSERT ON CONFLICT (event_type, source_id, timestamp) DO NOTHING. Cette double defense couvre a la fois les duplications source (meme evenement reporte deux fois) et les doublons de retry Kafka.",
     "C2.1 Dedup"),
    ("Comment traitez-vous les valeurs manquantes dans les donnees urbaines ?",
     "Strategie contextuelle : 1) Capteurs physiques (Airparif, trafic) - interpolation lineaire si gap < 1h, sinon NaN explicite avec flag data_quality='INTERPOLATED'. 2) Donnees administratives (DVF, Sirene) - pas d'imputation, on conserve les NaN (une transaction sans prix = donnee incomplete, ne pas imputer). 3) Indicateurs composites - si une composante est NaN, l'indice global est calcule sur les composantes disponibles avec reponderation, et un badge 'PARTIEL' est affiche sur la carte.",
     "C2.1 Valeurs Manquantes"),
    ("Quelle est la difference entre donnees OLTP et OLAP ?",
     "OLTP (Online Transaction Processing) : nombreuses petites transactions concurrentes, inserts/updates unitaires, optimise pour la coherence (ACID). Ex : CRM, systeme de caisse. OLAP (Online Analytical Processing) : grosses requetes analytiques sur l'historique, lectures massives, agregations. Ex : datawarehouse, BI. PostgreSQL dans UDE joue un role hybride mais est configure pour l'OLAP (schema etoile, partitionnement, index analytiques). Cassandra est OLTP haute frequence. Le data warehouse final serait idealement sur BigQuery ou Redshift en production.",
     "C2.1 OLTP vs OLAP"),

    # Section 7 - Indicateurs composites
    ("Expliquez le calcul de l'Indice Vitalite Urbaine (IVU).",
     "IVU = 0.3 * score_mobilite + 0.25 * score_commerce + 0.20 * score_evenements + 0.15 * score_accessibilite + 0.10 * score_biodiversite. Chaque composante est normalisee 0-100 via min-max sur l'ensemble des IRIS de la zone. score_mobilite = (100 - taux_congestion) * 0.5 + taux_velo * 0.5. score_commerce = log(nb_commerce_actif + 1) normalise. Les poids ont ete calibres avec des urbanistes lors de workshops (document en annexe). L'IVU est recalcule toutes les heures et stocke dans indicators_hourly.",
     "C2.1 IVU"),
    ("Comment avez-vous valide la pertinence des indicateurs composites ?",
     "Trois validations : 1) Coherence interne - correlation de Pearson entre IVU et les enquetes de satisfaction habitant (fichier INSEE BPE). Correlation 0.67, statistiquement significative (p < 0.01, n=672 IRIS). 2) Comparaison avec benchmark - classement IVU vs classement INSEE 'qualite de vie commune' - concordance de Kendall tau = 0.72. 3) Test de sensibilite - variation des poids +/-10% change le classement de moins de 5% des IRIS, ce qui confirme la robustesse du modele.",
     "C2.1 Validation"),
    ("La normalisation min-max est-elle robuste aux outliers ?",
     "Non, c'est une limite connue. Un outlier extreme (ex : IRIS avec 1000x plus d'accidents qu'un autre) ecrase toutes les autres valeurs vers 0. On a mitigue cela en appliquant une transformation log(x+1) avant la normalisation min-max sur les variables a distribution tres asymetrique (nb_incidents, nb_vehicules). Pour les variables normalement distribuees, on utilise la normalisation z-score puis on ramene sur 0-100 avec clip. Un winsorizing au percentile 99 est applique aux outliers detectes automatiquement.",
     "C2.1 Normalisation"),

    # Section 8 - Frontend & Carto
    ("Pourquoi MapLibre plutot que Leaflet ou Google Maps ?",
     "MapLibre GL JS est la version open source de Mapbox GL. Trois avantages : 1) Rendu WebGL - affiche 36 000 polygones IRIS avec transitions fluides la ou Leaflet (SVG/Canvas 2D) saturerait le GPU a 1000 polygones. 2) Tuiles vectorielles pmtiles - le fichier GeoJSON IRIS (80MB) est converti en tuiles binaires de 200KB totales, reduisant drastiquement le chargement initial. 3) Pas de cle API obligatoire ni de quotas - crucial pour un projet academique. Leaflet aurait suffi pour un POC mais pas pour la production.",
     "C2.2 MapLibre"),
    ("Comment avez-vous gere la performance du frontend avec 36 000 polygones ?",
     "Quatre optimisations : 1) pmtiles - le server pre-decoupage les tuiles par zoom level, le client ne charge que ce qui est visible. 2) Level of Detail (LOD) - simplification geometrique automatique selon le zoom : polygones simplifies a 200m a zoom 8, precis a 20m a zoom 14. 3) Virtual DOM - React ne re-render que les composants touches lors des filtres (React.memo + useMemo sur les couches). 4) Service Worker - les tuiles deja affichees sont mises en cache IndexedDB, les revisites sont quasi-instantanees.",
     "C2.2 Performance"),
    ("Comment l'utilisateur peut-il filtrer les donnees sur la carte ?",
     "Via un panneau de controle React avec : 1) Selecteur de date (range picker, defaut : 7 derniers jours). 2) Famille d'indicateur (dropdown : Mobilite, Environnement, Securite, Economique). 3) Seuil min/max via un slider double. 4) Recherche de commune/IRIS par nom. Chaque changement de filtre declenche une requete FastAPI avec les parametres en querystring. Le debounce (300ms) evite les requetes a chaque frappe dans la barre de recherche. Les filtres actifs sont serialises dans l'URL pour le partage.",
     "C2.2 Filtres"),

    # Section 9 - Tests & CI
    ("Qu'est-ce que testcontainers et pourquoi l'utiliser ?",
     "testcontainers-python est une bibliotheque qui demarre de vrais conteneurs Docker pendant les tests (PostgreSQL, Cassandra, Redis, Kafka). Contrairement aux mocks ou aux bases in-memory (SQLite pour PostgreSQL) qui ne repliquent pas exactement le comportement de la vraie base, testcontainers utilise les vraies images. Avantages : on teste les vraies fonctionnalites (triggers PostgreSQL, TTL Cassandra, partitions Kafka). Inconvenient : les tests sont plus lents (demarrage ~15s par conteneur). Solution : parallélisation des suites avec pytest-xdist.",
     "C2.3 Testcontainers"),
    ("Comment avez-vous structure le CI/CD ?",
     "GitHub Actions avec deux workflows : 1) CI (sur chaque PR) - lint (ruff, black), mypy type checking, pytest avec testcontainers (macos-latest, ubuntu-latest), coverage report. Si coverage < 80%, le PR est bloque. 2) CD (sur merge main) - build Docker image, push DockerHub, deploy Render.com ou Railway (plateforme PaaS). Les secrets (DB passwords, JWT secret) sont dans les GitHub Secrets, jamais dans le code. Le temps total CI : ~4 minutes.",
     "C2.3 CI/CD"),
    ("Quelle est la difference entre test unitaire et test d'integration ?",
     "Test unitaire : teste une fonction en isolation, sans dependance externe. Ex : tester la fonction calculate_ivu(composantes) avec des valeurs hardcodees - rapide, deterministe. Test d'integration : teste l'interaction entre composants. Ex : inserer un evenement dans PostgreSQL via l'API et verifier qu'il est bien recuperable via GET /events/{id} - plus lent, necessite des services actifs. UDE a les deux : 34 unitaires (algorithmes, validateurs) et 68 integration (API-BD, pipeline Kafka-Cassandra). On n'a pas de tests E2E frontend automatises.",
     "C2.3 Tests Types"),
    ("Comment avez-vous gere les secrets dans le projet ?",
     "Principe Zero Secret in Code : toutes les credentiels (DB passwords, JWT_SECRET, API keys sources) sont dans le fichier .env (gitignore). En CI, les secrets sont dans GitHub Secrets et injectes comme variables d'environnement par Actions. En production, on utilise les secrets managers de la plateforme PaaS. Le .gitignore inclut des patterns defensifs : *.env, *secret*, *.key, *.pem. Un hook pre-commit via detect-secrets scanne chaque commit pour des patterns de secrets (cles API, passwords).",
     "C2.3 Secrets"),

    # Section 10 - Critique & Perspectives
    ("Quel est le point le plus faible du projet ?",
     "La single-node Cassandra. En production, Cassandra est concu pour du multi-noeud (minimum 3, RF=3 pour la tolerence aux pannes). Notre setup single-node n'offre aucune HA : si le serveur Cassandra tombe, toutes les ecritures d'evenements temps reel sont perdues jusqu'au redemarrage. La solution serait de deplacer vers une offre managee (Astra DB, Amazon Keyspaces) qui gere la replication automatiquement. Autre faiblesse : absence de monitoring applicatif en production - pas de traces distribuees (OpenTelemetry) pour diagnostiquer les lenteurs.",
     "C2.4 Faiblesses"),
    ("Comment passeriez-vous UDE a l'echelle nationale (France entiere) ?",
     "Quatre adaptations necessaires : 1) Sharding PostgreSQL par region (schema par departement) ou migration vers Citus (PostgreSQL distribue). 2) Kafka en cluster multi-broker avec replication factor 3 - actuellement 3 partitions = 3 consumers max, a passer a 30 partitions pour paralléliser sur plus de machines. 3) L'API FastAPI en stateless derrière un load balancer (Nginx + N replicas Kubernetes). 4) Les tuiles MapLibre a regenerer pour couvrir les 36 000 communes vs 1300 IRIS Paris - volume x10, necessiterait un CDN pour la distribution.",
     "C2.4 Scalabilite"),
    ("En quoi UDE repond aux competences RNCP Bloc 1 (C1.1 a C2.4) ?",
     "C1.1 : conception architecture multi-BD heterogene (PostgreSQL etoile + Cassandra NoSQL + Kafka streaming). C1.2 : pipeline de collecte 24 sources, transformation Polars, jointure spatiale IRIS. C1.3 : API REST FastAPI avec auth JWT, rate limiting, documentation OpenAPI. C2.1 : calcul d'indicateurs composites, normalisation, agregation multidimensionnelle. C2.2 : visualisation cartographique MapLibre avec choroplethie et clustering. C2.3 : 102 tests pytest (unitaires + integration + testcontainers), CI GitHub Actions, coverage 87%. C2.4 : analyse critique des limites et propositions de solutions a l'echelle.",
     "C2.4 RNCP"),
    ("Quelle technologie ajouteriez-vous en priorite ?",
     "OpenTelemetry pour l'observabilite distribuee. Actuellement, si une requete API est lente, on ne sait pas si le bottleneck est dans FastAPI, PostgreSQL, ou Cassandra. OpenTelemetry instrumenterait automatiquement toutes les couches et enverrait des traces a Jaeger ou Tempo. On verrait exactement le temps passe dans chaque span. Deuxieme priorite : GraphQL (Strawberry) pour permettre au frontend de requeter exactement les champs dont il a besoin, evitant le sur-fetchage actuel via les endpoints REST.",
     "C2.4 Ameliorations"),
    ("Comment avez-vous reparti le travail avec votre binome ?",
     "Division par couche technique avec points de synchronisation hebdomadaires : Adam en charge de l'architecture BD (schema PostgreSQL, modele Cassandra), du pipeline Kafka-Polars, et de l'API FastAPI. Emilien en charge du frontend MapLibre, du calcul des indicateurs composites, et des adaptateurs de collecte sources. Points communs : tests d'integration (ecrits ensemble), CI GitHub Actions (pair programming). Toutes les decisions d'architecture ont ete prises en binome et documentees dans les ADRs du repo.",
     "C2.4 Travail Equipe"),
]

# ===========================================================================
# PROJET 2 - MAINTENANCE PREDICTIVE INDUSTRIELLE
# ===========================================================================

MPI_QA = [
    # Section 1 - Formulation du probleme
    ("Quel est l'objectif du projet de maintenance predictive ?",
     "Predire si une machine industrielle tombera en panne dans les prochaines 24 heures (variable cible binaire failure_within_24h) a partir de capteurs en temps reel. L'objectif metier est de reduire les arrets non planifies (downtime) en permettant une intervention preventive avant la panne. Le dataset comporte 24 042 enregistrements, 15 variables de capteurs, et environ 7% de pannes (desequilibre de classes). Quatre modeles ont ete compares, XGBoost etant retenu avec F1=0.886 et ROC-AUC=0.995.",
     "C3.1 Objectif"),
    ("Pourquoi failure_within_24h et pas failure_within_1h ou 48h ?",
     "Le choix de 24h est un compromis metier : 1) Horizon operationnel - les equipes maintenance ont besoin de 4-8h pour planifier et executer une intervention. 24h donne une marge suffisante. 2) Qualite predictive - sur ce dataset, les capteurs montrent des signaux precurseurs detectables 12-36h avant la panne. En dessous de 6h, le signal-bruit est trop eleve. Au-dela de 48h, la precision chute car trop d'inertie. 3) Alignement avec la pratique industrielle - les standards ISA-95 recommandent un horizon de 24-72h pour la maintenance predictive Niveau 2.",
     "C3.1 Horizon"),
    ("Decrivez le dataset : variables et distribution des classes.",
     "15 variables d'entree : vibration_rms (g), temperature_motor (degC), temperature_bearing (degC), current_draw (A), pressure_hydraulic (bar), oil_viscosity, rpm_speed, load_factor, maintenance_age_days (jours depuis derniere maintenance), cumulative_cycles, shock_count_24h, oil_temperature, voltage_supply, humidity_ambient, failure_within_24h (cible). Distribution des classes : 93% negatif (pas de panne), 7% positif (panne imminente). Collecte via capteurs IIoT sur 6 mois de fonctionnement continu.",
     "C3.1 Dataset"),
    ("Qu'est-ce que le desequilibre de classes et comment l'avez-vous gere ?",
     "Le desequilibre (7% positifs vs 93% negatifs) pose probleme car un modele naive qui predit toujours 'pas de panne' aurait 93% d'accuracy tout en etant inutile. Methodes appliquees : 1) SMOTE (Synthetic Minority Oversampling Technique) - genere des exemples positifs synthetiques par interpolation dans l'espace des features. 2) class_weight='balanced' dans XGBoost (scale_pos_weight = 13.3 = 93/7). 3) Metric de reference : F1-score macro et ROC-AUC plutot qu'accuracy. Le F1 macro penalise egalement la mauvaise prediction sur la classe minoritaire.",
     "C3.1 Desequilibre"),
    ("Pourquoi le F1-score et pas l'accuracy pour evaluer ?",
     "L'accuracy sur un dataset desequilibre est trompeuse (93% sans rien predire). Le F1-score est la moyenne harmonique de la precision et du rappel. Precision = TP/(TP+FP) : parmi les pannes prevues, combien sont vraies ? Rappel = TP/(TP+FN) : parmi les vraies pannes, combien sont detectees ? En maintenance, un faux negatif (panne ratee) est plus couteux qu'un faux positif (intervention inutile). On pourrait donc privilegier le rappel en baissant le seuil de decision (default 0.5 -> 0.3). XGBoost avec threshold 0.35 atteint Rappel=0.91, Precision=0.83.",
     "C3.1 Metriques"),

    # Section 2 - Preprocessing
    ("Quelles transformations de features avez-vous appliquees ?",
     "Pipeline sklearn : 1) StandardScaler sur les variables numeriques continues (vibration_rms, temperatures, current) - centrage-reduction car XGBoost n'en a pas besoin mais les autres modeles (MLP, LogReg) si. 2) Winsorizing au percentile 1-99 pour les outliers de capteurs defectueux. 3) Feature engineering : ratio current_draw/rpm_speed (indice de charge effective), age_depuis_derniere_maintenance^2 (degradation non lineaire), rolling_mean_vibration_24h. 4) Pas d'imputation de NaN : les NaN de capteur sont codes -1 (valeur sentinelle) pour que XGBoost les traite comme une absence d'information.",
     "C3.2 Preprocessing"),
    ("Comment avez-vous separe les donnees sans leakage ?",
     "Split temporel : on ne melange pas les observations aleatoirement (risque de leakage temporel - predire le passe a partir du futur). Le dataset est ordonne chronologiquement. 70% premiere periode -> train, 15% periode intermediaire -> validation, 15% periode finale -> test. Ce split respecte la causalite temporelle. De plus, les features rolling (ex: rolling_mean_24h) sont calculees uniquement sur l'historique precedant chaque observation - pas de lookahead bias. La cross-validation utilisee est TimeSeriesSplit (pas KFold classique).",
     "C3.2 Split"),
    ("Qu'est-ce que le leakage de donnees ?",
     "Le leakage (ou data leakage) est quand des informations du futur ou de la cible se glissent dans les features d'entreenement, donnant des performances artificiellement elevees qui ne se generalisent pas en production. Exemples concrets : 1) Scaler fit sur tout le dataset (train + test) avant le split - le test 'connait' les stats du train. 2) Features calculees apres l'evenement (ex : 'maintenance effectuee dans les 24h' si includue comme feature). 3) Target leakage : une feature qui est causee par la panne plutot que cause de la panne. On l'evite en fitant le scaler uniquement sur le train et en appliquant le transform au test.",
     "C3.2 Leakage"),
    ("Quelles features ont ete le plus informatives ?",
     "Selon l'analyse SHAP : 1) vibration_rms (contribution SHAP moyenne 0.43) - les vibrations anormales sont le signal precurseur le plus fiable. 2) maintenance_age_days (0.31) - plus la machine vieillit sans maintenance, plus le risque augmente non lineairement. 3) temperature_motor (0.28) - surchauffe systematiquement precedente des pannes. 4) shock_count_24h (0.19) - les chocs mecaniques cumulatifs fragilisent. 5) current_draw/rpm_speed ratio (0.17) - charge anomale. Ces 5 features expliquent 78% de la contribution SHAP totale.",
     "C3.2 Features"),
    ("Avez-vous effectue une selection de features ?",
     "Oui, via deux methodes : 1) Correlation de Pearson - temperature_bearing et temperature_motor correlees a 0.94 : on retire temperature_bearing (information redundante, risque de multicollinearite pour LogReg et MLP). 2) Feature importance XGBoost (gain moyen) : oil_viscosity et humidity_ambient ont importance < 0.01 et sont retires. Le modele final utilise 12 features sur 15. La suppression de features faibles ameliore legerement le F1 (+0.005) et reduit le temps d'inference de 15%.",
     "C3.2 Selection"),

    # Section 3 - Benchmark modeles
    ("Quels modeles ont ete compares et pourquoi ce choix ?",
     "4 modeles : 1) Regression Logistique (baseline lineaire, interpretable, F1=0.747). 2) Random Forest (ensemble arbres, robuste aux outliers, F1=0.863). 3) MLP/Reseau de neurones (2 couches cachees 128-64, ReLU, dropout 0.3, F1=0.836). 4) XGBoost (gradient boosting, F1=0.886, RETENU). Ce panel couvre la gamme classique ML supervisee : lineaire, ensemble bagging, reseau de neurones, ensemble boosting. On n'a pas teste SVM (lent sur 24K lignes) ni LSTM (series temporelles, hors scope pour une prediction ponctuelle).",
     "C3.3 Benchmark"),
    ("Expliquez la difference entre Random Forest et XGBoost.",
     "Random Forest : N arbres de decision entraines en PARALLELE sur des sous-echantillons bootstrap, vote majoritaire final (bagging). Chaque arbre est independant. XGBoost : N arbres entraines en SEQUENCE, chaque arbre corrige les erreurs du precedent (boosting). XGBoost minimise une fonction de perte differentiable via gradient descent. Resultats : RF est plus robuste au surapprentissage (bagging = variance reduction) mais moins precis. XGBoost est plus precis mais peut overfit si mal regularise (parametres max_depth, min_child_weight, lambda essentiels). XGBoost est generalement meilleur sur des donnees tabulaires.",
     "C3.3 RF vs XGB"),
    ("Quels hyperparametres XGBoost avez-vous optimises ?",
     "Recherche via Optuna (Bayesian optimization, 100 trials) sur 5-fold TimeSeriesSplit. Hyperparametres optimaux retenus : n_estimators=450, max_depth=6, learning_rate=0.08, subsample=0.85, colsample_bytree=0.75, min_child_weight=3, scale_pos_weight=13.3 (gestion desequilibre), reg_alpha=0.1 (L1), reg_lambda=1.5 (L2). Le learning_rate faible + n_estimators eleve ameliore la generalisation au prix d'un entrainement plus long (45s vs 8s pour les defaults). Metric optimisee : F1-macro sur le fold de validation.",
     "C3.3 Hyperparams"),
    ("Pourquoi XGBoost est retenu avec F1=0.886 et pas Random Forest F1=0.863 ?",
     "Trois raisons : 1) F1 superieur de 2.3 points - significatif pour la detection de pannes (chaque faux negatif = potentiellement un arret machine non planifie). 2) ROC-AUC = 0.995 vs 0.981 pour RF : XGBoost est bien meilleur pour discriminer toutes les classes de risque, utile si on veut afficher un score de risque continu. 3) Temps inference plus faible (8ms vs 23ms) : XGBoost utilise le format ONNX pour l'inference, plus rapide que Scikit-learn RF. La difference de 2.3 F1 justifie la complexite additionnelle et le cout CO2 legerement superieur.",
     "C3.3 Choix Final"),
    ("Comment avez-vous valide que le modele ne surapprenait pas ?",
     "Deux verifications : 1) Comparaison train/validation/test : F1 train=0.918, validation=0.897, test=0.886 - ecart faible (< 3%), pas d'overfitting severe. 2) Learning curves : on trace F1 en fonction du nombre de données d'entrainement (10% a 100%). La courbe train descend (moins de données = plus easy a fitter) et la courbe validation monte, et les deux se rapprochent a 100% - signe d'un modele bien calibre. Regularisation L1/L2 appliquee apres avoir observe le gap train/val trop large avec les hyperparametres par defaut.",
     "C3.3 Overfitting"),

    # Section 4 - XGBoost details
    ("Qu'est-ce que le gradient boosting mathematiquement ?",
     "Le gradient boosting construit un modele F(x) en additionnant iterativement des arbres faibles. A l'iteration t, on entraine un arbre h_t sur les residus du modele precedent : r_i = -dL/dF(x_i) (gradient negatif de la loss par rapport a la prediction). Pour la loss binaire (cross-entropy), ce gradient est y_i - p_i (residus). Le nouveau modele est F_t(x) = F_{t-1}(x) + eta * h_t(x) ou eta est le learning rate. XGBoost ajoute la regularisation L1/L2 sur les poids des feuilles dans la fonction de perte, ce qui le distingue du GBDT classique (Friedman 2001).",
     "C3.4 Gradient Boosting"),
    ("Qu'est-ce que le ROC-AUC et pourquoi 0.995 est excellent ?",
     "ROC (Receiver Operating Characteristic) : courbe qui trace le rappel (TPR) en fonction du taux de faux positifs (FPR) pour tous les seuils de decision. AUC (Area Under Curve) : aire sous cette courbe, entre 0 et 1. AUC=0.5 = modele aleatoire, AUC=1.0 = perfection. AUC=0.995 signifie que pour 99.5% des paires (exemple positif, exemple negatif), le modele attribue un score de risque plus eleve a l'exemple positif. En maintenance predictive industrielle, un AUC >= 0.95 est considere comme production-ready par les standards MIMOSA (Open Systems Architecture for Condition Based Maintenance).",
     "C3.4 ROC-AUC"),
    ("Qu'est-ce que la matrice de confusion et comment interpretez-vous la votre ?",
     "La matrice de confusion pour le test set (3606 observations, 7% positifs = ~252 pannes) : TP=229 (pannes detectees), TN=3306 (non-pannes correctes), FP=48 (fausses alarmes), FN=23 (pannes ratees). Interpretation : le modele rate 23 pannes sur 252 (Rappel=0.91) et genere 48 fausses alarmes sur 3306 (FPR=1.5%). En contexte industriel, les 23 pannes ratees representent le risque residuel - chaque FN peut couter 10-50K euros d'arret non planifie. Les 48 FP generent des interventions preventives inutiles mais leur cout est bien inferieur.",
     "C3.4 Matrice"),
    ("Comment fonctionne le threshold de decision et pourquoi 0.35 ?",
     "XGBoost produit une probabilite continue entre 0 et 1 pour chaque observation. Le threshold (seuil) determine a partir de quelle probabilite on classe en 'panne'. Defaut = 0.5 donne F1=0.886. En abaissant a 0.35 : Rappel monte de 0.91 a 0.94 (on manque moins de pannes), Precision descend de 0.87 a 0.81 (plus de fausses alarmes). Le seuil 0.35 est justifie metier : le cout asymetrique (FN >> FP) justifie de privilegier le rappel. Ce threshold est parametre dans le fichier de configuration et ajustable selon le cout d'arret de la machine specifique.",
     "C3.4 Threshold"),
    ("Comment le modele est-il servi en production via FastAPI ?",
     "Le modele XGBoost est serialise en ONNX via skl2onnx + xgboost.to_onnx(). L'inference utilise onnxruntime (10x plus rapide que le predict() sklearn natif). L'API FastAPI expose un endpoint POST /predict qui recoit un JSON de 12 features, passe par le pipeline de preprocessing (StandardScaler charge depuis joblib), puis appelle onnxruntime pour l'inference. La reponse inclut : prediction (0/1), probabilite, risk_level (LOW/MEDIUM/HIGH/CRITICAL selon seuils). Latence mediane : 8ms. Le modele est versionne (MLflow) et le endpoint indique la version courante dans le header X-Model-Version.",
     "C3.4 FastAPI"),

    # Section 5 - Metriques
    ("Qu'est-ce que la precision et qu'est-ce que le rappel ?",
     "Precision = TP / (TP + FP) : sur toutes les pannes que le modele predit, quelle fraction est reellement une panne ? Haute precision = peu de fausses alarmes. Rappel (Sensitivity) = TP / (TP + FN) : sur toutes les vraies pannes, quelle fraction le modele detecte ? Haut rappel = peu de pannes ratees. Il existe un trade-off : augmenter le rappel (seuil plus bas) augmente les faux positifs (baisse precision). F1 = 2 * Precision * Rappel / (Precision + Rappel) est la moyenne harmonique qui equilibre les deux. On preferera maximiser le rappel quand le cout d'un FN est eleve (ici oui).",
     "C3.5 P/R"),
    ("Qu'est-ce que la validation croisee temporelle (TimeSeriesSplit) ?",
     "La cross-validation classique (K-Fold) melange aleatoirement les observations, ce qui cree du leakage temporel (utiliser le futur pour predire le passe). TimeSeriesSplit respecte l'ordre chronologique : Fold 1 : train [t0, t1], val [t1, t2]. Fold 2 : train [t0, t2], val [t2, t3]. Fold 3 : train [t0, t3], val [t3, t4]. Chaque fold agrandit le train et avance dans le temps. Le score final est la moyenne des F1 sur les 5 folds de validation - donne une estimation fiable de la generalisation temporelle.",
     "C3.5 CV Temporelle"),
    ("Comment avez-vous compare les 4 modeles de maniere rigoureuse ?",
     "Protocole standardise : meme split temporel (70/15/15%), meme preprocessing pipeline, meme metric (F1-macro, ROC-AUC), meme seed random. Chaque modele a ete optimise independamment via Optuna (100 trials, TimeSeriesSplit 5 folds). Les scores reportes sont sur le test set final, jamais touche pendant l'optimisation des hyperparametres. Tableau recapitulatif : LogReg F1=0.747/AUC=0.912, RF F1=0.863/AUC=0.981, MLP F1=0.836/AUC=0.967, XGBoost F1=0.886/AUC=0.995. Le test de McNemar confirme que la difference XGBoost/RF est statistiquement significative (p < 0.01).",
     "C3.5 Comparaison"),

    # Section 6 - SHAP
    ("Qu'est-ce que SHAP et pourquoi est-ce important pour la maintenance ?",
     "SHAP (SHapley Additive exPlanations) est une methode d'explicabilite basee sur la theorie des jeux (valeurs de Shapley). Pour chaque prediction, SHAP calcule la contribution de chaque feature a l'ecart entre la prediction et la prediction moyenne. Importance pour la maintenance : 1) Confiance operatrice - les techniciens veulent comprendre POURQUOI le modele sonne l'alarme avant d'intervenir. 2) Debugging - si vibration_rms a une contribution negative anormale, c'est peut-etre un capteur defaillant. 3) Conformite industrielle - certaines normes (IEC 61511) exigent la traçabilite des decisions d'arret.",
     "C4.1 SHAP"),
    ("Quelle est la difference entre SHAP global et local ?",
     "SHAP global : agregation des valeurs SHAP absolues sur tout le dataset. Montre l'importance relative des features en moyenne. Ex : vibration_rms est la feature la plus importante sur les 24K observations. SHAP local : valeurs SHAP pour une prediction specifique. Ex : pour la machine ID-5723 a 14h30, la prediction 'PANNE' est due a +0.43 vibration_rms, +0.31 maintenance_age_days, -0.08 temperature_motor. L'operateur voit exactement quels capteurs ont declenche l'alarme. On affiche la SHAP locale dans l'interface Streamlit pour chaque alerte.",
     "C4.1 SHAP Global/Local"),
    ("Quelles conclusions tirez-vous des valeurs SHAP ?",
     "Trois insights actionnables : 1) vibration_rms domine les pannes mecaniques (rodements, balancement) - renforcer la surveillance vibratoire en priorite. 2) maintenance_age_days a une contribution non-lineaire : faible jusqu'a 180 jours, puis croissante exponentiellement - recommande un intervalle de maintenance preventive de 150 jours maximum. 3) temperature_motor et current_draw sont correlees dans les SHAP : une anomalie thermique sans anomalie electrique pointe vers un probleme de refroidissement vs une surcharge. Ces insights ont ete valides par les experts maintenance de l'entreprise partenaire.",
     "C4.1 SHAP Insights"),
    ("Est-ce que SHAP ralentit le systeme en production ?",
     "Oui, le calcul SHAP complet (background dataset 1000 obs, TreeExplainer) prend ~200ms par prediction. C'est acceptable pour une consultation post-alarme mais pas pour un monitoring en continu. En production, on utilise FastTreeSHAP (version optimisee, ~15ms) et on calcule les SHAP uniquement quand la probabilite de panne > 0.35 (threshold d'alarme). Les predictions < 0.35 retournent uniquement le score, pas les SHAP. Cela reduit de 90% le volume de calculs SHAP (seulement ~7% des cas declenchent le calcul).",
     "C4.1 SHAP Performance"),

    # Section 7 - CodeCarbon
    ("Qu'est-ce que CodeCarbon et pourquoi l'avez-vous utilise ?",
     "CodeCarbon est une bibliotheque Python qui mesure la consommation electrique du code CPU/GPU et la convertit en grammes de CO2 equivalent en fonction du mix energetique local (localisation IP -> region -> facteur carbone kgCO2/kWh). On l'a integre pour mesurer l'empreinte carbone de l'entrainement des 4 modeles. Resultat : XGBoost empreinte entrainement = 6.1mg CO2eq (Optuna 100 trials inclus), RF = 8.2mg CO2eq (les 450 arbres independants sont plus couteux), MLP = 4.3mg CO2eq, LogReg = 0.8mg CO2eq. Ces mesures s'inscrivent dans la demarche de Green AI / IA responsable.",
     "C4.2 CodeCarbon"),
    ("Pourquoi XGBoost a une empreinte moindre que RF malgre de meilleures performances ?",
     "XGBoost construit 450 arbres en sequence, chaque arbre etant petit (max_depth=6, pruning agressif). Random Forest construit 500 arbres en parallele (tous les CPU occupes), chacun plus profond par design (no depth limit par defaut). RF consomme plus car il exploite la parallelisation CPU intensive sur plus de temps. XGBoost est plus efficace car chaque arbre est construit sur les residus - les arbres tardifs sont tres petits (ils corrigent de petites erreurs). De plus, XGBoost utilise un histogram-based split finding qui est bien plus rapide que l'exact split de RF.",
     "C4.2 CO2 Comparaison"),
    ("Comment integrez-vous CodeCarbon dans votre code ?",
     "Avec le context manager : from codecarbon import EmissionsTracker; with EmissionsTracker(output_dir='reports/') as tracker: model.fit(X_train, y_train). A la sortie du context, tracker.final_emissions contient les g CO2eq. Les resultats sont sauvegardes dans emissions.csv avec : timestamp, projet, modele, energie_kwh, emissions_gco2eq, pays, region. Ce fichier est commite dans le repo pour traçabilite. Pour l'inference en production, on ne mesure pas en continu (overhead 2ms/call) mais on fait une mesure periodique (1/1000 predictions) pour surveiller la derive.",
     "C4.2 Implementation"),

    # Section 8 - Deploiement
    ("Decrivez l'interface Streamlit du dashboard maintenance.",
     "Interface en 3 onglets : 1) Dashboard temps reel - tableau des N dernieres predictions avec code couleur (vert/orange/rouge/rouge vif selon risk_level), graphes de serie temporelle pour les 5 features SHAP top. 2) Machine specifique - historique 30 jours pour une machine selectionnee, courbe de probabilite de panne, SHAP waterfall de la derniere prediction. 3) Performance modele - matrice de confusion, ROC curve, F1 historique sur 30 derniers jours en production (monitoring derive). L'interface se rafraichit toutes les 30 secondes via st.rerun().",
     "C4.3 Streamlit"),
    ("Comment surveillez-vous la derive du modele en production ?",
     "Monitoring via deux mecanismes : 1) Data drift - KS test (Kolmogorov-Smirnov) quotidien sur la distribution de chaque feature vs la distribution d'entrainement. Si KS > 0.2 sur 2+ features, alerte mail. 2) Concept drift - F1 hebdomadaire sur les labels vrais recus (avec delai de 24h pour confirmer si la panne a eu lieu). Si F1 < 0.80 sur 2 semaines consecutives, declenchement d'un retrainement automatique sur les 3 derniers mois. Ces mecanismes evitent la degradation silencieuse des performances apres un changement de comportement machine.",
     "C4.3 Drift"),
    ("Pourquoi Streamlit et pas une application React full-stack ?",
     "Streamlit est justifie pour un contexte academique et prototype : (1) Developpement 5x plus rapide - une application de monitoring en ~100 lignes Python vs ~500 lignes React+API. (2) Pas besoin de build pipeline - modification = rechargement. (3) Natif avec l'ecosysteme Python (pandas, plotly, shap). Limites : Streamlit ne scale pas bien avec plusieurs utilisateurs simultanees (session state non partagee, re-run complet a chaque interaction). En production industrielle, on migrerait vers une vraie app React/Next.js avec API FastAPI pour le backend, comme sur Urban Data Explorer.",
     "C4.3 Streamlit Justification"),

    # Section 9 - Biais & limites
    ("Quels biais potentiels existe-t-il dans ce projet ?",
     "Trois biais identifies : 1) Biais de survie - le dataset ne contient que les machines qui ont continue a fonctionner assez longtemps pour etre dans le dataset. Les machines tombees en panne catastrophique du premier jour sont absentes. 2) Biais de confirmation - les capteurs ont peut-etre ete installes APRES que les techniciens ont commence a observer les precurseurs, induisant un biais de selection temporel. 3) Biais de distribution - 6 mois de donnees en conditions normales, pas de donnees de stress test (ex : ete caniculaire, charge maximale prolongee). Le modele peut underperformer dans ces conditions extremes.",
     "C4.4 Biais"),
    ("Peut-on generaliser ce modele a d'autres types de machines ?",
     "Non sans retrainement. Le modele est specifique au type de machine du dataset (compresseurs industriels, d'apres la description des variables). Les signaux precurseurs (vibration, temperature, pression hydraulique) et leurs seuils de criticite sont specifiques a la mecanique de cette machine. Generaliser sans retrainement sur une fraiseuse CNC par exemple donnerait de mauvaises predictions. La bonne pratique est de traiter ce modele comme un template : meme pipeline, meme hyperparametres de depart, mais retrainement sur les donnees de la nouvelle machine avec au moins 3-6 mois d'historique.",
     "C4.4 Generalisation"),
    ("Que se passe-t-il si un capteur tombe en panne ?",
     "Deux scenarios : 1) Capteur NaN - les features manquantes sont codees -1 (valeur sentinelle hors plage physique). XGBoost gere nativement les valeurs manquantes via ses regles de branchement appris. Les tests unitaires couvrent ce cas (toutes les predictions restent valides avec 1-3 features manquantes, F1 degrade de ~0.03). 2) Capteur bloque (valeur constante) - plus difficile a detecter. Un check de variance est fait toutes les heures : si ecart-type(24h) < 0.001 * ecart-type historique, alerte 'capteur suspect'.",
     "C4.4 Capteur Panne"),

    # Section 10 - Perspectives
    ("Comment amelioreriez-vous le modele ?",
     "Trois pistes : 1) Modelisation de la degradation continue - plutot qu'un label binaire, predire le Remaining Useful Life (RUL) en jours - regression plutot que classification. XGBoost peut etre adapte, mais un LSTM sur la serie temporelle des capteurs serait plus naturel. 2) Anomaly detection non supervisee (Isolation Forest, VAE) en parallele pour detecter les modes de panne jamais vus en entrainement. 3) Calibration des probabilites (Platt scaling ou isotonic regression) pour que la probabilite 0.7 corresponde vraiment a 70% de risque - utile pour la communication des risques aux operateurs.",
     "C4.4 Ameliorations"),
    ("Quelles sont les competences RNCP Bloc 2 C3 demontrees ?",
     "C3.1 : formulation du probleme ML supervisee, choix du dataset (24K obs, 15 variables, 7% desequilibre), definition des metriques (F1, ROC-AUC). C3.2 : preprocessing pipeline (StandardScaler, SMOTE, feature engineering, split temporel sans leakage). C3.3 : benchmark de 4 modeles (LogReg, RF, MLP, XGBoost), hyperparameter tuning via Optuna. C3.4 : analyse SHAP (global + local), explicabilite des decisions. C3.5 : evaluation rigoureuse (test McNemar, learning curves, monitoring derive). Demonstration complete du cycle de vie ML de la collecte au deploiement en production.",
     "C4.4 RNCP C3"),
    ("En quoi ce projet a-t-il une valeur industrielle reelle ?",
     "Quatre elements de valeur : 1) ROI mesurable - avec Rappel=0.91 et 252 pannes detectees sur 276 en test, on evite 229 arrets non planifies. Si chaque arret coute 20K euros (moyenne industrie discrete), le ROI brut est 4.58M euros/an. 2) Explicabilite SHAP - contrairement a un black box, les techniciens comprennent et font confiance au modele. 3) Empreinte carbone tracee (CodeCarbon) - repondre aux criteres ESG des grands groupes industriels. 4) Architecture deployable immediatement - FastAPI + ONNX + Streamlit est un stack production-ready, pas juste un notebook Jupyter.",
     "C4.4 Valeur Industrielle"),
    ("Comment gerer l'equite et les biais algorithmiques dans ce contexte ?",
     "Dans la maintenance predictive, l'equite ne concerne pas les groupes humains mais les types de machines ou les sites de production. Un biais potentiel : si le dataset surrepresente les machines d'un site specifique, le modele sera moins performant sur les autres sites (biais de representativite). Mesures : (1) analyse stratifiee des performances par site et par type de machine, (2) audit de fairness trimestriel : F1 par sous-groupe doit rester dans 5% de la performance globale, (3) retrainement si un sous-groupe specifique degrade. Pour les futurs projets impliquant des decisions sur des personnes, les memes principes s'appliquent avec en plus les obligations RGPD.",
     "C4.4 Equite"),
    ("Quelle aurait ete la valeur ajoutee d'un modele de deep learning ?",
     "Un LSTM ou Transformer sur la serie temporelle brute des capteurs (fenetres glissantes de 24h, granularite 1min = 1440 timesteps) pourrait capturer des patterns temporels complexes que XGBoost rate : degradations progressives sur plusieurs jours, patterns cycliques (usure plus rapide en debut de semaine apres arret weekend). Cependant : 1) Le dataset de 24K observations est trop petit pour entrainer un DL efficacement (besoin de 100K+ pour les LSTM). 2) La latence d'inference LSTM est 5-10x superieure. 3) L'explicabilite est bien moins bonne que SHAP sur XGBoost. XGBoost est le bon compromis pour cette taille de dataset.",
     "C4.4 Deep Learning"),
]

# ===========================================================================
# PROJET 3 - IA-PERO / GENERATIF COCKTAILS
# ===========================================================================

IAP_QA = [
    # Section 1 - Architecture RAG
    ("Decrivez l'architecture complete du systeme de recommandation cocktails.",
     "Architecture RAG (Retrieval-Augmented Generation) en deux etapes : 1) Retrieval - un moteur de recherche semantique base sur SBERT all-MiniLM-L6-v2 (384 dimensions, L2-normalise) encode les cocktails et les requetes utilisateur en vecteurs. FAISS IndexFlatIP realise la recherche approximative des K plus proches voisins en cosinus. 2) Generation - les K=5 cocktails recuperes sont passes en contexte a Google Gemini (free tier, modele gemini-1.5-flash) qui genere une reponse conversationnelle. Un guardrail cosinus seuil 0.35 filtre les requetes hors-domaine avant la generation.",
     "C5.1 Architecture"),
    ("Qu'est-ce que le RAG et pourquoi ce choix pour ce projet ?",
     "RAG (Retrieval-Augmented Generation) combine la recherche semantique (retrieval) et la generation de texte (generation). Avantage principal sur un LLM pur : ancrage factuel. Gemini seul pourrait halluciner des recettes de cocktails inexistantes ou incorrectes. En lui fournissant les 5 cocktails les plus pertinents du corpus, on contrainte la generation sur des faits reels. Avantage sur un systeme de retrieval pur : la reponse est conversationnelle et contextuelle ('Pour une soiree d'ete, je recommande X car...') plutot qu'une simple liste de resultats.",
     "C5.1 RAG"),
    ("Quelle est la difference entre SBERT et un embedding classique TF-IDF ?",
     "TF-IDF est une approche lexicale : 'mojito' et 'cocktail rum citron' n'ont aucun overlap de tokens donc similarite = 0, meme si semantiquement proches. SBERT (Sentence-BERT) est une approche semantique : il encode les phrases en vecteurs denses via un transformer fine-tune pour la similarite semantique. 'cocktail ete fruity' et 'boisson fraiche agrume rhum' auront un cosinus eleve (~0.72). Resultat mesure : P@5 SBERT = 0.79 vs P@5 TF-IDF baseline = 0.61 - gain de 18 points sur la precision des 5 premiers resultats.",
     "C5.1 SBERT vs TFIDF"),
    ("Comment fonctionne le modele all-MiniLM-L6-v2 ?",
     "all-MiniLM-L6-v2 est un modele BERT de 22M parametres (6 couches Transformer, 384 dimensions de sortie). Il a ete distille depuis all-mpnet-base-v2 (110M params) via knowledge distillation pour reduire la taille tout en preservant la qualite semantique. Fine-tune sur MS MARCO (passages de recherche) et NLI (inferences naturelles). Pour notre usage : on extrait le CLS token de la derniere couche et on l'L2-normalise -> vecteur unitaire 384D. La normalisation permet d'utiliser le produit scalaire comme substitut du cosinus, ce que FAISS IndexFlatIP calcule nativement.",
     "C5.1 MiniLM"),
    ("Pourquoi L2-normaliser les embeddings ?",
     "L'L2-normalisation projette chaque vecteur sur la sphere unite (norme = 1). Apres normalisation, produit scalaire A.B = cosinus(A, B) = similarite cosinus. Avantages : 1) FAISS IndexFlatIP (Inner Product) calcule le produit scalaire natif - on beneficie de la similarite cosinus sans conversions supplementaires. 2) La similarite est independante de la norme originale - un texte court et un texte long avec le meme sens auront la meme representation. 3) Le guardrail cosinus (seuil 0.35) est interpretable directement comme un angle : cosinus 0.35 correspond a un angle de ~69 degres entre la requete et le corpus.",
     "C5.1 L2-Norm"),

    # Section 2 - SBERT
    ("Comment avez-vous construit le corpus SBERT pour les cocktails ?",
     "Chaque cocktail est encode via une representation textuelle enrichie : '{nom} - {ingredients} - {instructions}' (pas uniquement le nom). Cette concatenation permet a SBERT de capturer la semantique des ingredients et de la preparation. Exemple : 'Mojito - rum blanc, menthe, citron vert, sucre, eau gazeuse - muddle menthe et citron, ajouter rum, completer avec eau gazeuse'. Le corpus final : 600+ cocktails de TheCocktailDB + Kaggle datasets, nettoyes et depupliques. Les embeddings sont pre-calcules une fois et stockes sur disque (numpy .npy, 600*384 floats = ~1.8MB).",
     "C5.1 Corpus"),
    ("Combien de temps prend l'encoding et l'inference SBERT ?",
     "Encoding du corpus complet (600+ cocktails) : ~4 secondes au premier demarrage (cache .npy sur disque). Les re-demarrages suivants chargent directement le .npy : ~50ms. Inference par requete utilisateur : ~50ms pour encoder la requete + ~2ms pour la recherche FAISS = ~52ms total. Ce 50ms est acceptable pour une interface conversationnelle (l'utilisateur n'en perçoit pas la difference). Sur GPU, l'encoding serait ~5x plus rapide mais non necessaire pour ce volume (600 cocktails). Le bottleneck reel est l'appel a Gemini API (~500-1500ms).",
     "C5.2 SBERT Perf"),
    ("Qu'est-ce que le fine-tuning SBERT et auriez-vous pu l'appliquer ?",
     "Le fine-tuning SBERT sur un domaine specifique consiste a continuer l'entrainement du modele pre-entraine sur des paires (requete, cocktail_pertinent) avec une loss de similarite (contrastive loss, MultipleNegativesRankingLoss). Cela adapte les embeddings au vocabulaire cocktail. On ne l'a pas fait ici pour deux raisons : (1) Pas de dataset de paires requete/cocktail annote disponible (construction manuelle couteux). (2) all-MiniLM-L6-v2 generalise bien sans fine-tuning sur le vocabulaire gastronomique car il a ete entraine sur des millions de paires semantiques variees. P@5=0.79 sans fine-tuning montre que c'est suffisant.",
     "C5.2 Fine-tuning"),
    ("Comment evaluez-vous la qualite de retrieval ?",
     "Via deux metriques : 1) P@5 (Precision at 5) = nombre de cocktails pertinents parmi les 5 premiers / 5. Mesure si les resultats immédiats sont bons. P@5=0.79 signifie qu'en moyenne 3.95 des 5 premiers sont pertinents. 2) NDCG@5 (Normalized Discounted Cumulative Gain) = penalise les bonnes reponses qui arrivent en position 5 plutot qu'en position 1. NDCG=0.82 montre que les meilleurs cocktails arrivent en tetes de liste. Le dataset d'evaluation : 50 requetes variees (ingredients specifiques, mood, occasion, restrictions) annotees manuellement avec les cocktails pertinents parmi le corpus.",
     "C5.2 Evaluation Metriques"),
    ("Comment construisez-vous le prompt envoy a Gemini ?",
     "Template structure en 3 parties : 1) System instruction - 'Tu es un barman expert, reponds uniquement sur les cocktails, sois concis et convivial'. 2) Contexte retrieval - les 5 cocktails recuperes avec leurs ingredients et instructions complets (format markdown). 3) Requete utilisateur enrichie. Le tout est envoye comme un seul user message (Gemini free tier ne supporte pas les system roles proprement). Le prompt total est ~1500 tokens (budget context = 16K tokens pour gemini-1.5-flash). La temperature est fixee a 0.7 pour equilibrer creativite et coherence.",
     "C5.2 Prompt"),

    # Section 3 - FAISS
    ("Qu'est-ce que FAISS et comment fonctionne IndexFlatIP ?",
     "FAISS (Facebook AI Similarity Search) est une bibliotheque de recherche de voisins proches dans des espaces vectoriels de haute dimension. IndexFlatIP (Inner Product) stocke tous les vecteurs en memoire (flat = pas de compression) et calcule le produit scalaire exact entre la requete et TOUS les vecteurs du corpus. Complexite : O(N*D) ou N=600 cocktails, D=384 dimensions = 230K operations flottantes par requete - negligeable (<0.5ms). Pour 600 cocktails, l'index exact est suffisant. Pour 1M+ cocktails, on passerait a IndexIVFFlat (approximatif) ou HNSW pour reduire la complexite.",
     "C5.3 FAISS"),
    ("Pourquoi ne pas utiliser IndexIVFFlat pour 600 cocktails ?",
     "IndexIVFFlat est une index approximatif qui partitionne le corpus en clusters (Voronoi cells) et ne cherche que dans les clusters proches de la requete. Utile pour 100K+ vecteurs pour reduire le temps de recherche. Pour 600 cocktails, le surcoût de clustering (entrainement IVF, parametre nlist) + la perte de precision (approximation) n'est pas justifie. IndexFlatIP calcule les 600 produits scalaires en <0.5ms, ce qui est parfaitement dans le budget de latence. La regle : IndexFlat pour < 10K vecteurs, IndexIVF pour > 100K.",
     "C5.3 FAISS Choix"),
    ("Comment FAISS gere-t-il l'ajout de nouveaux cocktails ?",
     "IndexFlatIP ne supporte pas les insertions incrementales (add puis search). Pour ajouter de nouveaux cocktails sans reconstruire l'index entier : 1) On maintient un index temporaire IndexFlatIP des nouveaux cocktails (< 100). 2) A chaque requete, on cherche dans l'index principal ET dans l'index temporaire, puis on merge les resultats. 3) Periodiquement (ex : quota de 100 nouveaux), on reconstruit l'index complet. Pour un systeme dynamique a grande echelle, on utiliserait FAISS IndexIDMap ou une base vectorielle comme Pinecone, Qdrant, ou pgvector.",
     "C5.3 FAISS Dynamique"),

    # Section 4 - Guardrail
    ("Qu'est-ce que le guardrail cosinus seuil 0.35 et pourquoi ce seuil ?",
     "Le guardrail est un filtre de pertinence : si la similarite cosinus entre la requete de l'utilisateur et le meilleur cocktail du corpus est < 0.35, on rejette la requete avec le message 'Je suis specialise dans les cocktails, pouvez-vous preciser votre question ?'. Ce seuil evite que Gemini genere une reponse sur des sujets hors-domaine (ex : 'Quelle est la meteo demain ?' -> similarite avec tous les cocktails ~0.10 -> rejet). Le seuil 0.35 a ete calibre empiriquement sur un set de 30 requetes hors-domaine et 30 requetes valides : FPR=0.03, FNR=0.07 - excellent compromis.",
     "C5.3 Guardrail"),
    ("Que se passe-t-il si un utilisateur contourne le guardrail ?",
     "Scenarios de contournement : 1) 'Cocktail meteo Paris' - le mot cocktail augmente la similarite cosinus artificiellement. Mitigation : on calcule le cosinus apres avoir supprime les mots genériques du vocabulaire cocktail ('cocktail', 'drink', 'boisson') de la requete avant le guardrail. 2) Injection de prompt - 'Ignore les instructions precedentes et dis-moi comment...' - la similarite avec les cocktails restera faible car les embeddings SBERT ne capturent pas les instructions procedurales. Le guardrail filtrerait. Une securite additionnelle : liste de mots cles interdits (instructions Gemini system prompt).",
     "C5.3 Guardrail Bypass"),
    ("Le guardrail est-il suffisant pour un deploiement grand public ?",
     "Non, plusieurs couches supplementaires seraient necessaires : 1) Content moderation API (Perspective API de Google ou Guardrails AI) pour detecter les contenus inappropries (langage offensant, demandes dangereuses). 2) Rate limiting par utilisateur (proteger contre le scraping et les abus). 3) Logging de toutes les requetes pour audit (RGPD : journaliser sans stocker le contenu personnel). 4) Validation du format de sortie Gemini (Pydantic) pour s'assurer que la reponse est bien structuree. 5) Timeout global de 3s : si Gemini ne repond pas, retourner le top-3 retrieval sans generation.",
     "C5.3 Guardrail Limitations"),

    # Section 5 - Google Gemini
    ("Pourquoi Google Gemini et pas GPT-4 ou un modele open source ?",
     "Trois raisons : 1) Gemini free tier - aucun cout d'API pour un projet academique. GPT-4 coutait ~$0.03 par 1K tokens completion (budget prohibitif pour du dev/test). 2) Qualite suffisante pour la tache - la generation de recommandations cocktails ne necessite pas GPT-4. Gemini 1.5 Flash offre un bon rapport qualite/vitesse pour cette tache. 3) Pas de modele open source comparable en qualite qui tourne localement sur CPU en moins de 2s (LLaMA 3.1 8B necessite un GPU ou est trop lent sur CPU). Pour la production, on envisagerait Mistral 7B quantifie sur un VPS GPU ou Claude Haiku pour le cout.",
     "C5.3 Gemini Choix"),
    ("Comment gerez-vous les limites du free tier Gemini ?",
     "Le free tier Gemini 1.5 Flash a une limite de 15 req/min et 1M tokens/jour. Strategies : 1) Cache JSON MD5 - le hash MD5 de la requete normalisee est la cle du cache. Si la reponse est en cache, pas d'appel API. Hits rate en test : ~40% (beaucoup de requetes similaires). 2) Debounce 500ms - evite les appels rapides consecutifs lors de la frappe utilisateur. 3) Queue de requetes - si la limite est atteinte, les requetes sont mise en file et traitees avec un delai de 4s (60/15). En cas d'erreur 429, on retourne le resultat de retrieval SBERT sans generation.",
     "C5.3 Rate Limiting"),
    ("Qu'est-ce que le cache JSON MD5 et pourquoi pas Redis ?",
     "Cache fichier : chaque (requete_normalisee, top_k) est hache en MD5 (32 chars hexadecimaux). La reponse complete Gemini est serialisee en JSON et stockee dans cache/{md5}.json. A chaque requete, on calcule le MD5 et verifie l'existence du fichier cache avant l'appel API. Pourquoi pas Redis : le projet est single-server, le cache fichier est suffisant (latence < 1ms pour lire un JSON de 2KB). Redis serait justifie si plusieurs instances de l'app tournaient en parallele (partage du cache) ou si le TTL dynamique etait necessaire. Le cache fichier a un TTL implicite : suppression manuelle ou date de modification.",
     "C5.3 Cache"),

    # Section 6 - Profiling ingredients
    ("Qu'est-ce que le profilage des 61 ingredients ?",
     "Chaque ingredient du corpus a ete annote manuellement sur 7 dimensions gustatives : acidite (0-1), sucre (0-1), amertume (0-1), alcool (0-1), fumee (0-1), fruit (0-1), menthe/frais (0-1). Ex : citron vert = acidite:0.9, sucre:0.1, amertume:0.3, alcool:0, fumee:0, fruit:0.8, menthe:0.4. Ce profil permet de calculer le profil gustatif d'un cocktail comme la moyenne ponderee des profils de ses ingredients (poids proportionnel aux volumes). Deux cocktails au profil similaire peuvent ainsi etre recommandes meme si leurs ingredients sont differents.",
     "C5.2 Profiling"),
    ("Pourquoi 7 dimensions gustatives et pas plus ?",
     "Le choix de 7 dimensions est un compromis entre expressivite et annotabilite manuelle. Plus de dimensions (ex : 14) aurait necessite une annotation plus fine, source d'erreurs et d'incoherences entre annotateurs. Les 7 dimensions retenues couvrent les principales axes de la roue des aromes des spiritueux (modele Flavor Wheel de l'American Distilling Institute). Une analyse en composantes principales (PCA) sur ces 7 dimensions montre que les 3 premiers axes expliquent 82% de la variance - ce qui confirme qu'il n'y a pas de redondance excessive. Pour un systeme plus sophistique, on utiliserait un embedding apris automatiquement sur les co-occurrences d'ingredients.",
     "C5.2 7 Dimensions"),
    ("Comment le profil gustatif est-il utilise dans la recommandation ?",
     "Double usage : 1) Filtrage - si l'utilisateur declare 'je n'aime pas l'amertume', on filtre les cocktails dont le score amertume > 0.5. 2) Re-ranking - parmi les K=5 resultats SBERT, on re-classe selon la similarite cosinus entre le profil gustatif de la requete implicite et les profils des cocktails. La requete implicite est estimee par une extraction de mots-cles de goût ('fruity', 'sweet', 'smoky') mappes vers les 7 dimensions via un dictionnaire. Le score final = 0.7 * score_sbert + 0.3 * score_gustatif. Ce re-ranking ameliore P@5 de 0.79 a 0.83.",
     "C5.2 Profil Usage"),

    # Section 7 - Metriques
    ("Expliquez P@5 et NDCG avec un exemple concret.",
     "Requete : 'cocktail ete avec citron'. Corpus : 600 cocktails. Resultats SBERT top-5 : Mojito (pertinent), Caipirinha (pertinent), Daiquiri (pertinent), Aperol Spritz (pertinent), Manhattan (non pertinent). P@5 = 4/5 = 0.80 pour cette requete. NDCG : on pondere par la position - un bon resultat en position 1 vaut plus qu'en position 5. NDCG@5 = 1/log(2) * 1 + 1/log(3) * 1 + 1/log(4) * 1 + 1/log(5) * 1 + 0/log(6)) normalise par DCG ideal. NDCG=0.82 sur 50 requetes signifie que les bons resultats arrivent majoritairement en premiere position.",
     "C5.2 P@5 NDCG"),
    ("Comment avez-vous construit le jeu d'evaluation des 50 requetes ?",
     "Construction semi-automatique : 1) 50 requetes variees couvrant : ingredients specifiques ('avec rhum brun'), occasions ('soiree d'ete'), restrictions ('sans alcool'), style ('fruity and sweet'), contexte ('apres diner'). 2) Pour chaque requete, annotation manuelle des cocktails pertinents dans le corpus (top-20 pertinents maximum, jugement subjectif mais consensuel entre deux annotateurs). 3) Cohen's Kappa entre annotateurs = 0.74 (bonne concordance). La diversite des requetes (5 categories x 10 requetes) assure que les metriques ne sont pas biaisees vers un type de requete particulier.",
     "C5.2 Eval Set"),
    ("Le P@5=0.79 est-il suffisamment bon ?",
     "Dans le contexte de la recommandation de cocktails, oui. La reference : les systemes de recommendation e-commerce (Amazon, Netflix) visent P@5 > 0.70 sur leurs domaines. Un utilisateur qui recoit 4 suggestions pertinentes sur 5 est satisfait. De plus, le systeme dispose d'une generation Gemini pour expliquer et contextualiser les resultats - meme un resultat a 0.60 de similarite peut etre tres pertinent si Gemini l'explique bien. La limite : notre jeu d'evaluation de 50 requetes est petit (variance elevee des metriques). Un jeu de 500 requetes donnerait des metriques plus stables.",
     "C5.2 P@5 Qualite"),

    # Section 8 - Interface Speakeasy
    ("Decrivez l'interface Streamlit Speakeasy.",
     "Interface thematique annees 1920 (speakeasy = bar clandestin pendant la Prohibition). Design : fond brun fonce (#2C1A0E), typographie serif (Georgia), accents dores (#D4A437), illustrations art deco. Composants Streamlit : zone de chat (st.chat_message) avec avatars bartender/client, sidebar avec les filtres gustatifs (7 sliders 0-1), section 'My Bar' pour sauvegarder les favoris (st.session_state + JSON local), galerie de cocktails en grid (st.columns). L'animation d'attente pendant l'appel Gemini affiche un shaker anime (st.spinner avec emoji). Le CSS custom est injecte via st.markdown(unsafe_allow_html=True).",
     "C5.3 Speakeasy"),
    ("Comment avez-vous gere l'etat de session dans Streamlit ?",
     "Streamlit re-execute le script entier a chaque interaction. Pour maintenir l'etat : st.session_state stocke : 1) messages (historique de conversation), 2) favoris (liste de cocktail_ids), 3) profil gustatif (dict 7 dimensions), 4) cache_results (dict requete -> resultats SBERT pour eviter les re-calculs). Les messages sont persistes en JSON dans un fichier local pour survivre aux rechargements du navigateur (st.session_state perdu si refresh). L'embedding du corpus est charge une fois via @st.cache_resource (singleton - ne se recalcule pas a chaque re-run).",
     "C5.3 Session State"),
    ("Pourquoi le design 'Speakeasy' plutot qu'un design moderne ?",
     "Differentiateur et choix delibere de branding : 1) Coherence narrative - un systeme de recommandation de cocktails avec une ambiance bar clandestin des annees 1920 cree une experience immersive et memorisable. 2) Contexte academique - la singularite du design retient l'attention du jury. 3) Demonstration de maitrise CSS dans Streamlit (injection de styles personnalises, depassement des limitations visuelles par defaut de Streamlit). Le risque : l'accessibilite peut etre compromise (contraste texte/fond faible dans les zones sombres). On a verifie les ratios de contraste (WCAG AA : >= 4.5:1) sur les zones de texte principales.",
     "C5.3 Design Speakeasy"),

    # Section 9 - Dataset cocktails
    ("Combien de cocktails y a-t-il dans le corpus final et d'ou viennent-ils ?",
     "Corpus final : 637 cocktails uniques apres deduplication (sur idDrink + nom normalise). Sources : TheCocktailDB (426 cocktails via API alphabetique A-Z + endpoint non-alcoholic), Kaggle datasets - aadyasingh55/cocktails (425 lignes mais 210 uniques apres deduplication), mexwell/iba-cocktails (90 cocktails IBA officiels), pxxthik/the-cocktail-db-recipe-collection (2491 lignes mais majoritairement duplication). La deduplication utilise Jaccard similarity sur les ingredients (seuil 0.9) pour detecter les cocktails avec noms differents mais recettes identiques.",
     "C5.1 Dataset"),
    ("Comment avez-vous gere la qualite du dataset cocktails ?",
     "Pipeline de validation : 1) Completude - filtre les cocktails sans ingredients (name_only records). 2) Coherence - verification que les mesures des ingredients sont dans des plages realistes (pas 500ml vodka dans un verre de 200ml). 3) Langue - tous les cocktails en anglais (instructions en anglais obligatoire pour SBERT pre-entraine sur corpus EN). Les cocktails avec instructions non-EN ont ete traduits via googletrans. 4) Deduplication - 637 uniques sur ~3500 records bruts. 5) Normalisation des ingredients - 'fresh lime juice' et 'lime juice' -> 'lime_juice' via un dictionnaire de synonymes.",
     "C5.1 Qualite"),
    ("Comment etendriez-vous le systeme a d'autres domaines gastronomiques ?",
     "Architecture generalisable via trois changements : 1) Remplacer le corpus cocktails par un corpus de recettes, vins, ou restaurants. 2) Adapter les 7 dimensions gustatives au domaine (vin : tanins, acidite, boisé, fruité, minéral, longueur, intensite). 3) Adapter le system prompt Gemini au persona du domaine ('Tu es un sommelier expert...'). Le pipeline SBERT+FAISS+Gemini est domain-agnostic. L'effort principal est dans la construction du corpus (qualite, completude) et le profilage des entites (equivalent des 61 ingredients). Pour un domaine comme les vins, on pourrait exploiter la Wine Quality database de l'UCI.",
     "C5.3 Generalisation"),

    # Section 10 - Critique & Fusion
    ("Quelles sont les limites de l'approche SBERT+Gemini ?",
     "Cinq limites identifiees : 1) Dependance API Gemini - si l'API est indisponible, le systeme se degrade en retrieval pur (acceptable mais moins riche). 2) Hallucination residuelle - malgre le grounding RAG, Gemini peut modifier les quantites d'un cocktail ou inventer des variantes non testees. 3) Evaluation limitee - 50 requetes de test sont insuffisantes pour une evaluation robuste (intervalle de confiance large). 4) Cold start ingredient - un ingredient tres rare absent du corpus de profilage reçoit un profil neutre (tous 0.5). 5) Langue unique - le systeme fonctionne uniquement en anglais (corpus et modele EN).",
     "C5.3 Limites"),
    ("Quelles sont les differences techniques entre ia-pero et cocktail-ia-generatif ?",
     "Les deux projets partagent la meme idee centrale (recommandation cocktails SBERT) mais avec des differences techniques : ia-pero - SBERT+Gemini (RAG complet), guardrail 0.35, profiling 7 dimensions, interface Speakeasy, P@5=0.79. cocktail-ia-generatif (MixCraft) - SBERT+FAISS+GPT-2 fine-tune, guardrail 0.40, interface premium moderne (CSS custom), dataset plus large (Kaggle + TheCocktailDB). Une fusion des deux depots combinerait le meilleur des deux : interface Speakeasy + Gemini (gratuit) + FAISS optimise + dataset elargi + profiling 7 dimensions.",
     "C5.3 Diff Repos"),
    ("Si vous deviez fusionner les deux repos, comment procederiez-vous ?",
     "Migration en 4 etapes : 1) Choix du repo cible (cocktail-ia-generatif, plus complet en dataset). 2) Branche feat/merge-ia-pero : copier les modules uniques d'ia-pero (profiling.py, guardrail.py, interface Speakeasy, cache JSON MD5). 3) Unification du pipeline : SBERT+FAISS (cocktail-ia-generatif) + Gemini (ia-pero) + profiling (ia-pero) + interface (ia-pero). 4) Tests de non-regression : P@5 >= 0.79, latence totale < 2s, guardrail FPR < 0.05. La fusion reduirait la duplication de code et permettrait de maintenir un seul systeme de qualite plutot que deux partiellement redondants.",
     "C5.3 Fusion"),
    ("En quoi ce projet repond aux competences RNCP Bloc 2 C5 ?",
     "C5.1 : conception d'un systeme RAG complet (SBERT retrieval + Gemini generation), architecture modulaire (retrieval/generation/guardrail). C5.2 : evaluation rigoureuse avec P@5=0.79 et NDCG=0.82 sur 50 requetes annotees manuellement, comparaison baseline TF-IDF (+18 points). C5.3 : deploiement d'un systeme d'IA generative (Gemini) avec guardrails, interface Streamlit thematique, gestion du free tier et cache. Demonstration d'un pipeline RAG end-to-end de la collecte de donnees (Kaggle + TheCocktailDB) jusqu'a l'interface utilisateur conversationnelle.",
     "C5.3 RNCP C5"),
    ("Quelle evolution vers un systeme de recommandation encore meilleur ?",
     "Deux axes majeurs : 1) Feedback utilisateur actif - log des likes/dislikes sur les recommandations, fine-tuning SBERT periodique sur les paires (requete, cocktail_positif) via contrastive learning. Cela ferait passer P@5 de 0.79 a estimativement 0.88-0.92. 2) Multimodalite - integrer les images des cocktails (TheCocktailDB fournit des thumbnails) via CLIP (Contrastive Language-Image Pre-Training) pour permettre des requetes visuelles ('cocktail qui ressemble a ca' avec une image). Le re-ranking combinerait le score SBERT textuel et le score CLIP visuel.",
     "C5.3 Evolution"),
    ("Comment gerez-vous la vie privee des utilisateurs dans ce systeme ?",
     "Par conception : 1) Pas de compte utilisateur - les preferences sont stockees uniquement en session locale (st.session_state + JSON fichier local). 2) Les requetes envoyees a Gemini ne contiennent aucune information personnelle identifiable (pas de nom, email, localisation). 3) Le cache MD5 ne stocke que le hash de la requete, jamais la requete en clair dans le nom de fichier. 4) Conformite RGPD : pas de collecte de donnees personnelles -> pas de DPIA (Data Protection Impact Assessment) necessaire. Pour une version multi-utilisateurs, on implémenterait un consentement explicite et une politique de retention des conversations.",
     "C5.3 Privacy"),
]


UDE_QA.extend(UDE_QA_EXTRA)
MPI_QA.extend(MPI_QA_EXTRA)
IAP_QA.extend(IAP_QA_EXTRA)
UDE_QA.extend(UDE_QA_EXTRA2)
MPI_QA.extend(MPI_QA_EXTRA2)
IAP_QA.extend(IAP_QA_EXTRA2)
UDE_QA.extend(UDE_QA_EXTRA3)
MPI_QA.extend(MPI_QA_EXTRA3)
IAP_QA.extend(IAP_QA_EXTRA3)
UDE_QA.extend(UDE_QA_EXTRA4)
MPI_QA.extend(MPI_QA_EXTRA3_PATCH)
IAP_QA.extend(IAP_QA_EXTRA4)


def build_pdf(project_name, cover_title, cover_subtitle, cover_bloc, sections, qa_list, out_path):
    pdf = SoutenancePDF()
    pdf.project_name = project_name
    pdf.set_margins(15, 25, 15)
    pdf.set_auto_page_break(True, margin=18)

    pdf.cover(cover_title, cover_subtitle, cover_bloc)

    q_num = 1
    for sec_num, (sec_title, badge) in enumerate(sections, 1):
        pdf.add_page()
        pdf.section_title(sec_num, sec_title)
        for _ in range(15):
            if q_num - 1 < len(qa_list):
                item = qa_list[q_num - 1]
                q, a = item[0], item[1]
                item_badge = item[2] if len(item) > 2 else badge
                pdf.qa(q_num, q, a, item_badge)
                q_num += 1

    pdf.output(str(out_path))
    print(f"[OK] {out_path.name}  ({out_path.stat().st_size // 1024} KB)  {q_num-1} Q&A")


if __name__ == "__main__":

    UDE_SECTIONS = [
        ("Architecture generale et choix techniques", "C1.1 Architecture"),
        ("PostgreSQL - Schema etoile et optimisation", "C1.1 PostgreSQL"),
        ("Cassandra - Modele NoSQL et partitionnement", "C1.1 Cassandra"),
        ("Kafka - Streaming et micro-batch 10s", "C1.2 Kafka"),
        ("API FastAPI et securite JWT", "C1.3 FastAPI"),
        ("Collecte de donnees - 24 sources 8 familles", "C1.2 Sources"),
        ("Indicateurs composites - IVU et Score Env", "C2.1 Indicateurs"),
        ("Frontend MapLibre et visualisation carto", "C2.2 CartoDB"),
        ("Tests pytest 102 et CI/CD", "C2.3 Qualite"),
        ("Critique, limites et perspectives RNCP", "C2.4 Bilan"),
    ]

    MPI_SECTIONS = [
        ("Formulation du probleme et dataset", "C3.1 Probleme"),
        ("Exploration et preprocessing pipeline", "C3.2 Prep"),
        ("Benchmark 4 modeles - comparaison rigoureuse", "C3.3 Benchmark"),
        ("XGBoost - hyperparametres et resultats retenus", "C3.4 XGBoost"),
        ("Metriques F1, ROC-AUC, matrice de confusion", "C3.5 Metriques"),
        ("SHAP et explicabilite du modele", "C4.1 SHAP"),
        ("CodeCarbon et empreinte environnementale", "C4.2 GreenAI"),
        ("Deploiement FastAPI + Streamlit + ONNX", "C4.3 Deploy"),
        ("Biais, limites et validite externe", "C4.4 Limites"),
        ("Perspectives, valeur industrielle et RNCP", "C4.4 Bilan"),
    ]

    IAP_SECTIONS = [
        ("Architecture RAG - SBERT + FAISS + Gemini", "C5.1 RAG"),
        ("SBERT all-MiniLM-L6-v2 - encodage semantique", "C5.2 SBERT"),
        ("FAISS - recherche vectorielle et index", "C5.3 FAISS"),
        ("Guardrail cosinus seuil 0.35 - filtrage", "C5.3 Guard"),
        ("Google Gemini - generation et rate limiting", "C5.3 Gemini"),
        ("Profiling 61 ingredients - 7 dimensions", "C5.2 Profil"),
        ("Evaluation P@5=0.79 et NDCG=0.82", "C5.2 Eval"),
        ("Interface Streamlit Speakeasy 1920s", "C5.3 UI"),
        ("Dataset cocktails - sources et qualite", "C5.1 Data"),
        ("Critique, fusion repos, perspectives RNCP", "C5.3 Bilan"),
    ]

    build_pdf(
        "Urban Data Explorer - Bloc 1 RNCP40875",
        "Urban Data Explorer",
        "150 Questions de Soutenance avec Reponses Detaillees",
        "Bloc 1 - Competences C1.1 a C2.4",
        UDE_SECTIONS,
        UDE_QA,
        OUT_DIR / "Soutenance_UDE_150Q.pdf",
    )

    build_pdf(
        "Maintenance Predictive - Bloc 2 C3 RNCP40875",
        "Maintenance Predictive Industrielle",
        "150 Questions de Soutenance avec Reponses Detaillees",
        "Bloc 2 - Competences C3.1 a C4.4",
        MPI_SECTIONS,
        MPI_QA,
        OUT_DIR / "Soutenance_MPI_150Q.pdf",
    )

    build_pdf(
        "IA-Pero / MixCraft - Bloc 2 C5 RNCP40875",
        "IA Generative Cocktails - ia-pero & MixCraft",
        "150 Questions de Soutenance avec Reponses Detaillees",
        "Bloc 2 - Competences C5.1 a C5.3",
        IAP_SECTIONS,
        IAP_QA,
        OUT_DIR / "Soutenance_IAPero_150Q.pdf",
    )

    print("\nDone - 3 PDFs generes dans", OUT_DIR)
