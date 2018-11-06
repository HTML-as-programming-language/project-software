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

    def add(self, module):
        self.modules.append(module)
        self.insert(0, module.module["label"])

    def change_sensor_dataitem(self, module_id, sensor_id, key, value):
        for m in self.modules:
            if m.module["id"] != module_id:
                continue
            for s in m.module["sensors"]:
                if s["id"] != sensor_id:
                    continue
                print("new value:", key, value)
                print("old value:", s["data"][key])
                print(s["data"])
                s["data"][key] = value
            return m
        print("change_sensor_dataitem: unknown module or sensor:", module_id, sensor_id)
        return None

    def change_dataitem(self, module_id, key, value):
        for m in self.modules:
            if m.module["id"] != module_id:
                continue
            print("new value:", key, value)
            m.module["data"][key] = value
            return m
        print("change_dataitem: unknown module or sensor:", module_id)
        return None


    def remove(self, module_id):
        index = None
        for m, _ in enumerate(self.modules):
            if self.modules[m].module["id"] == module_id:
                index = m
                break

        del self.modules[index]

        self.delete(index)
