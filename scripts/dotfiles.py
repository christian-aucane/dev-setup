#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import yaml
import argparse
import sys


SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT = SCRIPTS_DIR.parent
CONFIG_PATH = SCRIPTS_DIR / "config.yaml"

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def log(message, *args, **kwargs):
    print(message, *args, **kwargs)


def ask_confirmation(message: str) -> bool:
    answer = input(f"{message} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def link(links_config):

    for entry in links_config:
        src = REPO_ROOT / entry["src"]
        dest = Path(entry["dest"]).expanduser()
        print(f"process {src} > {dest}")

        if not src.exists():
            log(f"[ERROR] source doesn't exist: '{src}'", file=sys.stderr)
            return EXIT_ERROR

        dest.parent.mkdir(parents=True, exist_ok=True)

        # Si le symlink existe ET est correct, rien à faire
        if dest.is_symlink() and dest.resolve() == src.resolve():
            log(f"[OK] '{dest}' already linked")
            continue

        # Sinon, si le fichier/symlink existe, backup ou supprimer
        if dest.exists() or dest.is_symlink():
            if not ask_confirmation(f"{dest} exists. Backup and replace?"):
                log(f"[SKIP] '{dest}'")
                continue

            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup = dest.with_name(dest.name + f".backup_{now_str}")

            if dest.is_symlink() or dest.is_file():
                dest.unlink()  # supprime symlink ou fichier
            else:
                dest.rename(backup)  # pour dossier, si jamais

            log(f"[BACKUP] {dest} -> {backup}")

        # ✅ Créer le symlink après backup
        dest.symlink_to(src)
        log(f"[LINK] {dest} -> {src}")

    return EXIT_SUCCESS
def install():
    ...


def update():
    ...


def check():
    ...

def parse_args():
    args = sys.argv
    return args


def dispatch(args, config):
    return link(config.get("links", []))

    return link(config)

def run():
    args = parse_args()
    if not CONFIG_PATH.exists():
        print(f"Config not found: {config_path}", file=sys.stderr)
        return EXIT_ERROR
    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)
    return dispatch(args, config)
    ...


if __name__ == "__main__":
    sys.exit(run())
