import subprocess
import sys
from utils import log, ask_confirmation
from constants import REPO_ROOT


def execute_command(*args, **kwargs):
    command = list(args)
    command_str = " ".join(command)
    log(f"[INFO] Execute command : {command_str}")
    subprocess.run(command, **kwargs)


def reload_fonts_cache() -> bool:
    # TODO: adapter a windows
    execute_command("fc-cache", "-fv")
    return True


def pip_install(packages, *args):
    execute_command(
        sys.executable,
        "-m",
        "pip",
        "install",
        "--user",
        *packages,
        *args,
        check=True,
    )
    return True


def pip_package_is_installed(package) -> bool:
    result = execute_command(
        "python3",
        "-m",
        "pip",
        "show",
        package,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def git_pull():
    try:
        execute_command("git", "-C", str(REPO_ROOT), "pull", "--rebase", check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            log("[WARN] Git pull failed: uncommitted changes present")
            if ask_confirmation("Do you want to stash changes and retry?"):
                log("[INFO] Stashing changes...")
                execute_command("git", "-C", str(REPO_ROOT), "stash", check=True)
                log("[INFO] Retrying git pull...")
                try:
                    execute_command(
                        "git", "-C", str(REPO_ROOT), "pull", "--rebase", check=True
                    )
                except subprocess.CalledProcessError as e2:
                    log(f"[ERROR] Git pull still failed with exit code {e2.returncode}")
                    return False
                log("[INFO] Applying stashed changes...")
                execute_command("git", "-C", str(REPO_ROOT), "stash", "pop", check=True)
            else:
                log("[INFO] Skipping git pull due to uncommitted changes")
        else:
            log(f"[ERROR] Git pull failed with exit code {e.returncode}")
            return False
    return True


def git_is_up_to_date():
    result = execute_command(
        "git",
        "-C",
        str(REPO_ROOT),
        "status",
        "--porcelain",
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        return False
    return True
