# Plan des 20 slides · soutenance Bloc 1 & 2

Structure imposée par le guide (slide 1-4 intro, 5-9 P1, 10-14 P2, 15-17 P3, 18-20 conclusion).
Charte conseillée · sobre, DSFR-like (cohérent avec Urban Data Explorer), 1 idée par slide, codes compétences C×.× visibles sur chaque slide projet.

| # | Titre | Contenu | Durée |
|---|---|---|---|
| 1 | Titre | Soutenance Bloc 1 & 2 · RNCP40875 · Adam Beloucif & Émilien Morice · M1 DE&IA EFREI · 2026-2027 | 15 s |
| 2 | Contexte & problématique | Fil rouge · « de la donnée brute à la décision » · 3 projets = 3 maillons · data engineering → data science → GenAI | 45 s |
| 3 | Vue d'ensemble des 3 projets | 3 cartes · Urban Data Explorer (Bloc 1) / Maintenance Prédictive (C3-C4) / IA Pero (C5) + stack logos | 30 s |
| 4 | Contributions individuelles | Tableau Adam / Émilien par projet · qui a porté quoi | 30 s |
| 5 | P1 · Besoin & architecture | Besoin · explorer le logement parisien multi-sources · schéma médaillon Bronze/Silver/Gold → PG/Cassandra → API → front (mermaid du README) | 2 min |
| 6 | P1 · Bases de données (C1.1, C1.2) | Schéma étoile PG (FK, index, test de charge p95) vs Cassandra query-first (partition, TTL) · justification SQL/NoSQL côte à côte | 2 min |
| 7 | P1 · Data Lake & streaming (C1.3, C2.2) | 24 sources · Parquet partitionné · Kafka producteur/consommateur temps réel + micro-batch 10 s | 1.5 min |
| 8 | P1 · API & sécurité (C2.1) + DEMO | JWT rôles, quotas 120/600, 429 · **démo live 90 s** · dashboard carto + Swagger + curl 403 | 2 min |
| 9 | P1 · Perf, résilience, limites (C1.4, C2.4) | Métriques pipeline rows/sec · test résilience kill-Postgres · limites · mono-nœud, pas de HA réelle → roadmap cluster | 1.5 min |
| 10 | P2 · Question métier (C4.1) | Panne non planifiée 5-50 k€/h · corrective vs préventive vs prédictive · cible · prédire la panne sous 24 h · stratégie d'intégration IA | 1.5 min |
| 11 | P2 · Données & EDA (C3.1, C3.3) | Dataset Kaggle 24 042×15 · avant/après nettoyage · distributions, corrélations, déséquilibre de classes · insights (vibration/température ↔ panne) | 2 min |
| 12 | P2 · Modèles & comparaison (C4.2, C4.3) | Tableau 4 modèles (F1, ROC-AUC, temps, **CO₂ CodeCarbon**) · score sélection F1 − 0.5σ · XGBoost retenu · anti-leakage | 2 min |
| 13 | P2 · Interprétabilité + DEMO (C3.2) | Feature importance / permutation · **démo Streamlit 90 s** · simulation scénario → prédiction temps réel → explication | 2 min |
| 14 | P2 · Limites | Données simulées · pas de temporel (LSTM en piste) · dérive → monitoring · bonus réalisés (multiclass, RUL, calibration) | 1 min |
| 15 | P3 · Cas d'usage & archi (C5.1) | Reco cocktails en langage naturel · pourquoi GenAI · pipeline questionnaire → SBERT → cosinus → guardrail → cache → Gemini (RAG) | 2 min |
| 16 | P3 · Solution + DEMO (C5.2) | **Démo 90 s** · requête libre → Top-5 + radar → hors-domaine refusé → génération · contraintes free-tier · cache MD5 · 1 appel par génération | 2 min |
| 17 | P3 · Évaluation & risques (C5.3) | Seuil 0.35 testé · tableau requête/score/décision · ajustements (seuil, prompt, température) · risques · hallucination, dépendance API, biais | 2 min |
| 18 | Synthèse compétences | Matrice C1.1→C5.3 × 3 projets, toutes cases vertes avec la preuve en un mot | 1.5 min |
| 19 | Limites & améliorations transverses | HA réelle, LSTM temporel, DB vectorielle, monitoring/dérive, CI/CD complet | 1 min |
| 20 | Conclusion & apprentissages | Ce qu'on referait · tests dès J1, métriques dès J1 · posture · justifier chaque choix · merci + repos GitHub QR codes | 1.5 min |

**Total parlé ≈ 29 min** · marge 1 min.

## Règles de production
- Chaque slide projet porte le badge de compétence (ex. « C2.1 · API sécurisée ») · le jury coche sa grille en vous écoutant.
- Aucun bloc de code sauf snippet ≤ 5 lignes lisible de loin.
- Démos · onglets pré-ouverts, données pré-chargées, screenshots de secours dans les slides annexes (21+, hors décompte, non présentées sauf panne).
- Générer le PPTX · réutiliser `scripts/generate_slides_pptx.py` (urban-data-explorer) comme base de générateur ou `scripts/11_build_pptx.py` (maintenance).
