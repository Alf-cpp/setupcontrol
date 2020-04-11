""" Hier werden die ankommenden Bilder der Callbackfunktion verarbeitet und anschließend angezeigt"""

import numpy as np
import cv2
import time 
import math

class ImageProcessing():
    def __init__(self):
        self.Counter =0
        self.PointCounter = 0
        self.TriggerMode = -1
        cv2.namedWindow('DifferenceImage', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('DifferenceImage',self.getMousePos)
    def test(self):
        self.Counter = self.Counter+1
        print("Counter:",self.Counter)

    def setTriggerMode(self, triggerMode):
        self.TriggerMode = triggerMode
        if self.TriggerMode == 1:
            cv2.namedWindow('TriggerPicture_1', cv2.WINDOW_NORMAL)
            cv2.namedWindow('TriggerPicture_2', cv2.WINDOW_NORMAL)
            cv2.destroyWindow('Continuous')
        elif self.TriggerMode == 0:
            cv2.namedWindow('Continuous', cv2.WINDOW_NORMAL)
            cv2.destroyWindow('TriggerPicture_1')
            cv2.destroyWindow('TriggerPicture_2')
        else:
            cv2.destroyWindow('Trigger')
            cv2.destroyWindow('Continuous')

    def imageProcess(self, image):
        if self.TriggerMode==1:
            if self.Counter==0:
                cv2.imshow('TriggerPicture_1',image)
                self.Image_01 = image
                #cv2.waitKey(1)
                self.Counter = self.Counter +1

            elif self.Counter==1:
                cv2.imshow('TriggerPicture_2',image)
                self.Image_02 = image
                self.DiffImage = self.Image_01-self.Image_02
                cv2.imshow('DifferenceImage',self.DiffImage)
                self.Counter = 0
        elif self.TriggerMode == 0:
            cv2.imshow('Continuous', image)

    def getImage_01(self):
        return self.Image_01
    def getImage_02(self):
        return self.Image_02
    def getDiffImage(self):
        return self.DiffImage

    def getMousePos(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('X:', x,'Y:',y,'Value:',self.DiffImage[x,y])
            if self.PointCounter==0:
                self.PointCenter = [x,y]
                self.PointCounter = self.PointCounter+1
            else:
                self.PointEdge = [x,y]
                distance = math.sqrt((self.PointCenter[0]-self.PointEdge[0])**2+(self.PointCenter[1]-self.PointEdge[1])**2)
                radius = int(round(distance))
                print('Radius:',radius)
                cv2.circle(self.DiffImage,(self.PointCenter[0], self.PointCenter[1]),radius,(255),2)
                cv2.imshow('DifferenceImage',self.DiffImage)
                self.PointCounter=0
