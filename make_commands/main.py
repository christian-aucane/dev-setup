# main.py
import sys
import argparse
import yaml

from logger import logger
from utils import get_platform
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
        logger.error(f"'{args.command}' is not valid !")
        return False
    return commands_mapping[command]()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage setup commands")
    parser.add_argument(
        "command",
        choices=["link", "install", "update", "check"],
        help="The command to execute",
    )
    return parser.parse_args(sys.argv[1:])


def run():
    args = parse_args()
    if not CONFIG_PATH.exists():
        logger.error(f"Config not found: {CONFIG_PATH}")
        return EXIT_ERROR
    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)
    platform_name = get_platform()

    if platform_name not in config:
        logger.error(f"No config for platform '{platform_name}' in file {CONFIG_PATH}")
        return EXIT_ERROR
    platform_config = config[platform_name]

    if not dispatch(args, platform_config):
        return EXIT_ERROR
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(run())
