
class Module:

    def __init__(self, name, data=None, config=None):
        self.name = name
        self.data = data if data else {}
        self.config = config if config else {}

    def readable_data_dir(self):
        """
        Should return a directory full of human readable data
        """
        return self.data
