from Robot import Robot
import signal

stop_requested = False

def handle_sigint(sig, frame):
    global stop_requested
    print("\nSIGINT received, stopping...")
    stop_requested = True

if __name__ == "__main__":
    robot = Robot()

    signal.signal(signal.SIGINT, handle_sigint)

    try:
        pos_1, pos_2 = map(float, input("set motor angles in radians (theta1 theta2): ").split())
        robot.motor_1.set_position(pos_1)
        robot.motor_2.set_position(pos_2)
        while not stop_requested:
            robot.print_motor_positions()
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()