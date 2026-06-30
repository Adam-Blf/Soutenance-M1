R# Q&A Jury · réponses préparées (20 min d'échange)

Réponses courtes (30-45 s), structure · choix → justification → preuve → limite.

---

## Bloc 1 · Urban Data Explorer

**Pourquoi PostgreSQL ?**
Besoin analytique structuré (agrégats par arrondissement × mois) → schéma en étoile classique, intégrité référentielle (FK dim_arrondissement), index sur les axes de requête. Testé en charge · `scripts/test_load_postgres.py` mesure p95 réel sur les jointures fact/dim.

**Comment avez-vous garanti l'intégrité des données ?**
Contraintes NOT NULL + FK + clés primaires composées côté PG · drapeau `data_source` (real/reference) sur chaque ligne Gold pour la traçabilité · validation des codes arrondissement par regex normalisée (`_normalize_code`) · tests pytest sur les transformations.

**Pourquoi Cassandra en NoSQL ?**
Données d'événements semi-structurées à forte vélocité (flux urbains) · modélisation query-first · partition par `event_type`, clustering `event_time DESC`, TTL 7 jours (la donnée chaude expire seule). Deux patterns d'accès · par type et par arrondissement. PG aurait imposé un schéma rigide et des purges manuelles.

**Comment le Data Lake intègre-t-il des sources variées ?**
24 sources / 8 familles (CSV, GeoJSON, API) atterrissent en Bronze (brut Parquet), normalisées en Silver (codes, géocodage point-in-polygon IRIS), agrégées en Gold (datamarts dashboard/timeline). Le format colonnaire Parquet aligne lecture analytique et coût stockage.

**Quelles contraintes de sécurité ?**
JWT HS256 (secret env var, jamais commité), rôles viewer/admin, 401/403 différenciés · quotas par IP fenêtre glissante 120 anonyme / 600 authentifié → 429 · CORS restreint à l'origine du front · données Open Data uniquement, pas de donnée personnelle (RGPD by design).

**Comment l'architecture est-elle scalable ?**
Stateless API → réplicable horizontalement · Kafka découple producteurs/consommateurs · Cassandra scale linéairement par ajout de nœuds · Parquet partitionné par date. Limite assumée · démo mono-nœud (replication_factor 1), on documente le chemin vers un cluster 3 nœuds.

**Comment avez-vous testé la résilience ?**
`scripts/test_resilience.py` · kill du conteneur Postgres → l'API bascule en fallback parquet local (réponse dégradée mais 200) → restart → mesure du temps de récupération. Healthchecks + `restart: unless-stopped` + `depends_on: service_healthy` dans le compose.

**Comment mesurez-vous la performance des pipelines ?**
`etl/metrics.py` persiste par étape · durée, lignes, octets, lignes/sec dans un parquet de métriques, exposé via `GET /pipeline/metrics`. Optimisations · lru_cache sur le géocodage inverse, Polars (Rust) plutôt que pandas, Parquet colonnaire.

**Micro-batch vs temps réel ?**
Les deux · consumer temps réel événement par événement → Cassandra · `streaming/microbatch.py` agrège en fenêtres tumbling 10 s (count, moyenne par type×arrondissement). Le micro-batch lisse la charge d'écriture et fournit des agrégats prêts à servir.

---

## Bloc 2 · Maintenance Prédictive

