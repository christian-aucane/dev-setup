from pathlib import Path

from logger import logger
from .system_commands import (
    git_pull,
    get_gnome_shell_version,
    is_gnome_extension_installed,
    load_gnome_dconf,
)
from .fetch_commands import download_gnome_extension
from .link import run as run_link


def update_gnome(gnome_config: dict) -> bool:
    """
    Met à jour les extensions GNOME listées dans gnome_config.
    """
    if not gnome_config:
        return True

    logger.update("Update Gnome...")

    shell_version = get_gnome_shell_version()
    if not shell_version:
        logger.error(
            "Could not determine GNOME Shell version. Aborting GNOME extensions update."
        )
        return False

    logger.info(f"GNOME Shell version detected: {shell_version}")

    all_success = True

    for ext in gnome_config.get("extensions", []):
        uuid = ext.get("uuid")
        dconf_file = ext.get("dconf_file")

        if not uuid:
            logger.warn("Skipping extension with missing UUID")
            continue

        logger.info(f"Checking extension '{uuid}'")

        if is_gnome_extension_installed(uuid):
            logger.info("Extension already installed (nothing to update)")
            continue

        zip_path = download_gnome_extension(uuid, shell_version)
        if not zip_path:
            logger.warn(f"Skipping '{uuid}' due to download failure")
            all_success = False
            continue

        if dconf_file:
            dconf_path = Path(dconf_file).expanduser()
            if not dconf_path.exists():
                logger.error(f"Dconf file not found: {dconf_path}")
                all_success = False
            else:
                if not load_gnome_dconf(uuid, dconf_path):
                    logger.error(f"Failed to load dconf for '{uuid}'")
                    all_success = False

    if all_success:
        logger.success("All GNOME extensions updated successfully")
    else:
        logger.warn("Some GNOME extensions failed to update")

    return all_success


def run(config) -> bool:
    logger.update("Update config...")

    status = True

    logger.update("Git pull...")
    status &= git_pull()
    status &= run_link(config["links"])
    status &= update_gnome(config.get("gnome"))

    if status:
        logger.success("Update finished successfully")
    else:
        logger.warn("Update finished with some errors")

    return status
