import sys
import os
import time
import json
import numpy as np
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
import unit_tests.Wheel_utils as Wheel_utils
from add_point import add_point
from solutions.a_remap_sol import get_angle1, get_angle2
filepath = os.path.join(parent_dir, "paths/points.json")

def read_points():
    with open(filepath, "r") as file:
       points = json.load(file)
    return points

# ------------------------------------------------------------------------------------------------





def invJ(joystick1, joystick2, theta1, theta2):
    speed1 = (((-np.cos(theta1+theta2))/(75*np.sin(theta2))) * joystick1) + (((-np.sin(theta1+theta2))/(75*np.sin(theta2))) * joystick2)
    speed2 = (((np.cos(theta1+theta2) - np.cos(theta1))/(75*np.sin(theta2))) * joystick1) + (((np.sin(theta1+theta2) - np.sin(theta1))/(75*np.sin(theta2))) * joystick2)

    speed1 = -speed1 * 4096 / 2 / np.pi
    speed2 = -speed2 * 4096 / 2 / np.pi
    print("Speed1: ", speed1, "Speed2: ", speed2)
    return [speed1, speed2]

    
    


# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    Wheel_utils.init()
    try:
        i = 0
        while True:
            i = i + 1
            joystick = Wheel_utils.get_joystick()
            speeds = invJ(joystick[0], joystick[1], get_angle1(Wheel_utils.read_servo_pos(1)), get_angle2(Wheel_utils.read_servo_pos(2)))
            Wheel_utils.write_servo_speed(1, int(speeds[0]))
            Wheel_utils.write_servo_speed(2, int(speeds[1]))
            if i > 50:
                i = 0
                add_point()

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        Wheel_utils.portHandler.closePort() # Close port

