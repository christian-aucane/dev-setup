from datetime import datetime
import shutil
from pathlib import Path

from logger import logger
from utils import ask_confirmation, get_platform, get_src_path, get_dest_path


def backup_path(path: Path) -> Path:
    """Créer un backup horodaté pour un fichier ou dossier existant."""
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = path.with_name(f"{path.name}.backup_{now_str}")

    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        path.rename(backup)

    logger.backup(f"{path} -> {backup}")
    return backup


def create_link(src: Path, dest: Path) -> bool:
    """Créer un symlink, avec fallback Windows si nécessaire."""
    try:
        dest.symlink_to(src, target_is_directory=src.is_dir())
        logger.link(f"Link created: {dest} -> {src}")
        return True

    except (OSError, NotImplementedError) as e:
        if get_platform() == "windows":
            try:
                if src.is_dir():
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
                logger.warn(f"Symlink not supported, copied instead: {dest} -> {src}")
                return True
            except (FileNotFoundError, PermissionError) as e2:
                logger.error(f"Fallback copy failed for {dest}: {e2}")
                return False

        logger.error(f"Failed to link {dest} -> {src}: {e}")
        return False


def run(links_config) -> bool:
    """Boucle principale pour créer tous les liens."""
    logger.link("Create symlinks...")

    success = True

    for entry in links_config:
        src = get_src_path(entry["src"])
        dest = get_dest_path(entry["dest"])

        if not src.exists():
            logger.error(f"Source does not exist: {src}")
            success = False
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)

        # Symlink déjà correct → rien à faire
        if dest.is_symlink() and dest.resolve() == src.resolve():
            logger.info(f"{dest} already linked")
            continue

        # Destination existante → backup ?
        if dest.exists() or dest.is_symlink():
            if not ask_confirmation(f"{dest} exists. Backup and replace?"):
                logger.info(f"Skipped {dest}")
                continue
            backup_path(dest)

        if not create_link(src, dest):
            success = False

    if success:
        logger.success("All symlinks created")
    return success
