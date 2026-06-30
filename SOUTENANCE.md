# Soutenance de fin d'études · Bloc 1 & 2 · RNCP40875

> Adam Beloucif · binôme Émilien Morice · EFREI M1 Data Engineering & IA · Session 2026-2027
> Format certificatif · jury · 50 minutes · présentation collective, évaluation individualisée

---

## 1. Format officiel (guide de préparation)

| Élément | Valeur |
|---|---|
| Durée totale | **50 min** · 30 min présentation/démo + 20 min échange jury |
| Slides | **20 max** |
| Évaluation | Collective en présentation, **individualisée** en notation |
| Logique imposée | Besoin métier → choix techniques → réalisation → **preuve** → résultat → limites |

### Déroulé minute par minute (recommandation du guide)

| # | Partie | Durée | Slides | Qui (proposition) |
|---|---|---|---|---|
| 1 | Introduction générale | 2 min | 1-4 | Adam |
| 2 | Projet 1 · Architecture data (Bloc 1) · **Urban Data Explorer** | 9 min | 5-9 | Adam (archi+API) / Émilien (data+front) |
| 3 | Projet 2 · Data Science (Bloc 2) · **Maintenance Prédictive** | 9 min | 10-14 | Émilien (EDA+prépa) / Adam (modèles+dashboard) |
| 4 | Projet 3 · IA générative (Bloc 2) · **L'IA Pero** | 6 min | 15-17 | Adam |
| 5 | Conclusion transversale | 4 min | 18-20 | Les deux |

