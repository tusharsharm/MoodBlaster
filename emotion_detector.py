"""
Facial emotion detection using MediaPipe and OpenCV.
"""

import cv2
import mediapipe as mp
import numpy as np
import math

class EmotionDetector:
    """Detects facial emotions using MediaPipe face landmarks."""
    
    def __init__(self):
        """Initialize the emotion detector."""
        # Initialize MediaPipe solutions with proper error handling
        try:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.mp_drawing = mp.solutions.drawing_utils  
            self.mp_drawing_styles = getattr(mp.solutions, 'drawing_styles', None)
        except Exception as e:
            print(f"Warning: MediaPipe initialization issue: {e}")
            self.mp_face_mesh = None
            self.mp_drawing = None
            self.mp_drawing_styles = None
        
        # Initialize face mesh with error handling
        if self.mp_face_mesh:
            try:
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=5,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
            except Exception as e:
                print(f"Warning: Face mesh initialization failed: {e}")
                self.face_mesh = None
        else:
            self.face_mesh = None
        
        # Initialize webcam with fallback for environments without camera
        self.cap = None
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception:
            pass
        
        # Key facial landmark indices for emotion detection
        self.MOUTH_LANDMARKS = [61, 84, 17, 314, 405, 320, 308, 324, 318]
        self.LEFT_EYEBROW = [70, 63, 105, 66, 107]
        self.RIGHT_EYEBROW = [296, 334, 293, 300, 276]
        self.LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def calculate_mouth_curvature(self, landmarks, image_shape):
        """Calculate mouth curvature to detect smiles."""
        h, w = image_shape[:2]
        
        # Get mouth corner and center points
        left_corner = landmarks[61]  # Left mouth corner
        right_corner = landmarks[291]  # Right mouth corner
        top_lip = landmarks[13]  # Top lip center
        bottom_lip = landmarks[14]  # Bottom lip center
        
        # Convert normalized coordinates to pixel coordinates
        left_corner = (int(left_corner.x * w), int(left_corner.y * h))
        right_corner = (int(right_corner.x * w), int(right_corner.y * h))
        top_lip = (int(top_lip.x * w), int(top_lip.y * h))
        bottom_lip = (int(bottom_lip.x * w), int(bottom_lip.y * h))
        
        # Calculate mouth width and height
        mouth_width = self.calculate_distance(left_corner, right_corner)
        mouth_height = self.calculate_distance(top_lip, bottom_lip)
        
        # Calculate curvature (smile detection)
        mouth_center_y = (top_lip[1] + bottom_lip[1]) / 2
        corner_avg_y = (left_corner[1] + right_corner[1]) / 2
        
        # Positive curvature indicates upward curve (smile)
        curvature = (mouth_center_y - corner_avg_y) / mouth_width if mouth_width > 0 else 0
        
        return curvature, mouth_width, mouth_height
    
    def calculate_eyebrow_position(self, landmarks, image_shape):
        """Calculate eyebrow position to detect anger/surprise."""
        h, w = image_shape[:2]
        
        # Get eyebrow and eye landmarks
        left_eyebrow_points = [landmarks[i] for i in self.LEFT_EYEBROW]
        right_eyebrow_points = [landmarks[i] for i in self.RIGHT_EYEBROW]
        left_eye_points = [landmarks[i] for i in self.LEFT_EYE[:6]]  # Upper eyelid
        right_eye_points = [landmarks[i] for i in self.RIGHT_EYE[:6]]  # Upper eyelid
        
        # Calculate average eyebrow and eye positions
        left_eyebrow_y = np.mean([p.y for p in left_eyebrow_points]) * h
        right_eyebrow_y = np.mean([p.y for p in right_eyebrow_points]) * h
        left_eye_y = np.mean([p.y for p in left_eye_points]) * h
        right_eye_y = np.mean([p.y for p in right_eye_points]) * h
        
        # Calculate eyebrow-eye distance (negative = eyebrows closer to eyes)
        left_distance = left_eye_y - left_eyebrow_y
        right_distance = right_eye_y - right_eyebrow_y
        avg_distance = (left_distance + right_distance) / 2
        
        return avg_distance
    
    def calculate_eye_aspect_ratio(self, landmarks, image_shape):
        """Calculate eye aspect ratio for blink/expression detection."""
        h, w = image_shape[:2]
        
        # Left eye landmarks
        left_eye = [landmarks[i] for i in [33, 160, 158, 133, 153, 144]]
        # Right eye landmarks  
        right_eye = [landmarks[i] for i in [362, 385, 387, 263, 373, 380]]
        
        def eye_aspect_ratio(eye_landmarks):
            # Convert to pixel coordinates
            eye_points = [(int(p.x * w), int(p.y * h)) for p in eye_landmarks]
            
            # Calculate vertical distances
            vertical_1 = self.calculate_distance(eye_points[1], eye_points[5])
            vertical_2 = self.calculate_distance(eye_points[2], eye_points[4])
            
            # Calculate horizontal distance
            horizontal = self.calculate_distance(eye_points[0], eye_points[3])
            
            # Calculate aspect ratio
            ear = (vertical_1 + vertical_2) / (2.0 * horizontal) if horizontal > 0 else 0
            return ear
        
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        
        return (left_ear + right_ear) / 2
    
    def classify_emotion(self, landmarks, image_shape):
        """Classify emotion based on facial landmarks."""
        if not landmarks:
            return None, 0.0
        
        # Calculate facial features
        mouth_curvature, mouth_width, mouth_height = self.calculate_mouth_curvature(landmarks, image_shape)
        eyebrow_distance = self.calculate_eyebrow_position(landmarks, image_shape)
        eye_ratio = self.calculate_eye_aspect_ratio(landmarks, image_shape)
        
        # Emotion classification logic
        emotion_scores = {
            'happy': 0.0,
            'angry': 0.0,
            'neutral': 0.0
        }
        
        # Happy emotion indicators
        if mouth_curvature > 0.02:  # Upward mouth curve
            emotion_scores['happy'] += 0.6
        if mouth_curvature > 0.04:  # Strong smile
            emotion_scores['happy'] += 0.3
        if eyebrow_distance > 25:  # Relaxed eyebrows
            emotion_scores['happy'] += 0.1
        
        # Angry emotion indicators
        if mouth_curvature < -0.015:  # Downward mouth curve
            emotion_scores['angry'] += 0.4
        if eyebrow_distance < 15:  # Lowered/furrowed eyebrows
            emotion_scores['angry'] += 0.5
        if eye_ratio < 0.2:  # Squinted eyes
            emotion_scores['angry'] += 0.1
        
        # Neutral emotion (baseline)
        if abs(mouth_curvature) < 0.02:  # Straight mouth
            emotion_scores['neutral'] += 0.4
        if 15 <= eyebrow_distance <= 25:  # Normal eyebrow position
            emotion_scores['neutral'] += 0.3
        if 0.2 <= eye_ratio <= 0.35:  # Normal eye opening
            emotion_scores['neutral'] += 0.3
        
        # Find dominant emotion
        if emotion_scores:
            detected_emotion = max(emotion_scores.keys(), key=lambda x: emotion_scores[x])
            confidence = emotion_scores[detected_emotion]
        else:
            return None, 0.0
        
        # Apply minimum confidence threshold
        if confidence < 0.3:
            return None, 0.0
        
        return detected_emotion, min(confidence, 1.0)
    
    def detect_emotion(self, frame):
        """Detect emotion from a video frame, supporting multiple faces."""
        if not self.face_mesh or frame is None:
            return None, 0.0, []
            
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results and results.multi_face_landmarks:
                all_faces = []
                best_emotion = None
                best_confidence = 0.0
                
                # Process all detected faces
                for face_landmarks in results.multi_face_landmarks:
                    emotion, confidence = self.classify_emotion(face_landmarks.landmark, frame.shape)
                    
                    # Store face data
                    face_data = {
                        'landmarks': face_landmarks.landmark,
                        'emotion': emotion,
                        'confidence': confidence
                    }
                    all_faces.append(face_data)
                    
                    # Track the most confident emotion
                    if confidence > best_confidence:
                        best_emotion = emotion
                        best_confidence = confidence
                
                # Return best emotion and all face landmarks
                all_landmarks = [face['landmarks'] for face in all_faces]
                return best_emotion, best_confidence, all_landmarks
                
        except Exception as e:
            print(f"Warning: Emotion detection failed: {e}")
        
        return None, 0.0, []


def draw_face_boxes(self, frame, all_landmarks):
    """Draw bounding boxes around detected faces."""
    h, w = frame.shape[:2]
    
    for face_landmarks in all_landmarks:
        xs = [int(lm.x * w) for lm in face_landmarks]
        ys = [int(lm.y * h) for lm in face_landmarks]
        
        if xs and ys:
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, "FACE DETECTED", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    def cleanup(self):
        """Clean up resources."""
        if self.cap and hasattr(self.cap, 'release'):
            self.cap.release()
