from Robot import Robot
from Joystick import Joystick
import signal

stop_requested = False

def handle_sigint(sig, frame):
    global stop_requested
    print("\nSIGINT received, stopping...")
    stop_requested = True

if __name__ == "__main__":
    robot = Robot()
    joystick = Joystick()

    signal.signal(signal.SIGINT, handle_sigint)

    try:
        robot.change_motor_mode("velocity")
        while not stop_requested:
            robot.print_tcp_position()
            soll = joystick.get_position()
            if soll is not None:
                soll_x, soll_y = soll
                robot.joystick_control(soll_x, soll_y)
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()