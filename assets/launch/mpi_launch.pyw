"""
Lanceur DEMO - Maintenance Predictive Industrielle
Clique depuis le PowerPoint de soutenance.
"""
import ctypes, subprocess, sys
from pathlib import Path

MPI = Path(r"C:\Users\adamb\maintenance-predictive-industrielle")

ctypes.windll.user32.MessageBoxW(
    0,
    "Maintenance Predictive va demarrer.\n\n"
    "  1. Une fenetre de chargement va s'ouvrir\n"
    "  2. Patience ~20 secondes\n"
    "  3. Le dashboard et l'API s'ouvrent automatiquement\n\n"
    "Cliquez OK pour lancer.",
    "DEMO - Maintenance Predictive",
    0x40
)

subprocess.Popen(
    [sys.executable, str(MPI / "app.py")],
    cwd=str(MPI),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
