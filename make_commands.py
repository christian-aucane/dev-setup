#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import yaml
import argparse
import sys
import shutil
import subprocess


SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT = SCRIPTS_DIR
CONFIG_PATH = REPO_ROOT / "config.yaml"

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


def install_fonts(fonts_config):
    log("[INSTALL] fonts")
    src = REPO_ROOT / fonts_config["src_dir"]
    dest = Path(fonts_config["dest_dir"]).expanduser()

    dest.mkdir(parents=True, exist_ok=True)

    for font in src.glob("*.ttf"):
        shutil.copy2(font, dest)

    subprocess.run(["fc-cache", "-fv"])
    log("[OK] fonts successfully installed !")


def install_nvim(nvim_config):
    log("[INSTALL] nvim")
    link(nvim_config["link"])
    log("[INSTALL] Python dependencies")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", *nvim_config["pip_packages"]],
        check=True,
    )
    log("[OK] nvim successfully installed !")


def install(config):
    log("[INSTALL] full setup")
    if link(config["link"]) == EXIT_ERROR:
        return EXIT_ERROR
    install_fonts(config["install"]["fonts"])
    install_nvim(config["install"]["nvim"])
    log("[OK] full setup successfully installed !")
    return EXIT_SUCCESS


def update():
    ...


def check():
    ...


def uninstall():
    ...


def dispatch(args, config):
    commands_mapping = {
        "link": lambda: link(config["link"]),
        "install": lambda: install(config),
    }
    try:
        return commands_mapping[args.command]()
    except KeyError:
        log(f"[ERROR] '{args.command}' is not valid !")
        return EXIT_ERROR



def parse_args():
    parser = argparse.ArgumentParser(description="Manage setup commands")
    parser.add_argument(
        "command",
        choices=["link", "install", "update", "check", "uninstall"],
        help="The command to execute"
    )
    args = parser.parse_args(sys.argv[1:])
    return args


def run():
    args = parse_args()
    if not CONFIG_PATH.exists():
        log(f"Config not found: {CONFIG_PATH}", file=sys.stderr)
        return EXIT_ERROR
    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)
    return dispatch(args, config)
    ...


if __name__ == "__main__":
    sys.exit(run())
