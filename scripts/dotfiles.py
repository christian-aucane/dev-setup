#!/usr/bin/env python3

from pathlib import Path
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
    for entry in links:
        src = REPO_ROOT / entry["src"]
        dest = Path(entry["dest"]).expanduser()
        if not src.exists():
            log(f"[ERROR] source doesn't exist: '{src}'", file=sys.stderr)
            return EXIT_ERROR
        if dest.exists() or dest.is_symlink():
            if dest.is_symlink() and dest.resolve() == src.resolve():
                log(f"[OK] '{dest}' already linked")
                continue
        if not ask_confirmation(f"{dest} exists. Backup and replace?")
            log(f"[SKIP] '{src}'")
            continue



    ...


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
    if not config_path.exists():
        print(f"Config not found: {config_path}", file=sys.stderr)
        return EXIT_ERROR
    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)
    return dispatch(args, config)
    ...


if __name__ == "__main__":
    sys.exit(run())
