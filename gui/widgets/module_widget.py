import tkinter


class ModuleWidget(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master, bg="blue")
        tkinter.Label(self, text="module widget").pack(side="left")
