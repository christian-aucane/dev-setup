import platform
from pathlib import Path
import os

from constants import REPO_ROOT


def get_platform():
    if platform.system().lower().startswith("win"):
        return "windows"
    return "linux"


def log(message: str, *args, **kwargs) -> None:
    print(message, *args, **kwargs)


def ask_confirmation(message: str) -> bool:
    answer = input(f"{message} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def get_src_path(entry: str) -> Path:
    """
    Retourne le chemin absolu vers la source dans le repo.
    Fonctionne pour Linux, macOS et Windows.
    """
    src = REPO_ROOT / entry
    return src.resolve()  # toujours absolu et canonique


def get_dest_path(entry: str) -> Path:
    """
    Retourne le chemin absolu vers la destination.
    Sur Windows, ~ est résolu vers %USERPROFILE%.
    """
    dest = Path(entry).expanduser()
    # Normaliser le séparateur pour Windows
    if get_platform() == "windows":
        dest = Path(os.path.normpath(str(dest)))
    return dest
