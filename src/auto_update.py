from shutil import move, rmtree
from subprocess import Popen
from sys import exit
from tempfile import NamedTemporaryFile, TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile

from requests import Response, get
from requests.exceptions import ReadTimeout

from .misc import GITHUB_URL, VERSION, folder


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
    app_dir = TemporaryDirectory(prefix="SalveTest")
    old_app_dir = TemporaryDirectory(prefix="OldSalveTest")
    urlretrieve(assets[0]["browser_download_url"], zip_path.name)
    with ZipFile(zip_path.name) as zip_ref:
        zip_ref.extractall(app_dir.name)
    move(folder, old_app_dir.name)
    try:
        rmtree("/Applications/SalveTest.app")
    except OSError or Exception:
        pass
    move(app_dir.name + "/SalveTest.app", "/Applications/SalveTest.app")
    app_dir.cleanup()
    zip_path.close()
    old_app_dir.cleanup()
    Popen(["chmod", "+x", "/Applications/SalveTest.app/Contents/MacOS/SalveTest"]).wait()
    Popen(["open", "/Applications/SalveTest.app"])
    exit(1)
