from Robot import Robot

if __name__ == "__main__":
    robot = Robot()
    try:
        x, y = map(float, input("set tcp position (x y): ").split())
        result = robot.set_tcp_position([x, y, 0, 1])
        if not result:
            print("Failed to set TCP position. TCP position may be out of reach.")
            raise KeyboardInterrupt
        while True:
            robot.print_tcp_position()
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        robot.shutdown()