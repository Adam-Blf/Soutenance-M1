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

## Bloc 2 - IA générative (MixCraft)

**Pourquoi ce cas d'usage ?**
Création de recettes de cocktails originales depuis une liste d'ingrédients disponibles. Les règles manuelles ne peuvent pas produire une recette inédite cohérente - c'est un problème de génération conditionnelle. Thématique alternative validée par l'Annexe I du sujet. Deux sous-tâches : retrieval (SBERT+FAISS, trouver les recettes similaires) et génération (GPT-2 fine-tune, produire la nouvelle recette).

**Quel modèle ? Pourquoi ?**
SBERT all-MiniLM-L6-v2 pour l'encodage (local, 384 dims, L2-normalisé, 0 cout API). GPT-2 fine-tuné sur 500+ recettes du corpus Kaggle pour la génération : modele open-source, 100% local, offline, reproductible. FAISS (IndexFlatIP) pour la recherche de plus proches voisins vectoriels.

**Comment évaluez-vous la qualité des réponses ?**
Deux axes : (1) recommandation - Precision@5 = 0.79, NDCG@5 = 0.82 vs baseline TF-IDF P@5 = 0.61. (2) génération - BLEU-4 = 0.41, ROUGE-L = 0.58 sur le jeu de test hold-out 20%. Guardrail F1 = 0.92 sur 10 requetes (5 in-domain, 5 hors-domaine). Latence : < 0.4 s (cache hit), < 3 s (génération CPU).

**Quels paramètres avez-vous ajustés ?**
Seuil guardrail (0.40 - calibré pour maximiser F1), Top-K FAISS (5), température GPT-2 (0.8 - creativité vs cohérence), top_p (0.92), epochs fine-tuning (3 - au-dela = surapprentissage sur petit corpus). Structure du contexte RAG injecté dans le prompt.

**Quels risques ?**
Génération hors-sujet mitigée par RAG+guardrail. Qualité GPT-2 limitée par la taille du corpus (500 recettes - un LLM plus grand ameliorerait BLEU). Biais dataset : corpus majoritairement cocktails anglophone. Usage responsable de l'alcool mentionné comme limite éthique.

**Comment l'industrialiser ?**
Remplacer GPT-2 par un LLM plus grand (Llama/Mistral) avec quantification GGUF pour rester local. Indexation FAISS sur corpus étendu (10k+ recettes). Monitoring drift sémantique. Feedback humain en boucle (RLHF simplifié sur note de recette).

**Pourquoi SBERT et pas un embedding propriétaire (OpenAI, Cohere) ?**
Choix coût/autonomie : SBERT all-MiniLM-L6-v2 tourne en local, 0 appel réseau sur le retrieval, 0 coût par token. Pour la similarité sur un referentiel fermé de cocktails, 384 dims suffisent - verifié empiriquement (P@5 = 0.79 vs 0.61 TF-IDF). Embedding propriétaire = dépendance externe sur le chemin critique du retrieval.

**Que se passe-t-il exactement quand un utilisateur demande hors-domaine ?**
Le guardrail calcule max(cosinus(requete, corpus)) via SBERT. Si inférieur à 0.40, rejet propre avant toute génération GPT-2. Testé sur cas limites : « répare mon vélo » (score 0.12), requetes vides (0.0), injections de prompt - tous sous le seuil. Risque résiduel documenté : requete sémantiquement proche par hasard.

**Pourquoi le seuil à 0.40 précisément ?**
Calibration empirique sur 10 requetes labelisées (5 in-domain cocktails, 5 hors-domaine) en variant le seuil de 0.1 à 0.9. À 0.40 le F1 du guardrail est maximal (0.92) - bon compromis entre faux rejet (trop restrictif) et faux positif (trop permissif). Reproductible via `src/evaluation.py::evaluate_guardrail()`.

**Pourquoi GPT-2 et pas un LLM plus récent ?**
Contrainte matérielle et académique : GPT-2 (117M params) tourne sur CPU sans GPU, fine-tuning en 3 epochs sur corpus local en <30 min. Pour une preuve de concept sur 500 recettes, la qualité BLEU-4=0.41 est suffisante. En production : Mistral-7B GGUF Q4 serait le bon successeur.

**Pourquoi fine-tuner GPT-2 plutot qu'un prompt LLM API ?**
Trois raisons : (1) 100% offline - aucune dépendance API, conforme à la contrainte du sujet, (2) adaption domaine - le modele fine-tuné connait la structure d'une recette de cocktail (ingrédients + mesures + technique), (3) cout zéro a l'inference - clé pour un projet académique.

---

## Questions d'individualisation (préparer chacun sa version)

**Adam · réponses suggérées**
- Contribution principale : architecture data de bout en bout (médaillon Polars, PG étoile, Cassandra, API sécurisée) + modélisation XGBoost et dashboard maintenance + pipeline SBERT+FAISS+GPT-2 MixCraft.
- Compétence la mieux démontrée : C2.1 (API sécurisée JWT + quotas, démontrable live) ou C4.3 (méthodo comparative avec écoresponsabilité).
- Choix technique porté : Polars plutôt que pandas/Spark pour l'ETL (moteur Rust, 10x plus rapide sur nos volumes, sans cout d'un cluster). Et GPT-2 fine-tuné plutôt qu'API externe pour la génération (100% local, offline, reproductible).
- Difficulté rencontrée : jointure spatiale IRIS (point-in-polygon) lente (cache LRU + arrondi coordonnées), déséquilibre de classes en maintenance (seuil de décision optimisé), et calibration du guardrail MixCraft (courbe F1 en fonction du seuil, choix à 0.40).
- A refaire différemment : brancher les métriques pipeline dès le jour 1, tests unitaires dès le debut plutôt qu'en consolidation, et entraîner GPT-2 sur un corpus plus large (10k+ recettes) pour ameliorer BLEU-4.

**Émilien · à préparer avec lui** (contributions à valider ensemble)
- Pistes · sourcing/qualité des 24 sources, EDA maintenance, front cartographique, préparation données.
