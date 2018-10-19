from tkinter import Frame, Label, Entry, Button, END

from moduleview import ModuleView

BG = "#d0d9e5"


class ModuleConfig(Frame):

    def __init__(self, master, module):
        super().__init__(master, borderwidth="2", relief="ridge", bg=BG)
        self.inputs = {}
        self.module = module

        row = 0
        for config_item in module.config.values():
            label = Label(self, text=config_item.name, bg=BG)
            label.grid(column=0, row=row, sticky="w")
            textbox = Entry(self)
            textbox.grid(column=1, row=row)

            self.inputs[config_item] = [textbox]

            if config_item.type is ModuleView.ConfigItem.Type.MIN_MAX:
                # add second textbox
                textbox1 = Entry(self)
                textbox1.grid(column=2, row=row)
                self.inputs[config_item].append(textbox1)

            row += 1

        apply_btn = Button(self, text="Apply", command=self.apply)
        apply_btn.grid(column=2, row=row+1, sticky="e")

    def apply(self):
        print("applyyyyyy")

        for config_item in self.module.config.values():
            inputs = self.inputs[config_item]
            values = []
            for i in inputs:
                values.append(i.get())

            config_item.values = values
            print(config_item.name, values)


