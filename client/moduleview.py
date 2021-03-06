from enum import Enum
import backend


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

        print("GET READABLE DATA DICT", d)
        print(self.module["sensors"])
        return d

    def get_config_items(self):
        c = []
        if "settings" in self.module:
            for sett in self.module["settings"]:
                typ = determine_config_type(sett["type"],
                                            sett.get("subtype", ""))

                on_apply = self.create_on_apply(None, sett, typ)

                c.append(ModuleView.ConfigItem(
                    sett["label"],
                    typ,
                    on_apply
                ))

        for s in self.module["sensors"]:
            for sett in s["settings"]:
                typ = determine_config_type(sett["type"],
                                            sett.get("subtype", ""))

                on_apply = self.create_on_apply(s, sett, typ, True)
                
                c.append(ModuleView.ConfigItem(
                    s["label"],
                    typ,
                    on_apply
                ))
        return c

    def create_on_apply(self, s, sett, typ, sensor=False):
        def on_apply(data):
            vals = []
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@222 data:", data)
            if typ == ModuleView.ConfigItem.Type.MIN_MAX:
                filled = False
                for x in data:
                    val = 0
                    try:
                        val = int(x)
                        filled = True
                    except ValueError:
                        print("not 0", x)
                    vals.append(val)
                if not filled:
                    print("not filled")
                    return
            elif typ == ModuleView.ConfigItem.Type.ONE_VALUE:
                if data == "":
                    print("not filled")
                    return
                vals = int(data)
            else:
                vals = data

            if sensor:
                backend.instance.set_module_sensor_setting(
                        self.module["id"],
                        s["id"],
                        sett["id"],
                        vals)
            else:
                backend.instance.set_module_setting(
                        self.module["id"],
                        sett["id"],
                        vals)

        return on_apply

    def get_actions(self):
        """
        Should return a dictionary with callbacks.
        eg: {
            "Do something": callback_func
        }
        """
        return {
            "Open": lambda: backend.instance.set_module_setting(
                self.module["id"], "hatch_force", 1),
            "Close": lambda: backend.instance.set_module_setting(
                self.module["id"], "hatch_force", 0),
            "Automatic": lambda: backend.instance.set_module_setting(
                self.module["id"], "automatic", 1),
            "Manual": lambda: backend.instance.set_module_setting(
                self.module["id"], "automatic", 0),
        }
