import sys
import argparse
import yaml

from utils import log, get_platform
from constants import EXIT_ERROR, EXIT_SUCCESS, CONFIG_PATH
from commands import run_link, run_install, run_update, run_check


def dispatch(args, config) -> bool:
    commands_mapping = {
        "link": lambda: run_link(config["links"]),
        "install": lambda: run_install(config),
        "update": lambda: run_update(config),
        "check": lambda: run_check(config),
    }
    command = args.command
    if command not in commands_mapping:
        log(f"[ERROR] '{args.command}' is not valid !")
        return False
    return commands_mapping[args.command]()


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage setup commands")
    parser.add_argument(
        "command",
        choices=["link", "install", "update", "check"],
        help="The command to execute",
    )
    args = parser.parse_args(sys.argv[1:])
    return args


def run():
    args = parse_args()
    if not CONFIG_PATH.exists():
        log(f"[ERROR] Config not found: {CONFIG_PATH}", file=sys.stderr)
        return EXIT_ERROR
    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)
    platform_name = get_platform()

    if platform_name not in config:
        log(
            f"[ERROR] no config for platform '{platform_name}' in file {CONFIG_PATH}",
            file=sys.stderr,
        )
        return EXIT_ERROR
    platform_config = config[platform_name]

    if not dispatch(args, platform_config):
        return EXIT_ERROR
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(run())
