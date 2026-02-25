from Robot import Robot

if __name__ == "__main__":
    robot = Robot()
    try:
        while True:
            robot.print_motor_positions(raw=True)
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        robot.shutdown()