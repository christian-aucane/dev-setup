import subprocess
import sys
from pathlib import Path

from utils import log, ask_confirmation
from constants import REPO_ROOT


def execute_command(*args, **kwargs):
    command = list(args)
    command_str = " ".join(command)
    log(f"[EXECUTE COMMAND] {command_str}")
    return subprocess.run(command, **kwargs)


def reload_fonts_cache() -> bool:
    try:
        execute_command("fc-cache", "-fv", check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        log(f"[ERROR] Failed to reload fonts cache: {e}")
        return False


def pip_install(packages, *args) -> bool:
    """
    Installe des packages Python avec pip pour l'utilisateur courant.
    Retourne True si succès, False sinon.
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
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        log(f"[ERROR] Failed to install pip packages {packages}: {e}")
        return False


def pip_package_is_installed(package) -> bool:
    result = execute_command(
        "python3",
        "-m",
        "pip",
        "show",
        package,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def git_pull() -> bool:
    try:
        execute_command("git", "-C", str(REPO_ROOT), "pull", "--rebase", check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            log("[WARN] Git pull failed: uncommitted changes present")
            if ask_confirmation("Do you want to stash changes and retry?"):
                log("[INFO] Stashing changes...")
                execute_command("git", "-C", str(REPO_ROOT), "stash", check=True)
                log("[INFO] Retrying git pull...")
                try:
                    execute_command(
                        "git", "-C", str(REPO_ROOT), "pull", "--rebase", check=True
                    )
                except subprocess.CalledProcessError as e2:
                    log(f"[ERROR] Git pull still failed with exit code {e2.returncode}")
                    return False
                log("[INFO] Applying stashed changes...")
                execute_command("git", "-C", str(REPO_ROOT), "stash", "pop", check=True)
            else:
                log("[INFO] Skipping git pull due to uncommitted changes")
        else:
            log(f"[ERROR] Git pull failed with exit code {e.returncode}")
            return False
    return True


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

    if result.stdout.strip():
        return False
    return True


def get_gnome_shell_version() -> str | None:
    """
    Retourne la version de GNOME Shell (ex: '44').
    Retourne None si la commande échoue.
    """
    try:
        result = execute_command(
            "gnome-shell", "--version", capture_output=True, text=True, check=True
        )
        version = result.stdout.strip().split()[-1]
        return version
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        log(f"[ERROR] Failed to get GNOME Shell version: {e}")
        return None


def install_gnome_extension(uuid: str, zip_path: Path) -> bool:
    """
    Installe et active une extension GNOME depuis un zip.
    Retourne True si succès, False sinon.
    """
    try:
        execute_command(
            "gnome-extensions", "install", "--force", str(zip_path), check=True
        )
        execute_command("gnome-extensions", "enable", uuid, check=True)
        log(f"[OK] Installed and enabled GNOME extension '{uuid}'")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        log(f"[ERROR] Failed to install GNOME extension '{uuid}': {e}")
        return False


def load_gnome_dconf(uuid: str, dconf_file: Path) -> bool:
    """
    Charge une configuration dconf pour une extension.
    Retourne True si succès, False sinon.
    """
    try:
        # on passe par shell=True pour le redirection < dconf load
        execute_command(
            f"dconf load /org/gnome/shell/extensions/{uuid}/ < {dconf_file}",
            shell=True,
            check=True,
        )
        log(f"[OK] Loaded dconf for '{uuid}' from {dconf_file}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        log(f"[ERROR] Failed to load dconf for '{uuid}': {e}")
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
        installed = uuid in result.stdout.splitlines()
        return installed
    except subprocess.CalledProcessError:
        return False
