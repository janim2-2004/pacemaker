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
        PVARP = paramList[3]
        AVdelay = paramList[4]
        reactTime = paramList[5]
        resFactor = paramList[6]
        actThresh = paramList[7]
        recTime = paramList[8]
        MSR = paramList[9]
        A_Amp = paramList[10]
        A_pw = paramList[11]
        ARP = paramList[12]
        aThres = paramList[13]
        V_Amp = paramList[14]
        V_pw = paramList[15]
        VRP = paramList[16]
        vThres = paramList[17]
        

        #binary values of parameters
        mode_b        = struct.pack("H", mode)
        LRL_b         = struct.pack("H", LRL)
        URL_b         = struct.pack("H", URL)
        PVARP_b       = struct.pack("H", PVARP)
        AVdelay_b     = struct.pack("H", AVdelay)
        reactTime_b   = struct.pack("H", MSR)
        resFactor_b   = struct.pack("H", A_Amp)
        actThresh_b   = struct.pack("f", A_pw)
        recTime_b     = struct.pack("H", V_Amp)
        MSR_b         = struct.pack("H", V_pw)
        A_Amp_b       = struct.pack("f", VRP)
        A_pw_b        = struct.pack("f", ARP)
        ARP_b         = struct.pack("H", aThres)
        aThres_b      = struct.pack("f", vThres)
        V_Amp_b       = struct.pack("f", reactTime)
        V_pw_b        = struct.pack("f", actThresh)
        VRP_b         = struct.pack("H", resFactor)
        vThres_b      = struct.pack("f", recTime)

        data = b"\x16\x55" + mode_b + LRL_b + URL_b + PVARP_b + AVdelay_b + reactTime_b + resFactor_b + actThresh_b + recTime_b  + MSR_b + A_Amp_b + A_pw_b + ARP_b + aThres_b + V_Amp_b + V_pw_b + VRP_b + vThres_b
        self.ser.write(data)
        sleep(0.25)

    def serRead(self):

        self.ser.write(b"\x16\x22" + b"\x00"*48)
        sleep(0.25)
        data_r = self.ser.read(50) #read 50 bytes

        mode = struct.unpack("H", data_r[0:2])[0]
        
        LRL = struct.unpack("H", data_r[2:4])[0]
        URL = struct.unpack("H", data_r[4:6])[0]

        PVARP = struct.unpack("H", data_r[6:8])# 2 bytes

        AVdelay = struct.unpack("H", data_r[8:10])[0] #2 bytes

        reactTime = struct.unpack("H", data_r[10:12])[0]
        resFactor = struct.unpack("H", data_r[12:14])[0]
        actThresh = struct.unpack("f", data_r[14:18])[0] #4 bytes
        recTime = struct.unpack("H", data_r[18:20])[0]   #2 bytes

        MSR = struct.unpack("H", data_r[20:22])[0]

        A_Amp = struct.unpack("f", data_r[22:26])[0]  # 4 bytes
        A_pw = struct.unpack("H", data_r[26:30])[0] # 4 bytes
        ARP = struct.unpack("H", data_r[38:40])[0] # 2 bytes
        aThres = struct.unpack("f", data_r[42:46])[0] # 4 bytes

        V_Amp = struct.unpack("f", data_r[30:34])[0] # 4 bytes
        V_pw = struct.unpack("H", data_r[34:38])[0] # 4 bytes
        VRP = struct.unpack("H", data_r[40:42])[0] # 2 bytes
        vThres = struct.unpack("f", data_r[46:50])[0] # 4 bytes
        
        parameters = [mode, LRL, URL, PVARP, AVdelay, reactTime, resFactor, actThresh, recTime, MSR, A_Amp, A_pw, ARP, aThres, V_Amp, V_pw, VRP, vThres]

        sleep(0.25)
        self.ser.write(b"\x16\x44") #stop pacemaker signal
        return parameters

    def startEgram(self):
        self.ser.write(b"\x16\x22" + b"\x00"*48)
        sleep(0.25) 

        data_r = self.ser.read(50)

        aSignal = struct.unpack("f", data_r[22:26])[0] * 3.3
        vSignal = struct.unpack("f", data_r[30:34])[0] * 3.3
        return aSignal, vSignal

    def stopEgram(self):
        self.ser.write(b"\x16\x44")
        sleep(0.25)
