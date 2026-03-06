import numpy as np 
import open3d as o3d 


class DepthProcessor:
    def __init__(self, min_depth=500, max_depth=3000):
        self.min_depth = min_depth
        self.max_depth = max_depth

    def preprocess_depth(self, depth_frame):
        mask = (depth_frame > self.min_depth) & (depth_frame < self.max_depth)
        segmented_depth = np.where(mask, depth_frame, 0)
        return segmented_depth

    def create_point_cloud(self, segmented_depth):
        foot_cloud = o3d.geometry.PointCloud()
        depth_points = np.argwhere(segmented_depth > 0)
        depth_values = segmented_depth[depth_points[:, 0], depth_points[:, 1]]
        foot_cloud.points = o3d.utility.Vector3dVector(np.column_stack((depth_points, depth_values)))
        return foot_cloud