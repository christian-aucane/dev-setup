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


def install_pip_packages(packages):
    log("[INSTALL] Python dependencies")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--user",
            *packages,
        ],
        check=True,
    )
    log("[OK] Python dependencies successfully installed !")


def install(config):
    log("[INSTALL] full setup")
    if link(config["link"]) == EXIT_ERROR:
        return EXIT_ERROR
    install_fonts(config["fonts"])
    install_pip_packages(config["pip_packages"])
    log("[OK] full setup successfully installed !")
    return EXIT_SUCCESS


def git_pull():
    log("[UPDATE] git pull")
    subprocess.run(
        ["git", "-C", str(REPO_ROOT), "pull", "--rebase"],
        check=True,
    )


def update_nvim():
    log("[UPDATE] nvim")
    subprocess.run(
        [
            "nvim",
            "--headless",
            "+Lazy! sync",
            "+MasonUpdate",
            "+TSUpdate",
            "+qa",
        ],
        check=True,
    )


def update(config):
    log("[UPDATE] full setup")

    git_pull()

    if link(config["link"]) == EXIT_ERROR:
        return EXIT_ERROR

    update_nvim()

    log("[OK] update finished")
    return EXIT_SUCCESS


def check_repo():
    log("[CHECK] repo")

    if not (REPO_ROOT / ".git").exists():
        log("[ERROR] not a git repository")
        return EXIT_ERROR

    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        log("[WARN] repo has uncommitted changes")
    else:
        log("[OK] repo clean")

    return EXIT_SUCCESS


def check_links(links_config):
    log("[CHECK] links")
    status = EXIT_SUCCESS

    for entry in links_config:
        src = (REPO_ROOT / entry["src"]).resolve()
        dest = Path(entry["dest"]).expanduser()

        if not src.exists():
            log(f"[ERROR] source missing: {src}")
            status = EXIT_ERROR
            continue

        if not dest.exists():
            log(f"[MISSING] {dest}")
            status = EXIT_ERROR
            continue

        if not dest.is_symlink():
            log(f"[WRONG] {dest} is not a symlink")
            status = EXIT_ERROR
            continue

        if dest.resolve() != src:
            log(f"[WRONG] {dest} -> {dest.resolve()}")
            status = EXIT_ERROR
            continue

        log(f"[OK] {dest}")

    return status


def check_pip_packages(packages):
    log("[CHECK] pip packages")
    status = EXIT_SUCCESS

    for pkg in packages:
        result = subprocess.run(
            ["python3", "-m", "pip", "show", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            log(f"[MISSING] {pkg}")
            status = EXIT_ERROR
        else:
            log(f"[OK] {pkg}")

    return status


def check_nvim():
    log("[CHECK] nvim")

    if not shutil.which("nvim"):
        log("[ERROR] nvim not found")
        return EXIT_ERROR

    log("[OK] nvim found")

    return EXIT_SUCCESS


def check_fonts(fonts_config):
    log("[CHECK] fonts")

    dest = Path(fonts_config["dest_dir"]).expanduser()

    if not dest.exists():
        log(f"[ERROR] fonts dir missing: {dest}")
        return EXIT_ERROR

    fonts = list(dest.glob("*.ttf"))
    if not fonts:
        log("[WARN] no fonts found")
        return EXIT_ERROR

    log(f"[OK] {len(fonts)} fonts installed")
    return EXIT_SUCCESS


def check_zsh():
    log("[CHECK] zsh")

    if not shutil.which("zsh"):
        log("[ERROR] zsh not found")
        return EXIT_ERROR
    log("[OK] zsh found")

    env_file = REPO_ROOT / "zsh" / "env.zsh"

    if env_file.exists():
        log("[OK] env.zsh present")
    else:
        log("[INFO] env.zsh not found (optional)")

    return EXIT_SUCCESS


def check(config):
    status = EXIT_SUCCESS

    status |= check_repo()
    status |= check_links(config["link"])
    status |= check_fonts(config["fonts"])
    status |= check_pip_packages(config["pip_packages"])
    status |= check_nvim()
    status |= check_zsh()

    if status == EXIT_SUCCESS:
        log("[OK] all checks passed")
    else:
        log("[WARN] some checks failed")

    return status

    def uninstall(): ...


def dispatch(args, config):
    commands_mapping = {
        "link": lambda: link(config["link"]),
        "install": lambda: install(config),
        "update": lambda: update(config),
        "check": lambda: check(config),
    }
    command = args.command
    if command not in commands_mapping:
        log(f"[ERROR] '{args.command}' is not valid !")
        return EXIT_ERROR
    return commands_mapping[args.command]()


def parse_args():
    parser = argparse.ArgumentParser(description="Manage setup commands")
    parser.add_argument(
        "command",
        choices=["link", "install", "update", "check", "uninstall"],
        help="The command to execute",
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


if __name__ == "__main__":
    sys.exit(run())
