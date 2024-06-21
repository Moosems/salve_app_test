from pathlib import Path

from requests import Response, get
from requests.exceptions import ReadTimeout

VERSION = "0.1.0"
try:
    folder = Path(__compiled__.containing_dir).resolve().parent.parent  # type: ignore # noqa: F821
except NameError:
    folder = Path(__file__).parent


def resize_app(app, keep_size: bool = False) -> None:
    app.update_idletasks()
    minimum_width = app.winfo_reqwidth()
    minimum_height = app.winfo_reqheight()
    x_coords = int(app.winfo_screenwidth() / 2 - minimum_width / 2)
    y_coords = int(app.wm_maxsize()[1] / 2 - minimum_height / 2)
    app.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")

    app.wm_minsize(minimum_width, minimum_height)


# NOTE: This should always be run in a subprocess!
def is_newest_version() -> bool:
    try:
        response: Response = get(
            "https://api.github.com/repos/Moosems/salve_app_test/releases/latest",
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


def download_newest_version(): ...
