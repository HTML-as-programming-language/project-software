import tkinter


class ModulesList(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth="2", relief="ridge")
        tkinter.Label(self, text="modules list").pack(side="left")
