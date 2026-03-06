import numpy as np  
import open3d as o3d 


class ICPRegistration:
    def __init__(self, shoe_model_path):
        self.shoe_model = o3d.io.read_triangle_mesh(shoe_model_path)

    def register(self, foot_cloud):
        threshold = 0.02  # distance threshold
        transformation = o3d.pipelines.registration.registration_icp(
            foot_cloud, self.shoe_model, threshold, np.identity(4),
            o3d.pipelines.registration.TransformationEstimationPointToPoint()
        )
        return transformation.transformation