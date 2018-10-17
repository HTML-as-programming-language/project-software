from tkinter import Frame

BG = "#d0d9e5"

class ModuleConfig(Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth="2", relief="ridge", bg=BG)