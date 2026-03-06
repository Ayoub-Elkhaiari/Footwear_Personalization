import cv2
import numpy as np

# Load left and right videos
left_video_path = "test_left.mp4"   # Change to your left video path
right_video_path = "test_right.mp4" # Change to your right video path

left_cap = cv2.VideoCapture(left_video_path)
right_cap = cv2.VideoCapture(right_video_path)

# Get video properties (assuming both videos have the same properties)
frame_width = int(left_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(left_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(left_cap.get(cv2.CAP_PROP_FPS))

# Define output video writers
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
color_output = cv2.VideoWriter("estimate_streo/stereo_rgb_output.mp4", fourcc, fps, (frame_width, frame_height))
depth_output = cv2.VideoWriter("estimate_streo/stereo_depth_output.mp4", fourcc, fps, (frame_width, frame_height), isColor=False)

# Initialize Stereo Block Matching (BM) or Stereo Semi-Global Matching (SGBM)
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=64,  # Must be multiple of 16
    blockSize=15,
    P1=8 * 3 * 15**2,
    P2=32 * 3 * 15**2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32
)

# Process video frame by frame
while left_cap.isOpened() and right_cap.isOpened():
    ret_left, frame_left = left_cap.read()
    ret_right, frame_right = right_cap.read()

    if not ret_left or not ret_right:
        break

    # Convert frames to grayscale
    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    # Compute disparity map (depth estimation)
    disparity = stereo.compute(gray_left, gray_right).astype(np.float32)

    # Normalize disparity for visualization
    disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    depth_map = np.uint8(disparity)

    # Write frames to output videos
    color_output.write(frame_left)  # Save RGB frame (using left camera as reference)
    depth_output.write(depth_map)  # Save depth frame

    # Show progress (optional)
    cv2.imshow("RGB (Left)", frame_left)
    cv2.imshow("Depth Map", depth_map)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
left_cap.release()
right_cap.release()
color_output.release()
depth_output.release()
cv2.destroyAllWindows()

print("Stereo depth estimation completed. RGB and depth videos saved.")
