# logger.py
import sys
from datetime import datetime
from enum import Enum


class Color:
    RESET = "\033[0m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Bright / flashy colors pour contraste
    RED = "\033[1;91m"  # erreur
    GREEN = "\033[1;92m"  # succès
    YELLOW = "\033[1;93m"  # warning
    BLUE = "\033[1;94m"  # info
    MAGENTA = "\033[1;95m"  # actions
    CYAN = "\033[1;96m"  # actions alternative
    GRAY = "\033[90m"  # debug / EXEC


class Level(Enum):
    # Actions / étapes
    INSTALL = ("INSTALL", Color.MAGENTA, "🛠️")
    CHECK = ("CHECK", Color.MAGENTA, "🔍")
    UPDATE = ("UPDATE", Color.MAGENTA, "🔄")
    LINK = ("LINK", Color.MAGENTA, "🔗")
    EXEC = ("EXEC", Color.GRAY, "⚡")

    # Status / résultats
    SUCCESS = ("SUCCESS", Color.GREEN, "✔️")
    INFO = ("INFO", Color.BLUE, "ℹ️")
    WARNING = ("WARN", Color.YELLOW, "⚠️")
    ERROR = ("ERROR", Color.RED, "❌")


class Logger:
    def __init__(
        self,
        *,
        enable_colors: bool = True,
        show_timestamp: bool = False,
        stream=sys.stdout,
    ):
        self._enable_colors = enable_colors
        self._show_timestamp = show_timestamp
        self._stream = stream

    # ---------- core ----------

    def _format_prefix(self, level: Level) -> str:
        label, color, emoji = level.value
        prefix = f"[{label}]\t{emoji}"

        if self._enable_colors:
            prefix = f"{color}{prefix}{Color.RESET}"

        return prefix

    def _format_message(self, message: str) -> str:
        if self._show_timestamp:
            ts = datetime.now().strftime("%H:%M:%S")
            return f"{Color.DIM}{ts}{Color.RESET} {message}"
        return message

    def _log(
        self,
        level: Level,
        message: str,
        *,
        inline: bool = False,
    ) -> None:
        prefix = self._format_prefix(level)
        msg = self._format_message(message)
        output = f"{prefix} {msg}"

        if inline:
            print(output, end="", flush=True, file=self._stream)
        else:
            print(output, file=self._stream)

    # ---------- semantic helpers ----------

    def install(self, message: str) -> None:
        self._log(Level.INSTALL, message)

    def check(self, message: str) -> None:
        self._log(Level.CHECK, message)

    def update(self, message: str) -> None:
        self._log(Level.UPDATE, message)

    def link(self, message: str) -> None:
        self._log(Level.LINK, message)

    def exec(self, message: str, *, inline: bool = False) -> None:
        self._log(Level.EXEC, message, inline=inline)

    def success(self, message: str) -> None:
        self._log(Level.SUCCESS, message)

    def info(self, message: str) -> None:
        self._log(Level.INFO, message)

    def warn(self, message: str) -> None:
        self._log(Level.WARNING, message)

    def error(self, message: str) -> None:
        self._log(Level.ERROR, message)


# instance globale simple à importer
logger = Logger()
