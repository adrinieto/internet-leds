import time
import serial


class Arduino:
    def __init__(self):
        self.serial = None

    def open_serial(self):
        """
        Opens a serial connection with the Arduino

        NOTE: If we call this function from the constructor with Flask debug=True it gives PermissionError
        """
        self.serial = serial.Serial("COM8", baudrate=9600, timeout=5, writeTimeout=2)

    def write_led_state(self, led_id, state):
        if not self.serial:
            self.open_serial()
        state_string = "on" if state else "off"
        action = "led{} {}\n".format(led_id, state_string)
        self.serial.write(bytes(action, 'utf-8'))


if __name__ == "__main__":
    arduino = Arduino()
    time.sleep(2)
    arduino.write_led_state(0, True)
    arduino.write_led_state(1, True)
    time.sleep(0.5)
    arduino.write_led_state(0, False)
    time.sleep(0.5)
    arduino.write_led_state(1, False)
