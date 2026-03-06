import cv2
import numpy as np
import open3d as o3d

class VirtualTryOn:
    def __init__(self, color_video, depth_video, shoe_model):
        self.color_video = color_video
        self.depth_video = depth_video
        self.shoe_model = shoe_model
        self.camera_intrinsics = self.get_camera_intrinsics()

    def get_camera_intrinsics(self):
        # Define camera intrinsics (modify based on actual camera parameters)
        fx, fy, cx, cy = 1000, 1000, 640, 360
        return np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    
    def read_videos(self):
        color_cap = cv2.VideoCapture(self.color_video)
        depth_cap = cv2.VideoCapture(self.depth_video)
        return color_cap, depth_cap
    
    def segment_foot(self, frame):
        # Use color filtering or deep learning for foot segmentation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        return mask
    
    def depth_to_point_cloud(self, depth_frame, mask):
        h, w = depth_frame.shape
        i, j = np.meshgrid(np.arange(w), np.arange(h))
        valid_pixels = mask > 0
        z = depth_frame[valid_pixels].astype(np.float32) / 1000.0  # Convert mm to meters
        x = (j[valid_pixels] - self.camera_intrinsics[0, 2]) * z / self.camera_intrinsics[0, 0]
        y = (i[valid_pixels] - self.camera_intrinsics[1, 2]) * z / self.camera_intrinsics[1, 1]
        points = np.vstack((x, y, z)).T
        return points
    
    def align_shoe_model(self, foot_pcd):
        # Load the shoe model and ensure it is a valid triangle mesh
        shoe_mesh = o3d.io.read_triangle_mesh(self.shoe_model)
        if not shoe_mesh.has_triangles():
            print("The shoe model is not a valid triangle mesh!")
            return None

        # Visualize the shoe mesh
        o3d.visualization.draw_geometries([shoe_mesh])

        # Sample points from the shoe mesh for ICP
        shoe_pcd = shoe_mesh.sample_points_uniformly(number_of_points=10000)
        print("Number of points in shoe model:", len(shoe_pcd.points))

        # ICP alignment
        threshold = 0.02  # ICP convergence threshold
        trans_init = np.eye(4)
        reg_p2p = o3d.pipelines.registration.registration_icp(
            shoe_pcd, foot_pcd, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())

        # Check the inlier RMSE to see if the ICP converged
        print("ICP Registration Inlier RMSE:", reg_p2p.inlier_rmse)
        
        # If RMSE is small, consider the alignment successful
        if reg_p2p.inlier_rmse < 0.01:
            print("ICP Converged successfully.")
        else:
            print("ICP did not converge properly.")
        
        return shoe_mesh.transform(reg_p2p.transformation)


    
    def render_overlay(self, color_frame, shoe_mesh):
        # Convert shoe mesh to an image overlay (this can be extended to render in 3D)
        return color_frame
    
    def process(self):
        color_cap, depth_cap = self.read_videos()
        while color_cap.isOpened() and depth_cap.isOpened():
            ret_color, color_frame = color_cap.read()
            ret_depth, depth_frame = depth_cap.read()
            if not ret_color or not ret_depth:
                break
            
            depth_frame = cv2.cvtColor(depth_frame, cv2.COLOR_BGR2GRAY)
            mask = self.segment_foot(color_frame)
            foot_points = self.depth_to_point_cloud(depth_frame, mask)
            
            if len(foot_points) == 0:
                print("No foot points detected!")
                continue
            
            foot_pcd = o3d.geometry.PointCloud()
            foot_pcd.points = o3d.utility.Vector3dVector(foot_points)
            print("Number of foot points:", len(foot_pcd.points))
            
            # Visualize foot point cloud
            o3d.visualization.draw_geometries([foot_pcd])

            # Align shoe model to foot
            aligned_shoe = self.align_shoe_model(foot_pcd)
            if aligned_shoe is None:
                print("Failed to align shoe model.")
                continue
            
            output_frame = self.render_overlay(color_frame, aligned_shoe)
            
            cv2.imshow("Virtual Try-On", output_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        color_cap.release()
        depth_cap.release()
        cv2.destroyAllWindows()

# Example usage
tryon = VirtualTryOn("estimate_streo/stereo_rgb_output.mp4", "estimate_streo/stereo_depth_output.mp4", "implementation_en_cours/3D_models_assets/shoe_0.obj")
tryon.process()
