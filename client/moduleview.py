import re
from enum import Enum

from backend.client import SensorType


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

    def __init__(self, client):
        self.client = client

    def readable_data_dict(self):
        """
        Should return a dictionary full of human readable data
        """
        client = self.client

        d = {
            "Hatch position:": f"{client.current_pos}%"
        }
        if SensorType.TEMP in client.supported_sensors:
            d["Current Temperature"] = f"{client.current_temp}°C"
        if SensorType.LIGHT in client.supported_sensors:
            d["Light level"] = f"{client.current_light}%"
        return d

    def get_config_items(self):
        c = []
        client = self.client
        if SensorType.TEMP in client.supported_sensors:
            def on_apply(values):
                for i in range(2):
                    ints = re.findall("\d+", values[i])
                    int_val = 0 if not len(ints) else int(ints[0])
                    (
                        client.set_threshold_open_temperature
                        if not i else
                        client.set_threshold_close_temperature
                    )(int_val)

            c.append(ModuleView.ConfigItem(
                "Min. and max. temperature", ModuleView.ConfigItem.Type.MIN_MAX,
                on_apply
            ))

        if SensorType.LIGHT in client.supported_sensors:
           c.append(ModuleView.ConfigItem(
                "Min. and max. light values",
                ModuleView.ConfigItem.Type.MIN_MAX,
                lambda: print("kut op")
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
            "Open": self.client.open_hatch,
            "Close": self.client.close_hatch
        }
