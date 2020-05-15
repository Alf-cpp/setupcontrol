#Autor: Albert Schürer
"""Klasse zur Erstellung eines Objektes der Thorlabs Kamera mit Funktionen zur Einstellung der Settings"""

import ctypes as C
import tisgrabber as IC
import time as time
import cv2
import numpy as np
import sys
from imageProcessing import ImageProcessing
import os
import tifffile



try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_camera_enums import OPERATION_MODE
from thorlabs_tsi_sdk.tl_camera_enums import TRIGGER_POLARITY
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK

TAG_BITDEPTH = 32768
TAG_EXPOSURE = 32769

class TLCamera():
    def __init__(self):
        #variables
        self.FILECOUNTER = 0
        self.counter = 0 # 0 = background Image ; 1 = wave Image
        self.singleTriggerMode = True

        #open camera and setup settings:
        self.sdk = TLCameraSDK()
        cameras = self.sdk.discover_available_cameras()
        if len(cameras) == 0:
            print("Error: no cameras detected!")

        self.camera = self.sdk.open_camera(cameras[0])
        self.camera.frames_per_trigger_zero_for_unlimited = 1
        self.camera.operation_mode = OPERATION_MODE.BULB # set Hardwaretrigger
        self.camera.trigger_polarity = TRIGGER_POLARITY.ACTIVE_HIGH # Trigger auf active HIGH
        #self.camera.exposure_time_us = 10
        print("Exposure Time :",self.camera.exposure_time_us)
        print("Bit Depth: ", self.camera.bit_depth)
        print(self.camera.operation_mode)
        print(self.camera.trigger_polarity)
        self.camera.image_poll_timeout_ms = 1000  # 1 second timeout   
        self.camera.arm(2)

    def setSingleTriggerMode(self):
        self.singleTriggerMode = True
        cv2.destroyWindow('Live')
        self.camera.image_poll_timeout_ms = 1000  # 1 second timeout

    def setContinuousTriggerMode(self):
        self.singleTriggerMode = False
        cv2.destroyWindow('BGimg')
        cv2.destroyWindow('WVimg')
        cv2.destroyWindow('DifferenceImage')
        self.camera.image_poll_timeout_ms = 1000

    def setGain(self, value):
        self.camera.gain(value)

    def snapImg(self):
        frame = self.camera.get_pending_frame_or_null()
        if frame is None:
            raise TimeoutError("Timeout was reached while polling for a frame, program will now exit")
        image_data = frame.image_buffer
        #self.ImProc.imageProcess(self.image_data)
        self.showImage(image_data)

    def closeCamera(self):
        self.camera.disarm()
        self.camera.dispose()

    def showSettings(self):
        print("Settings:")
        print("Exposure Time :",self.camera.exposure_time_us)
        print("Bit Depth: ", self.camera.bit_depth)
        print(self.camera.operation_mode)
        print(self.camera.trigger_polarity)

    def showImage(self, image):
        if self.singleTriggerMode == True:
            if self.counter==0:
                self.BGimg = image
                cv2.imshow("BGimg",self.BGimg)
                cv2.waitKey(1)
                self.counter=1
            else:
                self.WVimg = image
                cv2.imshow("WVimg",self.WVimg)
                self.Diffimg = cv2.absdiff(self.BGimg, self.WVimg)
                cv2.imshow('DifferenceImage',self.Diffimg)
                cv2.waitKey(1)
                self.counter=0
        else:
            cv2.imshow("Live", image)

    def saveImage(self, output_directory):
        tiff = tifffile.TiffWriter("O:\ou-mt\Mitarbeiter\Albert\Pictures\BGimg" + os.sep +str(self.FILECOUNTER).zfill(2)+ "BGimg"+".tif", append=True)
        tiff.save(data=self.BGimg,  # np.ushort image data array from the camera
                  compress=0,   # amount of compression (0-9), by default it is uncompressed (0)
                  extratags=[(TAG_BITDEPTH, 'I', 1, self.camera.bit_depth, False),  # custom TIFF tag for bit depth
                             (TAG_EXPOSURE, 'I', 1, self.camera.exposure_time_us, False)]  # custom TIFF tag for exposure
        )
        tiff = tifffile.TiffWriter("O:\ou-mt\Mitarbeiter\Albert\Pictures\WVimg" + os.sep +str(self.FILECOUNTER).zfill(2)+ "WVimg"+".tif", append=True)
        tiff.save(data=self.WVimg,  # np.ushort image data array from the camera
                  compress=0,   # amount of compression (0-9), by default it is uncompressed (0)
                  extratags=[(TAG_BITDEPTH, 'I', 1, self.camera.bit_depth, False),  # custom TIFF tag for bit depth
                             (TAG_EXPOSURE, 'I', 1, self.camera.exposure_time_us, False)]  # custom TIFF tag for exposure
        )
        tiff = tifffile.TiffWriter("O:\ou-mt\Mitarbeiter\Albert\Pictures\Diffimg" + os.sep +str(self.FILECOUNTER).zfill(2)+ "Diffimg"+".tif", append=True)
        tiff.save(data=self.WVimg,  # np.ushort image data array from the camera
                  compress=0,   # amount of compression (0-9), by default it is uncompressed (0)
                  extratags=[(TAG_BITDEPTH, 'I', 1, self.camera.bit_depth, False),  # custom TIFF tag for bit depth
                             (TAG_EXPOSURE, 'I', 1, self.camera.exposure_time_us, False)]  # custom TIFF tag for exposure
        )
        self.FILECOUNTER=self.FILECOUNTER+1