import platform
from pathlib import Path
import os

from constants import REPO_ROOT
from logger import logger


def get_platform():
    if platform.system().lower().startswith("win"):
        return "windows"
    return "linux"


def ask_confirmation(message: str) -> bool:
    logger.input(f"{message} [y/N] ", inline=True)
    answer = input().strip().lower()
    return answer in ("y", "yes")


def get_src_path(entry: str) -> Path:
    src = REPO_ROOT / entry
    return src.resolve()  # toujours absolu et canonique


def get_dest_path(entry: str) -> Path:
    dest = Path(entry).expanduser()
    # Normaliser le séparateur pour Windows
    if get_platform() == "windows":
        dest = Path(os.path.normpath(str(dest)))
    return dest
