import json

points = [
    {"x": 50, "y": 60, "gripper": 1},
    {"x": 50, "y": 100, "gripper": 0},
    {"x": 50, "y": 80, "gripper": 1},
    {"x": 70, "y": 80, "gripper": 0},
    {"x": 70, "y": 100, "gripper": 1},
    {"x": 70, "y": 60, "gripper": 0},

    {"x": 80, "y": 60, "gripper": 1},
    {"x": 80, "y": 80, "gripper": 0},
    {"x": 100, "y": 80, "gripper": 0},
    {"x": 100, "y": 60, "gripper": 0},
    {"x": 80, "y": 60, "gripper": 0},

    {"x": 110, "y": 60, "gripper": 1},
    {"x": 110, "y": 80, "gripper": 0},
    {"x": 110, "y": 95, "gripper": 1},
    {"x": 110, "y": 100, "gripper": 0},

    {"x": 110, "y": 60, "gripper": 1},
    {"x": 50, "y": 60, "gripper": 1},
    {"x": 50, "y": 60, "gripper": 0},
]



with open("paths/points.json", "w") as f:
    json.dump(points, f, indent=4)  # Pretty print with indentation