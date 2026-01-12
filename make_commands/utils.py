import platform
from pathlib import Path

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
    return REPO_ROOT / entry


def get_dest_path(entry: str) -> Path:
    return Path(entry).expanduser()
