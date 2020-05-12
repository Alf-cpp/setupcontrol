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

NUMBER_OF_IMAGES = 10  # Number of TIFF images to be saved
OUTPUT_DIRECTORY = os.path.abspath(r'.')  # Directory the TIFFs will be saved to
FILENAME = 'image'  # The filename of the TIFF


TAG_BITDEPTH = 32768
TAG_EXPOSURE = 32769

# delete image if it exists
if os.path.exists(OUTPUT_DIRECTORY + os.sep + FILENAME):
    os.remove(OUTPUT_DIRECTORY + os.sep + FILENAME)

class TLCamera():
    def __init__(self):
        self.FILECOUNTER = 0
        #open camera and setup settings:
        self.sdk = TLCameraSDK()
        cameras = self.sdk.discover_available_cameras()
        if len(cameras) == 0:
            print("Error: no cameras detected!")

        self.camera = self.sdk.open_camera(cameras[0])
        self.camera.frames_per_trigger_zero_for_unlimited = 1
        self.camera.operation_mode = OPERATION_MODE.HARDWARE_TRIGGERED # set Hardwaretrigger
        self.camera.trigger_polarity = TRIGGER_POLARITY.ACTIVE_HIGH # Trigger auf active HIGH
        self.camera.exposure_time_us = 10
        print("Exposure Time :",self.camera.exposure_time_us)
        print("Bit Depth: ", self.camera.bit_depth)
        print(self.camera.operation_mode)
        print(self.camera.trigger_polarity)
        self.camera.image_poll_timeout_ms = 1000  # 1 second timeout   
        self.camera.arm(10)

    def setGain(self, value):
        self.camera.exposure_time_us(value) #set exposure time in us

    def setBrightness(self, value):
        print("Error, there is no such setting for this Camera")

    def snapImg(self):
        self.tiff = tifffile.TiffWriter(OUTPUT_DIRECTORY + os.sep + FILENAME+str(self.FILECOUNTER)+".tif", append=True)
        frame = self.camera.get_pending_frame_or_null()
        if frame is None:
            raise TimeoutError("Timeout was reached while polling for a frame, program will now exit")
        image_data = frame.image_buffer
        self.tiff.save(data=image_data,  # np.ushort image data array from the camera
                  compress=0,   # amount of compression (0-9), by default it is uncompressed (0)
                  extratags=[(TAG_BITDEPTH, 'I', 1, self.camera.bit_depth, False),  # custom TIFF tag for bit depth
                             (TAG_EXPOSURE, 'I', 1, self.camera.exposure_time_us, False)]  # custom TIFF tag for exposure
        )
        self.FILECOUNTER = self.FILECOUNTER+1

    def closeCamera(self):
        self.camera.disarm()
        self.camera.dispose()

    def showSettings(self):
        print("Settings:")
        print("Exposure Time :",self.camera.exposure_time_us)
        print("Bit Depth: ", self.camera.bit_depth)
        print(self.camera.operation_mode)
        print(self.camera.trigger_polarity)