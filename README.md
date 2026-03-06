# Virtual Try-On System for Footwear Design Evaluation

A mixed reality system that overlays 3D shoe models onto a user's real feet for footwear design evaluation. The system supports **two approaches** depending on available hardware — one using a depth camera for real-time tracking, and one using phone images with depth estimation for camera-free use.

---

## The Idea

Footwear designers need to evaluate how a shoe looks on an actual foot — not just on a mannequin or in a 3D editor. This system aligns a virtual 3D shoe model with the user's foot and overlays it in real time, enabling design evaluation without physical prototypes.

---

## Two Approaches

### Approach 1 — RGB-D Camera (Kinect V2)

Uses a **Microsoft Kinect V2** which provides synchronized color and depth streams directly. This enables real-time foot tracking with no depth estimation needed.

```
Kinect V2
  ├── Color stream ──► Green marker detection  ──► Rough foot position (Stage 1)
  └── Depth stream ──► Point cloud + ICP        ──► Precise foot alignment (Stage 2)
                                                          │
                                                          ▼
                                                  Virtual shoe overlay
```

**Best for:** real-time live demo, lab or design studio environment.

---

### Approach 2 — Phone Images + Depth Estimation (No Depth Camera)

Uses a **smartphone** to capture images of the foot. Depth is then estimated computationally, making this approach accessible without any special hardware.

Two depth estimation methods are available:

#### Monocular Depth — MiDaS
A single video or image from the phone is passed through **MiDaS**, a deep learning model that estimates depth from a single RGB frame.

```
Phone video (single camera)
  └──► MiDaS model ──► Depth map per frame
                            │
                            ▼
                    Point cloud + ICP ──► Virtual shoe overlay
```

#### Stereo Depth — SGBM
Two photos or video clips taken from slightly different positions (simulating a stereo pair) are processed using **Stereo SGBM (Semi-Global Block Matching)** to compute a disparity map and recover depth.

```
Phone photo/video (left angle)  ──┐
                                   ├──► Stereo SGBM ──► Disparity map ──► Depth map
Phone photo/video (right angle) ──┘                                           │
                                                                               ▼
                                                                   Point cloud + ICP ──► Virtual shoe overlay
```

**Best for:** testing without a Kinect, field evaluations, accessible deployment on any device.

---

## Two-Stage Tracking Pipeline

Both approaches share the same two-stage alignment pipeline once depth data is available:

**Stage 1 — Rough Positioning**
- Green color markers on the foot are detected from the color/RGB image
- The virtual shoe is placed approximately in the correct position immediately

**Stage 2 — Precise 3D Registration**
- The foot is segmented from the background using the depth data
- A 3D point cloud is built from the segmented depth
- **ICP (Iterative Closest Point)** aligns the point cloud with a reference foot model
- A trim algorithm reduces the reference model to the visible view angle for efficiency
- The previous frame's result initializes the next for smooth continuous tracking

---

## Results

| ![Result 1](https://github.com/user-attachments/assets/3485b514-9720-4a11-b676-7a1bc45b6ee6) | ![Result 2](https://github.com/user-attachments/assets/5d427605-8a89-47e9-bad8-02d7734431e7) | ![Result 3](https://github.com/user-attachments/assets/322793b2-d3d5-48be-9531-f516346459a0) |


---

## Project Structure

```
project/
│
├── main.py                    # Entry point for Kinect-based pipeline
├── System_Framework.py        # Main orchestration of all modules
│
├── Kinect_Streaming.py        # Kinect V2 RGB-D frame capture
├── Color_Processing.py        # Green marker detection (Stage 1)
├── Depth_Processing.py        # Depth segmentation + point cloud (Stage 2)
├── ICP.py                     # ICP 3D registration
├── Visualization.py           # OpenGL shoe model rendering
│
├── estimate_depth.py          # Approach 2a: MiDaS monocular depth from phone video
├── estimate_stereo/
│   └── estimate.py            # Approach 2b: Stereo SGBM depth from two phone images
│
├── Another_one/               # Alternative implementations & experiments
│   ├── Try_on.py              # Open3D ICP pipeline using video files
│   ├── Try_on_2.py            # MediaPipe pose landmarks + trimesh
│   └── Try_on_3.py            # MediaPipe + pyrender offscreen rendering
│
├── 3D_models_assets/          # .obj shoe 3D models
├── 2_stages_en.md             # Two-stage pipeline documentation (English)
├── 2_stages_fr.md             # Two-stage pipeline documentation (French)
└── requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

### Approach 1 — Kinect V2 (Real-Time)

Plug in the Kinect V2 and run:

```bash
python main.py
```

Press `Q` to quit. To change the shoe model, edit `main.py`:

```python
shoe_model_path = "3D_models_assets/shoe_0.obj"
```

---

### Approach 2a — Monocular Depth (Phone, Single Video)

Record a video of your foot with your phone, then run:

```bash
python estimate_depth.py
```

Edit `estimate_depth.py` to point to your video:

```python
video_path = "your_foot_video.mp4"
```

Outputs `rgb_output.mp4` and `depth_output.mp4`.

---

### Approach 2b — Stereo Depth (Phone, Two Videos)

Record two videos from slightly different angles (left and right), then run:

```bash
python estimate_stereo/estimate.py
```

Edit the paths in `estimate.py`:

```python
left_video_path  = "foot_left.mp4"
right_video_path = "foot_right.mp4"
```

Outputs `stereo_rgb_output.mp4` and `stereo_depth_output.mp4`, which feed into `Another_one/Try_on.py`.

---

## Approach Comparison

| | Approach 1 (Kinect) | Approach 2a (MiDaS) | Approach 2b (Stereo) |
|---|---|---|---|
| Hardware needed | Kinect V2 | Phone | Phone (x2 angles) |
| Depth quality | High (hardware) | Medium (estimated) | Medium (estimated) |
| Real-time | Yes | Depends on GPU | Depends on GPU |
| Accessibility | Low | High | High |
| Best use case | Studio / lab | Field evaluation | Field evaluation |

---

## Key Dependencies

| Library | Purpose |
|---------|---------|
| `pykinect2` | Kinect V2 streaming |
| `open3d` | Point cloud + ICP registration |
| `opencv-python` | Image processing, video I/O, stereo SGBM |
| `torch` | MiDaS monocular depth estimation |
| `mediapipe` | Pose landmark detection (alternative pipelines) |
| `trimesh` / `pyrender` | 3D mesh loading and rendering |
| `PyOpenGL` | OpenGL-based rendering |

---

## References

- [MiDaS: Towards Robust Monocular Depth Estimation](https://arxiv.org/abs/1907.01341) — Ranftl et al.
- [Iterative Closest Point (ICP)](https://en.wikipedia.org/wiki/Iterative_closest_point) — 3D registration algorithm
- [Stereo SGBM](https://docs.opencv.org/4.x/d2/d85/classcv_1_1StereoSGBM.html) — OpenCV Semi-Global Block Matching
- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html) — Google real-time pose estimation
- [Microsoft Kinect V2](https://developer.microsoft.com/en-us/windows/kinect/) — RGB-D depth sensing hardware
