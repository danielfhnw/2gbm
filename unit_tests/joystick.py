from dotenv import load_dotenv
import os
import serial

load_dotenv()

com_port_nano = os.getenv("COM_PORT_NANO")
ser = serial.Serial(com_port_nano, 115200, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            values = line.split(",")
            
            if len(values) == 2:  # Check we received all four values
                print(values)



except KeyboardInterrupt:
    print("Program stopped")

finally:
    ser.close()  # Close the serial connection when done