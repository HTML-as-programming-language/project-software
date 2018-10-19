from enum import Enum

from backend.client import SensorType


class ModuleView:

    class ConfigItem:

        class Type(Enum):
            MIN_MAX = 1
            ONE_VALUE = 2

        def __init__(self, name, config_type):
            self.name = name
            self.type = config_type
            self.values = []

    def __init__(self, client):
        self.client = client

    def readable_data_dict(self):
        """
        Should return a dictionary full of human readable data
        """
        client = self.client

        d = {
            "Hatch position:", f"{client.current_pos}%"
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
            c.append(ModuleView.ConfigItem(
                "Min. and max. temperature", ModuleView.ConfigItem.Type.MIN_MAX
            ))

        if SensorType.LIGHT in client.supported_sensors:
            c.append(ModuleView.ConfigItem(
                "Min. and max. light values", ModuleView.ConfigItem.Type.MIN_MAX
            ))

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
