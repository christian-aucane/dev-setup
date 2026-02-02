import shutil
from pathlib import Path

from logger import logger
from utils import get_src_path, get_dest_path
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
    logger.install("Install fonts...")

    src = get_src_path(fonts_config["src_dir"])
    dest = get_dest_path(fonts_config["dest_dir"])

    if not src.exists():
        logger.error(f"Fonts source directory not found: {src}")
        return False

    dest.mkdir(parents=True, exist_ok=True)

    fonts = list(src.glob("*.ttf"))
    if not fonts:
        logger.warn("No font files found to install")
        return False

    installed_any = False

    for font in fonts:
        dest_file = dest / font.name
        if dest_file.exists():
            logger.info(f"{dest_file} already exists, skipping")
            continue

        try:
            shutil.copy2(font, dest_file)
            installed_any = True
            logger.success(f"Installed {dest_file}")
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to copy font {font}: {e}")
            return False

    if installed_any:
        if not reload_fonts_cache():
            logger.error("Failed to reload font cache")
            return False
        logger.success("Fonts installed and cache reloaded")
    else:
        logger.info("All fonts already installed, nothing to do")

    return True


def install_pip_packages(packages) -> bool:
    logger.install("Install Python packages...")

    if pip_install(packages):
        logger.success("Python dependencies successfully installed")
        return True

    logger.error("Failed to install Python dependencies")
    return False


def install_gnome(gnome_config: dict) -> bool:
    """
    Installe et configure toutes les extensions GNOME listées dans gnome_config.
    """
    if not gnome_config:
        return True

    logger.install("Install GNOME...")

    shell_version = get_gnome_shell_version()
    if not shell_version:
        logger.error(
            "Could not determine GNOME Shell version. "
            "Aborting GNOME extensions installation."
        )
        return False

    logger.info(f"GNOME Shell version detected: {shell_version}")

    all_success = True

    for ext in gnome_config.get("extensions", []):
        uuid = ext.get("uuid")
        dconf_file = ext.get("dconf_file")

        if not uuid:
            logger.error("Skipping extension with missing UUID")
            all_success = False
            continue

        logger.info(f"Processing extension '{uuid}'")

        if is_gnome_extension_installed(uuid):
            logger.info("Extension already installed")
        else:
            zip_path = download_gnome_extension(uuid, shell_version)
            if not zip_path:
                logger.warn(f"Skipping '{uuid}' due to download failure")
                all_success = False
                continue

            if not install_gnome_extension(uuid, zip_path):
                logger.error(f"Failed to install extension '{uuid}'")
                all_success = False
                continue

        if dconf_file:
            dconf_path = Path(dconf_file).expanduser()
            if not dconf_path.exists():
                logger.warn(f"Dconf file not found: {dconf_path}")
            else:
                if not load_gnome_dconf(uuid, dconf_path):
                    logger.error(f"Failed to load dconf for '{uuid}'")
                    all_success = False

    if all_success:
        logger.success("All GNOME extensions installed and configured successfully")
    else:
        logger.warn("Some GNOME extensions failed to install or configure")

    return all_success


def run(config) -> bool:
    logger.install("Instal configuration...")

    status = True

    logger.install("Git pull...")
    status &= git_pull()
    status &= run_link(config["links"])
    status &= install_fonts(config["fonts"])
    status &= install_pip_packages(config["pip_packages"])
    status &= install_gnome(config.get("gnome"))

    if status:
        logger.success("Full setup successfully installed")
    else:
        logger.warn("Full setup finished with some errors")

    return status
