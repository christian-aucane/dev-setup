import shutil

from .link import run as run_link
from .system_commands import reload_fonts_cache, pip_install, git_pull
from utils import log, get_src_path, get_dest_path


def install_fonts(fonts_config):
    log("[INSTALL] fonts")
    src = get_src_path(fonts_config["src_dir"])
    dest = get_dest_path(fonts_config["dest_dir"])

    dest.mkdir(parents=True, exist_ok=True)
    for font in src.glob("*.ttf"):
        shutil.copy2(font, dest)

    reload_fonts_cache()
    log("[OK] fonts successfully installed !")


def install_pip_packages(packages):
    log("[INSTALL] Python dependencies")
    pip_install(packages)
    log("[OK] Python dependencies successfully installed !")


def run(config) -> bool:
    log("[INSTALL] full setup")

    log("[INSTALL] git pull")
    git_pull()
    if not run_link(config["links"]):
        return False
    install_fonts(config["fonts"])
    install_pip_packages(config["pip_packages"])
    log("[OK] full setup successfully installed !")
    return True
