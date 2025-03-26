import sys
import os
import serial
import json
import numpy as np
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library
from h_check_workspace import check_elbow_left
from i_invKin import inverse_kinematics
from j_syncMove import get_speeds
from k_syncMove import adjust_speeds
import unit_tests.P2P_utils as P2P_utils
filepath = os.path.join(parent_dir, "paths/points.json")

def read_points():
    with open(filepath, "r") as file:
       points = json.load(file)
    return points

# ------------------------------------------------------------------------------------------------

# TODO change code only inside the moveP2P function



def moveP2P(points):  
    for point in points:
        x = int(point["x"])
        y = int(point["y"])
        print("Moving to point: ", x, y)
        if check_elbow_left(x, y):
            # TODO move to all the points in the list
            # INFO P2P_utils.read_servo_pos(1) returns the current position of servo 1
            # INFO P2P_utils.write_servo_pos(1, soll_pos1, speed1) writes the position and speed to servo 1
            time.sleep(2)
            print("Point reached")
        else:
            print("Point is not in elbow left workspace")





# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    P2P_utils.init_multiturn()
    points = read_points()
    try:
        moveP2P(points)

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        P2P_utils.portHandler.closePort() # Close port

