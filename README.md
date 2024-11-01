# Virtual Try-On System for Footwear Design Evaluation Using Depth-Sensing Technology

This paper introduces a virtual try-on system designed to evaluate footwear designs using depth-sensing technology. Here’s a breakdown of the system's key aspects:

1. **Mixed Reality Environment**: The system enables users to see a live video feed of their feet, overlaid with 3D models of shoes. This creates a "mixed reality" experience, where users can visualize how a specific shoe design would look on their feet in real time.

2. **Two-Stage Object Tracking Algorithm**: To align the virtual shoe models accurately with the user’s moving feet, the researchers developed a two-stage tracking approach, improving accuracy compared to using surface registration alone:
   - **Color Marker Detection**: Markers placed on the user’s foot are detected by the system to assist with initial foot positioning. This enables foot tracking without relying on external markers.
   - **Iterative Closest Point (ICP) Algorithm**: The ICP algorithm aligns the captured depth data with predefined 3D models of the foot, adjusting the shoe model as the foot moves for a seamless try-on experience.

3. **Increased Positional Accuracy**: Tests showed that this two-stage approach yields more accurate positioning of the virtual shoe compared to surface registration alone, which is less reliable with movement.

4. **Improved Computational Efficiency**: To enhance the ICP algorithm’s speed, the foot model is trimmed based on the current view angle, meaning only data relevant to the user’s viewing perspective is processed.

5. **Human-Centered Design Tool**: This virtual try-on system supports footwear designers by allowing them to evaluate how shoes appear on actual feet, assisting in user-centered design evaluations.

6. **Novel Application of RGB-D Cameras**: This system highlights how RGB-D cameras, which capture both color (RGB) and depth (D) data, can be used effectively in product design to create immersive and interactive consumer try-on experiences.

