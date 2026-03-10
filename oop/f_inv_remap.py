from Robot import Robot

if __name__ == "__main__":
    robot = Robot()
    try:
        pos_1, pos_2 = map(float, input("set motor angles in radians (theta1 theta2): ").split())
        robot.motor_1.set_position(pos_1)
        robot.motor_2.set_position(pos_2)
        while True:
            robot.print_motor_positions()
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        robot.shutdown()