from Joystick import Joystick

if __name__ == "__main__":
    joystick = Joystick()
    try:
        while True:
            position = joystick.get_position()
            if position is not None:
                x, y = position
                print(f"\rJoystick position - X: {x:<6} | Y: {y:<6}", end="", flush=True)
    except KeyboardInterrupt:
        print()
        print("Program stopped")
    finally:
        joystick.shutdown()