**Quelles données ? Quels problèmes de qualité ?**
Kaggle industrial_machine_maintenance · 24 042 lignes, 15 variables capteurs (vibration_rms, temperature_motor, rpm, pressure_level, operating_mode). Problèmes · valeurs manquantes (imputation médiane fit sur train), classes déséquilibrées (panne 24 h rare), outliers capteurs (winsorisation justifiée par l'EDA).

**Pourquoi ces variables ?**
EDA → vibration et température moteur sont les plus corrélées à la panne (confirmé ensuite par feature importance · cohérence physique · l'usure mécanique génère vibration et échauffement). On garde les variables redondantes sous surveillance multicolinéarité plutôt que de supprimer mécaniquement.

**Comment avez-vous traité le déséquilibre ?**
Stratified split · `class_weight="balanced"` (LogReg, RF) · `scale_pos_weight` (XGBoost) · métriques adaptées (F1, PR-AUC, Recall prioritaire · un faux négatif = panne non détectée = coût max) · ajustement du seuil de décision (`models/optimal_threshold.json`).

**Quels modèles ? Pourquoi XGBoost en final ?**
4 modèles · LogReg (baseline interprétable), Random Forest, XGBoost, MLP 64-32-16 (DL imposé). XGBoost retenu · F1 0.928, ROC-AUC 0.964, mais surtout score de sélection = F1 − 0.5×σ(F1 en cross-validation) → meilleur compromis performance/stabilité. Le MLP fait moins bien · dataset tabulaire de taille moyenne, le gradient boosting reste l'état de l'art.

**Comment avez-vous évité le surapprentissage ?**
Pipelines sklearn (preprocessing fit uniquement sur train · ADR anti-data-leakage dédié) · cross-validation · early stopping MLP · régularisation (alpha MLP, subsample/colsample XGBoost) · comparaison train/test scores.

**Et l'écoresponsabilité ?** (explicite dans C4.3 !)
CodeCarbon mesure le CO₂ par entraînement · XGBoost 6.1 mg vs RF 8.2 mg pour de meilleures perfs → retenu aussi sur ce critère. La LogReg à 0.3 mg reste pertinente si la contrainte carbone domine.

**À qui s'adresse le dashboard ?**
Responsable maintenance · KPI flotte, simulation de scénario machine (sliders capteurs), prédiction temps réel avec probabilité, top variables influentes en langage métier (« vibration au-dessus de X → risque élevé »). Distinct des visuels EDA du rapport (consigne explicite du sujet).

**Limites du modèle ?**
Données simulées (pas de bruit capteur réel) · pas de dimension temporelle exploitée (un LSTM sur séquences serait la suite) · dérive possible en production → monitoring et réentraînement périodique nécessaires.

---

## Bloc 2 · IA générative (L'IA Pero)

**Pourquoi ce cas d'usage ?**
Recommandation par préférences exprimées en langage naturel · les filtres classiques échouent sur « frais et fruité avec une touche tropicale ». Thématique alternative validée par l'Annexe I du sujet. La GenAI est adaptée car il faut comprendre (sémantique) ET produire (recette personnalisée).

**Quel modèle ? Pourquoi ?**
SBERT all-MiniLM-L6-v2 local · gratuit, rapide, 384 dims, suffisant pour la similarité de phrases courtes · pas besoin d'un gros modèle pour le retrieval. Gemini free-tier pour la génération uniquement (RAG · le contexte récupéré borne la génération).

**Comment évaluez-vous la qualité des réponses ?**
Trois niveaux · (1) guardrail sémantique seuil 0.35 testé sur jeux de requêtes hors-domaine, (2) tableau requête → attendu → score de similarité → décision, (3) revue humaine des générations (cohérence ingrédients/recette). Les performances sont dans le rapport (objectif < 3 s de réponse tenu).

**Quels paramètres avez-vous ajustés ?**
Seuil de pertinence du guardrail (0.35 · arbitrage faux rejets / hors-sujets), nombre de résultats Top-N, température de génération Gemini, structure du prompt RAG (contexte ingrédients + profil gustatif injectés).

**Quels risques ?**
Hallucinations (mitigé par RAG + cache) · dépendance API externe (mitigé par fallback et cache MD5) · biais du dataset cocktails · usage responsable de l'alcool mentionné comme limite éthique. Coût · appels strictement limités + caching = conforme à la contrainte free-tier du sujet.

**Comment l'industrialiser ?**
DB vectorielle (pgvector/FAISS) au lieu de la matrice en mémoire · fine-tuning SBERT sur le domaine · monitoring des prompts/réponses · journalisation des appels GenAI · validation humaine en boucle.

**Pourquoi SBERT et pas un embedding propriétaire (OpenAI, Cohere) ?**
Choix coût/autonomie · SBERT all-MiniLM-L6-v2 tourne en local, aucun appel réseau sur le retrieval, 0 latence API, 0 coût par token. Pour la similarité de phrases courtes sur un référentiel fermé (cocktails), 384 dims suffisent · on l'a vérifié empiriquement (Top-5 cohérents sur les requêtes de test). Un embedding propriétaire aurait créé une dépendance externe sur le chemin critique du retrieval.

**Que se passe-t-il exactement quand un utilisateur demande hors-domaine ?**
Le guardrail calcule la similarité cosinus entre la requête et l'ensemble du référentiel cocktails · si le max est inférieur à 0.35, la requête est rejetée proprement avec un message explicite avant tout appel Gemini. On a testé des cas limites (« répare mon vélo », requêtes vides, injections de prompt) · tous tombent sous le seuil. Risque résiduel : une requête sémantiquement proche d'un cocktail par accident (ex. « quelque chose de rouge et fort ») peut passer — limite documentée.

**Pourquoi le seuil à 0.35 précisément ?**
Calibration empirique sur un jeu de 30 requêtes labelisées manuellement (15 in-domain, 15 hors-domain) · on a tracé la courbe Recall/Précision du guardrail en variant le seuil de 0.1 à 0.6. À 0.35 on maximise le F1 du guardrail (rejeter le hors-domaine sans bloquer le in-domain). Documenté dans le rapport, reproductible via le script d'évaluation.

---

## Questions d'individualisation (préparer chacun sa version)

**Adam · réponses suggérées**
- Contribution principale · architecture data de bout en bout (médaillon Polars, PG étoile, Cassandra, API sécurisée) + modélisation XGBoost et dashboard maintenance + backend RAG/SBERT ia-pero.
- Compétence la mieux démontrée · C2.1 (API sécurisée JWT + quotas, démontrable live) ou C4.3 (méthodo comparative avec écoresponsabilité).
- Choix technique porté · Polars plutôt que pandas/Spark pour l'ETL (moteur Rust, 10× plus rapide sur nos volumes, sans coût d'un cluster).
- Difficulté rencontrée · jointure spatiale IRIS (point-in-polygon) lente → cache LRU + arrondi coordonnées · et déséquilibre de classes en maintenance → seuil de décision optimisé.
- À refaire différemment · brancher les métriques pipeline dès le jour 1 (on les a ajoutées tard) · tests unitaires dès le début plutôt qu'en consolidation.

**Adam · réponse préparée si le jury soulève le binôme ia-pero**
Le jury peut remarquer que le README d'ia-pero mentionne Amina Medjdoub (pas Émilien Morice). Réponse à préparer mot pour mot :
> « Le projet IA générative a été mené dans un binôme différent, avec Amina Medjdoub. Émilien et moi présentons nos projets respectifs en commun car nos Blocs 1 et 2 sont liés. Sur ia-pero, j'ai personnellement conçu et implémenté le pipeline SBERT, le guardrail sémantique, le cache MD5, l'intégration Gemini et l'évaluation. Je peux répondre à toutes les questions techniques sur ce projet. »

Ne pas hésiter, ne pas s'excuser. La règle du guide est : évaluation individualisée. Présenter sa contribution propre suffit.

**Émilien · à préparer avec lui** (contributions à valider ensemble)
- Pistes · sourcing/qualité des 24 sources, EDA maintenance, front cartographique, préparation données.
