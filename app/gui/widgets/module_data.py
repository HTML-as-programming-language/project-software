from tkinter import Frame

BG = "#eaeaea"

class ModuleData(Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth="2", relief="ridge", bg=BG)
