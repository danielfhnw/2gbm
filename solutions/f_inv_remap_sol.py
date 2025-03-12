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

parser = argparse.ArgumentParser(description="get angle1 and angle2")
parser.add_argument("angle1", type=float, help="angle1")
parser.add_argument("angle2", type=float, help="angle2")
args = parser.parse_args()





def get_servo2(angle2):
    offset = 3630
    pos2 = (-angle2 * 4000 / (2 * np.pi) + offset) % 4000
    return pos2

def get_servo1(angle1):
    # TODO implement angle calculation
    # INFO motor position is in range 0-4000
    # Output is in radians
    pos1 = 0
    return pos1





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
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                values = line.split(",")
                
                if len(values) == 2:  # Check we received all four values

                    # remap sensor values to corresponing axis
                    speed1 = int(values[1])*10
                    speed2 = int(values[0])*10
                                    
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
                
                    # Write STServo goal position/moving speed/moving acc
                    sts_comm_result, sts_error = packetHandler.WritePosEx(STS_ID_2, soll_pos2, 500, 0)
                    if sts_comm_result != COMM_SUCCESS:
                        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
                    if sts_error != 0:
                        print("%s" % packetHandler.getRxPacketError(sts_error))

                    print(f"servo1: {get_servo1(args.angle1)}, servo2_soll: {get_servo2(args.angle2)}, servo2_ist: {servo_position2}")

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
