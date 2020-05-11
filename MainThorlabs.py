# Autor: Albert Schürer
"""Main Programm, welches alle Bauteile (Trigger, Kamera, Bildverarbeitung) vereint"""
import ctypes as C
import cv2
import time 
import serial
import tisgrabber as IC
from thorLabsCamera import TLCamera
import numpy as np
from trigger import Trigger
import datetime

print('#########################',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'################################')

#Trigger
trig = Trigger()
trig.resetSettings()
trig.singleTriggerSettings()
trig.settingsShutterClosed()

#Kamera hier erstellen und Einstellungen vornehmen
tlCam = TLCamera()
time.sleep(1)
tlCam.closeCamera()

#Einstellung der Dateipfae zum Laden und Abspeichern von Bildern
imagePath = 'O:\\ou-mt\\Mitarbeiter\\Albert\\Pictures\\'
filecounter = 0
#Callbackfunction for Trackbars:
def setGain(x):
    gain=cv2.getTrackbarPos('Gain','OptionWindow')
    #icCam.setGain(gain)
def setBrightness(x):
    brightness=cv2.getTrackbarPos('Brightness','OptionWindow')
    #icCam.setBrightness(brightness)

#OptionWindow with Trackbars:
img = np.zeros((1,1,3), np.uint8)
cv2.namedWindow('OptionWindow', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Gain','OptionWindow',280,480, setGain)                # dB/100 = Gain (max 48 dB)
cv2.createTrackbar('Brightness','OptionWindow',240,511, setBrightness)    # Max = 511, Default normalerweise 240...
cv2.imshow('OptionWindow',img)
while(True):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('t'):
        #icCam.stopLive()
        #icCam.triggerSettings()
        trig.singleTriggerSettings()
        trig.settingsShutterClosed()
        time.sleep(0.1)
        trig.trigger()
        time.sleep(0.4)
        trig.settingsShutterOpen()
        time.sleep(0.1)
        trig.trigger()
        time.sleep(0.4)
        #icCam.getImprocPictures()
    #if key == ord('s'):
        #icCam.ImProc.saveImg(imagePath)        
    if key == ord('a'):
        #icCam.stopLive()
        #icCam.startLiveMode()
        trig.setContinous()
    if key == ord('q'):
        tlCam.closeCamera()
        break

# When everything done, release the capture
cv2.destroyAllWindows()