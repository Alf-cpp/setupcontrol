#Autor: Albert Schürer
""" Ansteuern des Delay-Generators über die serielle Schnittstelle 
Port Belegung: AB= Enable Laser, CD= Kamera Trigger, EF= Shutter"""
import time 
import serial

class Trigger():
    def __init__(self):
        self.serialObject = serial.Serial('COM4')
        print(self.serialObject.name)

    def trigger(self):
        self.serialObject.write(b'*trg\n')

    def resetSettings(self):
        self.serialObject.write(b'*rst\n')

    def singleTriggerSettings(self):
        self.serialObject.write(b'tsrc5\n')
        #self.write(b'trat1\n') #brauch ich das <-???
        #Laser
        self.serialObject.write(b'dlay2,0,26e-3\n')
        self.serialObject.write(b'dlay3,2,1e-3\n')   
        #Kamera:
        self.serialObject.write(b'dlay4,0,20e-3\n')
        self.serialObject.write(b'dlay5,4,4e-3\n')    

    def settingsShutterOpen(self):
        self.serialObject.write(b'lpol3,1\n')
        self.serialObject.write(b'dlay6,0,0\n')
        self.serialObject.write(b'dlay7,0,0.2\n')

    def settingsShutterClosed(self):    #eventuell gibt es eine Feinere Art den Ausgang auf 0 zu setzten?
        self.serialObject.write(b'lpol3,1\n')
        self.serialObject.write(b'dlay6,0,0\n')
        self.serialObject.write(b'dlay7,6,0\n')

    def setManualTrigger(self):
        #Input Manuell setzen:
        self.serialObject.write(b'tsrc5\n')
        #Shutter:
        self.serialObject.write(b'pres3,2\n')    #Shutter Prescaler: nur jedes 2te mal reagieren
        self.serialObject.write(b'dlay6,0,0\n')
        self.serialObject.write(b'dlay7,0,0.1\n')
        #Laser
        self.serialObject.write(b'dlay2,0,26e-3\n')
        self.serialObject.write(b'dlay3,2,1e-3\n')   
        #Kamera:
        self.serialObject.write(b'dlay4,0,25e-3\n')
        self.serialObject.write(b'dlay5,4,1e-3\n')  

    def setContinous(self):
        #Shutter auf 0 setzten... muss vorerst von Hand auf 1 gesetzt werden 
        self.serialObject.write(b'dlay6,0,0\n')
        self.serialObject.write(b'dlay7,0,0\n')
        self.serialObject.write(b'lpol3,0\n')
        #Laser
        self.serialObject.write(b'dlay2,0,5e-3\n')
        self.serialObject.write(b'dlay3,2,1e-3\n')   
        #Kamera:
        self.serialObject.write(b'dlay4,0,0\n')
        self.serialObject.write(b'dlay5,4,4e-3\n')   
        #Trigger Line:
        self.serialObject.write(b'tsrc6\n') 