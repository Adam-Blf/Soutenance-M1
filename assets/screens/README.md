# Screenshots · captures live du 2026-06-12 (Playwright, 1600×900)

## Urban Data Explorer (Bloc 1) · slides 5-9
- `urban-dashboard-live.png` · vue d'ensemble DSFR · choroplèthe + panneaux
- `urban-district-selected.png` · sélection + indicateurs panel droit
- `ude-light.png` / `ude-dark.png` · thèmes clair/sombre (repo)
- `ude-api.png` · Swagger UI (repo)
- `correlation_matrix.png`, `monthly_trends.png`, `quality_completeness.png`, `geocoding_integrity.png`, `infrastructures_stacked_bar.png` · EDA notebooks (annexes)

## Maintenance Prédictive (Bloc 2 DS) · slides 10-14
- `maintenance-dashboard-live.png` · état du parc · KPI temps réel + machines prioritaires
- `maintenance-diagnostic-live.png` · onglet Diagnostic · sliders capteurs → décision recommandée (LA démo C3.2)

## L'IA Pero (Bloc 2 GenAI) · slides 15-17
- `iapero-similarity-live.png` · matrice de similarité SBERT 4 textes + légende (preuve C5.3 · chat/félin 0.59 vs hors-sujet 0.32)
- `iapero-speakeasy-live.png` · interface Speakeasy (questionnaire + budget)
- `iapero-recommendation-live.png` / `iapero-recommendation-full.png` · génération "Le Secret du Speakeasy" en 3.6 s

Apps relançables ·
- urban · `python -m uvicorn api.main:app --port 8000` + `cd frontend && npx vite`
- maintenance · `python -m streamlit run dashboard/app.py` (modèles entraînés présents dans `models/`)
- ia-pero · `python -m streamlit run src/app.py` (Speakeasy) ou `app.py` (explorateur similarité)
