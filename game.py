"""
Game logic and state management for Mood Blaster.
"""

import cv2
import time
import random
import math
import numpy as np
from emotion_detector import EmotionDetector
from ui_renderer import UIRenderer

class GameState:
    """Enumeration of game states."""
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class MoodBlasterGame:
    """Main game class for Mood Blaster facial expression game."""
    
    def __init__(self):
        """Initialize the game."""
        self.emotion_detector = EmotionDetector()
        self.ui_renderer = UIRenderer()
        self.state = GameState.MENU
        
        # Demo mode for environments without webcam
        self.demo_mode = False
        self.demo_emotion = None
        
        # Game variables
        self.score = 0
        self.level = 1
        self.lives = 3
        self.current_target_emotion = None
        self.prompt_start_time = 0
        self.prompt_duration = 3.0  # Start with 3 seconds
        self.min_prompt_duration = 1.0  # Minimum time for higher levels
        
        # Emotions list
        self.emotions = ['happy', 'neutral', 'angry']
        self.emotion_sequence = []
        self.sequence_index = 0
        
        # Performance tracking
        self.reaction_times = []
        self.accuracy_streak = 0
        self.max_streak = 0
        
        # Game timing
        self.last_frame_time = time.time()
        self.fps = 30
        
    def generate_new_prompt(self):
        """Generate a new emotion prompt for the player."""
        # For higher levels, create sequences like Simon Says
        if self.level > 3 and len(self.emotion_sequence) == 0:
            # Create a sequence of emotions
            sequence_length = min(3 + (self.level // 4), 6)  # Max 6 emotions
            self.emotion_sequence = [random.choice(self.emotions) for _ in range(sequence_length)]
            self.sequence_index = 0
        
        if self.emotion_sequence:
            # Use sequence
            self.current_target_emotion = self.emotion_sequence[self.sequence_index]
            self.sequence_index += 1
            if self.sequence_index >= len(self.emotion_sequence):
                self.emotion_sequence = []
        else:
            # Random emotion
            self.current_target_emotion = random.choice(self.emotions)
        
        self.prompt_start_time = time.time()
        
        # Decrease prompt duration as level increases
        level_modifier = max(0.1, 1.0 - (self.level - 1) * 0.15)
        self.prompt_duration = max(self.min_prompt_duration, 3.0 * level_modifier)
    
    def check_emotion_match(self, detected_emotion, confidence):
        """Check if the detected emotion matches the target."""
        if detected_emotion == self.current_target_emotion and confidence > 0.6:
            # Calculate reaction time
            reaction_time = time.time() - self.prompt_start_time
            
            # Score based on speed and accuracy
            speed_bonus = max(0, int((self.prompt_duration - reaction_time) * 100))
            accuracy_bonus = int(confidence * 100)
            points = 100 + speed_bonus + accuracy_bonus
            
            self.score += points
            self.accuracy_streak += 1
            self.max_streak = max(self.max_streak, self.accuracy_streak)
            self.reaction_times.append(reaction_time)
            
            # Level up every 5 successful matches
            if len(self.reaction_times) % 5 == 0:
                self.level += 1
            
            return True
        return False
    
    def update_game(self):
        """Update game logic."""
        if self.state != GameState.PLAYING:
            return
        
        current_time = time.time()
        
        # Check if time is up for current prompt
        if current_time - self.prompt_start_time > self.prompt_duration:
            # Time's up - lose a life
            self.lives -= 1
            self.accuracy_streak = 0
            
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
            else:
                self.generate_new_prompt()
    
    def start_game(self):
        """Start a new game."""
        self.state = GameState.PLAYING
        self.score = 0
        self.level = 1
        self.lives = 3
        self.accuracy_streak = 0
        self.reaction_times = []
        self.emotion_sequence = []
        self.generate_new_prompt()
    
    def handle_input(self, key):
        """Handle keyboard input."""
        if key == ord(' '):  # Spacebar
            if self.state == GameState.MENU or self.state == GameState.GAME_OVER:
                self.start_game()
        elif key == 27:  # ESC
            return False  # Quit game
        elif self.demo_mode:
            # Demo mode keyboard controls
            if key == ord('h'):
                self.demo_emotion = 'happy'
            elif key == ord('a'):
                self.demo_emotion = 'angry'
            elif key == ord('n'):
                self.demo_emotion = 'neutral'
        return True
    
    def create_demo_frame(self):
        """Create a demo frame for environments without webcam."""
        # Create a black frame with demo text
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add demo mode indicators
        cv2.putText(frame, "DEMO MODE", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, "Press keys to simulate emotions:", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        cv2.putText(frame, "H = Happy, A = Angry, N = Neutral", (120, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        if self.demo_emotion:
            cv2.putText(frame, f"Current: {self.demo_emotion.upper()}", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame
    
    def handle_demo_input(self):
        """Handle demo mode emotion detection."""
        if self.demo_emotion:
            return self.demo_emotion, 0.9, None  # High confidence for demo
        return None, 0.0, None
    
    def run(self):
        """Main game loop."""
        clock = 0
        
        while True:
            current_time = time.time()
            dt = current_time - self.last_frame_time
            
            # Cap frame rate
            if dt < 1.0 / self.fps:
                continue
            
            self.last_frame_time = current_time
            clock += 1
            
            # Get frame (webcam or demo)
            if self.demo_mode:
                # Create a demo frame
                frame = self.create_demo_frame()
                detected_emotion, confidence, all_faces = self.handle_demo_input()
            else:
                if self.emotion_detector.cap and self.emotion_detector.cap.isOpened():
                    ret, frame = self.emotion_detector.cap.read()
                    if not ret:
                        print("Error: Could not read from webcam")
                        break
                    # Flip frame horizontally for mirror effect
                    frame = cv2.flip(frame, 1)
                    # Detect emotion
                    detected_emotion, confidence, all_faces = self.emotion_detector.detect_emotion(frame)
                else:
                    print("Error: No webcam available")
                    break
            
            # Update game logic
            self.update_game()
            
            # Check for emotion match during gameplay
            if (self.state == GameState.PLAYING and 
                detected_emotion and 
                self.current_target_emotion):
                
                if self.check_emotion_match(detected_emotion, confidence):
                    self.generate_new_prompt()
            
            # Render UI
            if self.state == GameState.MENU:
                frame = self.ui_renderer.render_menu(frame)
            elif self.state == GameState.PLAYING:
                time_left = max(0, self.prompt_duration - (current_time - self.prompt_start_time))
                frame = self.ui_renderer.render_game(
                    frame, 
                    self.current_target_emotion,
                    detected_emotion,
                    confidence,
                    self.score,
                    self.level,
                    self.lives,
                    time_left,
                    all_faces,
                    self.accuracy_streak
                )
            elif self.state == GameState.GAME_OVER:
                avg_reaction_time = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
                frame = self.ui_renderer.render_game_over(
                    frame,
                    self.score,
                    self.level,
                    len(self.reaction_times),
                    avg_reaction_time,
                    self.max_streak
                )
            
            # Show frame
            cv2.imshow('Mood Blaster', frame)
            
            # Handle input
            key = cv2.waitKey(1) & 0xFF
            if not self.handle_input(key):
                break
        
        # Cleanup
        self.emotion_detector.cleanup()
