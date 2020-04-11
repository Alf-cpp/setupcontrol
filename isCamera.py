#Autor: Albert Schürer
"""Klasse zur Erstellung eines Objektes der Imaging Source Kamera mit Funktionen zur Einstellung der Settings"""
import ctypes as C
import tisgrabber as IC
import time as time
import cv2
import numpy as np
import sys
from callbackUserData import CallbackUserdata
from imageProcessing import ImageProcessing

class ISCamera():
    def __init__(self):
        self.Camera = IC.TIS_CAM()
        #self.Camera.ShowDeviceSelectionDialog()
        print("Open Camera:         ",self.Camera.openVideoCaptureDevice("DMK 33UX174"))    # Hier richtige Kamera einfügen!!
        print("VideoFormat:         ",self.Camera.SetVideoFormat("Y800 (1920x1200)"))       # Format der Kamera auf Y16 setzen mit richtiger Auflösung!!
        self.Camera.SetFormat(IC.SinkFormats.Y800)                                          # No Return Value
        print("Continuous Mode OFF: ",self.Camera.SetContinuousMode(0))
        self.Camera.StartLive(0)
        print("Gain Auto off:       ",self.Camera.SetPropertySwitch("Gain","Auto",0))       # Gain Manuell einstellen
        print("Gain Value set:      ",self.Camera.SetPropertyValue("Gain","Value",0))       # Gain auf 0
        print("Brightness Value Set:",self.Camera.SetPropertyValue("Brightness","Value", 0))# Brightness auch auf 0 (=BlackLevel)
        print("Exposure Auto off:   ",self.Camera.SetPropertySwitch("Exposure","Auto",0))
        print("Exposure Value set:  ",self.Camera.SetPropertyAbsoluteValue("Exposure","Value",0.001)) #Exposure time in seconds

        # Für Callback:
        self.ImProc = ImageProcessing()
        self.Callbackfunc = IC.TIS_GrabberDLL.FRAMEREADYCALLBACK(self.Callback)
        self.ImageDescription = CallbackUserdata()
        print("set Callback        :",self.Camera.SetFrameReadyCallback(self.Callbackfunc, self.ImageDescription ))
        self.Imageformat = self.Camera.GetImageDescription()[:3]
        self.ImageDescription.width = self.Imageformat[0]
        self.ImageDescription.height= self.Imageformat[1]
        self.ImageDescription.iBitsPerPixel=self.Imageformat[2]//8
        self.ImageDescription.buffer_size = self.ImageDescription.width * self.ImageDescription.height * self.ImageDescription.iBitsPerPixel
        print("ImageDescription height:", self.ImageDescription.height)
        print("ImageDescription width :", self.ImageDescription.width)
        print("ImageDescription BpP   :", self.ImageDescription.iBitsPerPixel)
        self.Camera.StopLive()

    def triggerSettings(self):
        self.ImProc.setTriggerMode(1)
        self.Camera.StartLive(0)
        print("Trigger Mode ON:     ",self.Camera.SetPropertySwitch("Trigger","Enable",1))   
        print("Trigger rising Edge: ",self.Camera.SetPropertySwitch("Trigger","Polarity",1))
        print("Trigger Debounce Set:",self.Camera.SetPropertyAbsoluteValue("Trigger","Debounce Time",10000))    #10ms debounce time

    def startLiveMode(self):
        self.ImProc.setTriggerMode(0)
        print("Trigger Mode OFF:     ",self.Camera.SetPropertySwitch("Trigger","Enable",0))  
        self.Camera.SetFrameRate(30.0)
        self.Camera.StartLive(0)                            #1: Video wird gezeigt, 0: Video wird nicht gezeigt (gestartet wird dennoch)

    def snapImg(self):
        self.Camera.SnapImage()
        return self.Camera.GetImage()

    def stopLive(self):
        self.Camera.StopLive()

    def getImage(self):
        return self.Camera.GetImage()

    def setGain(self, value):
        print("Gain Value set:      ",self.Camera.SetPropertyValue("Gain","Value",value))       # Gain auf übergebenen Wert

    def setBrightness(self, value):
        print("Brightness Value Set:",self.Camera.SetPropertyValue("Brightness","Value", value))

    def printParams(self):  #Zum Debggen: Zeigt, ob Parameter von der Kamera übernommen wurden oder nicht
        GainValue=[0]
        error = self.Camera.GetPropertyAbsoluteValue("Gain","Value",GainValue)
        if error==1:
            print("Gain Value:      ", GainValue[0])
        else:
            print("Gain Error:      ",error)

        BrightnessValue=[0]
        error = self.Camera.GetPropertyAbsoluteValue("Brightness","Value",BrightnessValue)  #Funktioniert nicht, warum???
        if error==1:
            print("Brightness Value:", BrightnessValue[0])
        else:
            print("Brightness Error:",error)

        ExposureTime=[0]
        error = self.Camera.GetPropertyAbsoluteValue("Exposure","Value",ExposureTime)
        if error==1:
            print("Exposure Value:  ", ExposureTime[0])
        else:
            print("Exposure Error:  ",error)

    def Callback(self, hGrabber, pBuffer, framenumber, pData):
        """:param: hGrabber: This is the real pointer to the grabber object.
        :param: pBuffer : Pointer to the first pixel's first byte
        :param: framenumber : Number of the frame since the stream started
        :param: pData : Pointer to additional user data structure"""
        image = C.cast(pBuffer, C.POINTER(C.c_ubyte * pData.buffer_size))
        cvMat = np.ndarray(buffer = image.contents,
                        dtype = np.uint8,
                        shape = (pData.height,
                                pData.width,
                                pData.iBitsPerPixel))
        #print("Shape pData height:", pData.height)
        #print("Shape pData width :", pData.width)
        #print("Shape pData BpP   :", pData.iBitsPerPixel)
        self.ImProc.imageProcess(cvMat)

