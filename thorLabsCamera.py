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
FILENAME = 'image.tif'  # The filename of the TIFF

TAG_BITDEPTH = 32768
TAG_EXPOSURE = 32769

# delete image if it exists
if os.path.exists(OUTPUT_DIRECTORY + os.sep + FILENAME):
    os.remove(OUTPUT_DIRECTORY + os.sep + FILENAME)

class TLCamera():
    def __init__(self):
        #open camera and setup settings:
        camera = TLCameraSDK()
        cameras = camera.discover_available_cameras()
        if len(cameras) == 0:
            print("Error: no cameras detected!")

        self.camera = camera.open_camera(cameras[0])
        self.camera.frames_per_trigger_zero_for_unlimited = 1
        self.camera.operation_mode(OPERATION_MODE.HARDWARE_TRIGGERED)   #set Hardwaretrigger
        self.camera.trigger_polarity(TRIGGER_POLARITY.ACTIVE_HIGH) 
        self.camera.arm()
        

    def setGain(self, value):
        self.camera.exposure_time_us(value) #set exposure time in us

    def setBrightness(self, value):
        print("Error, there is no such setting for this Camera")

    def closeCamera(self):
        self.camera.disarm()
        self.camera.dispose()