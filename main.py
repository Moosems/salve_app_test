from tkinter import Tk

from salve_ipc import IPC


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.context = IPC()

    def destroy(self) -> None:
        super().destroy()
        self.context.kill_IPC()


if __name__ == "__main__":
    app = App()
    app.mainloop()
