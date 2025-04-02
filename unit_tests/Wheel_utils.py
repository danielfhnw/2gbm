import sys
import os
import serial
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # unit_test/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *                 # Uses STServo SDK library

def init():
    global portHandler
    global packetHandler
    global ser

    load_dotenv()
    com_port_motor = os.getenv("COM_PORT_MOTOR")
    portHandler = PortHandler(com_port_motor)
    packetHandler = sts(portHandler)

    com_port_nano = os.getenv("COM_PORT_NANO")
    ser = serial.Serial(com_port_nano, 115200, timeout=1)  # Open serial port for Arduino Nano
    
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

def get_joystick():
    while True:
        if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                values = line.split(",")
                
                if len(values) == 2:  # Check we received all values
                    updown = int(values[0])
                    leftright = int(values[1])
                    return [leftright, updown]
            

def read_servo_pos(id):
    servo_position, servo_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(id)
    if sts_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(sts_comm_result))
    if sts_error != 0:
        print(packetHandler.getRxPacketError(sts_error))
    return servo_position

def write_servo_speed(id, speed):
    sts_comm_result, sts_error = packetHandler.WriteSpec(id, speed, 255)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    if sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))

def change_hold(hold):
    sts_comm_result, sts_error = packetHandler.change_hold(1, hold)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))
    sts_comm_result, sts_error = packetHandler.change_hold(2, hold)
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler.getRxPacketError(sts_error))
    print("hold: %s" % hold)