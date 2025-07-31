# Mood Blaster - Webcam Facial Expression Game

## Overview

Mood Blaster is a real-time facial expression recognition game that uses computer vision to detect emotions through a webcam. Players must match their facial expressions to on-screen prompts within time limits, creating an interactive gaming experience that combines machine learning with entertainment.

## User Preferences

Preferred communication style: Simple, everyday language.
Game timing preference: No time limits - progress only when correct emotion is detected.
Interface preference: Camera-only mode with automatic face detection and green bounding box around detected faces.
Confidence threshold preference: Progress to next level when emotion detection reaches 90% confidence.

## System Architecture

### Core Architecture Pattern
The application follows a modular, object-oriented architecture with clear separation of concerns:

- **Computer Vision Layer**: MediaPipe and OpenCV for facial landmark detection and emotion recognition
- **Game Logic Layer**: State management, scoring, and gameplay mechanics
- **UI Rendering Layer**: OpenCV-based visual interface and graphics rendering
- **Main Controller**: Application entry point and coordination

### Technology Stack
- **Primary Language**: Python 3
- **Computer Vision**: MediaPipe for facial landmark detection, OpenCV for image processing
- **Graphics**: OpenCV for real-time UI rendering and camera input
- **Architecture Pattern**: Component-based with clear interface boundaries

## Key Components

### EmotionDetector (`emotion_detector.py`)
- **Purpose**: Processes webcam feed to detect facial emotions using MediaPipe
- **Key Features**: 
  - Real-time face mesh analysis with 468 facial landmarks
  - Emotion classification based on facial geometry (mouth curvature, eyebrow position, eye state)
  - Optimized for single-face detection with confidence thresholds
- **Design Decision**: Uses geometric analysis rather than deep learning for faster, more predictable performance

### MoodBlasterGame (`game.py`)
- **Purpose**: Central game logic and state management
- **Key Features**:
  - State machine (MENU → PLAYING → GAME_OVER)
  - Progressive difficulty with decreasing time limits
  - Performance tracking (reaction times, accuracy streaks)
  - Lives system and scoring mechanism
- **Design Decision**: Separates game logic from rendering for maintainability and testability

### UIRenderer (`ui_renderer.py`)
- **Purpose**: Handles all visual rendering and user interface
- **Key Features**:
  - Real-time overlay graphics on camera feed
  - Emotion icons using geometric shapes
  - Animation system with pulse effects
  - Color-coded emotion feedback
- **Design Decision**: Uses OpenCV for rendering to avoid additional GUI framework dependencies

### Main Controller (`main.py`)
- **Purpose**: Application entry point and error handling
- **Key Features**:
  - Camera initialization and validation
  - Global exception handling
  - User instructions and game startup
- **Design Decision**: Minimal main function focused on coordination and error recovery

## Data Flow

1. **Camera Input**: Webcam captures real-time video frames
2. **Face Detection**: MediaPipe processes frames to extract facial landmarks
3. **Emotion Analysis**: Geometric calculations determine current emotion from landmark positions
4. **Game Logic**: Current emotion compared against target emotion with timing validation
5. **UI Update**: Rendered frame combines camera feed with game overlay graphics
6. **Display Output**: Final composited frame displayed to user

## External Dependencies

### Core Libraries
- **OpenCV**: Camera input, image processing, and UI rendering
- **MediaPipe**: Google's face mesh detection and landmark extraction
- **NumPy**: Mathematical operations and array processing

### System Requirements
- **Webcam**: Required for facial detection input
- **Python 3.7+**: Runtime environment
- **Sufficient Processing Power**: Real-time computer vision processing

## Deployment Strategy

### Local Development
- **Run Method**: Direct Python execution (`python main.py`)
- **Dependencies**: Install via pip (opencv-python, mediapipe, numpy)
- **Platform**: Cross-platform (Windows, macOS, Linux)

### Considerations
- **Camera Permissions**: Application requires webcam access
- **Performance**: Real-time processing requires adequate CPU/GPU resources
- **Environment**: Works best in well-lit conditions for accurate face detection

### Future Scalability
- Modular design allows for easy addition of new emotions
- Component separation enables potential web deployment with different rendering backends
- Game logic abstraction supports future multiplayer or mobile implementations