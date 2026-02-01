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
)
from .fetch_commands import download_gnome_extension


def install_fonts(fonts_config):
    log("[INSTALL] fonts")
    src = get_src_path(fonts_config["src_dir"])
    dest = get_dest_path(fonts_config["dest_dir"])

    dest.mkdir(parents=True, exist_ok=True)
    for font in src.glob("*.ttf"):
        shutil.copy2(font, dest)

    reload_fonts_cache()
    log("[OK] fonts successfully installed !")


def install_pip_packages(packages):
    log("[INSTALL] Python dependencies")
    pip_install(packages)
    log("[OK] Python dependencies successfully installed !")


def install_gnome_extensions(gnome_config: list[dict]):
    """
    Installe et configure toutes les extensions GNOME listées dans gnome_config.

    gnome_config : liste de dicts avec les clés suivantes :
        - uuid : UUID de l'extension
        - dconf_file : chemin vers le fichier de configuration dconf (optionnel)
    """

    if not gnome_config:
        return
    log("INSTALL] Gnome")
    shell_version = get_gnome_shell_version()
    if not shell_version:
        log(
            "[ERROR] Could not determine GNOME Shell version. Aborting GNOME extensions installation."
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
            log("[INFO] Extension allready installed.")
            continue
        zip_path = download_gnome_extension(uuid, shell_version)
        if not zip_path:
            log(f"[WARN] Skipping '{uuid}' due to download failure")
            all_success = False
            continue
        success = install_gnome_extension(uuid, zip_path)
        if not success:
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


def run(config) -> bool:
    log("[INSTALL] full setup")

    log("[INSTALL] git pull")
    git_pull()
    if not run_link(config["links"]):
        return False
    install_fonts(config["fonts"])
    # install_pip_packages(config["pip_packages"])
    install_gnome_extensions(config.get("gnome"))
    log("[OK] full setup successfully installed !")
    return True
