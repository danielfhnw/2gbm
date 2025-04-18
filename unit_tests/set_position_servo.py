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
    parser = argparse.ArgumentParser(description="get servo1 and servo2")
    parser.add_argument("servo1", type=int, help="servo1")
    parser.add_argument("servo2", type=int, help="servo2")
    args = parser.parse_args()

load_dotenv()

com_port_motor = os.getenv("COM_PORT_MOTOR")
portHandler = PortHandler(com_port_motor)
packetHandler = sts(portHandler)


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

sts_comm_result, sts_error = packetHandler.ServoMode(2)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

sts_comm_result, sts_error = packetHandler.set_multiturn(2)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

sts_comm_result, sts_error = packetHandler.set_min_angle(2, 0)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

sts_comm_result, sts_error = packetHandler.set_max_angle(2, 0)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

sts_comm_result, sts_error = packetHandler.WritePosEx(2, args.servo2, 1000, 0)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
if sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

print(f"SERVO -> servo1_soll: {args.servo1}, servo2_soll: {args.servo2}")

# Close port
portHandler.closePort()
