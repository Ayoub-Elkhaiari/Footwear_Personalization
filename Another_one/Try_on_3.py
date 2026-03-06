import cv2
import numpy as np
import mediapipe as mp
import trimesh
import pyrender
from pyrender.constants import RenderFlags

# Load the shoe model (correctly extract the mesh)
shoe_mesh_scene = trimesh.load(r'C:\Users\hp\Desktop\MLAIM\S3\AR\project\implementation_en_cours\3D_models_assets\shoe_0.obj')
shoe_mesh = shoe_mesh_scene.geometry[list(shoe_mesh_scene.geometry.keys())[0]]  # Extract the first mesh
mesh = pyrender.Mesh.from_trimesh(shoe_mesh)


# MediaPipe Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False)

# Camera setup (assumed intrinsics - adjust if needed)
focal_length = 500
cam_matrix = np.array([
    [focal_length, 0, 640/2],
    [0, focal_length, 480/2],
    [0, 0, 1]
], dtype=np.float32)

# Pyrender scene setup
scene = pyrender.Scene()
camera = pyrender.IntrinsicsCamera(
    fx=cam_matrix[0,0],
    fy=cam_matrix[1,1],
    cx=cam_matrix[0,2],
    cy=cam_matrix[1,2]
)
scene.add(camera)

# Add light
light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=2.0)
scene.add(light, pose=np.eye(4))

# Add shoe to scene
shoe_node = scene.add(mesh, pose=np.eye(4))

# Video processing
cap = cv2.VideoCapture(r'C:\Users\hp\Desktop\MLAIM\S3\AR\project\test_right.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame with MediaPipe Pose
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_world_landmarks:
        landmarks = results.pose_world_landmarks.landmark

        # Foot landmarks (MediaPipe indices: 27-32 for left foot, 27-32 for right foot)
        # Adjust based on which foot you're targeting
        ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value]
        foot_index = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

        # Calculate foot direction vector (from heel to toe)
        heel_pos = np.array([heel.x, heel.y, heel.z])
        toe_pos = np.array([foot_index.x, foot_index.y, foot_index.z])
        direction = toe_pos - heel_pos
        length = np.linalg.norm(direction)
        direction /= length

        # Calculate rotation
        up = np.array([0, -1, 0])  # Assuming Y-axis up in MediaPipe
        right = np.cross(direction, up)
        up = np.cross(right, direction)
        rotation = np.vstack([right, up, direction]).T

        # Translation (use heel position as base)
        translation = heel_pos

        # Scale shoe model based on foot length (adjust scaling factor as needed)
        scale_factor = length / 0.25  # Assuming shoe model length is 0.25m
        scale = np.diag([scale_factor, scale_factor, scale_factor, 1.0])

        # Transformation matrix
        transform = np.eye(4)
        transform[:3, :3] = rotation
        transform[:3, 3] = translation
        transform = transform @ scale

        # Update shoe node in the scene
        scene.set_pose(shoe_node, transform)

        # Render the scene
        r = pyrender.OffscreenRenderer(viewport_width=frame.shape[1], viewport_height=frame.shape[0])
        color, _ = r.render(scene, flags=RenderFlags.RGBA)

        # Overlay rendered shoe on the frame
        mask = color[:, :, 3] > 0
        frame[mask] = cv2.addWeighted(frame, 0.5, color[:, :, :3], 0.5, 0)[mask]

    out.write(frame)
    cv2.imshow('Output', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()