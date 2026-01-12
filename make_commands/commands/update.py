from .system_commands import git_pull
from .link import run as run_link
from utils import log


def run(config):
    log("[UPDATE] full setup")

    log("[UPDATE] git pull")
    if not git_pull():
        return False

    if not run_link(config["links"]):
        return False

    log("\n[OK] update finished")
    return True
