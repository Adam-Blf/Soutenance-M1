# Actions avant soutenance · état au 2026-06-13

## ✅ Fait le 2026-06-13

- **P0 #1 · branche `feat/bloc1-hardening` mergée** · 6 commits granulaires → PR #3 squash → `main`. 102 tests pytest verts revérifiés, `npm run build` OK.
- **P0 #2 · frontend** · les modifs non commitées contenaient déjà popup hover carte, replay timeline, fixes WCAG (`aria-pressed`, `inert`, contraste) · incluses dans PR #3. Reste seulement le lazy-load Mapbox / retrait deps mortes (bundle ~1.8 MB mapbox-gl, warning non bloquant).
- **P0 #3 · README** · PR #4 · badge auto-décerné « Conforme 20/20 » retiré, liens `file:///` morts → relatifs, claim Spark retiré de la commande compose (aucun service spark câblé), badge version 1.1.0 → 1.2.0. (Mismatch PostgreSQL déjà inexistant.)

## ✅ Fait le 2026-06-13 (suite)

- **PPTX 20 slides + 3 annexes généré** · `Soutenance_Bloc1-2_Adam_Emilien.pptx` (aussi dans `Documents/`). Produit via le skill `pptx-official` (html2pptx + PptxGenJS, rendu Playwright). **DA EFREI** (bleu #163767, rose #FF43B8, navy #051832, bleu logo #0C78B4 extraits de efrei.fr). Français accentué impeccable. Images placées en aspect-fit optimisé.
- **Boutons cliquables qui LANCENT les démos** · hyperliens `file://` → `demos/launch_*.pyw` (3 lanceurs Python, conformes EDR, ports 8501/8502/5173+8000). Plus boutons repos GitHub. Doc · `demos/README.md`.
- **Binôme Émilien Morice affiché sur les 3 projets** (ia-pero inclus, plus aucune mention Amina dans le PPTX).
- Générateur reproductible · `build_deck.js` (+ `preview.js` pour QA visuelle Playwright).

## P0 restant · bloquant pour la démo

4. **Hébergement `urban.beloucif.com`** (demande Adam) · déploiement Vercel du frontend + DNS OVH · API sur Render (render.yaml prêt). ⚠️ DNS OVH = action manuelle d'Adam.

---

## Archive · état initial au 2026-06-12

1. **urban-data-explorer · merger la branche `feat/bloc1-hardening`** (en local, non commitée).
   Contenu déjà implémenté et vérifié (102 tests pytest verts) ·
   - Fix critique JWT · le secret env (`UDE_JWT_SECRET`) n'était jamais lu (mismatch `.env.example`)
   - Fix bypass quota (n'importe quel header Authorization donnait le tier 600 req·min)
   - Fix pipeline PG cassé (mismatch colonnes COPY · le schéma étoile n'était jamais peuplé)
   - Fix données DVF/INSEE réelles écrasées par des constantes à la lecture (le « réel » n'atteignait jamais l'API)
   - Migration python-jose (CVE) → PyJWT · suppression dep morte scrapling
   - Nouveau · `streaming/microbatch.py` (C2.2 micro-batch), `etl/metrics.py` + `GET /pipeline/metrics` (C2.4), `scripts/test_resilience.py` (C1.4), 2e table Cassandra query-first (C1.2)
   - Suite pytest complète `tests/` (étape suivante · commits granulaires + PR + merge)
2. **Frontend urban-data-explorer · vague interrompue, à relancer** · popup hover sur la carte (exigence du brief, absente), replay timeline animé (exigence, absente), fixes WCAG (aria-pressed, inert, contraste légende), retrait deps mortes (~2 MB bundle), lazy-load Mapbox.
3. **README urban-data-explorer** · 3 liens `file:///c:/Users/adamb/...` morts sur GitHub (L187-188) · badge « Conforme 20/20 » auto-décerné à retirer (risqué devant jury) · claim Spark dans le profil Docker alors qu'aucun service spark n'est câblé · mention « PostgreSQL 15 » vs postgres:16.
4. **Hébergement `urban.beloucif.com`** (demande Adam) · déploiement Vercel du frontend + DNS OVH · API sur Render (render.yaml prêt). À faire après merge.

## P1 · qualité soutenance

5. **Clarifier le binôme ia-pero** · README dit Adam + Amina Medjdoub, Émilien n'a aucun commit. Demander au tuteur comment présenter le projet GenAI si le groupe de soutenance est Adam+Émilien.
6. **Préparer les démos scénarisées** + screenshots backup + vidéo courte (consigne explicite des 3 guides).
7. **Générer le PPTX 20 slides** selon PLAN_SLIDES.md · logos EFREI fournis dans `assets/` (**Logo-Efrei-CMJN.png = principal**, Noir/Blanc selon fond de slide).
8. **Caler la répartition orale avec Émilien** · timings du SOUTENANCE.md + ses réponses d'individualisation (QA_JURY.md section finale).
9. **Vérifier que les 3 repos tournent from scratch** sur la machine de démo (clone → install → run), réseau école compris (prévoir hotspot).

## P2 · bonus points

10. maintenance-predictive · le tableau de métriques du README est marqué « (exemple) » · regénérer les vrais chiffres via `scripts/03_train_models.py` et figer le tableau (le jury peut vérifier).
11. urban-data-explorer · CI GitHub Actions (pytest + build Vite) · gros plus « maturité pro » en soutenance.
12. Imprimer la grille d'évaluation Bloc 1 (29 critères /145) et la grille Bloc 2 (1 pt/critère + 2+2+1) · s'auto-noter à blanc une semaine avant.
