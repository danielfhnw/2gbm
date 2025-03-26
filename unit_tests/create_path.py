import json
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
filepath = os.path.join(parent_dir, "paths/points.json")

points = [
    {"x": 0, "y": 0},
    {"x": 80, "y": 0},
    {"x": 80, "y": 80},
    {"x": 40, "y": 120},
    {"x": 0, "y": 80},
    {"x": 0, "y": 0},
    {"x": 80, "y": 80},
    {"x": 0, "y": 80},
    {"x": 80, "y": 0},
    {"x": 0, "y": 0}
]

with open(filepath, "w") as f:
    json.dump(points, f, indent=4)  # Pretty print with indentation