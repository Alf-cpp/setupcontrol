import ctypes as C

class CallbackUserdata(C.Structure):
    """ Example for user data passed to the callback function. """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.iBitsPerPixel = 0
        self.buffer_size = 0
        self.oldbrightness = 0