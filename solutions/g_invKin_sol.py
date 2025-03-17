import argparse
import sys
import os
import serial
import numpy as np
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library
from f_inv_remap_sol import get_servo1, get_servo2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get x and y")
    parser.add_argument("x", type=float, help="x_soll")
    parser.add_argument("y", type=float, help="y_soll")
    args = parser.parse_args()
# ------------------------------------------------------------------------------------------------





def inverse_kinematics(x, y):
    theta2 = np.arctan2(y, x)
    servo_pos = get_servo2(theta2)
    return servo_pos





# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    load_dotenv()
    com_port_motor = os.getenv("COM_PORT_MOTOR")
    portHandler = PortHandler(com_port_motor)
    packetHandler = sts(portHandler)

    com_port_nano = os.getenv("COM_PORT_NANO")
    ser = serial.Serial(com_port_nano, 115200, timeout=1)

    STS_MOVING_ACC              = 50          # STServo moving acc
    STS_ID_1                      = 1           # STServo ID
    STS_ID_2                      = 2           # STServo ID


    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(1000000):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        quit()

    # change Servos to Servo Mode
    sts_comm_result, sts_error = packetHandler.ServoMode(STS_ID_2)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))    
    

    try:
        once = True
        while once:
            once = False
            # Read STServo present position
            servo_position1, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(STS_ID_1)
            if sts_comm_result != COMM_SUCCESS:
                print(packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print(packetHandler.getRxPacketError(sts_error))
            servo_position2, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(STS_ID_2)
            if sts_comm_result != COMM_SUCCESS:
                print(packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print(packetHandler.getRxPacketError(sts_error))

            soll_pos1 = 0
            soll_pos2 = int(inverse_kinematics(args.x, args.y))
        
            # Write STServo goal position/moving speed/moving acc
            sts_comm_result, sts_error = packetHandler.WritePosEx(STS_ID_2, soll_pos2, 500, 50)
            if sts_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print("%s" % packetHandler.getRxPacketError(sts_error))

            print(f"servo1: {soll_pos1}, servo2: {soll_pos2}")

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        ser.close()  # Close the serial connection when done
        portHandler.closePort() # Close port
