from tkinter import Toplevel
from tkinter.ttk import Button, Entry, Frame, Label

from salve_ipc import AUTOCOMPLETE, IPC, is_unicode_letter

from .misc import resize_app


class AutocompletePage(Toplevel):
    def __init__(self, context: IPC) -> None:
        Toplevel.__init__(self)
        self.context = context
        self.withdraw()
        self.main_entry = Entry(self)
        self.main_entry.insert(0, "from code import function; func")
        self.main_entry.grid(row=0, column=0, rowspan=1, sticky="nsew")
        self.output_label = Label(self)
        self.output_label.grid(row=1, column=0, rowspan=1, sticky="nsew")
        self.run_button = Button(self, text="Get autocompletes", command=self.run)
        self.run_button.grid(row=2, column=0, rowspan=1, sticky="nsew")
        resize_app(self)
        self.after_idle(self.loop)
        self.deiconify()

    def loop(self) -> None:
        output = self.context.get_response(AUTOCOMPLETE)
        if output:
            self.output_label.config(text=str(output["result"]))  # type: ignore

        self.after(50, self.loop)

    def run(self) -> None:
        text = self.main_entry.get()
        word = ""
        for letter in reversed(text):
            if not is_unicode_letter(letter):
                break
            word = letter + word
        self.context.update_file("example_file", text)
        self.context.request(
            file="example_file", command=AUTOCOMPLETE, current_word=word
        )
