import glob
from client import Client

class Backend:
    #clients = {}

    def __init__(self):
        self.clients = {}

    def find_ports(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')

        found = []

        for port in ports:
            found.append(port)
            if port not in self.clients:
                c = Client(port)
                c.port = port
                self.clients["port"] = c
        
        # TODO: Cleanup disconnected/inactive clients.
        # Give Clients a queue to send a message to when they finish.

b = Backend()
b.find_ports()

for _, c in b.clients.items():
    c.open_hatch()
