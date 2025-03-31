import json

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

points = [
    {"x": 60, "y": 60},
    {"x": 90, "y": 60},
    {"x": 90, "y": 90},
    {"x": 75, "y": 105},
    {"x": 60, "y": 90},
    {"x": 60, "y": 60},
    {"x": 90, "y": 90},
    {"x": 60, "y": 90},
    {"x": 90, "y": 60}
]


with open("paths/points.json", "w") as f:
    json.dump(points, f, indent=4)  # Pretty print with indentation