from pathlib import Path
import shutil

from commands.system_commands import (
    git_is_up_to_date,
    pip_package_is_installed,
    get_gnome_shell_version,
    is_gnome_extension_installed,
)
from utils import log, get_src_path, get_dest_path
from constants import REPO_ROOT


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

    if not (fonts := list(dest.glob("*.ttf"))):
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


def check_gnome_extention(uuid, dconf_file):
    if not uuid:
        log("[ERROR] GNOME extension entry without UUID, skipping")
        return False

    log(f"[CHECK] GNOME extension '{uuid}'")

    if not is_gnome_extension_installed(uuid):
        log(f"[ERROR] Extension NOT installed: {uuid}")
        return False
    log(f"[OK] Extension installed: {uuid}")

    if dconf_file:
        dconf_path = Path(dconf_file)
        if not dconf_path.exists():
            log(f"[ERROR] Missing dconf file: {dconf_file}")
            return False
        log(f"[OK] Dconf file found: {dconf_file}")
    return True


def check_gnome(gnome_config: dict) -> bool:
    if not gnome_config:
        return True
    log("[CHECK] Gnome")
    if not (gnome_version := get_gnome_shell_version()):
        log("[ERROR] GNOME Shell is required but not detected")
        return False
    log(f"[INFO] GNOME Shell version detected: {gnome_version}")

    if not (extensions := gnome_config.get("extensions")):
        log("[INFO] No GNOME extensions configured")
        return True

    all_ok = True
    for ext in extensions:
        uuid = ext.get("uuid")
        dconf_file = ext.get("dconf_filename")
        all_ok &= check_gnome_extention(uuid, dconf_file)
    return all_ok


def run(config):
    status = True

    status &= check_repo()
    status &= check_links(config["links"])
    status &= check_fonts(config["fonts"])
    status &= check_pip_packages(config["pip_packages"])
    status &= check_nvim()
    status &= check_zsh()
    status &= check_lazygit()
    status &= check_gnome(config.get("gnome"))

    if not status:
        log("[WARN] some checks failed")
    else:
        log("[OK] all checks passed")
    return status
