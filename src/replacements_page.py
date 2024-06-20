from tkinter import Toplevel
from tkinter.ttk import Button, Entry, Frame, Label

from salve_ipc import IPC, REPLACEMENTS, is_unicode_letter

from .misc import resize_app


class ReplacementsPage(Toplevel):
    def __init__(self, context: IPC) -> None:
        Toplevel.__init__(self)
        self.context = context
        self.withdraw()
        self.main_frame = Frame()
        self.main_entry = Entry(self)
        self.main_entry.insert(
            0, "from code import function, replacement_word"
        )
        self.main_entry.grid(row=0, column=0, rowspan=1, sticky="nsew")
        self.replacement_word_entry = Entry(self)
        self.replacement_word_entry.insert(0, "replacement_worb")
        self.replacement_word_entry.grid(
            row=1, column=0, rowspan=1, sticky="nsew"
        )
        self.output_label = Label(self)
        self.output_label.grid(row=2, column=0, rowspan=1, sticky="nsew")
        self.run_button = Button(self, command=self.run)
        self.run_button.grid(row=3, column=0, rowspan=1, sticky="nsew")
        resize_app(self)
        self.after_idle(self.loop)
        self.deiconify()

    def loop(self) -> None:
        output = self.context.get_response(REPLACEMENTS)
        if output:
            self.output_label.config(text=str(output["result"]))  # type: ignore

        self.after(50, self.loop)

    def run(self) -> None:
        text = self.main_entry.get()
        self.context.update_file("example_file", text)
        self.context.request(
            file="example_file",
            command=REPLACEMENTS,
            current_word=self.replacement_word_entry.get(),
        )
