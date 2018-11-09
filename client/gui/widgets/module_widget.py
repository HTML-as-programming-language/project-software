import tkinter

from gui.widgets.module_actions import ModuleActions
from gui.widgets.module_config import ModuleConfig
from gui.widgets.module_data import ModuleData

TITLE_FONT_SIZE = 20
BG = "#434d5b"


class ModuleWidget(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.module = None
        self.title = tkinter.Label(self,
                                   text="Select a module...",
                                   bg=BG, fg="white",
                                   font=("Helvetica", TITLE_FONT_SIZE))
        self.title.grid(column=0, row=0)

        self.data_and_actions_frame = tkinter.Frame(self)
        # will be created when module is selected
        self.module_data = None
        self.module_actions = None
        self.module_config = None

        self.data_and_actions_frame.columnconfigure(0, weight=1)
        self.data_and_actions_frame.columnconfigure(1, weight=1)
        self.data_and_actions_frame.rowconfigure(0, weight=1)
        self.data_and_actions_frame.grid(column=0, row=1, sticky="nesw")

        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def show_module(self, module):
        self.module = module
        self.title.config(text=f"Connected module: {module.module['label']}",
                          font=("Helvetica", TITLE_FONT_SIZE))
        self.update_module_data(module)

        self.module_actions = ModuleActions(self.data_and_actions_frame,
                                            module)
        self.module_actions.grid(column=1, row=0, sticky="nesw")

        self.module_config = ModuleConfig(self, module)
        self.module_config.grid(column=0, row=2, sticky="nesw")
        self.after(100, self.update_module_data, module)

    def update_module_data(self, module):
        if self.module_data:
            self.module_data.destroy()
        self.module_data = ModuleData(self.data_and_actions_frame, module)
        self.module_data.grid(column=0, row=0, sticky="nesw")
