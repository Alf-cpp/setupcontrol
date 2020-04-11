# Autor: Albert Schürer
"""Main zum Test der ImagingSource Kamera"""
import ctypes as C
import cv2
import time 
import serial
from isCamera import ISCamera
import tisgrabber as IC
import numpy as np
import datetime

print('#########################',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'################################')


#Kamera hier erstellen und Einstellungen vornehmen
icCam = ISCamera()
icCam.printParams()

#Einstellung der Dateipfae zum Laden und Abspeichern von Bildern
imagePath = 'EMod'

#Callbackfunctions for Trackbars:
def setGain(x):
    gain=cv2.getTrackbarPos('Gain','OptionWindow')
    icCam.setGain(gain)
def setBrightness(x):
    brightness=cv2.getTrackbarPos('Brightness','OptionWindow')
    icCam.setBrightness(brightness)

#OptionWindow with Trackbars:
img = np.zeros((1,1,3), np.uint8)
cv2.namedWindow('OptionWindow', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Gain','OptionWindow',0,480, setGain)
cv2.createTrackbar('Brightness','OptionWindow',0,511, setBrightness)
cv2.imshow('OptionWindow',img)

while(True):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('t'):
        icCam.triggerSettings()


    if key == ord('a'):
        icCam.startLiveMode()

    #if key == ord('p'):#

    
    if key == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()