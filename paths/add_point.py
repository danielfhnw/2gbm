import os
import sys
import json
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from solutions.d_forwKin_sol import forward_kinematics
from unit_tests.Wheel_utils import init, read_servo_pos

def add_point():
    if not os.path.exists("paths/points.json"):
            with open("paths/points.json", "w") as file:
                json.dump([], file)  # Initialize with an empty list

    with open("paths/points.json", "r") as file:
        points = json.load(file)

    point = forward_kinematics(read_servo_pos(1), read_servo_pos(2))
    print("Add new point: ", point)

    points.append({"x": point[0], "y": point[1], "gripper": 0}) 

    with open("paths/points.json", "w") as file:
        json.dump(points, file, indent=4)  # Pretty print with indentation

if __name__ == "__main__":
    init()
    add_point()