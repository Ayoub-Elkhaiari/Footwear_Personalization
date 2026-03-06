import cv2
from pykinect2 import PyKinectRuntime, PyKinectV2

# Initialize the Kinect runtime for color frame
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

try:
    while True:
        # Check if a new color frame is available
        if kinect.has_new_color_frame():
            # Get the color frame as a 1D array
            frame = kinect.get_last_color_frame()

            # Kinect color frame is a single array; reshape it into (height, width, 4) (RGBA)
            frame = frame.reshape((1080, 1920, 4))  # Kinect RGB resolution: 1920x1080
            
            # Convert RGBA to RGB for OpenCV (discard the alpha channel)
            frame = frame[:, :, :3]
            
            # Convert from BGRA to BGR (OpenCV color format)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Resize frame for display (optional)
            display_frame = cv2.resize(frame, (960, 540))  # Resize for a smaller display window

            # Show the frame in a window
            cv2.imshow('Kinect RGB Stream', display_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release resources
    kinect.close()
    cv2.destroyAllWindows()
