from Robot import Robot

if __name__ == "__main__":
    robot = Robot()
    try:
        while True:
            robot.print_tcp_position()
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        robot.shutdown()