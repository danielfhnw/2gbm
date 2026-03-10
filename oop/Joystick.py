import serial
import os
from dotenv import load_dotenv

class Joystick:
    def __init__(self):
        load_dotenv()
        self.com_port_nano = os.getenv("COM_PORT_NANO")
        self.ser = serial.Serial(self.com_port_nano, 115200, timeout=1)   

    def shutdown(self):
        self.ser.close()
  
    def get_position_raw(self):
        return self.ser.readline().decode("utf-8").strip()

    def get_position(self):
        position_raw = self.get_position_raw()

        if not position_raw:
            return None

        try:
            x_str, y_str = position_raw.split(",")
            x = int(x_str)
            y = int(y_str)
            return x, y
        except ValueError:
            # malformed line
            return None

