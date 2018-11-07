import threading
import serial
from enum import Enum
from multiprocessing import Queue
from queue import Empty
from time import sleep
from serial.serialutil import SerialException


class SensorType(Enum):
    TEMP = 0
    LIGHT = 1


class StateChange:
    def __init__(self, module_id):
        self.module_id = module_id
        self.sensor_id = None
        self.data_item = None
        self.value = None
        self.new = None


class Client:
    """
    Client is a module; an device connected to this computer by UART
    and controlling a hatch based on data from its sensor(s).
    supported_sensors: list of SensorType.
    current_temp: temperature in tenth degrees celsius.
    current_light: light in percentage.
    current_pos: position of hatch/sunscreen in percentage.
    current_distance: distance.
    is_automatic: boolean
    """

    class WriteReq:
        """
        WriteReq is a struct which contains information needed to send a
        packet.
        """
        def __init__(self, pid, data=0):
            self.pid = pid
            self.data = data

    def __init__(self, name, port, baud_rate=9600, quit=None,
                 state_change=None):
        self.name = name
        self.port = port

        sleep(1)

        try:
            # self.connection = serial.Serial(port,
            #         baudrate=9600,
            #         bytesize=serial.EIGHTBITS,
            #         parity=serial.PARITY_NONE,
            #         stopbits=serial.STOPBITS_ONE,
            #         timeout=1,
            #         xonxoff=0,
            #         rtscts=0
            #         )
            # Toggle DTR to reset Arduino
            # self.connection.setDTR(False)
            # sleep(1)
            # toss any data already received, see
            # http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
            # self.connection.flushInput()
            # self.connection.setDTR(True)

            self.connection = serial.Serial(
                port=port,
                baudrate=baud_rate,
                # timeout=1,
                # parity=serial.PARITY_NONE,
                # stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
                # rtscts=1,
                # parity=serial.PARITY_EVEN,
                # timeout=0,
                # rtscts=1,
                )
            # self.connection.flushInput()
            # self.connection.flushOutput()
        except SerialException as e:
            print(self.port, e)
            raise e
            return

        self.initialized = False
        self.quit_queue = quit
        self.state_change_queue = state_change
        self.supported_sensors = []
        self.current_temp = 0
        self.current_light = 0
        self.current_pos = 0
        self.current_distance = 0

        self.is_automatic = True

        self.initted = False

        self.write_queue = Queue()

        print(self.port, "waiting for connection to open")
        self.connection.isOpen()
        print(self.port, "connection opened")
        self.thread = threading.Thread(target=self.run_serial_connection)
        self.thread.start()

    def run_serial_connection(self):
        print(self.port, "run serial connection")

        def handle_data(pid, data):
            print(self.port, "incoming packet:", pid, data)

            if pid == 101:
                # Initialisation

                if self.initted:
                    print(self.port, "has already initted")
                    return

                try:
                    if data & 0x01:
                        self.supported_sensors.append(
                                SensorType(SensorType.TEMP))
                    if data & 0x02:
                        self.supported_sensors.append(
                                SensorType(SensorType.LIGHT))

                    self.initialized = True
                except ValueError:
                    print(self.port, "unsupported sensor:", data)

                print(self.port, "Added client:", self.port)
                change = StateChange(self.name)
                change.new = True
                change.value = self
                self.state_change_queue.put(change)

                self.initted = True

                print(self.port, "Informed api clients of added module")
            elif pid == 102:
                # Temperature update
                # self.current_temp = random.randint(data, 100)
                self.current_temp = data/10

                # TODO: Also send update for "temp" value, not label.
                change = StateChange(self.name)
                change.sensor_id = "0"
                change.data_item = "label"
                change.value = str(self.current_temp) + "C"
                self.state_change_queue.put(change)

            elif pid == 103:
                # Light update
                self.current_light = data

                # TODO: Also send update for "temp" value, not label.
                change = StateChange(self.name)
                change.sensor_id = "1"
                change.data_item = "label"
                change.value = str(data) + "%"
                self.state_change_queue.put(change)

            elif pid == 104:
                # Current pos
                # self.current_pos = random.randint(data, 100)
                self.current_pos = data

                # TODO: Also send update for "temp" value, not label.
                change = StateChange(self.name)
                change.data_item = "labelHatch open"
                change.value = str(self.current_pos) + "%"
                self.state_change_queue.put(change)
            elif pid == 105:
                # Light update
                self.current_distance = data

                change = StateChange(self.name)
                change.data_item = "labelDistance"
                change.value = str(self.current_distance) + " cm"
                self.state_change_queue.put(change)
            else:
                print(self.port, "unknown packet id:", pid)

        next_is_id = False
        pid = 0

        self.connection.flushInput()
        self.connection.flushOutput()

        while True:
            data_in = []

            # TODO: Make this nicer. Use select() or something.
            try:
                bytesToRead = self.connection.inWaiting()
                if not bytesToRead:
                    # No bytes to read. Check the write queue.

                    try:
                        item = self.write_queue.get_nowait()
                    except Empty:
                        sleep(0.2)
                        continue

                    print(self.port, "write packet:", item.__dict__)
                    self.connection.write(
                            [0xff,
                             *item.pid.to_bytes(1, byteorder="big"),
                             *item.data.to_bytes(1, byteorder="big")])
                    self.connection.flush()
                else:
                    # Receive packet
                    data_in = self.connection.read(1)
                    int_data = int.from_bytes(data_in, byteorder="big")
                    print(self.port, "int data", int_data)
                    if int_data == 0xff:
                        # Start of a packet
                        next_is_id = True
                    elif next_is_id:
                        next_is_id = False
                        pid = int_data
                    elif pid:
                        handle_data(pid, int_data)
                        pid = 0
            except OSError as e:
                print(self.port, "OSError :<", e)
                self.connection.close()
                if self.quit_queue:
                    self.quit_queue.put(self.name)
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

    def disable_autonomus(self):
        """
        Send packet to disable autonomus function.
        """
        self.write_queue.put(Client.WriteReq(53, 1))
        self.is_automatic = False

        change = StateChange(self.name)
        change.data_item = "labelAutomatic"
        change.value = str(self.is_automatic)
        self.state_change_queue.put(change)

    def enable_autonomus(self):
        """
        Send packet to enable autonomus function.
        """
        self.write_queue.put(Client.WriteReq(53, 0))
        self.is_automatic = True

        change = StateChange(self.name)
        change.data_item = "labelAutomatic"
        change.value = str(self.is_automatic)
        self.state_change_queue.put(change)
