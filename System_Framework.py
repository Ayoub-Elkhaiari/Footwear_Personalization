from Kinect_Streaming import KinectStream
from Depth_Processing import DepthProcessor
from ICP import ICPRegistration
from Color_Processing import ColorProcessor
from Visualization import Visualizer
import cv2 




class VirtualTryOnSystem:
    def __init__(self, shoe_model_path):
        self.kinect_stream = KinectStream()
        self.depth_processor = DepthProcessor()
        self.color_processor = ColorProcessor()
        self.icp_registration = ICPRegistration(shoe_model_path)
        self.visualizer = None

    def run(self):
        try:
            while True:
                color_frame, depth_frame = self.kinect_stream.get_frames()
                if depth_frame is not None and color_frame is not None:
                    # Process depth frame
                    segmented_depth = self.depth_processor.preprocess_depth(depth_frame)
                    foot_cloud = self.depth_processor.create_point_cloud(segmented_depth)

                    # Detect green points on the foot using the color frame
                    green_points = self.color_processor.detect_green_points(color_frame)
                    
                    # Perform ICP registration to align shoe with foot
                    transformation = self.icp_registration.register(foot_cloud)

                    # Apply the transformation to the shoe model
                    self.icp_registration.shoe_model.transform(transformation)

                    # For visualization, display the green points and the depth frame
                    for point in green_points:
                        cv2.circle(color_frame, tuple(point), 5, (0, 255, 0), -1)  # Draw green points

                    # Show the color frame with green points overlaid
                    cv2.imshow("Virtual Try-On with Markerless Tracking", color_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.kinect_stream.close()