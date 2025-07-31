"""
UI rendering for the Mood Blaster game using OpenCV.
"""

import cv2
import numpy as np
import math
import time

class UIRenderer:
    """Handles all UI rendering for the game."""
    
    def __init__(self):
        """Initialize the UI renderer."""
        # Colors (BGR format)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (255, 0, 0)
        self.YELLOW = (0, 255, 255)
        self.PURPLE = (255, 0, 255)
        self.CYAN = (255, 255, 0)
        self.ORANGE = (0, 165, 255)
        self.PINK = (255, 192, 203)
        
        # Emotion colors
        self.emotion_colors = {
            'happy': self.GREEN,
            'angry': self.RED,
            'neutral': self.BLUE
        }
        
        # Animation variables
        self.pulse_time = 0
        
    def draw_text(self, frame, text, position, font_scale=1.0, color=(255, 255, 255), thickness=2):
        """Draw text on the frame with outline for better visibility."""
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Draw outline
        cv2.putText(frame, text, position, font, font_scale, self.BLACK, thickness + 2)
        # Draw main text
        cv2.putText(frame, text, position, font, font_scale, color, thickness)
        
        return frame
    
    def draw_emotion_icon(self, frame, emotion, position, size=80, animated=False):
        """Draw an emotion icon using geometric shapes."""
        x, y = position
        radius = size // 2
        
        # Pulse animation
        if animated:
            self.pulse_time += 0.1
            pulse_factor = 1.0 + 0.2 * math.sin(self.pulse_time * 6)
            radius = int(radius * pulse_factor)
        
        # Draw face circle
        color = self.emotion_colors.get(emotion, self.WHITE)
        cv2.circle(frame, (x, y), radius, color, -1)
        cv2.circle(frame, (x, y), radius, self.BLACK, 3)
        
        # Draw eyes
        eye_offset = radius // 3
        eye_radius = radius // 8
        left_eye = (x - eye_offset, y - radius // 4)
        right_eye = (x + eye_offset, y - radius // 4)
        
        cv2.circle(frame, left_eye, eye_radius, self.BLACK, -1)
        cv2.circle(frame, right_eye, eye_radius, self.BLACK, -1)
        
        # Draw mouth based on emotion
        mouth_y = y + radius // 4
        mouth_width = radius // 2
        
        if emotion == 'happy':
            # Smiling mouth (arc)
            axes = (mouth_width, radius // 4)
            cv2.ellipse(frame, (x, mouth_y), axes, 0, 0, 180, self.BLACK, 3)
        elif emotion == 'angry':
            # Frowning mouth (inverted arc)
            axes = (mouth_width, radius // 4)
            cv2.ellipse(frame, (x, mouth_y - radius // 6), axes, 0, 180, 360, self.BLACK, 3)
            # Angry eyebrows
            brow_y = y - radius // 2
            cv2.line(frame, (x - eye_offset - 10, brow_y), (x - eye_offset + 10, brow_y + 5), self.BLACK, 4)
            cv2.line(frame, (x + eye_offset - 10, brow_y + 5), (x + eye_offset + 10, brow_y), self.BLACK, 4)
        else:  # neutral
            # Straight mouth
            cv2.line(frame, (x - mouth_width//2, mouth_y), (x + mouth_width//2, mouth_y), self.BLACK, 3)
        
        return frame
    
    def draw_progress_bar(self, frame, progress, position, size, color=None):
        """Draw a progress bar."""
        x, y, width, height = position[0], position[1], size[0], size[1]
        
        # Background
        cv2.rectangle(frame, (x, y), (x + width, y + height), self.BLACK, -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height), self.WHITE, 2)
        
        # Progress fill
        fill_width = int(width * progress)
        if color is None:
            # Color based on progress (red to green)
            if progress > 0.6:
                color = self.GREEN
            elif progress > 0.3:
                color = self.YELLOW
            else:
                color = self.RED
        
        if fill_width > 0:
            cv2.rectangle(frame, (x + 2, y + 2), (x + fill_width - 2, y + height - 2), color, -1)
        
        return frame
    
    def draw_heart(self, frame, position, size=20, color=None):
        """Draw a heart shape for lives."""
        if color is None:
            color = self.RED
        
        x, y = position
        # Simple heart approximation using circles and triangle
        cv2.circle(frame, (x - size//4, y), size//3, color, -1)
        cv2.circle(frame, (x + size//4, y), size//3, color, -1)
        
        # Bottom triangle
        points = np.array([[x, y + size//2], [x - size//2, y], [x + size//2, y]], np.int32)
        cv2.fillPoly(frame, [points], color)
        
        return frame
    
    def render_menu(self, frame):
        """Render the main menu screen."""
        height, width = frame.shape[:2]
        
        # Create a semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), self.BLACK, -1)
        frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
        
        # Title
        title_text = "MOOD BLASTER"
        title_size = 2.5
        text_size = cv2.getTextSize(title_text, cv2.FONT_HERSHEY_SIMPLEX, title_size, 3)[0]
        title_x = (width - text_size[0]) // 2
        title_y = height // 4
        
        # Animated title with rainbow effect
        colors = [self.RED, self.ORANGE, self.YELLOW, self.GREEN, self.CYAN, self.BLUE, self.PURPLE]
        for i, char in enumerate(title_text):
            char_color = colors[i % len(colors)]
            char_width = cv2.getTextSize(char, cv2.FONT_HERSHEY_SIMPLEX, title_size, 3)[0][0]
            self.draw_text(frame, char, (title_x, title_y), title_size, char_color, 3)
            title_x += char_width
        
        # Subtitle
        subtitle = "Facial Expression Challenge Game"
        subtitle_size = cv2.getTextSize(subtitle, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        subtitle_x = (width - subtitle_size[0]) // 2
        self.draw_text(frame, subtitle, (subtitle_x, title_y + 80), 1.0, self.WHITE, 2)
        
        # Emotion icons demo
        center_y = height // 2
        emotions = ['happy', 'neutral', 'angry']
        for i, emotion in enumerate(emotions):
            x = width // 4 + i * (width // 4)
            self.draw_emotion_icon(frame, emotion, (x, center_y), 60, True)
            
            # Emotion labels
            label_size = cv2.getTextSize(emotion.upper(), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            label_x = x - label_size[0] // 2
            self.draw_text(frame, emotion.upper(), (label_x, center_y + 80), 0.8, self.emotion_colors[emotion], 2)
        
        # Instructions
        instructions = [
            "Match the facial expressions as fast as you can!",
            "Get ready to smile, frown, and stay neutral.",
            "",
            "Press SPACE to start",
            "Press ESC to quit"
        ]
        
        start_y = height - 200
        for i, instruction in enumerate(instructions):
            if instruction:
                text_size = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                text_x = (width - text_size[0]) // 2
                self.draw_text(frame, instruction, (text_x, start_y + i * 30), 0.7, self.WHITE, 2)
        
        return frame
    
    def render_game(self, frame, target_emotion, detected_emotion, confidence, score, level, lives, time_left, landmarks, streak):
        """Render the main game interface."""
        height, width = frame.shape[:2]
        
        # Draw face landmarks if available
        if landmarks:
            for landmark in landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                cv2.circle(frame, (x, y), 1, self.GREEN, -1)
        
        # Top UI bar
        ui_height = 100
        cv2.rectangle(frame, (0, 0), (width, ui_height), (0, 0, 0, 180))
        
        # Score
        self.draw_text(frame, f"Score: {score}", (20, 30), 0.8, self.WHITE, 2)
        
        # Level
        self.draw_text(frame, f"Level: {level}", (20, 60), 0.8, self.WHITE, 2)
        
        # Lives (hearts)
        lives_start_x = width - 150
        self.draw_text(frame, "Lives:", (lives_start_x - 60, 40), 0.6, self.WHITE, 2)
        for i in range(lives):
            self.draw_heart(frame, (lives_start_x + i * 30, 35), 15)
        
        # Streak indicator
        if streak > 0:
            streak_text = f"Streak: {streak}"
            streak_size = cv2.getTextSize(streak_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            streak_x = width - streak_size[0] - 20
            self.draw_text(frame, streak_text, (streak_x, 70), 0.6, self.YELLOW, 2)
        
        # Target emotion display
        if target_emotion:
            # Large target emotion icon
            icon_x = width - 120
            icon_y = height - 120
            self.draw_emotion_icon(frame, target_emotion, (icon_x, icon_y), 80, True)
            
            # Target label
            target_text = f"Show: {target_emotion.upper()}"
            self.draw_text(frame, target_text, (icon_x - 60, icon_y + 60), 0.8, self.emotion_colors[target_emotion], 2)
            
            # Time remaining
            progress = time_left / 3.0  # Assuming max 3 seconds
            self.draw_progress_bar(frame, progress, (icon_x - 60, icon_y + 80), (120, 20))
            time_text = f"{time_left:.1f}s"
            self.draw_text(frame, time_text, (icon_x - 20, icon_y + 105), 0.6, self.WHITE, 2)
        
        # Detected emotion display
        if detected_emotion and confidence > 0.3:
            detect_x = 80
            detect_y = height - 120
            
            # Scale icon based on confidence
            icon_size = int(60 + 40 * confidence)
            self.draw_emotion_icon(frame, detected_emotion, (detect_x, detect_y), icon_size)
            
            # Detection info
            detect_text = f"Detected: {detected_emotion.upper()}"
            confidence_text = f"Confidence: {confidence:.1f}"
            
            self.draw_text(frame, detect_text, (detect_x - 50, detect_y + 50), 0.7, self.emotion_colors[detected_emotion], 2)
            self.draw_text(frame, confidence_text, (detect_x - 50, detect_y + 75), 0.6, self.WHITE, 2)
            
            # Match indicator
            if target_emotion and detected_emotion == target_emotion and confidence > 0.6:
                match_text = "MATCH!"
                self.draw_text(frame, match_text, (detect_x - 30, detect_y + 100), 1.0, self.GREEN, 3)
        
        # Center prompt for urgency
        if time_left < 1.0 and target_emotion:
            urgent_text = f"SHOW {target_emotion.upper()}!"
            text_size = cv2.getTextSize(urgent_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
            urgent_x = (width - text_size[0]) // 2
            urgent_y = height // 2 - 50
            
            # Pulsing effect
            pulse = int(255 * (0.5 + 0.5 * math.sin(time.time() * 10)))
            urgent_color = (0, 0, pulse) if target_emotion == 'angry' else (0, pulse, 0) if target_emotion == 'happy' else (pulse, pulse, 0)
            
            self.draw_text(frame, urgent_text, (urgent_x, urgent_y), 1.5, urgent_color, 3)
        
        return frame
    
    def render_game_over(self, frame, score, level, successful_matches, avg_reaction_time, max_streak):
        """Render the game over screen."""
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), self.BLACK, -1)
        frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
        
        # Game Over title
        title = "GAME OVER"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 2.0, 3)[0]
        title_x = (width - title_size[0]) // 2
        title_y = height // 4
        self.draw_text(frame, title, (title_x, title_y), 2.0, self.RED, 3)
        
        # Stats
        stats_y = height // 2 - 50
        stats = [
            f"Final Score: {score}",
            f"Level Reached: {level}",
            f"Successful Matches: {successful_matches}",
            f"Max Streak: {max_streak}",
            f"Avg Reaction Time: {avg_reaction_time:.2f}s" if avg_reaction_time > 0 else "Avg Reaction Time: N/A"
        ]
        
        for i, stat in enumerate(stats):
            stat_size = cv2.getTextSize(stat, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            stat_x = (width - stat_size[0]) // 2
            self.draw_text(frame, stat, (stat_x, stats_y + i * 40), 0.8, self.WHITE, 2)
        
        # Performance message
        perf_y = stats_y + len(stats) * 40 + 40
        if avg_reaction_time > 0:
            if avg_reaction_time < 1.0:
                perf_msg = "Lightning Fast! ⚡"
                perf_color = self.YELLOW
            elif avg_reaction_time < 2.0:
                perf_msg = "Great Reflexes! 🎯"
                perf_color = self.GREEN
            else:
                perf_msg = "Keep Practicing! 💪"
                perf_color = self.BLUE
            
            perf_size = cv2.getTextSize(perf_msg, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            perf_x = (width - perf_size[0]) // 2
            self.draw_text(frame, perf_msg, (perf_x, perf_y), 1.0, perf_color, 2)
        
        # Restart instructions
        restart_y = height - 100
        restart_text = "Press SPACE to play again or ESC to quit"
        restart_size = cv2.getTextSize(restart_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        restart_x = (width - restart_size[0]) // 2
        self.draw_text(frame, restart_text, (restart_x, restart_y), 0.7, self.WHITE, 2)
        
        return frame
