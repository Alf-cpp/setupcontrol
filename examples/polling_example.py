"""
Polling Example

This example shows how to open a camera, adjust some settings, and poll for images. It also shows how 'with' statements
can be used to automatically clean up camera and SDK resources.

"""

try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

import numpy as np
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK

NUM_FRAMES = 10  # adjust to the desired number of frames


with TLCameraSDK() as sdk:
    available_cameras = sdk.discover_available_cameras()
    if len(available_cameras) < 1:
        print("no cameras detected")

    with sdk.open_camera(available_cameras[0]) as camera:
        camera.frames_per_trigger_zero_for_unlimited = 0  # start camera in continuous mode
        camera.image_poll_timeout_ms = 1000  # 1 second polling timeout
        camera.exposure_time_us = 11000  # set exposure to 11 ms

        camera.roi = (100, 100, 600, 600)  # set roi to be at origin point (100, 100) with a width & height of 500

        camera.arm(2)
        camera.issue_software_trigger()

        for i in range(NUM_FRAMES):
            frame = camera.get_pending_frame_or_null()
            if frame is not None:
                print("frame #{} received!".format(frame.frame_count))

                frame.image_buffer  # .../ perform operations using the data from image_buffer

                #  NOTE: frame.image_buffer is a temporary memory buffer that may be overwritten during the next call
                #        to get_pending_frame_or_null. The following line makes a deep copy of the image data:
                image_buffer_copy = np.copy(frame.image_buffer)
            else:
                print("timeout reached during polling, program exiting...")
                break

#  Because we are using the 'with' statement context-manager, disposal has been taken care of.

print("program completed")
