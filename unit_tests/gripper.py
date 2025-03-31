import argparse
from dotenv import load_dotenv
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library

def grip(portHandler, closed):
    packetHandlerSC = scscl(portHandler)

    if closed:
        gripper_soll = 200
    else:
        gripper_soll = 0

    sts_comm_result, sts_error = packetHandlerSC.WritePos(3, gripper_soll, 0, 1000) 
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandlerSC.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandlerSC.getRxPacketError(sts_error))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="set the gripper to open or close")
    parser.add_argument("open", type=int, help="open (1) or close (0)")

    args = parser.parse_args()

    load_dotenv()

    com_port_motor = os.getenv("COM_PORT_MOTOR")
    portHandler = PortHandler(com_port_motor)
    packetHandler = sts(portHandler)


    portHandler = PortHandler(com_port_motor)
    packetHandlerSC = scscl(portHandler)
        
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

    gripper_pos, sts_comm_result, sts_error = packetHandlerSC.ReadPos(3) 
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandlerSC.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandlerSC.getRxPacketError(sts_error))

    print("gripper_pos: %d" % gripper_pos)


    grip(portHandler, int(args.open))


    # Close port
    portHandler.closePort()
