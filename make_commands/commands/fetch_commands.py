import requests
from pathlib import Path

from utils import log


def download_gnome_extension(uuid: str, gnome_version: str) -> Path:
    """
    Fetches the latest extension .zip from extensions.gnome.org.
    Returns the local path to the downloaded zip file.
    Returns None if the extension is not found or if a network error occurs.
    """
    base_api = "https://extensions.gnome.org/extension-info/"
    params = {"uuid": uuid, "shell_version": gnome_version.split()[0]}

    try:
        resp = requests.get(base_api, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log(f"[ERROR] Failed to fetch info for '{uuid}': {e}")
        return None

    download_path = data.get("download_url")
    if not download_path:
        log(
            f"[WARN] No download_url found for '{uuid}' @ shell version {gnome_version}"
        )
        return None

    full_url = f"https://extensions.gnome.org{download_path}"
    zip_filename = Path("/tmp") / f"{uuid}.zip"

    try:
        with requests.get(full_url, stream=True, timeout=30) as download:
            download.raise_for_status()
            with open(zip_filename, "wb") as f:
                for chunk in download.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.RequestException as e:
        log(f"[ERROR] Failed to download extension '{uuid}': {e}")
        return None

    log(f"[INFO] Downloaded '{uuid}' to {zip_filename}")
    return zip_filename
