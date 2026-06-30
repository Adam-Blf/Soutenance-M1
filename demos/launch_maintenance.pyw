#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lanceur demo · Maintenance Predictive (dashboard Streamlit, port 8501).
Avant de lancer : recupere la derniere version du repo GitHub (git pull main)
puis installe les dependances, puis demarre l'app et ouvre le navigateur.
Conforme regle EDR : python.exe / git direct, aucun .bat/.ps1."""
import os
import sys
import time
import shutil
import webbrowser
import subprocess
import urllib.request

PROJ = r"C:\Users\adamb\maintenance-predictive-industrielle"
APP = os.path.join(PROJ, "dashboard", "app.py")
PORT = 8501
URL = f"http://localhost:{PORT}"
DETACHED = 0x00000008  # DETACHED_PROCESS

py = sys.executable.replace("pythonw.exe", "python.exe")
GIT = shutil.which("git") or "git"
_RUN = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def update_repo():
    """Recupere la derniere version de main (best-effort, ne bloque jamais la demo)."""
    for args, t in (
        (["fetch", "origin", "main"], 90),
        (["checkout", "main"], 30),
        (["pull", "--ff-only", "origin", "main"], 90),
    ):
        try:
            subprocess.run([GIT, "-C", PROJ, *args], timeout=t, **_RUN)
        except Exception:
            pass
    try:
        subprocess.run([py, "-m", "pip", "install", "-q", "-r",
                        os.path.join(PROJ, "requirements.txt")], timeout=300, **_RUN)
    except Exception:
        pass


def already_up():
    try:
        urllib.request.urlopen(URL, timeout=1)
        return True
    except Exception:
        return False


def main():
    if not already_up():
        update_repo()
        subprocess.Popen(
            [py, "-m", "streamlit", "run", APP,
             "--server.port", str(PORT), "--server.headless", "true"],
            cwd=PROJ, creationflags=DETACHED, **_RUN,
        )
        for _ in range(120):
            if already_up():
                break
            time.sleep(1)
    webbrowser.open(URL)


if __name__ == "__main__":
    main()
