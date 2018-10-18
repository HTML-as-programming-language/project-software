import threading
import serial
from enum import Enum
from multiprocessing import Queue
from queue import Empty
import select
from time import sleep

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

    # These values should be used as read-only.
    # There are written off the main thread.
    supported_sensors = []
    current_temp = 0
    current_light = 0
    current_pos = 0

    write_queue = None

    class WriteReq:
        def __init__(self, pid, data=0):
            self.pid = pid
            self.data = data

    def __init__(self, port, baud_rate=9600):
        self.connection = serial.Serial(
            port=port,
            baudrate=baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )

        self.write_queue = Queue()
        
        self.thread = threading.Thread(target=self.run_serial_connection)
        self.thread.start()

    def run_serial_connection(self):
        def handle_data(pid, data):
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

        next_is_id = False
        pid = 0

        while True:
            bytesToRead = self.connection.inWaiting()
            if bytesToRead < 2:
                # No bytes to read. Check the write queue.
                
                try:
                    item = self.write_queue.get_nowait()
                except Empty:
                    sleep(0.1)
                    continue

                print("write")
                self.connection.write([0xff, 0xff,
                        *item.pid.to_bytes(2, byteorder="big"),
                        *item.data.to_bytes(2, byteorder="big")])
                self.connection.flush()
                print("donewrite")
            else:
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
                    handle_data(pid, int_data)
                    pid = 0

    
    def open_hatch(self):
        self.write_queue.put(Client.WriteReq(51))
        pass

    def close_hatch(self):
        self.write_queue.put(Client.WriteReq(52))
        pass
