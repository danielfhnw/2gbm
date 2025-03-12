from dotenv import load_dotenv
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                  # Uses STServo SDK library   

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

# Try to ping the STServo
# Get STServo model number
for i in range(20):
    sts_model_number, sts_comm_result, sts_error = packetHandler.ping(i+1)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    else:
        print("[ID:%03d] ping Succeeded. STServo model number : %d" % (i+1, sts_model_number))
    if sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

# Close port
portHandler.closePort()
