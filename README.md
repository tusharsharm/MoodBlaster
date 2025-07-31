# Mood Blaster - Webcam Facial Expression Game

A real-time facial expression recognition game that uses computer vision to detect emotions through your webcam. Challenge yourself to match prompted emotions using your facial expressions!

## Features

- **Real-time Face Detection**: Uses MediaPipe for accurate facial landmark detection
- **Emotion Recognition**: Detects happy, neutral, and angry expressions
- **Camera-only Gameplay**: Automatic camera activation with visual face detection feedback
- **Live Emotion Percentages**: See real-time confidence scores for all emotions
- **No Time Pressure**: Progress at your own pace - advance only when correct emotion is detected
- **Visual Feedback**: Green bounding box around detected faces with "FACE DETECTED" indicator
- **Progressive Scoring**: Level up every 5 successful matches with performance tracking

## Technology Stack

- **Backend**: Python Flask web application
- **Computer Vision**: MediaPipe for facial landmarks, OpenCV for image processing
- **Frontend**: HTML5, CSS3, JavaScript with Canvas API for face detection overlay
- **Real-time Processing**: WebRTC for camera access, AJAX for emotion analysis

## Game Rules

1. **Camera Activation**: Camera starts automatically when you begin the game
2. **Emotion Prompts**: Follow on-screen instructions to show specific emotions
3. **Detection Threshold**: Achieve 90% confidence in the target emotion to progress
4. **No Time Limits**: Take as much time as you need to show the correct expression
5. **Lives System**: You have 3 lives (though timeout penalties are disabled)
6. **Scoring**: Earn points based on accuracy and build up streaks

## Installation

### On Replit (Recommended)
1. Fork or import this project to Replit
2. Dependencies are automatically installed via `pyproject.toml`
3. Click "Run" to start the application
4. The game will be available at the provided URL

### Local Installation
1. **Install Dependencies**:
   ```bash
   pip install flask opencv-python mediapipe numpy pillow
   ```
   
   Or install from pyproject.toml:
   ```bash
   pip install -e .
   ```

2. **Run the Application**:
   ```bash
   python web_app.py
   ```

3. **Access the Game**:
   Open your web browser and navigate to `http://localhost:5000`

See `DEPENDENCIES.md` for detailed dependency information.

## Requirements

- **Python 3.7+**
- **Webcam**: Required for facial expression detection
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge with WebRTC support
- **Good Lighting**: Well-lit environment recommended for accurate face detection

## Browser Permissions

The game requires camera access to function. When prompted by your browser:
1. Click "Allow" when asked for camera permissions
2. Ensure your webcam is not being used by other applications
3. If camera access is blocked, check your browser settings

## Technical Architecture

### Core Components

- **EmotionDetector** (`emotion_detector.py`): MediaPipe-based emotion recognition
- **WebMoodBlasterGame** (`web_app.py`): Flask web server and game logic
- **Face Detection Overlay**: Real-time canvas rendering of face boundaries
- **Emotion Analysis API**: RESTful endpoints for frame processing

### Data Flow

1. Browser captures webcam frames via WebRTC
2. Frames sent to Flask backend every 200ms
3. MediaPipe processes facial landmarks
4. Geometric analysis determines emotion confidence
5. Results returned with face landmark coordinates
6. Frontend draws green detection box and updates percentages
7. Auto-progression when 90% confidence threshold is reached

## Supported Emotions

- **Happy**: Smile detection based on mouth curvature
- **Neutral**: Relaxed facial expression
- **Angry**: Frown detection with eyebrow position analysis

## Performance Tips

- **Lighting**: Ensure good, even lighting on your face
- **Position**: Sit directly facing the camera, about arm's length away
- **Background**: Use a simple background for better face detection
- **Expression**: Make clear, deliberate facial expressions for higher confidence scores

## Troubleshooting

### Camera Not Working
- Check if another application is using your webcam
- Verify browser permissions are granted
- Try refreshing the page and allow camera access again

### Low Detection Confidence
- Improve lighting conditions
- Move closer to the camera
- Make more exaggerated facial expressions
- Ensure your full face is visible in the camera frame

### Performance Issues
- Close unnecessary browser tabs
- Ensure stable internet connection
- Check that your device meets minimum requirements

## Development

### File Structure
```
mood-blaster/
├── web_app.py              # Flask web server and game logic
├── emotion_detector.py     # MediaPipe emotion detection
├── templates/
│   └── index.html         # Frontend interface
├── main.py                # Desktop version (legacy)
├── game.py                # Game logic classes
├── ui_renderer.py         # UI rendering utilities
├── pyproject.toml         # Python dependencies and project config
└── DEPENDENCIES.md        # Detailed dependency information
```

### API Endpoints

- `GET /` - Main game interface
- `POST /api/start_game` - Initialize new game session
- `POST /api/submit_emotion` - Manual emotion submission (legacy)
- `POST /api/analyze_frame` - Process webcam frame for emotion detection
- `GET /api/game_state` - Get current game status

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with different lighting conditions and devices
5. Submit a pull request

## License

This project is open source 

## Acknowledgments

- **MediaPipe**: Google's machine learning framework for face detection
- **OpenCV**: Computer vision library for image processing
- **Flask**: Lightweight web framework for Python
