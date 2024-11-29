import serial
import struct
from time import sleep

from serial.serialutil import SerialException
from serial.tools.list_ports import comports

class COM:

    def __init__(self):
        self.ser = serial.Serial()
        self.conn = False

    def serialList(self):
        return comports()

    def serOpen(self, serPort):
        
        try:
            self.ser = serial.Serial(port = serPort, baudrate = 115200)
            self.conn = True
        except SerialException:
            self.conn = False
        
    def serClose(self):
        self.ser.close()
        self.conn = False
    
    def serState(self):
        activePort = self.ser.port
        current = ""
        for port in comports():
            if activePort in port:
                current = port
        return [self.conn, current]

    def serWrite(self, paramList):
        mode = paramList[0]
        LRL = paramList[1]
        URL = paramList[2]
        A_Amp = paramList[3]
        A_pw = paramList[4]
        V_Amp = paramList[5]
        V_pw = paramList[6]
        VRP = paramList[7]
        ARP = paramList[8]
        aSens = paramList[9]
        vSens = paramList[10]
        rateAdapt = paramList[11]
        MSR = paramList[12]
        actThresh = paramList[13]
        reactTime = paramList[14]
        resFactor = paramList[15]
        recTime = paramList[16]
        AVdelay = paramList[17]

        mode_b = struct.pack("b", mode)
        LRL_b = struct.pack("B", LRL)
        URL_b = struct.pack("B", URL)
        A_Amp_b = struct.pack("f", A_Amp)
        A_pw_b=struct.pack("B", A_pw)
        V_Amp_b=struct.pack("f", V_Amp)
        V_pw_b=struct.pack("B", V_pw)
        ARP_b=struct.pack("H", ARP)
        VRP_b=struct.pack("H", VRP)
        aSens_b = struct.pack("f", aSens)
        vSens_b = struct.pack("f", vSens)
        AVdelay_b = struct.pack("H", AVdelay)
        rateAdapt_b = struct.pack("B", rateAdapt)
        MSR_b = struct.pack("B", MSR)
        actThresh_b = struct.pack("f", actThresh)
        reactTime_b = struct.pack("d", reactTime)
        resFactor_b = struct.pack("B", resFactor)
        recTime_b = struct.pack("d", recTime)

        data = b"\x16\x55" + LRL_b + URL_b + A_Amp_b + A_pw_b + V_Amp_b + V_pw_b + ARP_b + VRP_b + aSens_b + vSens_b + mode_b + AVdelay_b + actThresh_b + reactTime_b + recTime_b + MSR_b + rateAdapt_b + resFactor_b
        self.ser.write(data)
        sleep(0.25)

    def serRead(self):

        self.ser.write(b"\x16\x22")
        sleep(0.25)
        data_r = self.ser.read(38) #read 38 bytes

        mode = data_r[0]
        
        LRL = data_r[1]
        URL = data_r[2]

        PVARP = struct.unpack("H", data_r[3:5])# 2 bytes

        AVdelay = struct.unpack("H", data_r[5:7])[0] #2 bytes

        reactTime = data_r[7] #1 byte
        resFactor = data_r[8] #1 byte
        actThresh = struct.unpack("f", data_r[9:13])[0] #4 bytes
        recTime = struct.unpack("H", data_r[13:15])[0]   #2 bytes

        MSR = data_r[15]

        A_Amp = struct.unpack("f", data_r[16:20])[0]  # 4 bytes
        A_pw = data_r[20]                            # 4 bytes
        V_Amp = struct.unpack("f", data_r[21:25])[0] # 4 bytes
        V_pw = data_r[25]                           # 4 bytes

        ARP = struct.unpack("H", data_r[26:28])[0] # 2 bytes
        VRP = struct.unpack("H", data_r[28:30])[0] # 2 bytes

        aThres = struct.unpack("f", data_r[30:34])[0] # 4 bytes
        vThres = struct.unpack("f", data_r[34:38])[0] # 4 bytes
        
        parameters = [mode, LRL, URL, A_Amp, A_pw, V_Amp, V_pw, VRP, ARP, aThres, vThres, PVARP, MSR, actThresh, reactTime, resFactor, recTime, AVdelay]

        return parameters

    def startEgram(self):
        self.ser.write(b"\x16\63") # edit
        sleep(0.25) 

        data_r = self.ser.read(50)

        aSignal = struct.unpack("d", data_r[0:8])[0] * 3.3
        vSignal = struct.unpack("d", data_r[8:16])[0] * 3.3
        return aSignal, vSignal

    def stopEgram(self):
        self.ser.write(b"\x16\x16")
        sleep(0.25)
