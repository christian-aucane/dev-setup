from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT = SCRIPTS_DIR.parent
CONFIG_PATH = REPO_ROOT / "config.yaml"

EXIT_SUCCESS = 0
EXIT_ERROR = 1
