import shutil
from pathlib import Path

from utils import log, get_src_path, get_dest_path
from .link import run as run_link
from .system_commands import (
    reload_fonts_cache,
    pip_install,
    git_pull,
    get_gnome_shell_version,
    install_gnome_extension,
    is_gnome_extension_installed,
    load_gnome_dconf,
)
from .fetch_commands import download_gnome_extension


def install_fonts(fonts_config) -> bool:
    log("[INSTALL] fonts")

    src = get_src_path(fonts_config["src_dir"])
    dest = get_dest_path(fonts_config["dest_dir"])

    if not src.exists():
        log(f"[ERROR] Fonts source directory not found: {src}")
        return False

    dest.mkdir(parents=True, exist_ok=True)

    fonts = list(src.glob("*.ttf"))
    if not fonts:
        log("[WARN] No font files found to install")
        return False

    installed_any = False
    for font in fonts:
        dest_file = dest / font.name
        if dest_file.exists():
            log(f"[SKIP] {dest_file} already exists")
            continue
        try:
            shutil.copy2(font, dest_file)
            installed_any = True
            log(f"[OK] Installed {dest_file}")
        except (FileNotFoundError, PermissionError) as e:
            log(f"[ERROR] Failed to copy font {font}: {e}")
            return False

    if installed_any:
        if not reload_fonts_cache():
            log("[ERROR] Failed to reload font cache")
            return False
        log("[OK] fonts successfully installed and cache reloaded !")
    else:
        log("[INFO] All fonts already installed, nothing to do")

    return True


def install_pip_packages(packages) -> bool:
    log("[INSTALL] Python dependencies")
    if pip_install(packages):
        log("[OK] Python dependencies successfully installed !")
        return True
    return False


def install_gnome(gnome_config: list[dict]) -> bool:
    """
    Installe et configure toutes les extensions GNOME listées dans gnome_config.
    """
    if not gnome_config:
        return True

    log("[INSTALL] Gnome")

    shell_version = get_gnome_shell_version()
    if not shell_version:
        log(
            "[ERROR] Could not determine GNOME Shell version."
            "\tAborting GNOME extensions installation."
        )
        return False
    log(f"[INFO] GNOME Shell version detected: {shell_version}")

    all_success = True

    for ext in gnome_config.get("extensions", []):
        uuid = ext.get("uuid")
        dconf_file = ext.get("dconf_file")  # optionnel
        if not uuid:
            log("[WARN] Skipping extension with missing UUID")
            continue

        log(f"[INFO] Processing extension '{uuid}'")

        if is_gnome_extension_installed(uuid):
            log("[INFO] Extension already installed.")
        else:
            zip_path = download_gnome_extension(uuid, shell_version)
            if not zip_path:
                log(f"[WARN] Skipping '{uuid}' due to download failure")
                all_success = False
                continue
            if not install_gnome_extension(uuid, zip_path):
                log(f"[ERROR] Failed to install extension '{uuid}'")
                all_success = False
                continue

        # Charger la config dconf si disponible
        if dconf_file:
            dconf_path = Path(dconf_file).expanduser()
            if not dconf_path.exists():
                log(f"[WARN] Dconf file not found: {dconf_path}")
            else:
                if not load_gnome_dconf(uuid, dconf_path):
                    log(f"[ERROR] Failed to load dconf for '{uuid}'")
                    all_success = False

    if all_success:
        log("[OK] All GNOME extensions installed and configured successfully!")
    else:
        log("[WARN] Some GNOME extensions failed to install or configure. Check logs.")
    return all_success


def run(config) -> bool:
    log("[INSTALL] full setup")

    status = True

    status &= git_pull()
    status &= run_link(config["links"])
    status &= install_fonts(config["fonts"])
    status &= install_pip_packages(config["pip_packages"])
    status &= install_gnome(config.get("gnome"))

    if status:
        log("[OK] full setup successfully installed !")
    else:
        log("[WARN] Full setup finished with some errors. Check logs.")
    return status
