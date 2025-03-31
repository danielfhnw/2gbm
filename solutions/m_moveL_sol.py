import sys
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library
from h_check_workspace_sol import check_elbow_left
from i_invKin_sol import inverse_kinematics
from j_syncMove_sol import get_speeds
from k_syncMove_sol import adjust_speeds
from l_moveP2P_sol import moveP2P, verschleifen
import unit_tests.P2P_utils as P2P_utils
filepath = os.path.join(parent_dir, "paths/points.json")

def read_points():
    with open(filepath, "r") as file:
       points = json.load(file)
    return points

# ------------------------------------------------------------------------------------------------





def moveL(points):
    x_old = int(points[0]["x"])
    y_old = int(points[0]["y"])
    for point in points:
        x = int(point["x"])
        y = int(point["y"])
        if x != x_old or y != y_old:
            if check_elbow_left(x, y):
                print("Moving to point: ", x, y)
                rx = x - x_old
                ry = y - y_old
                n = 11
                for i in range(1, n):
                    x_interp = int(x_old + (rx * i) / 10)
                    y_interp = int(y_old + (ry * i) / 10)
                    soll_pos = inverse_kinematics(x_interp, y_interp)
                    soll_pos1 = int(soll_pos[0])
                    soll_pos2 = int(soll_pos[1])
                    speeds = adjust_speeds(get_speeds(P2P_utils.read_servo_pos(1), soll_pos1, P2P_utils.read_servo_pos(2), soll_pos2))
                    speed1 = int(speeds[0])
                    speed2 = int(speeds[1])
                    P2P_utils.write_servo_pos(1, soll_pos1, speed1)
                    P2P_utils.write_servo_pos(2, soll_pos2, speed2)
                    while verschleifen(x_interp, y_interp):
                        pass
                    #time.sleep(1.5/n)
                print("Point reached")
                x_old = x
                y_old = y
            else:
                print("Point is not in elbow left workspace")

    
    


# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    P2P_utils.init_multiturn()
    points = read_points()
    try:
        moveP2P([points[0]])
        moveL(points)

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        P2P_utils.portHandler.closePort() # Close port

