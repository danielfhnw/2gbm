import argparse
import sys
import os
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get speed for servo1")
    parser.add_argument("speed1", type=int, help="speed1")
    args = parser.parse_args()

    load_dotenv()

    com_port_motor = os.getenv("COM_PORT_MOTOR")
    portHandler = PortHandler(com_port_motor)
    packetHandler = sts(portHandler)
        
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

    sts_comm_result, sts_error = packetHandler.WheelMode(1)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

    try:
        while True:
            # Read STServo present position
            servo_position, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(1)
            if sts_comm_result != COMM_SUCCESS:
                print(packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print(packetHandler.getRxPacketError(sts_error))

            # Write STServo goal position/moving speed/moving acc
            sts_comm_result, sts_error = packetHandler.WriteSpec(1, args.speed1, 0)
            if sts_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(sts_comm_result))
            if sts_error != 0:
                print("%s" % packetHandler.getRxPacketError(sts_error))

            print(f"Position: {servo_position}, Geschwindigkeit: {servo_speed}")

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        sts_comm_result, sts_error = packetHandler.WriteSpec(STS_ID, 0, 0)
        if sts_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(sts_comm_result))
        if sts_error != 0:
            print("%s" % packetHandler.getRxPacketError(sts_error))
        portHandler.closePort() # Close port
