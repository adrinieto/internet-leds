import serial


class Arduino:
    def __init__(self):
        self.serial = serial.Serial("COM8", baudrate=9600, timeout=5, writeTimeout=2)

    def write_led_state(self, led_id, state):
        state_string = "on" if state else "off"
        action = "led{} {}\n".format(led_id, state_string)
        self.serial.write(bytes(action, 'utf-8'))
