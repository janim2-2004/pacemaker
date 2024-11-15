import serial 

com = serial.Serial("COM3", 115200, timeout=60)

class egram_data:
        def __init__(self, time, value):
            self.time = time
            self.value = value

        def read_egram_data(self):
            #read egram data
            com.write("0x77")
            raw_data = com.read()
            #decode raw data
            decoded_data = raw_data.decode('utf-8').strip()
            time, value = map(float, decoded_data.split(','))

            return egram_data(time,value)
            









