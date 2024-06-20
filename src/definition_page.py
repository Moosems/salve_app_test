from tkinter import Toplevel, Text
from tkinter.ttk import Button, Entry, Frame, Label
from salve_ipc import DEFINITION, IPC, is_unicode_letter

from .misc import resize_app

# TODO: Write this


class DefinitionPage(Toplevel):
    def __init__(self, context: IPC) -> None:
        Toplevel.__init__(self)
        self.context = context
        self.withdraw()
        self.text_area = Text(self)
        self.text_area.insert("1.0", "from this import s")
        self.text_area.grid(row=0, column=0, sticky="nsew")
        self.main_entry = Entry(self)
        self.main_entry.insert(0, "this")
        self.main_entry.grid(row=1, column=0, sticky="nsew")
        self.run_button = Button(self, text="Get Definition", command=self.run)
        self.run_button.grid(row=2, column=0, sticky="nsew")
        resize_app(self)
        self.after_idle(self.loop)
        self.deiconify()

    def loop(self) -> None:
        output = self.context.get_response(DEFINITION)
        if output:
            tp = Toplevel()
            Label(tp, text=str(output["result"])).pack()  # type: ignore

        self.after(50, self.loop)

    def run(self) -> None:
        text = self.text_area.get("1.0", "end")
        self.context.update_file("example_file", text)
        self.context.request(
            file="example_file",
            command=DEFINITION,
            current_word=self.main_entry.get(),
        )
