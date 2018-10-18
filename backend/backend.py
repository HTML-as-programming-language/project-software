import glob
from client import Client

class Backend:
    #clients = []

    def __init__(self):
        self.clients = []

    def find_ports(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')

        found = []

        for port in ports:
            found.append(port)
            if port not in self.clients:
                c = Client(port)
                self.clients.append(c)
        
        # TODO: Cleanup disconnected/inactive clients.

b = Backend()
b.find_ports()

for c in b.clients:
    c.open_hatch()
