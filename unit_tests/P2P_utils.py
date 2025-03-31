import sys
import os
import serial
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library

def init_multiturn():
    global portHandler
    global packetHandler

    global SERVO_POS_1
    global SERVO_POS_2
    global SERVO_OFFSET_1
    global SERVO_OFFSET_2

    load_dotenv()
    com_port_motor = os.getenv("COM_PORT_MOTOR")
    portHandler = PortHandler(com_port_motor)
    packetHandler = sts(portHandler)

    com_port_nano = os.getenv("COM_PORT_NANO")

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

    sts_comm_result, sts_error = packetHandler.ServoMode(STS_ID_2)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))    

    sts_comm_result, sts_error = packetHandler.set_multiturn(STS_ID_2)
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

    SERVO_OFFSET_1 = 0
    SERVO_OFFSET_2 = 4096
    SERVO_POS_1 = read_servo_pos(1)
    if SERVO_POS_1 > 3500:
        SERVO_OFFSET_1 = 4096
        SERVO_POS_1 = read_servo_pos(1)
    SERVO_POS_2 = read_servo_pos(2)
    print("Servo 1 Startposition: ", SERVO_POS_1)
    print("Servo 2 Startposition: ", SERVO_POS_2)
    

def read_servo_pos(id):
    servo_position, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(id)
    if sts_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(sts_comm_result))
    if sts_error != 0:
        print(packetHandler.getRxPacketError(sts_error))
    if id == 1:
        servo_position = servo_position - SERVO_OFFSET_1
    if id == 2:
        servo_position = servo_position - SERVO_OFFSET_2
    return servo_position

def write_servo_pos(id, pos, speed):
    # print(" before writing to Servo %d Position: %d" % (id, pos))
    
    if pos < 0:
        pos = -(pos + 32768)

    if id == 1:
        pos = pos + SERVO_OFFSET_1
    if id == 2:
        pos = pos + SERVO_OFFSET_2

    if pos < 0:
         pos = -32768 + pos

    sts_comm_result, sts_error = packetHandler.WritePosEx(id, pos, speed, 255)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    if sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

    # print("writing to Servo %d Position: %d" % (id, pos))