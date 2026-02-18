import argparse
import sys
import os
import serial
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library

def check_id(id):
    if 1 <= id <= 20:
        print("ID is valid.")
        return True
    else:
        print("Invalid IDs: must be between 1 and 20 (inclusive).")
        return False

parser = argparse.ArgumentParser(description="Check if the ID is within range (1-20).")
parser.add_argument(
    "id",
    type=int,
    nargs="?",          # makes it optional
    default=2,          # default value if not provided
    help="Servo ID (1-20), default is 2"
)
args = parser.parse_args()

if check_id(args.id):
    print("Proceeding with the operation.")
else:
    print("Operation aborted.")
    quit()

load_dotenv()
com_port_motor = os.getenv("COM_PORT_MOTOR")
portHandler = PortHandler(com_port_motor)
packetHandler = sts(portHandler)

com_port_nano = os.getenv("COM_PORT_NANO")
ser = serial.Serial(com_port_nano, 115200, timeout=1)

STS_MOVING_ACC              = 50          # STServo moving acc
STS_ID                      = args.id           # STServo ID

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

# change Servos to Wheel Mode
sts_comm_result, sts_error = packetHandler.WheelMode(STS_ID)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            values = line.split(",")
            
            if len(values) == 2:  # Check we received all four values

                # remap sensor values to corresponing axis
                speed = int(values[0])*10
                                
                # Read STServo present position
                servo_position, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(STS_ID)
                if sts_comm_result != COMM_SUCCESS:
                    print(packetHandler.getTxRxResult(sts_comm_result))
                if sts_error != 0:
                    print(packetHandler.getRxPacketError(sts_error))
            
                # Write STServo goal position/moving speed/moving acc
                sts_comm_result, sts_error = packetHandler.WriteSpec(STS_ID, speed, 0)
                if sts_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
                if sts_error != 0:
                    print("%s" % packetHandler.getRxPacketError(sts_error))

                print(f"Position: {servo_position}, Geschwindigkeit: {servo_speed}")

except KeyboardInterrupt:
    print("Program stopped")

finally:
    ser.close()  # Close the serial connection when done
    sts_comm_result, sts_error = packetHandler.WriteSpec(STS_ID, 0, 0)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    if sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))
    portHandler.closePort() # Close port
