from utils import log
from .system_commands import (
    git_pull,
    get_gnome_shell_version,
    is_gnome_extension_installed,
    load_gnome_dconf,
)
from .fetch_commands import download_gnome_extension
from .link import run as run_link


def update_gnome(gnome_config: list[dict]):
    """
    Met à jour les extensions GNOME listées dans gnome_config.

    gnome_config : liste de dicts avec les clés suivantes :
        - uuid : UUID de l'extension
        - dconf_file : chemin vers le fichier de configuration dconf (optionnel)
    """
    if not gnome_config:
        return True
    log("[UPDATE] Gnome")
    if not (shell_version := get_gnome_shell_version()):
        log(
            "[ERROR] Could not determine GNOME Shell version. Aborting GNOME extensions update."
        )
        return False
    log(f"[INFO] GNOME Shell version detected: {shell_version}")

    all_success = True
    for ext in gnome_config.get("extensions", []):
        if not (uuid := ext.get("uuid")):
            log("[WARN] Skipping extension with missing UUID")
            continue

        log(f"[INFO] Checking extension '{uuid}'")
        if is_gnome_extension_installed(uuid):
            log("[INFO] Extension allready installed")
            continue

        if not (zip_path := download_gnome_extension(uuid, shell_version)):
            log(f"[WARN] Skipping '{uuid}' due to download failure")
            all_success = False
            continue

        if dconf_file := ext.get("dconf_file"):
            dconf_path = Path(dconf_file).expanduser()
            if not dconf_path.exists():
                log(f"[ERROR] Dconf file not found: {dconf_path}")
                all_success = False
            else:
                if not load_gnome_dconf(uuid, dconf_path):
                    log(f"[ERROR] Failed to load dconf for '{uuid}'")
                    all_success = False

    if all_success:
        log("[OK] All GNOME extensions updated successfully!")
        return True
    else:
        log("[WARN] Some GNOME extensions failed to update. Check logs.")
        return False


def run(config):
    log("[UPDATE] full setup")

    if not git_pull():
        return False

    if not run_link(config["links"]):
        return False

    if not update_gnome(config.get("gnome")):
        return False

    log("\n[OK] update finished")
    return True
