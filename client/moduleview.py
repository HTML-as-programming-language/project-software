import re
from enum import Enum

def determine_config_type(type_str, sub_type=""):
    if type_str == "int":
        if sub_type == "minmax":
            print("yey minmax")
            return ModuleView.ConfigItem.Type.MIN_MAX
        return ModuleView.ConfigItem.Type.ONE_VALUE

class ModuleView:
    class ConfigItem:
        class Type(Enum):
            MIN_MAX = 1
            ONE_VALUE = 2

        def __init__(self, name, config_type, on_apply):
            self.name = name
            self.type = config_type
            self.values = []
            self.on_apply = on_apply

    def __init__(self, module):
        self.module = module

    def readable_data_dict(self):
        """
        Should return a dictionary full of human readable data
        """

        d = {}
        for key, value in self.module["data"].items():
            if key.startswith("label"):
                d[key[5:]] = value

        for s in self.module["sensors"]:
            for key, value in s["data"].items():
                if key.startswith("label"):
                    d[s["label"] + " " + key[5:]] = value
            
        return d

    def get_config_items(self):
        c = []
        for s in self.module["sensors"]:
            for sett in s["settings"]:
                def on_apply():
                    print("Applied")

                c.append(ModuleView.ConfigItem(
                    s["label"],
                    determine_config_type(sett["type"], sett.get("subtype", "")),
                    on_apply
                ))
        return c

    def get_actions(self):
        """
        Should return a dictionary with callbacks.
        eg: {
            "Do something": callback_func
        }
        """
        return {
            "Open": lambda: backend.instance.set_module_setting("hatch_force", 1),
            "Close": lambda: backend.instance.set_module_setting("hatch_force", 0)
        }
