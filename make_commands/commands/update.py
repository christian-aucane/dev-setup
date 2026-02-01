from .system_commands import (
    git_pull,
    get_gnome_shell_version,
    is_gnome_extension_installed,
    load_gnome_dconf,
)
from .fetch_commands import download_gnome_extension
from .link import run as run_link
from utils import log


def update_gnome(gnome_config: list[dict]):
    """
    Met à jour les extensions GNOME listées dans gnome_config.

    gnome_config : liste de dicts avec les clés suivantes :
        - uuid : UUID de l'extension
        - dconf_file : chemin vers le fichier de configuration dconf (optionnel)
    """
    if not gnome_config:
        return
    log("[UPDATE] Gnome")
    shell_version = get_gnome_shell_version()
    if not shell_version:
        log(
            "[ERROR] Could not determine GNOME Shell version. Aborting GNOME extensions update."
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

        log(f"[INFO] Checking extension '{uuid}'")
        if is_gnome_extension_installed(uuid):
            log("[INFO] Extension allready installed")
            continue

        zip_path = download_gnome_extension(uuid, shell_version)
        if not zip_path:
            log(f"[WARN] Skipping '{uuid}' due to download failure")
            all_success = False
            continue

        # Comparer les versions (ici on simplifie en utilisant le nom du zip)
        if installed_version == zip_path.stem:
            log(f"[INFO] Extension '{uuid}' is up-to-date. Skipping reinstallation.")
        else:
            log(f"[INFO] Updating extension '{uuid}'")
            success = install_gnome_extension(uuid, zip_path)
            if not success:
                log(f"[ERROR] Failed to update extension '{uuid}'")
                all_success = False
                continue

        # Recharger la configuration Dconf si disponible
        if dconf_file:
            dconf_path = Path(dconf_file).expanduser()
            if not dconf_path.exists():
                log(f"[WARN] Dconf file not found: {dconf_path}")
            else:
                if not load_gnome_dconf(uuid, dconf_path):
                    log(f"[ERROR] Failed to load dconf for '{uuid}'")
                    all_success = False

    if all_success:
        log("[OK] All GNOME extensions updated successfully!")
    else:
        log("[WARN] Some GNOME extensions failed to update. Check logs.")


def run(config):
    log("[UPDATE] full setup")

    log("[UPDATE] git pull")
    if not git_pull():
        return False

    if not run_link(config["links"]):
        return False

    if not update_gnome(config.get("gnome")):
        return False

    log("\n[OK] update finished")
    return True
