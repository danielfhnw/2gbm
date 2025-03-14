import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get x and y")
    parser.add_argument("x", type=float, help="x_soll")
    parser.add_argument("y", type=float, help="y_soll")
    args = parser.parse_args()
# ------------------------------------------------------------------------------------------------

# TODO change code only inside the check_ functions



def check_elbow_left(x, y):
    # TODO check if x and y are in the workspace with elbow left configuration
    return False

def check_elbow_right(x, y):
    # TODO check if x and y are in the workspace with elbow right configuration
    return False
    




# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Coordinates x: {args.x}, y: {args.y} are in the workspace with elbow left configuration: {check_elbow_left(args.x, args.y)}")
    print(f"Coordinates x: {args.x}, y: {args.y} are in the workspace with elbow right configuration: {check_elbow_right(args.x, args.y)}")