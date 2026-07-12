# Soutenance M1 · Blocs 1-2 · EFREI

<!-- adam-badges:start -->
[![commits](https://img.shields.io/github/commit-activity/t/Adam-Blf/Soutenance-M1?color=001329&label=commits&style=flat-square)](https://github.com/Adam-Blf/Soutenance-M1/commits)
[![visites](https://hits.sh/github.com/Adam-Blf/Soutenance-M1.svg?style=flat-square&label=visites&color=001329)](https://hits.sh/github.com/Adam-Blf/Soutenance-M1/)
[![last commit](https://img.shields.io/github/last-commit/Adam-Blf/Soutenance-M1?color=D4A437&style=flat-square&label=dernier%20push)](https://github.com/Adam-Blf/Soutenance-M1/commits)
[![top language](https://img.shields.io/github/languages/top/Adam-Blf/Soutenance-M1?style=flat-square)](https://github.com/Adam-Blf/Soutenance-M1)
[![license](https://img.shields.io/github/license/Adam-Blf/Soutenance-M1?style=flat-square&color=D4A437)](LICENSE)
<!-- adam-badges:end -->

Supports de soutenance du M1 Mastère Data Engineering & IA (EFREI · RNCP 40875),
blocs de compétences 1 et 2. Binôme Adam Beloucif & Emilien Morice.

## Contenu

| Fichier | Rôle |
|---------|------|
| `Soutenance_Bloc1-2_Adam_Emilien_v2.pptx` | Deck de soutenance (version finale) |
| `SOUTENANCE.md` · `PLAN_SLIDES.md` | Script oral + plan détaillé des slides |
| `QA_JURY.md` · `QA_JURY_COMPLET.pdf` | Préparation questions / réponses jury |
| `Soutenance_IAPero_150Q.pdf` | 150 questions · projet IA Pero (NLP, similarité sémantique) |
| `Soutenance_MPI_150Q.pdf` | 150 questions · projet Maintenance Prédictive Industrielle |
| `Soutenance_UDE_150Q.pdf` | 150 questions · projet Urban Data Explorer |
| `.preview/` | Rendus HTML + PNG de chaque slide (s01 → s23) |

## Projets couverts

```mermaid
flowchart LR
    S["Soutenance Blocs 1-2"]
    P1["IA Pero<br/>NLP · Sentence-Transformers · Streamlit"]
    P2["Maintenance Prédictive Industrielle<br/>ML multi-modèles · scikit-learn"]
    P3["Urban Data Explorer<br/>data engineering · open data"]
    S --> P1
    S --> P2
    S --> P3
    P1 & P2 & P3 --> Q["3 × 150 questions jury<br/>+ QA complet PDF"]
```

Les dépôts de code correspondants ·
[ia-pero](https://github.com/Adam-Blf/ia-pero) ·
[maintenance-predictive-industrielle](https://github.com/Adam-Blf/maintenance-predictive-industrielle) ·
[urban-data-explorer](https://github.com/Adam-Blf/urban-data-explorer)

## Nature du dépôt

Dépôt de livrables (slides, scripts, préparation jury), pas de code applicatif.
Le code des projets vit dans les dépôts liés ci-dessus.
