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
import os

print('#########################',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'################################')

#Paths
os.environ['PATH'] +=r'C:\Master\setupcontrol\dlls'+os.sep+'64_lib;'

#print(os.environ['PATH'])

#_sdk = C.cdll.LoadLibrary("thorlabs_tsi_camera_sdk.dll")

#Directory
# delete image if it exists
OUTPUT_DIRECTORY = 'O:\ou-mt\Mitarbeiter\Albert\Pictures'  #os.path.abspath(r'.\pictures')  # Directory the TIFFs will be saved to
os.mkdir(OUTPUT_DIRECTORY+os.sep+datetime.datetime.now().strftime('%Y-%m-%d %H.%M'))
OUTPUT_DIRECTORY = 'O:\ou-mt\Mitarbeiter\Albert\Pictures'+os.sep+datetime.datetime.now().strftime('%Y-%m-%d %H.%M')
FILENAME = 'image'  # The filename of the TIFF

if os.path.exists(OUTPUT_DIRECTORY + os.sep + FILENAME):
    os.remove(OUTPUT_DIRECTORY + os.sep + FILENAME)

#Trigger
trig = Trigger()
trig.resetSettings()
trig.singleTriggerSettings()
trig.settingsShutterClosed()

#Kamera hier erstellen und Einstellungen vornehmen

tlCam = TLCamera()

#Einstellung der Dateipfae zum Laden und Abspeichern von Bildern
imagePath = 'O:\\ou-mt\\Mitarbeiter\\Albert\\Pictures\\'
filecounter = 0


#Callbackfunction for Trackbars:
def setMaxIntensity(x):
    maxIntensity=cv2.getTrackbarPos('MaxIntensity','OptionWindow')
    tlCam.setMaxIntensity(maxIntensity)

def setMinIntensity(x):
    minIntensity=cv2.getTrackbarPos('MinIntensity','OptionWindow')
    tlCam.setMinIntensity(minIntensity)

#OptionWindow with Trackbars:
img = np.zeros((1,1,3), np.uint8)
cv2.namedWindow('OptionWindow', cv2.WINDOW_NORMAL)
cv2.createTrackbar('MaxIntensity','OptionWindow',65536,65536, setMaxIntensity) 
cv2.createTrackbar('MinIntensity','OptionWindow',0,65536, setMinIntensity)
cv2.imshow('OptionWindow',img)

while(True):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('t'):
        tlCam.setSingleTriggerMode()
        trig.singleTriggerSettings()    
        trig.settingsShutterClosed()    #1.: BG Image
        trig.trigger()
        tlCam.snapImg()
        trig.settingsShutterOpen()      #2.: Wave Image 
        trig.trigger()
        tlCam.snapImg()
        trig.settingsShutterClosed()    #3.: 2tes BG Image
        trig.trigger()
        tlCam.snapImg()
    if key == ord('s'):
        tlCam.saveImage(OUTPUT_DIRECTORY)     
    if key == ord('a'):
        while(True):
            key = cv2.waitKey(1) & 0xFF
            trig.settingsShutterClosed()
            trig.trigger()
            tlCam.snapImg()
            trig.settingsShutterOpen()
            trig.trigger()
            tlCam.snapImg()
            if key == ord('q'):
                key=1
                break
    if key == ord('q'):
        tlCam.closeCamera()
        break

# When everything done, release the capture
cv2.destroyAllWindows()