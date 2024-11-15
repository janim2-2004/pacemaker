
import serial

PORT = "COM4"

s = serial.Serial(PORT, 115200, timeout = 60)

s.reset_output_buffer()
s.reset_input_buffer()

measurment = s.readline().decode().split()