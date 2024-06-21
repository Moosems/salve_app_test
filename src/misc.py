from pathlib import Path

GITHUB_URL = (
    "https://api.github.com/repos/Moosems/salve_app_test/releases/latest"
)

VERSION = "0.1.3"
is_frozen = False
try:
    folder = Path(__compiled__.containing_dir).resolve().parent.parent  # type: ignore # noqa: F821
    is_frozen = True
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
