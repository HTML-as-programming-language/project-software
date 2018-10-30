from tkinter import *


class ModulesList(Listbox):
    def __init__(self, master, on_selection_changed):
        super().__init__(master, borderwidth="2", relief="ridge", selectmode="browse")
        self.on_selection_changed = on_selection_changed
        self.prev_curselection = ()
        self.modules = []
        self.poll()

    def poll(self):
        self.after(20, self.poll)
        cs = self.curselection()
        if cs != self.prev_curselection and len(cs) >= 1:
            self.on_selection_changed(self.modules[cs[0]])
        self.prev_curselection = cs

    def update_list(self, modules):
        self.modules = modules
        self.prev_curselection = ()

        self.delete(0)
        for module in modules:
            self.insert(0, module.module["label"])
