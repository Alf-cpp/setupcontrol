import numpy as np
import cv2
import time 
import serial
from trigger import Trigger

trig = Trigger()
trig.resetSettings()
trig.singleTriggerSettings()
trig.settingsShutterClosed()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
imagePath = 'C:\\Users\\localadmin\\EMod\\Images\\'
initframe = cv2.imread('C:\\Users\\localadmin\\EMod\\startImage.jpg', cv2.IMREAD_COLOR)
cv2.namedWindow('DiffImage', cv2.WINDOW_NORMAL)
cv2.imshow('DiffImage',initframe)

while(True):
    key = cv2.waitKey(1) & 0xFF

    if key == ord('t'): #trigger start

        trig.resetSettings()
        trig.singleTriggerSettings()
        trig.settingsShutterClosed()
        trig.trigger()
        time.sleep(0.1)
        ret, bgImg = cap.read()

        trig.settingsShutterOpen()
        trig.trigger()

        time.sleep(0.1)
        ret, wvImg = cap.read()

        diffImg = wvImg-bgImg
        diffImg = cv2.blur(diffImg,(5,5))
        cv2.namedWindow('DiffImage', cv2.WINDOW_NORMAL)
        cv2.imshow('DiffImage',diffImg)
        cv2.resizeWindow('DiffImage', 960, 600)

    if key == ord('m'): #manuelles Triggern am Delaygenerator:
        trig.setManualTrigger()
        while(True):
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):
                cv2.destroyAllWindows()
                break
            
    if key == ord('c'): #Kontinuierliches Triggern und Bild aufnehmen, ohne Shutter zu schließen!!
        trig.resetSettings()
        trig.setContinous()
        while(True):
            ret, frame = cap.read()
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            cv2.namedWindow('LiveImg', cv2.WINDOW_NORMAL)
            cv2.imshow('LiveImg',frame)
            cv2.resizeWindow('LiveImg', 960, 600)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):
                cv2.destroyWindow('LiveImg')
                break
            
    if key == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()