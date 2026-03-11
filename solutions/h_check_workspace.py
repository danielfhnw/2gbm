from Robot import Robot

if __name__ == "__main__":
    robot = Robot()
    try:
        x, y = map(float, input("set tcp position (x y): ").split())
        result =robot.check_workspace([x, y, 0, 1], elbow_left=True)
        if result:
            print("Position is reachable")
        else:
            print("Position is not reachable")
        
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        robot.shutdown()