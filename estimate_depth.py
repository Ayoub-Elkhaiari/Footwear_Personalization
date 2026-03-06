# import torch
# import cv2
# import numpy as np

# # Load MiDaS from torch hub
# midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")  # "DPT_Large" for better quality
# midas.eval()

# # Load transforms
# midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
# transform = midas_transforms.small_transform  # Use `dpt_transform` for "DPT_Large"

# # Open video file
# video_path = "test_r.mp4"  # Change to your video path
# cap = cv2.VideoCapture(video_path)

# # Get video properties
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(cap.get(cv2.CAP_PROP_FPS))

# # Define output video writers
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# color_output = cv2.VideoWriter("rgb_output.mp4", fourcc, fps, (frame_width, frame_height))
# depth_output = cv2.VideoWriter("depth_output.mp4", fourcc, fps, (frame_width, frame_height), isColor=False)

# # Process video frame by frame
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert frame to RGB (needed for MiDaS)
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Apply MiDaS transform
#     input_batch = transform(frame_rgb).unsqueeze(0)

#     # Estimate depth
#     with torch.no_grad():
#         depth_map = midas(input_batch)

#     # Convert depth map to numpy
#     depth_map = depth_map.squeeze().cpu().numpy()

#     # Normalize depth for visualization
#     depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min()) * 255
#     depth_map = depth_map.astype(np.uint8)

#     # Resize depth map to match original frame size
#     depth_map_resized = cv2.resize(depth_map, (frame_width, frame_height))

#     # Write frames to output videos
#     color_output.write(frame)  # Save RGB frame
#     depth_output.write(depth_map_resized)  # Save depth frame

#     # Show progress (optional)
#     cv2.imshow("RGB", frame)
#     cv2.imshow("Depth", depth_map_resized)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# # Release resources
# cap.release()
# color_output.release()
# depth_output.release()
# cv2.destroyAllWindows()

# print("Depth estimation completed. RGB and depth videos saved.")


# ------------------------------------


import torch
import cv2
import numpy as np

# Load MiDaS from torch hub
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")  # "DPT_Large" for better quality
midas.eval()

# Load transforms
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.small_transform  # Use `dpt_transform` for "DPT_Large"

# Open video file
video_path = "test_r.mp4"  # Change to your video path
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define output video writers
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
color_output = cv2.VideoWriter("rgb_output.mp4", fourcc, fps, (frame_width, frame_height))
depth_output = cv2.VideoWriter("depth_output.mp4", fourcc, fps, (frame_width, frame_height), isColor=False)

# Process video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (needed for MiDaS)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply MiDaS transform (batch the frame as the model expects a batch of images)
    input_batch = transform(frame_rgb).unsqueeze(0)  # Unsqueeze to create a batch dimension

    # Estimate depth
    with torch.no_grad():
        depth_map = midas(input_batch)

    # Convert depth map to numpy
    depth_map = depth_map.squeeze().cpu().numpy()

    # Normalize depth for visualization
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min()) * 255
    depth_map = depth_map.astype(np.uint8)

    # Resize depth map to match original frame size
    depth_map_resized = cv2.resize(depth_map, (frame_width, frame_height))

    # Write frames to output videos
    color_output.write(frame)  # Save RGB frame
    depth_output.write(depth_map_resized)  # Save depth frame

    # Show progress (optional)
    cv2.imshow("RGB", frame)
    cv2.imshow("Depth", depth_map_resized)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
color_output.release()
depth_output.release()
cv2.destroyAllWindows()

print("Depth estimation completed. RGB and depth videos saved.")
