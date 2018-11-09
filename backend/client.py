import threading
import serial
from enum import Enum
from multiprocessing import Queue
from queue import Empty
from time import sleep
from serial.serialutil import SerialException

from constants import SPAM_DEBUG


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
        self.thread_read = threading.Thread(target=self.read_loop)
        self.thread_read.start()

        self.thread_write = threading.Thread(target=self.write_loop)
        self.thread_write.start()

    def write_loop(self):
        try:
            while True:

                try:
                    item = self.write_queue.get_nowait()
                except Empty:
                    sleep(0.1)
                    continue

                print(self.port, "write packet:", item.__dict__)
                self.connection.write(
                        [0xff,
                         *item.pid.to_bytes(1, byteorder="big"),
                         *item.data.to_bytes(1, byteorder="big")])
                self.connection.flush()
        except OSError as e:
            print(self.port, "OSError write loop :<", e)
            self.connection.close()
            if self.quit_queue:
                self.quit_queue.put(self.name)
            return

    def read_loop(self):
        next_is_id = False
        pid = 0

        self.connection.flushInput()
        self.connection.flushOutput()


        try:
            while True:
                # Receive packet
                data_in = self.connection.read(1)
                int_data = int.from_bytes(data_in, byteorder="big")
                if int_data == 0xff:
                    # Start of a packet
                    next_is_id = True
                elif next_is_id:
                    next_is_id = False
                    pid = int_data
                elif pid:
                    log_msg = self.handle_data(pid, int_data)

                    print(self.port, "incoming packet:", pid, int_data, " : ", log_msg)
                    pid = 0
        except OSError as e:
            print(self.port, "OSError read loop :<", e)
            self.connection.close()
            if self.quit_queue:
                self.quit_queue.put(self.name)
            return

    def handle_data(self, pid, data):
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

            if SPAM_DEBUG:
                print(self.port, "Informed api clients of added module")
        elif pid == 102:
            data /= 10
            data += 5

            if self.current_temp == data:
                return "is the same"

            # Temperature update
            # self.current_temp = random.randint(data, 100)
            self.current_temp = data

            change = StateChange(self.name)
            change.sensor_id = "0"
            change.data_item = "label"
            change.value = str(self.current_temp) + "°C"
            self.state_change_queue.put(change)

            change = StateChange(self.name)
            change.sensor_id = "0"
            change.data_item = "temp"
            change.value = self.current_temp
            self.state_change_queue.put(change)
        elif pid == 103:
            if self.current_light == data:
                return "is the same"

            # Light update
            self.current_light = data

            change = StateChange(self.name)
            change.sensor_id = "1"
            change.data_item = "label"
            change.value = str(data) + "%"
            self.state_change_queue.put(change)

            change = StateChange(self.name)
            change.sensor_id = "1"
            change.data_item = "light"
            change.value = data
            self.state_change_queue.put(change)
        elif pid == 104:
            # Current pos
            # self.current_pos = random.randint(data, 100)
            if self.current_pos == data:
                return "is the same"

            self.current_pos = data

            change = StateChange(self.name)
            change.data_item = "labelHatch open"
            change.value = str(self.current_pos) + "%"
            self.state_change_queue.put(change)

            change = StateChange(self.name)
            change.data_item = "hatch_open"
            change.value = self.current_pos
            self.state_change_queue.put(change)
        elif pid == 105:
            if self.current_distance == data:
                return "is the same"

            # Distance update
            self.current_distance = data

            change = StateChange(self.name)
            change.data_item = "labelDistance"
            change.value = str(self.current_distance) + " cm"
            self.state_change_queue.put(change)

            change = StateChange(self.name)
            change.data_item = "distance"
            change.value = self.current_distance
            self.state_change_queue.put(change)

        else:
            return "unknown packet id"

        return ""


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

        temp -= 5
        temp *= 10

        self.write_queue.put(Client.WriteReq(11, temp))

    def set_threshold_close_temperature(self, temp):
        """
        Send packet to set the threshold temperature to close the latch
        (packet 12)

        temp: int tenth degrees celcius.
        """

        temp -= 5
        temp *= 10

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

    def set_servo_open_perc(self, perc):
        """
        Send packet to set the open position of the servo
        (packet 15).

        perc: 
        """

        val = perc/100*35+35

        self.write_queue.put(Client.WriteReq(15, int(val)))

    def set_servo_close_perc(self, perc):
        """
        Send packet to set the close position of the servo
        (packet 15).

        perc: 
        """

        val = perc/100*35+35

        self.write_queue.put(Client.WriteReq(16, int(val)))
