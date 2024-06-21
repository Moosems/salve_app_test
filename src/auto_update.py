from .misc import GITHUB_URL, VERSION
from pathlib import Path
from requests import Response, get
from requests.exceptions import ReadTimeout
import urllib.request
from tempfile import TemporaryDirectory


# NOTE: This should always be run in a subprocess!
def is_newest_version() -> bool:
    try:
        response: Response = get(
            GITHUB_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=3,
        )
        version: str = response.json()["tag_name"].lstrip("v")
    except ReadTimeout:
        return False

    return True if version == VERSION else False


def download_newest_version() -> None:
    try:
        response: Response = get(
            GITHUB_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=3,
        )
    except ReadTimeout:
        return

    assets: str = response.json()["assets"]

    if not assets:
        return

    file_path = TemporaryDirectory(prefix="SalveTest.app")
    urllib.request.urlretrieve(assets[0], file_path.name)
    # Swap files

    file_path.cleanup()


download_newest_version()
