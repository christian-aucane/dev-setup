from commands.system_commands import (
    get_gnome_shell_version,
    is_gnome_extension_installed,
)
from utils import log
from pathlib import Path
import shutil
from commands.system_commands import execute_command
from commands.install import is_gnome_extension_installed

from .system_commands import git_is_up_to_date, pip_package_is_installed
from constants import REPO_ROOT
from utils import log, get_src_path, get_dest_path


def check_repo():
    log("[CHECK] repo")

    if not (REPO_ROOT / ".git").exists():
        log("[ERROR] not a git repository")
        return False

    if git_is_up_to_date():
        log("[OK] repo clean")
    else:
        log("[WARN] repo has uncommitted changes")
    return True


def check_links(links_config):
    log("[CHECK] links")
    status = True

    for entry in links_config:
        src = get_src_path(entry["src"]).resolve()
        dest = get_dest_path(entry["dest"])

        if not src.exists():
            log(f"[ERROR] source missing: {src}")
            status = False
            continue

        if not dest.exists():
            log(f"[MISSING] {dest}")
            status = False
            continue

        if not dest.is_symlink():
            log(f"[WRONG] {dest} is not a symlink")
            status = False
            continue

        if dest.resolve() != src:
            log(f"[WRONG] {dest} -> {dest.resolve()}")
            status = False
            continue

        log(f"[OK] {dest}")

    return status


def check_pip_packages(packages):
    log("[CHECK] pip packages")
    status = True

    for pkg in packages:
        if pip_package_is_installed(pkg):
            log(f"[OK] {pkg}")
        else:
            log(f"[MISSING] {pkg}")
            status = False

    return status


def check_nvim():
    log("[CHECK] nvim")

    if not shutil.which("nvim"):
        log("[ERROR] nvim not found")
        return False

    log("[OK] nvim found")

    return True


def check_fonts(fonts_config):
    log("[CHECK] fonts")

    dest = get_dest_path(fonts_config["dest_dir"])

    if not dest.exists():
        log(f"[ERROR] fonts dir missing: {dest}")
        return False

    fonts = list(dest.glob("*.ttf"))
    if not fonts:
        log("[WARN] no fonts found")
        return False

    log(f"[OK] {len(fonts)} fonts installed")
    return False


def check_zsh():
    log("[CHECK] zsh")

    if not shutil.which("zsh"):
        log("[ERROR] zsh not found")
        return False
    log("[OK] zsh found")

    env_file = REPO_ROOT / "zsh" / "env.zsh"

    if env_file.exists():
        log("[OK] env.zsh present")
    else:
        log("[INFO] env.zsh not found (optional)")

    return False


def check_lazygit():
    log("[CHECK] lazygit")

    if not shutil.which("lazygit"):
        log("[ERROR] lazygit not found")
        return False

    log("[OK] lazygit found")
    return True


def check_gnome(gnome_config: dict) -> bool:
    if not gnome_config:
        return True
    # GNOME est requis → on échoue si absent
    gnome_version = get_gnome_shell_version()
    if not gnome_version:
        log("[ERROR] GNOME Shell is required but not detected")
        return False

    log(f"[INFO] GNOME Shell version detected: {gnome_version}")

    extensions = gnome_config.get("extensions", [])
    if not extensions:
        log("[INFO] No GNOME extensions configured")
        return True

    all_ok = True

    for ext in extensions:
        uuid = ext.get("uuid")
        dconf_file = ext.get("dconf_filename")

        if not uuid:
            log("[WARN] GNOME extension entry without UUID, skipping")
            continue

        log(f"[CHECK] GNOME extension '{uuid}'")

        if is_gnome_extension_installed(uuid):
            log(f"[OK] Extension installed: {uuid}")
        else:
            log(f"[ERROR] Extension NOT installed: {uuid}")
            all_ok = False

        if dconf_file:
            dconf_path = Path(dconf_file)
            if dconf_path.exists():
                log(f"[OK] Dconf file found: {dconf_file}")
            else:
                log(f"[ERROR] Missing dconf file: {dconf_file}")
                all_ok = False

    return all_ok


def run(config):
    status = True

    status |= check_repo()
    status |= check_links(config["links"])
    status |= check_fonts(config["fonts"])
    status |= check_pip_packages(config["pip_packages"])
    status |= check_nvim()
    status |= check_zsh()
    status |= check_lazygit()
    status |= check_gnome(config.get("gnome"))

    if not status:
        log("[WARN] some checks failed")
    else:
        log("[OK] all checks passed")
    return status
