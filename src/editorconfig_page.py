from tkinter import Toplevel
from tkinter.ttk import Button, Entry, Label

from salve_ipc import EDITORCONFIG, IPC

from .misc import resize_app


class EditorconfigPage(Toplevel):
    def __init__(self, context: IPC) -> None:
        Toplevel.__init__(self)
        self.context = context
        self.withdraw()
        self.main_entry = Entry(self)
        self.main_entry.insert(0, "/path/to/file")
        self.main_entry.grid(row=0, column=0, sticky="nsew")
        self.output_label = Label(self)
        self.output_label.grid(row=2, column=0, sticky="nsew")
        self.run_button = Button(
            self, text="Get editorconfig info", command=self.run
        )
        self.run_button.grid(row=3, column=0, sticky="nsew")
        resize_app(self)
        self.after_idle(self.loop)
        self.deiconify()

    def loop(self) -> None:
        output = self.context.get_response(EDITORCONFIG)
        if output:
            self.output_label.config(text=str(output["result"]))  # type: ignore

        self.after(50, self.loop)

    def run(self) -> None:
        self.context.request(
            command=EDITORCONFIG, file_path=self.main_entry.get()
        )
