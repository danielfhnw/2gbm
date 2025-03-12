from dotenv import load_dotenv
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library


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

sts_comm_result, sts_error = packetHandler.ServoMode(1)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))
sts_comm_result, sts_error = packetHandler.ServoMode(2)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

servo_position1, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(1)
if sts_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(sts_comm_result))
if sts_error != 0:
    print(packetHandler.getRxPacketError(sts_error))
servo_position2, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(2)
if sts_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(sts_comm_result))
if sts_error != 0:
    print(packetHandler.getRxPacketError(sts_error))

print(f"SERVO -> servo1: {servo_position1}, servo2: {servo_position2}")

# Close port
portHandler.closePort()
