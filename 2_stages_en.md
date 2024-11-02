# Two-Stage Foot Tracking System for Virtual Footwear Try-On

This document explains the process flow of a two-stage foot tracking system for accurately aligning 3D virtual footwear models with a user’s foot in a mixed reality environment. The system uses depth data and color data captured by an RGB-D camera and is divided into two main stages: **Stage 1 - Initial Detection** and **Stage 2 - Precise Tracking**.

## Overview of Inputs
- **Image Capture**: An RGB-D camera captures both color and depth data of the user's foot.
  - **Depth Data**: Provides 3D information of the foot's shape and position.
  - **Color Data**: Captures color information, useful for initial marker detection.

## Stage 1: Initial Detection and Rough Positioning
In the first stage, the system performs initial detection and rough alignment of the virtual shoe model to the user's foot.

1. **Marker Detecting**:
   - Uses color data to detect specific color markers on the foot. These markers help locate and identify key points on the foot.
   - Provides a general position and orientation of the foot for rough alignment.

2. **Rough Positioning**:
   - Positions the virtual shoe model roughly in line with the user’s foot.
   - Displays the rough alignment overlay on the screen, providing immediate feedback.

## Stage 2: Precise Foot Tracking and Registration
The second stage refines the alignment using depth data for a more accurate fit.

1. **Foot Segmentation**:
   - Segments the user’s foot using depth data, isolating it from the background for accurate tracking.

2. **ICP 3D Registration**:
   - Uses the Iterative Closest Point (ICP) algorithm to align the depth data of the foot with a reference foot model.
   - Fine-tunes the virtual shoe alignment, minimizing the distance between real foot points and the virtual model.

3. **Trim Algorithm**:
   - Trims the reference model based on the view angle, reducing computational load and improving efficiency.

4. **Previous Tracking Result**:
   - Utilizes the previous frame’s tracking data to ensure smooth tracking, especially when the foot moves quickly.

## Final Output: Foot Location
The precise foot location is then displayed with an accurately aligned virtual shoe model, creating a realistic, responsive virtual try-on experience.

---
