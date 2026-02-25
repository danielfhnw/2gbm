import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get x and y")
    parser.add_argument("x", type=float, help="x_soll")
    parser.add_argument("y", type=float, help="y_soll")
    args = parser.parse_args()
# ------------------------------------------------------------------------------------------------





def check_elbow_left(x, y):
    r = 75
    if (x + r) ** 2 + y ** 2 < r ** 2:
        return False
    if (x - r) ** 2 + y ** 2 <= r ** 2:
        return True
    if y < 0:
        return False
    if x ** 2 + y ** 2 <= (2 * r) ** 2:
        return True
    return False

def check_elbow_right(x, y):
    r = 75
    if (x + r) ** 2 + y ** 2 <= r ** 2:
        return True
    if (x - r) ** 2 + y ** 2 < r ** 2:
        return False
    if y < 0:
        return False
    if x ** 2 + y ** 2 <= (2 * r) ** 2:
        return True
    return False
    




# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Coordinates x: {args.x}, y: {args.y} are in the workspace with elbow left configuration: {check_elbow_left(args.x, args.y)}")
    print(f"Coordinates x: {args.x}, y: {args.y} are in the workspace with elbow right configuration: {check_elbow_right(args.x, args.y)}")