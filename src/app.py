from tkinter import StringVar, Tk
from tkinter.ttk import Button, OptionMenu, Style

from salve_ipc import COMMANDS, IPC

from .autocomplete_page import AutocompletePage
from .misc import resize_app
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
        self.choice_menu.grid(row=0, column=0, rowspan=1, sticky="nsew")
        self.open_ipc_page_button = Button(
            self, text="Open IPC action page", command=self.make_ipc_page
        )
        self.open_ipc_page_button.grid(
            row=1, column=0, rowspan=1, sticky="nsew"
        )
        resize_app(self)
        self.deiconify()

    def make_ipc_page(self) -> None:
        option = self.ipc_option.get()
        match option:
            case "autocomplete":
                AutocompletePage(self.context)
            case "replacements":
                ReplacementsPage(self.context)
            case "highlight":
                ...
            case "editorconfig":
                ...
            case "definition":
                ...

    def destroy(self) -> None:
        super().destroy()
        self.context.kill_IPC()
