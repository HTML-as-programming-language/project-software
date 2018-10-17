
class Module:

    def __init__(self, name, data=None, config=None):
        self.name = name
        self.data = data if data else {}
        self.config = config if config else {}
