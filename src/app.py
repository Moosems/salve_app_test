from tkinter import StringVar, Tk, Toplevel
from tkinter.ttk import Button, Label, OptionMenu, Style
from multiprocessing import Process

from salve_ipc import COMMANDS, IPC

from src.definition_page import DefinitionPage
from src.editorconfig_page import EditorconfigPage

from .auto_update import download_newest_version, is_newest_version  # type: ignore # noqa: F401
from .autocomplete_page import AutocompletePage
from .highlight_page import HighlightPage
from .misc import resize_app, is_frozen
from .replacements_page import ReplacementsPage


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.withdraw()
        self.title("SalveTest")
        Style(self).theme_use("clam")
        self.context = IPC()
        self.ipc_option = StringVar()
        self.ipc_option.set(COMMANDS[0])
        self.choice_menu = OptionMenu(
            self, self.ipc_option, COMMANDS[0], *COMMANDS
        )
        self.choice_menu.grid(row=0, column=0, sticky="nsew")
        self.open_ipc_page_button = Button(
            self, text="Open IPC action page", command=self.make_ipc_page
        )
        self.open_ipc_page_button.grid(row=1, column=0, sticky="nsew")
        resize_app(self)
        if not is_newest_version() and is_frozen:
            Process(target=download_newest_version, daemon=True).start()

            tp = Toplevel(self)
            tp.withdraw()
            Label(tp, text="App auto-update in progress").pack()
            resize_app(tp)
            tp.deiconify()
        self.deiconify()

    def make_ipc_page(self) -> None:
        option = self.ipc_option.get()
        match option:
            case "autocomplete":
                AutocompletePage(self.context)
            case "replacements":
                ReplacementsPage(self.context)
            case "highlight":
                HighlightPage(self.context)
            case "editorconfig":
                EditorconfigPage(self.context)
            case "definition":
                DefinitionPage(self.context)

    def destroy(self) -> None:
        super().destroy()
        self.context.kill_IPC()
