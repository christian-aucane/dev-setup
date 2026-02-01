from datetime import datetime
import shutil
from pathlib import Path

from utils import log, ask_confirmation, get_platform, get_src_path, get_dest_path


def backup_path(path: Path) -> Path:
    """Créer un backup horodaté pour un fichier ou dossier existant."""
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = path.with_name(f"{path.name}.backup_{now_str}")
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        path.rename(backup)
    log(f"[BACKUP] {path} -> {backup}")
    return backup


def create_link(src: Path, dest: Path) -> bool:
    """Créer un symlink, avec fallback Windows si nécessaire."""
    try:
        dest.symlink_to(src, target_is_directory=src.is_dir())
        log(f"[LINK] {dest} -> {src}")
        return True
    except (OSError, NotImplementedError) as e:
        if get_platform() == "windows":
            # fallback: copie si symlink impossible
            if src.is_dir():
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
            log(f"[FALLBACK] Copied {src} -> {dest}")
            return True
        log(f"[ERROR] Failed to link {dest} -> {src}: {e}")
        return False


def run(links_config) -> bool:
    """Boucle principale pour créer tous les liens."""
    success = True
    for entry in links_config:
        src = get_src_path(entry["src"])
        dest = get_dest_path(entry["dest"])

        if not src.exists():
            log(f"[ERROR] Source doesn't exist: '{src}'")
            success = False
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)

        # Si le symlink existe ET est correct, rien à faire
        if dest.is_symlink() and dest.resolve() == src.resolve():
            log(f"[OK] '{dest}' already linked")
            continue

        # Si le fichier/dossier existe, demander backup
        if dest.exists() or dest.is_symlink():
            if not ask_confirmation(f"{dest} exists. Backup and replace?"):
                log(f"[SKIP] '{dest}'")
                continue
            backup_path(dest)

        # Créer le lien ou fallback
        if not create_link(src, dest):
            success = False

    return success
