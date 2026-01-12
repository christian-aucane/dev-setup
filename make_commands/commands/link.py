from datetime import datetime

from utils import log, ask_confirmation, get_src_path, get_dest_path


# TODO: separer les responsabilites
def run(links_config) -> bool:
    for entry in links_config:
        src = get_src_path(entry["src"])
        dest = get_dest_path(entry["dest"])

        if not src.exists():
            log(f"[ERROR] source doesn't exist: '{src}'")
            return False

        dest.parent.mkdir(parents=True, exist_ok=True)

        # Si le symlink existe ET est correct, rien à faire
        if dest.is_symlink() and dest.resolve() == src.resolve():
            log(f"[OK] '{dest}' already linked")
            continue

        # Sinon, si le fichier/symlink existe, backup ou supprimer
        if dest.exists() or dest.is_symlink():
            if not ask_confirmation(f"{dest} exists. Backup and replace?"):
                log(f"[SKIP] '{dest}'")
                continue
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup = dest.with_name(f"{dest.name}.backup_{now_str}")

            if dest.is_symlink() or dest.is_file():
                dest.unlink()  # supprime symlink ou fichier
            else:
                dest.rename(backup)  # pour dossier, si jamais

            log(f"[BACKUP] {dest} -> {backup}")

        # ✅ Créer le symlink après backup
        dest.symlink_to(src)
        log(f"[LINK] {dest} -> {src}")

    return True
