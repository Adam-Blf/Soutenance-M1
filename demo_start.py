#!/usr/bin/env python3
"""
Demo launcher - Soutenance M1 RNCP40875.

Mode standalone (script pose n'importe ou) :
  - Clone automatiquement les 3 projets dans Bureau/soutenance-demo/
  - Installe pip + npm si besoin
  - Lance les apps et ouvre le navigateur

Mode repo (script dans soutenance-m1/) :
  - Fait git pull des repos adjacents (../urban-data-explorer etc.)

Ports (aucun conflit) :
    Urban Data Explorer  - API 8000 / front 5173
    Maintenance Predict. - API 8001 / Streamlit 8502
    L'IA Pero            - Streamlit 8503

Usage :
    python demo_start.py              # menu interactif
    python demo_start.py urban        # Urban Data Explorer
    python demo_start.py maintenance  # Maintenance Predictive
    python demo_start.py iapero       # L'IA Pero
    python demo_start.py all          # Les 3 en parallele
"""
from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

# ---------------------------------------------------------------------------
# Chemin de base des projets
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
_IS_REPO = (_SCRIPT_DIR / "scripts").exists() or (_SCRIPT_DIR / "assets").exists()

if _IS_REPO:
    BASE_DIR = _SCRIPT_DIR.parent          # mode repo : projets dans ../
else:
    # mode standalone : clone dans Bureau/soutenance-demo/
    _desktop = Path(os.environ.get("USERPROFILE", Path.home())) / "Desktop"
    BASE_DIR = _desktop / "soutenance-demo"

# ---------------------------------------------------------------------------
# Configuration des 3 projets
# ---------------------------------------------------------------------------
PROJECTS = {
    "urban": {
        "name":        "Urban Data Explorer",
        "repo":        "https://github.com/Adam-Blf/urban-data-explorer",
        "dir":         BASE_DIR / "urban-data-explorer",
        "requirements":"requirements.txt",
        "steps":       "api+front",
        "api_cmd":     [sys.executable, "-m", "uvicorn", "api.main:app",
                        "--host", "127.0.0.1", "--port", "8000"],
        "front_dir":   "frontend",
        "urls":        ["http://localhost:5173", "http://127.0.0.1:8000/docs"],
        "port_api":    8000,
        "port_front":  5173,
    },
    "maintenance": {
        "name":        "Maintenance Predictive",
        "repo":        "https://github.com/Adam-Blf/maintenance-predictive-industrielle",
        "dir":         BASE_DIR / "maintenance-predictive-industrielle",
        "requirements":"requirements.txt",
        "steps":       "python_app",
        "app_cmd":     [sys.executable, "app.py"],
        "app_env":     {"MPI_API_PORT": "8001", "MPI_DASH_PORT": "8502"},
        "urls":        ["http://localhost:8502", "http://127.0.0.1:8001/docs"],
        "port_check":  8502,
    },
    "iapero": {
        "name":        "L'IA Pero",
        "repo":        "https://github.com/Adam-Blf/ia-pero",
        "dir":         BASE_DIR / "ia-pero",
        "requirements":"requirements.txt",
        "steps":       "streamlit",
        "app_cmd":     [sys.executable, "-m", "streamlit", "run", "src/app.py",
                        "--server.port", "8503", "--server.headless", "true"],
        "urls":        ["http://localhost:8503"],
        "port_check":  8503,
    },
}

# ---------------------------------------------------------------------------
# Affichage
# ---------------------------------------------------------------------------
_W = 58

def _bar(label: str = "", char: str = "=") -> None:
    print(char * _W)
    if label:
        pad = (_W - len(label) - 2) // 2
        print(f"{' ' * pad} {label} {' ' * pad}")
        print(char * _W)


def _step(n: int, total: int, msg: str) -> None:
    print(f"  [{n}/{total}] {msg}")


def _ok(msg: str) -> None:
    print(f"  OK  {msg}")


def _warn(msg: str) -> None:
    print(f"  !!  {msg}")


