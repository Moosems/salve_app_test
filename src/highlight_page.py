from tkinter import Toplevel, Text
from tkinter.ttk import Button, Entry, Frame, Label

from salve_ipc import HIGHLIGHT, IPC, is_unicode_letter

from .misc import resize_app


class HighlightPage(Toplevel):
    def __init__(self, context: IPC) -> None:
        Toplevel.__init__(self)
        self.context = context
        self.withdraw()
        self.text_area = Text(self)
        self.text_area.insert("1.0", "# Some python code")
        self.text_area.grid(row=0, column=0, sticky="nsew")
        self.run_button = Button(self, text="Highlight", command=self.run)
        self.run_button.grid(row=1, column=0, sticky="nsew")
        resize_app(self)
        self.after_idle(self.loop)
        self.deiconify()

    def loop(self) -> None:
        output = self.context.get_response(HIGHLIGHT)
        if output:
            tp = Toplevel(self)
            txt = Text(tp)
            txt.pack()
            for token in output["result"]:  # type: ignore
                txt.insert("end", (str(token) + "\n"))

        self.after(50, self.loop)

    def run(self) -> None:
        text = self.text_area.get("1.0", "end")
        self.context.update_file("example_file", text)
        self.context.request(
            file="example_file", command=HIGHLIGHT, language="python"
        )
