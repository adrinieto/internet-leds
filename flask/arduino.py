import time
import serial


class Arduino:
    def __init__(self, port, baudrate=9600, read_timeout=5, write_timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.read_timeout = read_timeout
        self.write_timeout = write_timeout
        self.serial = None
        self._leds = []

    @property
    def leds(self):
        if not self.serial:
            self.open_serial()
        return self._leds

    def open_serial(self):
        """
        Opens a serial connection with the Arduino

        NOTE: If we call this function from the constructor with Flask debug=True it gives PermissionError
        """
        self.serial = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.read_timeout,
                                    writeTimeout=self.write_timeout)
        led_count = int(self.serial.readline())
        self._leds = [dict(id=i, state=False) for i in range(led_count)]

    def write_led_state(self, led_id, state):
        if not self.serial:
            self.open_serial()
        state_string = "on" if state else "off"
        action = "led{} {}\n".format(led_id, state_string)
        self.serial.write(bytes(action, 'utf-8'))
        self.serial.readline()  # Read the previous line
        response = self.serial.readline().decode("utf-8")
        state_led = response.split()[1]
        self._leds[led_id]['state'] = True if state_led == 'on' else False


if __name__ == "__main__":
    arduino = Arduino("COM4")
    print("{} leds".format(len(arduino.leds)))
    time.sleep(2)
    arduino.write_led_state(0, True)
    arduino.write_led_state(1, True)
    print(arduino.leds)
    time.sleep(0.5)
    arduino.write_led_state(0, False)
    time.sleep(0.5)
    arduino.write_led_state(1, False)
    print(arduino.leds)
