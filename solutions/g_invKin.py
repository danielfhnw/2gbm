from Robot import Robot

if __name__ == "__main__":
    robot = Robot()
    try:
        while True:
            x, y = map(float, input("set tcp position (x y): ").split())
            robot.set_tcp_position([x, y, 0, 1])
            robot.print_tcp_position()
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        robot.shutdown()