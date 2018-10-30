from tkinter import Frame, Button

BG = "#d6d0ed"


class ModuleActions(Frame):

    def __init__(self, master, module):
        super().__init__(master, borderwidth="2", relief="ridge", bg=BG)
        actions = module.get_actions()
        row = 0
        for key in actions.keys():
            btn = Button(self, text=key, command=actions[key])
            btn.grid(column=0, row=row, sticky="w")
            row += 1

