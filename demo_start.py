#!/usr/bin/env python3
"""
Demo launcher - Soutenance M1 RNCP40875.

Telecharge (git clone / git pull) un projet depuis GitHub,
installe les dependances, puis lance l'application.

Ports (aucun conflit) :
    Urban Data Explorer  - API 8000  / front 5173
    Maintenance Predict. - API 8001  / Streamlit 8502
    L'IA Pero            - Streamlit 8503

Usage:
    python demo_start.py urban        # Urban Data Explorer
    python demo_start.py maintenance  # Maintenance Predictive
    python demo_start.py iapero       # L'IA Pero
    python demo_start.py all          # Lance les 3 en parallele

Sans argument : menu interactif.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

# --------------------------------------------------------------------------
# Configuration des 3 projets
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # dossier parent de soutenance-m1

PROJECTS = {
    "urban": {
        "name": "Urban Data Explorer",
        "repo": "https://github.com/Adam-Blf/urban-data-explorer",
        "dir": BASE_DIR / "urban-data-explorer",
        "requirements": "requirements.txt",
        "steps": "api+front",
        "api_cmd": [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000"],
        "front_cmd": ["npm", "run", "dev"],
        "front_dir": "frontend",
        "urls": ["http://127.0.0.1:8000/docs", "http://localhost:5173"],
        "port_check": 8000,
    },
    "maintenance": {
        "name": "Maintenance Predictive",
        "repo": "https://github.com/Adam-Blf/maintenance-predictive-industrielle",
        "dir": BASE_DIR / "maintenance-predictive-industrielle",
        "requirements": "requirements.txt",
        "steps": "python_app",
        "app_cmd": [sys.executable, "app.py"],
        # env vars lus par app.py : MPI_API_PORT + MPI_DASH_PORT
        "app_env": {"MPI_API_PORT": "8001", "MPI_DASH_PORT": "8502"},
        "urls": ["http://127.0.0.1:8001/docs", "http://localhost:8502"],
        "port_check": 8502,
    },
    "iapero": {
        "name": "L'IA Pero",
        "repo": "https://github.com/Adam-Blf/ia-pero",
        "dir": BASE_DIR / "ia-pero",
        "requirements": "requirements.txt",
        "steps": "streamlit",
        "app_cmd": [sys.executable, "-m", "streamlit", "run", "src/app.py",
                    "--server.port", "8503", "--server.headless", "true"],
        "urls": ["http://localhost:8503"],
        "port_check": 8503,
    },
}

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check)


def clone_or_pull(proj: dict) -> Path:
    """Git clone if not present, git pull if already cloned."""
    d: Path = proj["dir"]
    if (d / ".git").exists():
        print(f"  git pull  {d.name}...")
        run(["git", "pull", "--rebase"], cwd=d)
    else:
        print(f"  git clone {proj['repo']} -> {d}...")
        d.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", proj["repo"], str(d)])
    return d


def install_requirements(d: Path, req: str = "requirements.txt") -> None:
    req_path = d / req
    if req_path.exists():
        print(f"  pip install -r {req}...")
        run([sys.executable, "-m", "pip", "install", "-r", str(req_path), "-q"])
    else:
        print(f"  [warn] {req} not found, skipping pip install")


def wait_for_port(port: int, timeout: int = 30) -> bool:
    """Return True when port accepts connections."""
    import socket
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def open_urls(urls: list[str], delay: float = 0.6) -> None:
    for url in urls:
        webbrowser.open(url)
        time.sleep(delay)


# --------------------------------------------------------------------------
# Launch functions per project type
# --------------------------------------------------------------------------

def launch_urban(proj: dict) -> list[subprocess.Popen]:
    d: Path = proj["dir"]
    procs: list[subprocess.Popen] = []

    print("  Starting API (uvicorn port 8000)...")
    api = subprocess.Popen(proj["api_cmd"], cwd=d)
    procs.append(api)

    if wait_for_port(8000):
        print("  API ready.")
    else:
        print("  [warn] API did not respond within 30s")

    front_dir = d / proj["front_dir"]
    if front_dir.exists():
        # npm install if node_modules missing
        if not (front_dir / "node_modules").exists():
            print("  npm install...")
            subprocess.run(["npm", "install"], cwd=front_dir, check=True)
        print("  Starting frontend (vite port 5173)...")
        front = subprocess.Popen(["npm", "run", "dev"], cwd=front_dir)
        procs.append(front)
        time.sleep(3)

    open_urls(proj["urls"])
    return procs


def launch_python_app(proj: dict) -> list[subprocess.Popen]:
    """Projects with their own orchestrator app.py (maintenance)."""
    d: Path = proj["dir"]
    env = os.environ.copy()
    env.update(proj.get("app_env", {}))
    print(f"  Starting {proj['name']} (python app.py)...")
    print(f"  Ports: API {env.get('MPI_API_PORT', 8001)}  Streamlit {env.get('MPI_DASH_PORT', 8502)}")
    proc = subprocess.Popen(proj["app_cmd"], cwd=d, env=env)
    return [proc]


def launch_streamlit(proj: dict) -> list[subprocess.Popen]:
    d: Path = proj["dir"]
    print(f"  Starting {proj['name']} (Streamlit port {proj['port_check']})...")
    proc = subprocess.Popen(proj["app_cmd"], cwd=d)

    if wait_for_port(proj["port_check"]):
        print("  Streamlit ready.")
        open_urls(proj["urls"])
    else:
        print("  [warn] Streamlit did not respond within 30s")
        open_urls(proj["urls"])

    return [proc]


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

LAUNCH_FN = {
    "api+front": launch_urban,
    "python_app": launch_python_app,
    "streamlit": launch_streamlit,
}


def start(key: str) -> list[subprocess.Popen]:
    proj = PROJECTS[key]
    print(f"\n{'='*55}")
    print(f"  {proj['name']}")
    print(f"{'='*55}")

    d = clone_or_pull(proj)
    install_requirements(d, proj["requirements"])

    fn = LAUNCH_FN[proj["steps"]]
    return fn(proj)


def menu() -> str:
    print("\nSoutenance M1 · Demo Launcher\n")
    for i, (k, v) in enumerate(PROJECTS.items(), 1):
        print(f"  {i}. {v['name']}")
    print("  4. Tout lancer")
    choice = input("\nChoix [1-4]: ").strip()
    mapping = {"1": "urban", "2": "maintenance", "3": "iapero", "4": "all"}
    return mapping.get(choice, "all")


def main() -> int:
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else menu()

    if arg not in PROJECTS and arg != "all":
        print(f"[error] Unknown project '{arg}'. Use: urban | maintenance | iapero | all")
        return 1

    keys = list(PROJECTS.keys()) if arg == "all" else [arg]
    all_procs: list[subprocess.Popen] = []

    for k in keys:
        procs = start(k)
        all_procs.extend(procs)

    if not all_procs:
        return 0

    print("\nTous les processus sont demarres. Ctrl+C pour arreter.\n")
    try:
        while True:
            dead = [p for p in all_procs if p.poll() is not None]
            if dead:
                print(f"[warn] {len(dead)} processus termine(s) de maniere inattendue.")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nArret en cours...")
    finally:
        for p in all_procs:
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
