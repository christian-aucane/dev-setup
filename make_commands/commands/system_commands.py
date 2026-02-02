import subprocess
import sys
from pathlib import Path

from logger import logger
from utils import ask_confirmation
from constants import REPO_ROOT


def execute_command(*args, **kwargs):
    command = list(args)
    command_str = " ".join(command)
    logger.exec(command_str)
    return subprocess.run(command, **kwargs)


def reload_fonts_cache() -> bool:
    try:
        execute_command("fc-cache", "-fv", check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to reload fonts cache: {e}")
        return False


def pip_install(packages, *args) -> bool:
    """
    Installe des packages Python avec pip pour l'utilisateur courant.
    """
    try:
        execute_command(
            sys.executable,
            "-m",
            "pip",
            "install",
            "--user",
            *packages,
            *args,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to install pip packages {packages}: {e}")
        return False


def pip_package_is_installed(package) -> bool:
    result = execute_command(
        sys.executable,
        "-m",
        "pip",
        "show",
        package,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def git_is_up_to_date() -> bool:
    result = execute_command(
        "git",
        "-C",
        str(REPO_ROOT),
        "status",
        "--porcelain",
        capture_output=True,
        text=True,
    )
    return not bool(result.stdout.strip())


def git_pull() -> bool:
    def _git_pull():
        if git_is_up_to_date():
            logger.info("Repository is up to date!")
            return
        logger.info("Repository not up to date, pulling...")
        execute_command(
            "git",
            "-C",
            str(REPO_ROOT),
            "pull",
            "--rebase",
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.success("Git pull successfully !")

    try:
        _git_pull()
        return True

    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            logger.warn("Git pull failed: uncommitted changes present")

            if ask_confirmation("Do you want to stash changes and retry?"):
                logger.info("Stashing changes...")
                execute_command("git", "-C", str(REPO_ROOT), "stash", check=True)

                logger.info("Retrying git pull...")
                try:
                    _git_pull()
                except subprocess.CalledProcessError as e2:
                    logger.error(
                        f"Git pull still failed with exit code {e2.returncode}"
                    )
                    return False

                logger.info("Applying stashed changes...")
                execute_command("git", "-C", str(REPO_ROOT), "stash", "pop", check=True)
                return True

            logger.info("Skipping git pull due to uncommitted changes")
            return True

        logger.error(f"Git pull failed with exit code {e.returncode}")
        return False


def get_gnome_shell_version() -> str | None:
    """
    Retourne la version de GNOME Shell (ex: '48.7').
    """
    try:
        result = execute_command(
            "gnome-shell",
            "--version",
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split()[-1]
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to get GNOME Shell version: {e}")
        return None


def install_gnome_extension(uuid: str, zip_path: Path) -> bool:
    try:
        execute_command(
            "gnome-extensions", "install", "--force", str(zip_path), check=True
        )
        logger.success(f"GNOME extension '{uuid}' installed successfully!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to install GNOME extension '{uuid}': {e}")
        return False


def enable_gnome_extension(uuid: str) -> bool:
    try:
        execute_command("gnome-extensions", "enable", uuid, check=True)
        logger.success(f"GNOME extension '{uuid}' enabled successfully!")
        return True
    except Exception as e:
        logger.error(f"Failed to enable GNOME extension '{uuid}': {e}")
        return False


def load_gnome_dconf(uuid: str, dconf_file: Path) -> bool:
    try:
        execute_command(
            f"dconf load /org/gnome/shell/extensions/{uuid}/ < {dconf_file}",
            shell=True,
            check=True,
        )
        logger.success(f"Loaded dconf for '{uuid}' from {dconf_file}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to load dconf for '{uuid}': {e}")
        return False


def is_gnome_extension_installed(uuid: str) -> bool:
    try:
        result = execute_command(
            "gnome-extensions",
            "list",
            capture_output=True,
            text=True,
            check=True,
        )
        return uuid in result.stdout.splitlines()
    except subprocess.CalledProcessError:
        return False