def _spin(msg: str, secs: float) -> None:
    frames = ["-", "\\", "|", "/"]
    t0 = time.time()
    i = 0
    while time.time() - t0 < secs:
        print(f"\r  {frames[i % 4]}  {msg}   ", end="", flush=True)
        time.sleep(0.15)
        i += 1
    print(f"\r  {' ' * (len(msg) + 8)}\r", end="", flush=True)


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def _run(cmd: list[str], cwd: Path | None = None, env: dict | None = None,
         capture: bool = False) -> subprocess.CompletedProcess:
    kw: dict = dict(cwd=cwd, env=env)
    if capture:
        kw["capture_output"] = True
        kw["text"] = True
    return subprocess.run(cmd, check=True, **kw)


def _git_available() -> bool:
    return shutil.which("git") is not None


def _npm_available() -> bool:
    return shutil.which("npm") is not None


def clone_or_pull(proj: dict) -> Path:
    d: Path = proj["dir"]
    if not _git_available():
        _warn("git introuvable dans le PATH - impossible de telecharger le projet.")
        _warn("Installe Git : https://git-scm.com/download/win")
        raise RuntimeError("git manquant")

    if (d / ".git").exists():
        _step(1, 3, f"Mise a jour  {d.name}  (git pull)...")
        try:
            _run(["git", "pull", "--rebase", "--autostash"], cwd=d, capture=True)
            _ok("Depot a jour.")
        except subprocess.CalledProcessError:
            _warn("git pull a echoue - on continue avec la version locale.")
    else:
        print()
        print(f"  Dossier de destination : {d}")
        _step(1, 3, f"Telechargement  {proj['name']}  depuis GitHub...")
        print(f"  Repo : {proj['repo']}")
        d.parent.mkdir(parents=True, exist_ok=True)
        try:
            _run(["git", "clone", "--depth", "1", proj["repo"], str(d)])
            _ok(f"Telecharge dans  {d}")
        except subprocess.CalledProcessError as exc:
            _warn(f"git clone a echoue : {exc}")
            raise
    return d


def install_python_deps(d: Path, req: str = "requirements.txt") -> None:
    req_path = d / req
    if not req_path.exists():
        _warn(f"{req} absent, pip skipped.")
        return
    _step(2, 3, "Installation des dependances Python (pip)...")
    try:
        _run([sys.executable, "-m", "pip", "install", "-r", str(req_path), "-q"])
        _ok("Dependances Python OK.")
    except subprocess.CalledProcessError as exc:
        _warn(f"pip install a rencontre des erreurs : {exc}")


def install_npm_deps(front_dir: Path) -> None:
    if not _npm_available():
        _warn("npm introuvable - frontend ne pourra pas demarrer.")
        return
    if (front_dir / "node_modules").exists():
        return
    _step(3, 3, "Installation des dependances Node.js (npm install)...")
    try:
        _run(["npm", "install"], cwd=front_dir)
        _ok("Dependances Node OK.")
    except subprocess.CalledProcessError as exc:
        _warn(f"npm install a rencontre des erreurs : {exc}")


def wait_port(port: int, timeout: int = 45, label: str = "") -> bool:
    label = label or f"port {port}"
    deadline = time.time() + timeout
    printed = False
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                if printed:
                    print()
                return True
        except OSError:
            if not printed:
                print(f"  En attente de {label}", end="", flush=True)
                printed = True
            else:
                print(".", end="", flush=True)
            time.sleep(1)
    if printed:
        print()
    _warn(f"{label} n'a pas repondu dans {timeout}s - on ouvre quand meme.")
    return False


def open_urls(urls: list[str], delay: float = 0.7) -> None:
    for url in urls:
        print(f"  Ouverture : {url}")
        webbrowser.open(url)
        time.sleep(delay)


# ---------------------------------------------------------------------------
# Launchers
# ---------------------------------------------------------------------------

