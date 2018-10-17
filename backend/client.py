import threading
import serial
from enum import Enum

class SensorType(Enum):
    TEMP = 0
    LIGHT = 1

class Client:
    """
    Client is a module: an device connected to this computer by UART
    and controlling a hatch based on data from its sensor(s).
    """

    connection = None
    thread = None

    supported_sensors = []

    current_temp = 0
    current_light = 0
    current_pos = 0

    def __init__(self, port):
        self.connection = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
        
        self.thread = threading.Thread(target=self.read_from_port)
        self.thread.start()

    def read_from_port(self):
        next_is_id = False
        pid = 0

        while True:
            bytesToRead = self.connection.inWaiting()
            if bytesToRead < 2:
                continue

            data_in = self.connection.read(2)
            print(len(data_in), data_in)
            int_data = int.from_bytes(data_in, byteorder="big")
            print("read", int_data)
            if int_data == 0xffff:
                print("start packet")
                # Start of a packet
                next_is_id = True
            elif next_is_id:
                print("get pid")
                next_is_id = False
                pid = int_data
            elif pid:
                print("yey packet")
                self.handle_data(pid, int_data)
                pid = 0

    def handle_data(self, pid, data):
        if pid == 101:
            # Initialisation

            try:
                self.supported_sensors.append(SensorType(data))
            except ValueError:
                print("unsupported sensor")

            print("init", self.supported_sensors)
        elif pid == 102:
            # Temperature update
            self.current_temp = data
        elif pid == 103:
            # Light update
            self.current_light = data
        elif pid == 104:
            # Current pos
            self.current_pos = data
        else:
            print("unknown packet id:", pid)
        pass
