import requests
from pathlib import Path

from logger import logger


def download_gnome_extension(uuid: str, gnome_version: str) -> Path | None:
    """
    Fetch the latest extension .zip from extensions.gnome.org.
    Returns the local path to the downloaded zip file.
    Returns None if the extension is not found or if a network error occurs.
    """
    logger.exec(f"Download GNOME extension {uuid}")

    base_api = "https://extensions.gnome.org/extension-info/"
    params = {
        "uuid": uuid,
        "shell_version": gnome_version.split()[0],
    }

    try:
        resp = requests.get(base_api, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch info for '{uuid}': {e}")
        return None

    download_path = data.get("download_url")
    if not download_path:
        logger.warn(f"No download_url for '{uuid}' (GNOME {gnome_version})")
        return None

    full_url = f"https://extensions.gnome.org{download_path}"
    zip_filename = Path("/tmp") / f"{uuid}.zip"

    try:
        with requests.get(full_url, stream=True, timeout=30) as download:
            download.raise_for_status()
            with open(zip_filename, "wb") as f:
                for chunk in download.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.RequestException as e:
        logger.error(f"Failed to download '{uuid}': {e}")
        return None

    logger.success(f"Downloaded '{uuid}' → {zip_filename}")
    return zip_filename
