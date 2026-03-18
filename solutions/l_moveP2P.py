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
        x, y = map(float, input("set tcp position (x y): ").split())
        start_position = robot.get_tcp_position()
        result = robot.move_l([x, y, 0, 1], start_position=start_position)
        result = robot.move_l([0, 66, 0, 1], start_position=[x, y, 0, 1])
        #result = robot.move_l([x, y, 0, 1], start_position=[0, 66, 0, 1])
        #result = robot.move_l([0, 66, 0, 1], start_position=[x, y, 0, 1])
        if not result:
            print()
            print("Failed to set TCP position. TCP position may be out of reach.")
            stop_requested = True
        while not stop_requested:
            robot.move()
            robot.print_tcp_position()
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()