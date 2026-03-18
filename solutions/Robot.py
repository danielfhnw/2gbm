from Motor import Motor
import sys
import os
import numpy as np
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

        self.path = []

    def shutdown(self):
        self.motor_1.shutdown()
        self.motor_2.shutdown()
        self.port_handler.closePort()
        print("Robot shutdown")
  
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
        theta1, theta2 = self.get_motor_positions()
        T54 = np.array([
            [1, 0, 0, 75],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        T43 = np.array([
            [np.cos(theta2), -np.sin(theta2), 0, 0],
            [np.sin(theta2),  np.cos(theta2), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        T32 = np.array([
            [1, 0, 0, -75],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        T21 = np.array([
            [np.cos(theta1), -np.sin(theta1), 0, 0],
            [np.sin(theta1),  np.cos(theta1), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        T10 = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 66],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        p = np.array([0, 0, 0, 1])
        p = T10 @ T21 @ T32 @ T43 @ T54 @ p

        return p
    
    def set_tcp_position(self, tcp_position):
        # solution for startexercise, not for general case
        # theta2 = np.arctan(tcp_position[1] / tcp_position[0])
        # self.motor_2.set_position(theta2)   
        # return True    

        if not self.check_workspace(tcp_position, elbow_left=True):
            return False

        x = tcp_position[0]
        y = tcp_position[1]

        y = y - 66 # differenz zum joystick

        theta2 = np.arccos((75**2 + 75**2 - (x**2 + y**2)) / (2*75*75))
        theta1 = -np.pi/2 + np.arctan2(y,x) - theta2/2

        self.move_sync(theta1, theta2)
        return True
    
    def move_sync(self, theta1_soll, theta2_soll, speed=1000):
        theta1_ist = self.motor_1.get_position()
        theta2_ist = self.motor_2.get_position()

        theta1_diff = abs(theta1_soll - theta1_ist)
        theta2_diff = abs(theta2_soll - theta2_ist)

        if theta1_diff > theta2_diff:
            speed1 = speed
            speed2 = speed * theta2_diff / theta1_diff
        else:
            speed2 = speed
            speed1 = speed * theta1_diff / theta2_diff

        self.motor_1.set_position(theta1_soll, speed1)
        self.motor_2.set_position(theta2_soll, speed2)

    def check_workspace(self, tcp_position, elbow_left=True):
        x, y = tcp_position[0], tcp_position[1]
        y = y - 66 # differenz zum joystick
        r = 75
        if elbow_left:
            if (x + r) ** 2 + y ** 2 < r ** 2:
                return False
            if (x - r) ** 2 + y ** 2 <= r ** 2:
                return True
            if y < 0:
                return False
            if x ** 2 + y ** 2 <= (2 * r) ** 2:
                return True
            return False
        else:
            if (x + r) ** 2 + y ** 2 <= r ** 2:
                return True
            if (x - r) ** 2 + y ** 2 < r ** 2:
                return False
            if y < 0:
                return False
            if x ** 2 + y ** 2 <= (2 * r) ** 2:
                return True
            return False
    
    def print_tcp_position(self):
        p = self.get_tcp_position()
        x, y = p[0], p[1]
        print(f"\rTCP position: x={x:<6} | y={y:<6}", end="", flush=True)

    def move_l(self, target_position, start_position, step_size=50):
        if not self.check_workspace(target_position, elbow_left=True):
            return False
        
        distance = np.linalg.norm(np.array(target_position) - np.array(start_position))
        if distance < step_size:
                self.path.append(target_position)
                return True
        else:
            step_count = distance / step_size
            direction = (np.array(target_position) - np.array(start_position)) / step_count
            for i in range(1, int(np.floor(step_count)) + 1):
                intermediate_position = start_position + direction * i
                self.path.append((start_position + direction * i).tolist())
                if not self.check_workspace(intermediate_position, elbow_left=True):
                    return False
            self.path.append(target_position)
            return True
    
    def move(self, tolerance=2):
        if self.path:
            target_position = self.path[0]
            current_position = self.get_tcp_position()
            if np.linalg.norm(np.array(target_position) - np.array(current_position)) < tolerance:
                self.path.pop(0)
            else:
                self.set_tcp_position(target_position)