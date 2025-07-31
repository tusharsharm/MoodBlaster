# Project Dependencies

This project uses the following Python packages, which are already configured in `pyproject.toml`:

## Core Dependencies

### Web Framework
- **flask** - Lightweight web framework for the game interface

### Computer Vision & Machine Learning
- **opencv-python** - Computer vision library for image processing
- **mediapipe** - Google's ML framework for facial landmark detection
- **numpy** - Numerical computing for array operations

### Image Processing
- **pillow** - Python Imaging Library for image manipulation

## Installation

Dependencies are automatically managed by the Replit environment. If running locally:

```bash
# Using pip
pip install flask opencv-python mediapipe numpy pillow

# Or using the existing pyproject.toml
pip install -e .
```

## Version Information

The project is compatible with:
- Python 3.7+
- All dependencies are pinned to stable versions in pyproject.toml
- Cross-platform support (Windows, macOS, Linux)

## System Requirements

### Hardware
- Webcam (required for facial detection)
- Minimum 4GB RAM (recommended for MediaPipe processing)
- CPU with decent processing power for real-time computer vision

### Software
- Modern web browser with WebRTC support
- Camera permissions enabled in browser
- Good lighting conditions for optimal face detection