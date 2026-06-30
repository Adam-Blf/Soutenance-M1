#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lanceur demo · Urban Data Explorer (API FastAPI :8000 + front Vite :5173).
Avant de lancer : recupere la derniere version du repo GitHub (git pull main),
installe les dependances Python + npm, puis demarre l'API et le front et ouvre
le navigateur. Local-first. Conforme regle EDR : python/git/npm direct, pas de .bat/.ps1."""
import os
import sys
import time
import shutil
import webbrowser
import subprocess
import urllib.request

PROJ = r"C:\Users\adamb\urban-data-explorer"
FRONT = os.path.join(PROJ, "frontend")
API_PORT = 8000
FRONT_PORT = 5173
FRONT_URL = f"http://localhost:{FRONT_PORT}"
API_DOCS = f"http://localhost:{API_PORT}/docs"
DETACHED = 0x00000008

py = sys.executable.replace("pythonw.exe", "python.exe")
GIT = shutil.which("git") or "git"
npm = shutil.which("npm") or "npm.cmd"
_RUN = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def update_repo():
    """Pull main + install des dependances (best-effort, ne bloque jamais la demo)."""
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
    try:
        subprocess.run([npm, "install"], cwd=FRONT, timeout=300, shell=False, **_RUN)
    except Exception:
        pass


def up(url):
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except Exception:
        return False


def main():
    fresh = not (up(API_DOCS) and up(FRONT_URL))
    if fresh:
        update_repo()
    if not up(API_DOCS):
        subprocess.Popen(
            [py, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", str(API_PORT)],
            cwd=PROJ, creationflags=DETACHED, **_RUN,
        )
    if not up(FRONT_URL):
        subprocess.Popen(
            [npm, "run", "dev", "--", "--port", str(FRONT_PORT)],
            cwd=FRONT, creationflags=DETACHED, shell=False, **_RUN,
        )
    for _ in range(150):
        if up(FRONT_URL):
            break
        time.sleep(1)
    webbrowser.open(FRONT_URL)
    time.sleep(1)
    webbrowser.open(API_DOCS)


if __name__ == "__main__":
    main()
