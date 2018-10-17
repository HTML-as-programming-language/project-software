import tkinter

from gui.widgets.module_config import ModuleConfig
from gui.widgets.module_data import ModuleData

TITLE_FONT_SIZE = 20
BG = "#434d5b"

class ModuleWidget(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.module = None
        self.title = tkinter.Label(self, text="Select a module...", bg=BG, fg="white", font=("Helvetica", TITLE_FONT_SIZE))
        self.title.grid(column=0, row=0)

        self.module_data = ModuleData(self)
        self.module_config = ModuleConfig(self)
        self.module_data.grid(column=0, row=1, sticky="nesw")
        self.rowconfigure(1, weight=1)
        self.module_config.grid(column=0, row=2, sticky="nesw")
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def show_module(self, module):
        self.module = module
        self.title.config(text=f"Connected module: {module.name}", font=("Helvetica", TITLE_FONT_SIZE))
        self.module_data.show_data_for_module(module)
