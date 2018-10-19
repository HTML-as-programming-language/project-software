from tkinter import Frame, Label

BG = "#eaeaea"


class ModuleData(Frame):

    def __init__(self, master, module):
        super().__init__(master, borderwidth="2", relief="ridge", bg=BG)
        data = module.readable_data_dict()
        row = 0
        for key in data.keys():
            keylabel = Label(self, text=key, bg=BG)
            vallabel = Label(self, text=data[key], bg=BG, fg="#34266b")
            keylabel.grid(column=0, row=row)
            vallabel.grid(column=1, row=row)
            row += 1
