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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get angle1 and angle2")
    parser.add_argument("angle1", type=float, help="angle1")
    parser.add_argument("angle2", type=float, help="angle2")
    args = parser.parse_args()
# ------------------------------------------------------------------------------------------------





def get_servo2(angle2):
    if angle2 >= 0:
        return -32768 - (-angle2 * 4096 / (2 * np.pi))
    else:
        return (-angle2 * 4096 / (2 * np.pi))

def get_servo1(angle1):
    if angle1 > 0 or angle1 < -np.pi:
        print("angle1 is out of range")
        exit()
    if angle1 >= 0:
        return -32768 - (-angle1 * 4096 / (2 * np.pi))
    else:
        return (-angle1 * 4096 / (2 * np.pi))





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
    sts_comm_result, sts_error = packetHandler.ServoMode(STS_ID_1)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))  

    sts_comm_result, sts_error = packetHandler.ServoMode(STS_ID_2)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))    
    
    sts_comm_result, sts_error = packetHandler.set_max_angle(STS_ID_1, 0)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

    sts_comm_result, sts_error = packetHandler.set_min_angle(STS_ID_1, 0)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

    sts_comm_result, sts_error = packetHandler.set_multiturn(STS_ID_1)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

        sts_comm_result, sts_error = packetHandler.set_max_angle(STS_ID_2, 0)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

    sts_comm_result, sts_error = packetHandler.set_min_angle(STS_ID_2, 0)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

    sts_comm_result, sts_error = packetHandler.set_multiturn(STS_ID_2)
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

            soll_pos2 = int(get_servo2(args.angle2))
            soll_pos1 = int(get_servo1(args.angle1))
        
            # Write STServo goal position/moving speed/moving acc
            sts_comm_result, sts_error = packetHandler.WritePosEx(STS_ID_1, soll_pos1, 1000, 0)
            if sts_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print("%s" % packetHandler.getRxPacketError(sts_error))

            sts_comm_result, sts_error = packetHandler.WritePosEx(STS_ID_2, soll_pos2, 1000, 0)
            if sts_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print("%s" % packetHandler.getRxPacketError(sts_error))

            print(f"servo1_soll: {soll_pos1}, servo1_ist: {servo_position1}, servo2_soll: {soll_pos2}, servo2_ist: {servo_position2}")

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        ser.close()  # Close the serial connection when done
        portHandler.closePort() # Close port
