import argparse
from dotenv import load_dotenv
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library


def check_ids(id1, id2):
    if all(1 <= i <= 20 for i in (id1, id2)):
        print("Both IDs are valid.")
        return True
    else:
        print("Invalid IDs: Both must be between 1 and 20 (inclusive).")
        return False

# Set up argument parsing
parser = argparse.ArgumentParser(description="Check if two IDs are within range (1-20).")
parser.add_argument("id_old", type=int, help="First ID (1-20)")
parser.add_argument("id_new", type=int, help="Second ID (1-20)")

args = parser.parse_args()

# Validate the IDs
if check_ids(args.id_old, args.id_new):
    print("Proceeding with the operation.")
else:
    print("Operation aborted.")
    quit()

load_dotenv()

com_port_motor = os.getenv("COM_PORT_MOTOR")
portHandler = PortHandler(com_port_motor)
packetHandler = sts(portHandler)


portHandler = PortHandler(com_port_motor)
packetHandler = scscl(portHandler)
    
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

sts_comm_result, sts_error = packetHandler.changeID(args.id_old, args.id_new) 
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))
    print("Now STServo ID is %d" % args.id_new)

# Close port
portHandler.closePort()
