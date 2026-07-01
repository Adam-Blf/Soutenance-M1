"""
Lanceur DEMO - L'IA Pero (MixCraft)
Clique depuis le PowerPoint de soutenance.
"""
import ctypes, subprocess, sys, time, webbrowser
from pathlib import Path

IAPERO = Path(r"C:\Users\adamb\cocktail-ia-generatif")

ctypes.windll.user32.MessageBoxW(
    0,
    "L'IA Pero (MixCraft) va demarrer.\n\n"
    "  1. Une fenetre de chargement va s'ouvrir\n"
    "  2. Patience ~15 secondes\n"
    "  3. L'application s'ouvre automatiquement\n\n"
    "Cliquez OK pour lancer.",
    "DEMO - L'IA Pero",
    0x40
)

proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run",
     str(IAPERO / "app" / "app.py"),
     "--server.port", "8503",
     "--server.headless", "true"],
    cwd=str(IAPERO),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)

# Attendre le demarrage puis ouvrir le navigateur
time.sleep(6)
webbrowser.open_new_tab("http://localhost:8503")
