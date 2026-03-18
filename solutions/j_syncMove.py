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
        result = robot.set_tcp_position([x, y, 0, 1])
        if not result:
            print()
            print("Failed to set TCP position. TCP position may be out of reach.")
        while not stop_requested:
            robot.print_tcp_position()
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()