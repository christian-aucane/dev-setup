from pathlib import Path
import shutil

from logger import logger
from utils import get_src_path, get_dest_path
from constants import REPO_ROOT
from .system_commands import (
    git_is_up_to_date,
    pip_package_is_installed,
    get_gnome_shell_version,
    is_gnome_extension_installed,
)


def check_repo() -> bool:
    logger.check("Check repository ...")

    if not (REPO_ROOT / ".git").exists():
        logger.error("Not a git repository")
        return False

    if git_is_up_to_date():
        logger.success("Repository clean !")
    else:
        logger.warn("Repository has uncommitted changes")
    return True


def check_links(links_config) -> bool:
    logger.check("Check links...")
    status = True

    for entry in links_config:
        src = get_src_path(entry["src"]).resolve()
        dest = get_dest_path(entry["dest"])

        if not src.exists():
            logger.error(f"Source missing: {src}")
            status = False
            continue

        if not dest.exists():
            logger.error(f"Missing destination: {dest}")
            status = False
            continue

        if not dest.is_symlink():
            logger.error(f"{dest} is not a symlink")
            status = False
            continue

        if dest.resolve() != src:
            logger.error(f"{dest} points to {dest.resolve()} instead of {src}")
            status = False
            continue

        logger.success(f"{dest}")

    return status


def check_pip_packages(packages) -> bool:
    logger.check("Check Python packages...")
    status = True

    for pkg in packages:
        if pip_package_is_installed(pkg):
            logger.success(pkg)
        else:
            logger.error(f"Missing pip package: {pkg}")
            status = False

    return status


def check_nvim() -> bool:
    logger.check("Check Neovim...")

    if not shutil.which("nvim"):
        logger.error("Neovim not found")
        return False

    logger.success("Neovim found")
    return True


def check_fonts(fonts_config) -> bool:
    logger.check("Check fonts...")

    dest = get_dest_path(fonts_config["dest_dir"])

    if not dest.exists():
        logger.error(f"Fonts directory missing: {dest}")
        return False

    fonts = list(dest.glob("*.ttf"))
    if not fonts:
        logger.warn("No fonts found")
        return False

    logger.success(f"{len(fonts)} fonts installed")
    return True


def check_zsh() -> bool:
    logger.check("Check ZSH...")

    if not shutil.which("zsh"):
        logger.error("zsh not found")
        return False

    logger.success("zsh found")

    env_file = REPO_ROOT / "zsh" / "env.zsh"
    if env_file.exists():
        logger.success("env.zsh present")
    else:
        logger.info("env.zsh not found (optional)")

    return True


def check_lazygit() -> bool:
    logger.check("Check Lazygit...")

    if not shutil.which("lazygit"):
        logger.error("lazygit not found")
        return False

    logger.success("Lazygit found")
    return True


def check_gnome_extension(uuid: str, dconf_file: str | None) -> bool:
    if not uuid:
        logger.error("GNOME extension entry without UUID")
        return False

    logger.check(f"Check GNOME extension '{uuid}'...")

    if not is_gnome_extension_installed(uuid):
        logger.error(f"Extension not installed: {uuid}")
        return False

    logger.success(f"Extension installed: {uuid}")

    if dconf_file:
        dconf_path = Path(dconf_file)
        if not dconf_path.exists():
            logger.error(f"Missing dconf file: {dconf_file}")
            return False
        logger.success(f"Dconf file found: {dconf_file}")

    return True


def check_gnome(gnome_config: dict | None) -> bool:
    if not gnome_config:
        return True

    logger.check("Check Gnome...")

    gnome_version = get_gnome_shell_version()
    if not gnome_version:
        logger.error("GNOME Shell not detected")
        return False

    logger.info(f"GNOME Shell version: {gnome_version}")

    extensions = gnome_config.get("extensions")
    if not extensions:
        logger.info("No GNOME extensions configured")
        return True

    status = True
    for ext in extensions:
        status &= check_gnome_extension(
            ext.get("uuid"),
            ext.get("dconf_filename"),
        )

    return status


def run(config) -> bool:
    logger.check("Check config...")

    status = True
    status &= check_repo()
    status &= check_links(config["links"])
    status &= check_fonts(config["fonts"])
    status &= check_pip_packages(config["pip_packages"])
    status &= check_nvim()
    status &= check_zsh()
    status &= check_lazygit()
    status &= check_gnome(config.get("gnome"))

    if status:
        logger.success("All checks passed")
    else:
        logger.warn("Some checks failed")

    return status
