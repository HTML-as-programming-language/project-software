from enum import Enum


class Module:

    class ConfigItem:

        class Type(Enum):
            MIN_MAX = 1
            ONE_VALUE = 2

        def __init__(self, name, config_type):
            self.name = name
            self.type = config_type
            self.values = []

    def __init__(self, name, data=None, config=None, actions=None):
        self.name = name
        self.data = data if data else {}
        self.config = config if config else {}
        self.actions = actions if actions else {}

    def readable_data_dict(self):
        """
        Should return a dictionary full of human readable data
        """
        return self.data

    def get_actions(self):
        """
        Should return a dictionary with callbacks.
        eg: {
            "Do something": callback_func
        }
        """
        return self.actions

    def apply_config(self):
        """
        Called when config is changed
        """
        pass