def launch_urban(proj: dict) -> list[subprocess.Popen]:
    d: Path = proj["dir"]
    procs: list[subprocess.Popen] = []

    _step(3, 3, "Lancement de l'API FastAPI (port 8000)...")
    api = subprocess.Popen(proj["api_cmd"], cwd=d,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(api)
    wait_port(proj["port_api"], label="API Urban (8000)")

    front_dir = d / proj["front_dir"]
    if front_dir.exists():
        install_npm_deps(front_dir)
        print("  Lancement du frontend Vite (port 5173)...")
        front = subprocess.Popen(
            ["npm", "run", "dev"], cwd=front_dir,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        procs.append(front)
        wait_port(proj["port_front"], timeout=30, label="Frontend Vite (5173)")
    else:
        _warn("Dossier frontend/ absent.")

    open_urls(proj["urls"])
    return procs


def launch_python_app(proj: dict) -> list[subprocess.Popen]:
    d: Path = proj["dir"]
    env = os.environ.copy()
    env.update(proj.get("app_env", {}))
    port = proj["port_check"]
    _step(3, 3, f"Lancement de {proj['name']} (python app.py)...")
    proc = subprocess.Popen(proj["app_cmd"], cwd=d, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_port(port, timeout=45, label=f"{proj['name']} ({port})")
    open_urls(proj["urls"])
    return [proc]


def launch_streamlit(proj: dict) -> list[subprocess.Popen]:
    d: Path = proj["dir"]
    port = proj["port_check"]
    _step(3, 3, f"Lancement de {proj['name']} (Streamlit port {port})...")
    proc = subprocess.Popen(proj["app_cmd"], cwd=d,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_port(port, timeout=45, label=f"Streamlit ({port})")
    open_urls(proj["urls"])
    return [proc]


LAUNCH_FN = {
    "api+front": launch_urban,
    "python_app": launch_python_app,
    "streamlit":  launch_streamlit,
}

# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def start(key: str) -> list[subprocess.Popen]:
    proj = PROJECTS[key]
    _bar(proj["name"])
    try:
        d = clone_or_pull(proj)
        install_python_deps(d, proj["requirements"])
        return LAUNCH_FN[proj["steps"]](proj)
    except RuntimeError as exc:
        _warn(str(exc))
        return []
    except subprocess.CalledProcessError as exc:
        _warn(f"Erreur : {exc}")
        return []


def menu() -> str:
    _bar("SOUTENANCE M1 - Demo Launcher")
    print()
    if not _IS_REPO:
        print(f"  Dossier de destination : {BASE_DIR}")
        print()
    for i, (k, v) in enumerate(PROJECTS.items(), 1):
        d = v["dir"]
        status = "telecharge" if (d / ".git").exists() else "a telecharger"
        print(f"  {i}.  {v['name']:<35}  [{status}]")
    print(f"  4.  Lancer les 3 projets")
    print()
    choice = input("Choix [1-4] : ").strip()
    return {"1": "urban", "2": "maintenance", "3": "iapero", "4": "all"}.get(choice, "all")


def main() -> int:
    # Affiche le dossier de destination au demarrage en mode standalone
    if not _IS_REPO:
        print()
        _bar("SOUTENANCE M1 - Demo Launcher")
        print(f"  Projets : {BASE_DIR}")
        print()

    arg = sys.argv[1].lower() if len(sys.argv) > 1 else menu()

    if arg not in PROJECTS and arg != "all":
        _warn(f"Argument inconnu '{arg}'. Utilise : urban | maintenance | iapero | all")
        return 1

    keys = list(PROJECTS.keys()) if arg == "all" else [arg]
    all_procs: list[subprocess.Popen] = []

    for k in keys:
        procs = start(k)
        all_procs.extend(procs)

    if not all_procs:
        return 0

    _bar()
    print("  Toutes les apps tournent. Ctrl+C pour tout arreter.")
    _bar()

    try:
        while True:
            dead = [p for p in all_procs if p.poll() is not None]
            if dead:
                _warn(f"{len(dead)} processus termine(s) de facon inattendue.")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n  Arret en cours...")
    finally:
        for p in all_procs:
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill()
    print("  Termine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
