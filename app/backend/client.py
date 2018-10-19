import threading
import serial
from enum import Enum
from multiprocessing import Queue
from queue import Empty
import select
from time import sleep
from serial.serialutil import SerialException

class SensorType(Enum):
    TEMP = 0
    LIGHT = 1

class Client:
    """
    Client is a module; an device connected to this computer by UART
    and controlling a hatch based on data from its sensor(s).
    supported_sensors: list of SensorType.
    current_temp: temperature in tenth degrees celsius.
    current_light: light in percentage.
    current_pos: position of hatch/sunscreen in percentage.
    """

    #connection = None
    #thread = None

    # These values should be used as read-only.
    # There are written off the main thread.
    #supported_sensors = []
    #current_temp = 0
    #current_light = 0
    #current_pos = 0

    write_queue = None

    class WriteReq:
        """
        WriteReq is a struct which contains information needed to send a
        packet.
        """
        def __init__(self, pid, data=0):
            self.pid = pid
            self.data = data

    def __init__(self, port, baud_rate=9600, quit=None):
        try:
            self.connection = serial.Serial(
                port=port,
                baudrate=baud_rate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
                )
        except SerialException as e:
            raise e
            return

        self.quit_queue = quit

        self.port = port

        self.supported_sensors = []
        self.current_temp = 0
        self.current_light = 0
        self.current_pos = 0

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
            # TODO: Make this nicer. Use select() or something.
            try:
                bytesToRead = self.connection.inWaiting()
                if bytesToRead < 2:
                    # No bytes to read. Check the write queue.
                    
                    try:
                        item = self.write_queue.get_nowait()
                    except Empty:
                        sleep(0.1)
                        continue

                    print("write packet:", item.__dict__)
                    self.connection.write([0xff, 0xff,
                            *item.pid.to_bytes(2, byteorder="big"),
                            *item.data.to_bytes(2, byteorder="big")])
                    self.connection.flush()
                    print("donewrite")
                else:
                    # Receive packet
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
            except OSError as e:
                print("OSError :<", e)
                if self.quit_queue:
                    self.quit_queue.put(self.port)
                return

    
    def open_hatch(self):
        """
        Send packet to open the hatch (packet 51).
        """

        self.write_queue.put(Client.WriteReq(51))

    def close_hatch(self):
        """
        Send packet to close the hatch (packet 52).
        """

        self.write_queue.put(Client.WriteReq(52))

    def set_threshold_open_temperature(self, temp):
        """
        Send packet to set the threshold temperature to open the latch
        (packet 11)

        temp: int tenth degrees celcius.
        """

        self.write_queue.put(Client.WriteReq(11, temp))

    def set_threshold_close_temperature(self, temp):
        """
        Send packet to set the threshold temperature to close the latch
        (packet 12)

        temp: int tenth degrees celcius.
        """

        self.write_queue.put(Client.WriteReq(12, temp))

    def set_threshold_open_lightintensity(self, temp):
        """
        Send packet to set the threshold light intensity to open the
        latch (packet 13).

        temp: int percentage of light intensity.
        """

        self.write_queue.put(Client.WriteReq(13, temp))

    def set_threshold_close_lightintensity(self, temp):
        """
        Send packet to set the threshold light intensity to close the
        latch (packet 14).

        temp: int percentage of ligt intensity.
        """

        self.write_queue.put(Client.WriteReq(14, temp))
