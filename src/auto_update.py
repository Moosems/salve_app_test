from sys import exit
from urllib.request import urlretrieve
from subprocess import Popen
from shutil import move
from tempfile import NamedTemporaryFile, TemporaryDirectory
from zipfile import ZipFile

from requests import Response, get
from requests.exceptions import ReadTimeout

from .misc import GITHUB_URL, VERSION, folder, is_frozen

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

    assets: list[dict[str, str]] = response.json()["assets"]

    if not assets:
        return

    zip_path = NamedTemporaryFile(prefix="SalveTest.app.zip")
    app_dir = TemporaryDirectory(prefix="SalveTest.app")
    urlretrieve(assets[0]["browser_download_url"], zip_path.name)
    with ZipFile(zip_path.name) as zip_ref:
        zip_ref.extractall(app_dir.name)
    move(app_dir.name, "/Applications/SalveTest.app")
    move(folder, app_dir.name)
    app_dir.cleanup()
    zip_path.close()
    Popen(["open", "/Applications/SalveTest.app"])
    exit(1)

print("Old version")

if not is_newest_version() and is_frozen:
    download_newest_version()