⚠️ **Point à clarifier avec le tuteur AVANT la soutenance** · ia-pero a été réalisé avec **Amina Medjdoub** (pas Émilien · 0 commit d'Émilien sur le repo). Si le groupe de soutenance est Adam+Émilien, vérifier si chacun présente son propre projet GenAI ou si un seul des deux est montré. Préparer la réponse · « le projet GenAI a été mené dans un binôme différent, je présente ma contribution ».

---

## 2. Les 3 projets · pitch et chiffres clés

### Projet 1 · Urban Data Explorer (Bloc 1 · C1.1 → C2.4)
- **Pitch** · « Plateforme data complète d'exploration du logement parisien · 24 sources Open Data, architecture médaillon Bronze/Silver/Gold en Polars, PostgreSQL en étoile, Cassandra pour le streaming, Kafka, API FastAPI sécurisée JWT + quotas, dashboard React/MapLibre charte DSFR. »
- **Chiffres** · 24 sources / 8 familles · DVF 2023 réel (prix m² médian par arrondissement) · INSEE Filosofi 2020 · 5 niveaux carto (ville → bâtiment) · quotas API 120/600 req·min · 102 tests pytest (branche en cours de merge).
- **Preuves démontrables** · `/docs` Swagger live · `postgres/init.sql` schéma étoile + index · `cassandra/schema.cql` modélisation query-first · `docker-compose` healthchecks + profils · ADR 0001 · script résilience (kill container Postgres → fallback parquet).
- Repo · github.com/Adam-Blf/urban-data-explorer · binôme Émilien ✓

### Projet 2 · Maintenance Prédictive Industrielle (Bloc 2 · C3.1 → C4.3)
- **Pitch** · « Système intelligent multi-modèles prédisant la panne machine sous 24 h à partir de capteurs IoT (vibration, température, RPM, pression) · 4 modèles comparés dont 1 Deep Learning, dashboard décisionnel Streamlit, API FastAPI, mesure CO₂ CodeCarbon. »
- **Chiffres à apprendre par cœur** ·

| Modèle | F1 | ROC-AUC | CV F1 moy | Score sélection | Temps | CO₂ |
|---|---|---|---|---|---|---|
| LogReg (baseline) | 0.747 | 0.959 | 0.750 | 0.746 | 3.2 s | 0.3 mg |
| Random Forest | 0.863 | 0.992 | 0.844 | 0.839 | 45 s | 8.2 mg |
| **XGBoost (retenu)** | **0.886** | **0.995** | **0.886** | **0.880** | 35 s | 6.1 mg |
| MLP 64-32-16 (DL) | 0.836 | 0.984 | 0.795 | 0.790 | 18 s | 3.8 mg |

Source réelle : `reports/03/metrics_summary.json`. CO₂ = estimations CodeCarbon (non mesuré sur cette run).

- **Sélection** · score = F1 − 0.5×σ(F1_CV) · XGBoost meilleur score (0.880) ET meilleur F1 test (0.886).
- **Bonus déjà faits** · multiclass (type de panne) + régression (RUL) + calibration + tuning · ADR anti-data-leakage (pipeline sklearn fit sur train uniquement).
- **Dataset** · Kaggle industrial_machine_maintenance · 24 042 lignes · 15 variables · cible `failure_within_24h`.
- Repo · github.com/Adam-Blf/maintenance-predictive-industrielle · binôme Émilien ✓ (82 commits Adam / 13 Émilien)

### Projet 3 · L'IA Pero (Bloc 2 · C5.1 → C5.3)
- **Pitch** · « Moteur de recommandation de cocktails par IA sémantique · SBERT all-MiniLM-L6-v2 (embeddings 384 dims), similarité cosinus, guardrail sémantique seuil 0.35, RAG + Google Gemini avec cache MD5 pour limiter les appels API, interface Streamlit Speakeasy. »
- **Conformité sujet AISCA (thématique alternative acceptée)** · questionnaire hybride (texte libre + filtres) ✓ · référentiel structuré (cocktails.csv + known_ingredients.json) ✓ · scoring Top-5 cosinus ✓ · GenAI contrôlée (cache, appels limités, fallback) ✓ · radar chart ✓.
- **Preuves** · RAPPORT_FINAL.md (27 pages) · SOUTENANCE_SLIDES.md (12 slides) · tests guardrail · exemple refus hors-domaine (« réparer mon vélo » → similarité < 0.35 → refus).
- Repo · github.com/Adam-Blf/ia-pero · binôme **Amina Medjdoub** ⚠️

---

## 3. Mapping compétences → preuves (le cœur de la note)

Le guide insiste · relier EXPLICITEMENT chaque partie à la compétence. Formule type · « Cette partie démontre la compétence C1.3 car… »

### Bloc 1 (grille 29 critères × 5 pts = /145, convertie /20)

| Comp. | Preuve à montrer | Où |
|---|---|---|
| C1.1 relationnel | Schéma étoile, FK, index, contraintes + test de charge | `postgres/init.sql`, `scripts/test_load_postgres.py` |
| C1.2 NoSQL | Cassandra query-first, partition par event_type, TTL 7 j, 2 patterns d'accès | `cassandra/schema.cql` |
| C1.3 Data Lake | Bronze/Silver/Gold Parquet, partitionnement, métriques pipeline | `data/`, `etl/metrics.py`, `/pipeline/metrics` |
| C1.4 scalable/résilient | healthchecks, restart policies, depends_on healthy, test résilience | `docker-compose.yml`, `scripts/test_resilience.py` |
| C2.1 API | FastAPI Swagger, JWT rôles viewer/admin, quotas 120/600, 401/403/429 | `api/security.py`, démo curl |
| C2.2 streaming | Producteur/consommateur Kafka temps réel + **micro-batch** fenêtres 10 s | `streaming/producer.py`, `consumer.py`, `microbatch.py` |
| C2.3 transformations | Polars multi-sources, jointure spatiale IRIS, fusion DVF+INSEE réels | `etl/processing.py`, `etl/external.py` |
| C2.4 perf pipelines | Parquet colonnaire, index PG, lru_cache géocodage, métriques rows/sec | `etl/metrics.py`, bench PG |

### Bloc 2 · Data Science (1 pt par critère + rapport 2 pts + présentation 2 pts + méthodo collaborative 1 pt)

| Comp. | Preuve |
|---|---|
| C3.1 prépa données | Pipeline `src/preprocessing.py`, imputation, encodage, scaling fit-train-only |
| C3.2 dashboard | Streamlit · KPI, simulation scénario machine, prédiction temps réel, filtres |
| C3.3 EDA | `scripts/02_eda.py`, distributions, corrélations, déséquilibre de classes |
| C4.1 stratégie IA | Contexte métier · corrective 100 €/h → prédictive 20 €/h, roadmap d'intégration |
| C4.2 modèles ML | 4 modèles, hyperparamètres justifiés, code testé (pytest) |
| C4.3 éval comparative | Tableau métriques + **écoresponsabilité CodeCarbon** (explicitement dans le référentiel !) |

### Bloc 2 · IA générative

| Comp. | Preuve |
|---|---|
| C5.1 cas d'usage | Personas, scénarios, pourquoi la GenAI (texte libre → recette personnalisée) |
| C5.2 solution | SBERT local coût zéro + Gemini free-tier + cache + guardrail + Streamlit |
| C5.3 évaluation | Seuil de similarité testé, tableau requête/attendu/score, ajustement paramètres, limites |

---

## 4. Démos live (3 × ~90 s, scénarios préparés)

Consigne explicite des guides · entrées préparées À L'AVANCE + screenshots de backup + 1 cas alternatif.

1. **Urban Data Explorer** · ouvrir dashboard → choroplèthe prix m² → clic 11e arr. → mode comparaison 11e vs 16e → `/docs` Swagger → curl token JWT → 403 sans rôle admin.
2. **Maintenance** · dashboard Streamlit → simulation scénario (vibration haute + temp haute) → prédiction panne + probabilité → feature importance → comparatif 4 modèles.
3. **IA Pero** · requête « quelque chose de frais et fruité » → Top-5 + radar → requête hors-domaine (« répare mon vélo ») → refus guardrail → génération Gemini (ou cache si API lente).

Backup obligatoire · screenshots de chaque étape + courte vidéo enregistrée.

---

## 5. Checklist auto-évaluation (grille du guide · tout doit être OUI)

**Bloc 1** · base relationnelle adaptée ✓ · justification SQL/NoSQL ✓ · Data Lake ✓ · sécurité/accès ✓ · API ✓ · pipelines ✓ · perf/scalabilité/résilience ✓ · preuves techniques ✓
**Bloc 2 DS** · prépa expliquée ✓ · insights EDA ✓ · dashboard décisionnel ✓ · modèle prédictif ✓ · plusieurs modèles ✓ · justification modèle retenu ✓ · limites ✓ · stratégie d'intégration IA ✓
**Bloc 2 GenAI** · cas d'usage justifié ✓ · choix modèle justifié ✓ · solution fonctionnelle ✓ · qualité évaluée ✓ · ajustements expliqués ✓ · limites/risques ✓
**Individualisation** · chacun connaît sa contribution, 1 choix technique porté, ses compétences, les limites

## 6. Les 5 erreurs fatales (guide)

1. Présenter sans relier aux compétences → toujours citer le code C×.×.
2. Résultats sans justification → chaque choix a un « parce que ».
3. Oublier les limites → en donner à chaque projet (recul professionnel = points).
4. Démo trop longue → 90 s max chacune, scénarisée.
5. Individualisation non préparée → réponses personnelles, pas « on a fait ».
