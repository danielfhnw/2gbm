from Motor import Motor
import sys
import os
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # oop/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *    

class Robot:
    def __init__(self):
        load_dotenv()
        self.port_handler = PortHandler(os.getenv("COM_PORT_MOTOR"))
        self.packet_handler = sts(self.port_handler)
        
        # open port
        if self.port_handler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()

        # set baudrate
        if self.port_handler.setBaudRate(1000000):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

        offset_servo1 = os.getenv("OFFSET_SERVO_1")
        self.motor_1 = Motor(1, int(offset_servo1) if offset_servo1 else 0, self.packet_handler)
        offset_servo2 = os.getenv("OFFSET_SERVO_2")
        self.motor_2 = Motor(2, int(offset_servo2) if offset_servo2 else 0, self.packet_handler)

    def shutdown(self):
        self.motor_1.shutdown()
        self.motor_2.shutdown()
        self.port_handler.closePort()
  
    def get_motor_positions(self, raw=False):
        if raw:
            pos1 = self.motor_1.get_position_raw()
            pos2 = self.motor_2.get_position_raw()
        else:
            pos1 = self.motor_1.get_position()
            pos2 = self.motor_2.get_position()
        return pos1, pos2

    def print_motor_positions(self, raw=False):
        pos1, pos2 = self.get_motor_positions(raw)
        print(f"\rMotor_1: {pos1:<6} | Motor_2: {pos2:<6}", end="", flush=True)

    def get_tcp_position(self):
        # TODO implement forward kinematics


        return 0, 0
    
    def print_tcp_position(self):
        x, y = self.get_tcp_position()
        print(f"\rTCP position: x={x:<6} | y={y:<6}", end="", flush=True)