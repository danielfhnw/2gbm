import sys
import os
import serial
import numpy as np
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library
from a_remap_sol import get_angle1, get_angle2





def forward_kinematics(servo_position1, servo_position2):
    theta1 = get_angle1(servo_position1)
    theta2 = get_angle2(servo_position2)
    # TODO implement forward kinematics from coordinate system 5 to 1
    # INFO p is the position of the end effector
    T54 = np.array([
        [1, 0, 0, 75],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    T43 = np.array([
        [np.cos(theta2), -np.sin(theta2), 0, 0],
        [np.sin(theta2),  np.cos(theta2), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    T32 = np.array([
        [1, 0, 0, -75],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    T21 = np.array([
        [np.cos(theta1), -np.sin(theta1), 0, 0],
        [np.sin(theta1),  np.cos(theta1), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    p = np.array([0, 0, 0, 1])
    p = T21 @ T32 @ T43 @ T54 @ p
    return p




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

    # change Servos to Wheel Mode
    sts_comm_result, sts_error = packetHandler.WheelMode(STS_ID_1)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))
    sts_comm_result, sts_error = packetHandler.WheelMode(STS_ID_2)
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
                    coords = forward_kinematics(servo_position1, servo_position2)
                
                    # Write STServo goal position/moving speed/moving acc
                    sts_comm_result, sts_error = packetHandler.WriteSpec(STS_ID_1, speed1, 0)
                    if sts_comm_result != COMM_SUCCESS:
                        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
                    if sts_error != 0:
                        print("%s" % packetHandler.getRxPacketError(sts_error))
                    sts_comm_result, sts_error = packetHandler.WriteSpec(STS_ID_2, speed2, 0)
                    if sts_comm_result != COMM_SUCCESS:
                        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
                    if sts_error != 0:
                        print("%s" % packetHandler.getRxPacketError(sts_error))

                    print(f"x: {coords[0]}, y: {coords[1]}")

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
