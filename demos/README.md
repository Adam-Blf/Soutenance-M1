# Boutons de démo · soutenance Bloc 1 & 2

Chaque slide projet du PPTX (`Soutenance_Bloc1-2_Adam_Emilien.pptx`) porte un bouton
**« ▶ Lancer la démo »**. Cliquer dessus exécute le projet en local et ouvre le
navigateur sur la bonne URL.

| Bouton | Lanceur | App démarrée | URL |
|---|---|---|---|
| Urban Data Explorer | `launch_urban.pyw` | API FastAPI + front Vite | http://localhost:5173 + http://localhost:8000/docs |
| Maintenance Prédictive | `launch_maintenance.pyw` | Dashboard Streamlit | http://localhost:8501 |
| L'IA Pero | `launch_iapero.pyw` | Streamlit Speakeasy | http://localhost:8502 |

## Première utilisation

1. **Avertissement PowerPoint** · au premier clic, Office affiche un avertissement de
   sécurité (lien vers un fichier local). Cliquer **Oui / Activer** pour autoriser.
2. **Association `.pyw`** · les lanceurs sont des fichiers Python (`pythonw.exe`).
   Vérifier qu'un double-clic sur un `.pyw` lance bien Python.
3. **Dépendances** · une fois par projet, installer les libs :
   `pip install -r requirements.txt` dans chaque repo.

Maintenance (8501) et IA Pero (8502) tournent sur des ports distincts : les deux
peuvent être lancés en même temps. Les lanceurs détectent si l'app tourne déjà et se
contentent d'ouvrir le navigateur (pas de double démarrage).

## Repli si un bouton ne réagit pas

Lancer manuellement (aucun `.bat`/`.ps1`, conforme EDR) :

```
python demos\launch_maintenance.pyw
python demos\launch_iapero.pyw
python demos\launch_urban.pyw
```

Ou directement :

```
python -m streamlit run C:\Users\adamb\maintenance-predictive-industrielle\dashboard\app.py --server.port 8501
python -m streamlit run C:\Users\adamb\ia-pero\src\app.py --server.port 8502
python -m uvicorn api.main:app --port 8000   (depuis urban-data-explorer)
```

## Conseil soutenance

Pré-lancer les 3 démos **avant** de passer en mode présentation (onglets prêts), et
garder les boutons comme filet de sécurité. Slides d'annexe 21-23 = screenshots de
backup si le réseau école coupe.
