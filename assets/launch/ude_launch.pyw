"""
Lanceur DEMO - Urban Data Explorer
Clique depuis le PowerPoint de soutenance.
"""
import ctypes, subprocess, sys
from pathlib import Path

UDE = Path(r"C:\Users\adamb\urban-data-explorer")

# Boite de dialogue claire pour n'importe qui
ctypes.windll.user32.MessageBoxW(
    0,
    "Urban Data Explorer va demarrer.\n\n"
    "  1. Une fenetre de chargement va s'ouvrir\n"
    "  2. Patience ~20 secondes\n"
    "  3. Les onglets navigateur s'ouvrent automatiquement\n\n"
    "Cliquez OK pour lancer.",
    "DEMO - Urban Data Explorer",
    0x40  # Icone Information
)

subprocess.Popen(
    [sys.executable, str(UDE / "lancer_soutenance.py"), "--api-seulement"],
    cwd=str(UDE),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
