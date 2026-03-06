import cv2
import numpy as np
import trimesh
import mediapipe as mp
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

# Load the 3D shoe model
shoe = trimesh.load_mesh(r'C:\Users\hp\Desktop\MLAIM\S3\AR\project\implementation_en_cours\3D_models_assets\shoe_0.obj')

# Initialize MediaPipe for pose estimation
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Function to segment the foot (basic segmentation example using color thresholding)
def segment_foot(frame):
    # Convert to HSV and threshold for foot-like colors (this could be adjusted based on your video)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 30, 50])
    upper_skin = np.array([20, 150, 255])
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Perform morphological operations to improve segmentation
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

# Function to align the shoe to the foot based on pose landmarks
def align_shoe_to_foot(shoe, foot_keypoints):
    # Using key points such as the ankle and toe for alignment
    ankle = np.array([foot_keypoints[24].x, foot_keypoints[24].y, foot_keypoints[24].z])
    big_toe = np.array([foot_keypoints[31].x, foot_keypoints[31].y, foot_keypoints[31].z])

    # Compute the direction vector between the ankle and the big toe (foot's forward direction)
    direction = big_toe - ankle
    direction = direction / np.linalg.norm(direction)  # Normalize

    # Assuming the shoe has an orientation that needs to match this direction
    # We will use rotation to align the shoe model with the direction vector of the foot

    # Create a rotation matrix from the current shoe orientation (assuming Z-axis of shoe points forward)
    shoe_orientation = np.array([0, 0, 1])  # Shoe's original forward direction (Z-axis)
    rotation_axis = np.cross(shoe_orientation, direction)
    rotation_angle = np.arccos(np.dot(shoe_orientation, direction))
    rotation_matrix = R.from_rotvec(rotation_axis * rotation_angle).as_matrix()

    # Apply the rotation to the shoe
    shoe.apply_transform(rotation_matrix)
    
    # Translate the shoe model to align with the foot
    shoe_center = shoe.centroid
    translation = ankle - shoe_center
    shoe.apply_translation(translation)

    return shoe

# Function to render the shoe over the foot in a video frame
def render_shoe_on_foot(frame, shoe, foot_keypoints):
    # Render the shoe onto the frame using a simple overlay (this part is conceptual)
    # Here, you'd project the 3D shoe into the 2D frame and visualize it. We will simulate it by drawing a bounding box.
    
    ankle = foot_keypoints[24]
    toe = foot_keypoints[31]
    
    foot_center = (int(ankle.x * frame.shape[1]), int(ankle.y * frame.shape[0]))
    toe_position = (int(toe.x * frame.shape[1]), int(toe.y * frame.shape[0]))
    
    # Draw bounding box of the shoe (for demonstration purposes)
    cv2.rectangle(frame, foot_center, toe_position, (0, 255, 0), 2)
    
    # Here you can replace this with actual rendering logic for the shoe
    return frame

# Check if video file is accessible
cap = cv2.VideoCapture(r'C:\Users\hp\Desktop\MLAIM\S3\AR\project\test_right.mp4')
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break

    # Check if frame is valid
    print(f"Frame size: {frame.shape}")

    # Step 1: Segment the foot in the current frame
    foot_mask = segment_foot(frame)

    # Step 2: Detect keypoints of the foot using pose estimation
    results = pose.process(frame)
    if results.pose_landmarks:
        print("Landmarks detected.")
        foot_keypoints = results.pose_landmarks.landmark

        # Step 3: Align the shoe to the foot using keypoints
        aligned_shoe = align_shoe_to_foot(shoe, foot_keypoints)

        # Step 4: Render the aligned shoe model over the foot in the frame
        frame_with_shoe = render_shoe_on_foot(frame, aligned_shoe, foot_keypoints)

        # Display the frame with shoe
        print("Displaying frame with shoe...")
        cv2.imshow('Aligned Shoe on Foot', frame_with_shoe)

    # Check for key press (wait for 1 ms)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
