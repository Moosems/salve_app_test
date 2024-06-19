from tkinter import StringVar, Tk
from tkinter.ttk import Button, OptionMenu, Style

from salve_ipc import COMMANDS, IPC


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
        self.resize_app()
        self.deiconify()

    def resize_app(self, keep_size: bool = False) -> None:
        self.update_idletasks()
        minimum_width = self.winfo_reqwidth()
        minimum_height = self.winfo_reqheight()
        x_coords = int(self.winfo_screenwidth() / 2 - minimum_width / 2)
        y_coords = int(self.wm_maxsize()[1] / 2 - minimum_height / 2)
        self.geometry(
            f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}"
        )

        self.wm_minsize(minimum_width, minimum_height)

    def make_ipc_page(self) -> None:
        option = self.ipc_option.get()
        print(option)

    def destroy(self) -> None:
        super().destroy()
        self.context.kill_IPC()


if __name__ == "__main__":
    app = App()
    app.mainloop()
