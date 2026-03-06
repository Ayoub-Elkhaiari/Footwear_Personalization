from pykinect2 import PyKinectRuntime, PyKinectV2



class KinectStream:
    def __init__(self):
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)

    def get_frames(self):
        color_frame, depth_frame = None, None
        if self.kinect.has_new_color_frame():
            color_frame = self.kinect.get_last_color_frame().reshape((1080, 1920, 4))[:, :, :3]
        if self.kinect.has_new_depth_frame():
            depth_frame = self.kinect.get_last_depth_frame().reshape((424, 512))
        return color_frame, depth_frame

    def close(self):
        self.kinect.close()