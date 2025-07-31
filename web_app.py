#!/usr/bin/env python3
"""
Web-based Mood Blaster Game using Flask
Compatible with Replit environment
"""

from flask import Flask, render_template, request, jsonify, Response
import cv2
import json
import time
import random
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import threading
from emotion_detector import EmotionDetector

app = Flask(__name__)

class WebMoodBlasterGame:
    """Web-based version of Mood Blaster game."""
    
    def __init__(self):
        self.state = "menu"  # menu, playing, game_over
        self.score = 0
        self.level = 1
        self.lives = 3
        self.current_target_emotion = None
        self.prompt_start_time = 0
        self.prompt_duration = 5.0
        self.emotions = ['happy', 'neutral', 'angry']
        self.accuracy_streak = 0
        self.reaction_times = []
        self.game_running = False
        
    def start_game(self):
        """Start a new game."""
        self.state = "playing"
        self.score = 0
        self.level = 1
        self.lives = 3
        self.accuracy_streak = 0
        self.reaction_times = []
        self.generate_new_prompt()
        self.game_running = True
        
    def generate_new_prompt(self):
        """Generate a new emotion prompt."""
        self.current_target_emotion = random.choice(self.emotions)
        self.prompt_start_time = time.time()
        # Decrease prompt duration as level increases
        level_modifier = max(0.4, 1.0 - (self.level - 1) * 0.05)
        self.prompt_duration = max(3.0, 5.0 * level_modifier)
        
    def check_emotion_match(self, detected_emotion):
        """Check if detected emotion matches target."""
        if detected_emotion == self.current_target_emotion:
            reaction_time = time.time() - self.prompt_start_time
            
            # Calculate score based on speed
            speed_bonus = max(0, int((self.prompt_duration - reaction_time) * 100))
            points = 100 + speed_bonus
            
            self.score += points
            self.accuracy_streak += 1
            self.reaction_times.append(reaction_time)
            
            # Level up every 5 successful matches
            if len(self.reaction_times) % 5 == 0:
                self.level += 1
                
            self.generate_new_prompt()
            return True
        return False
        
    def check_timeout(self):
        """Check if current prompt has timed out."""
        if self.state == "playing" and self.current_target_emotion:
            time_elapsed = time.time() - self.prompt_start_time
            if time_elapsed > self.prompt_duration:
                self.lives -= 1
                self.accuracy_streak = 0
                if self.lives <= 0:
                    self.state = "game_over"
                    self.game_running = False
                else:
                    self.generate_new_prompt()
                return True
        return False
        
    def get_game_state(self):
        """Get current game state for web interface."""
        time_left = 0
        if self.state == "playing" and self.current_target_emotion:
            time_left = max(0, self.prompt_duration - (time.time() - self.prompt_start_time))
            
        return {
            'state': self.state,
            'score': self.score,
            'level': self.level,
            'lives': self.lives,
            'target_emotion': self.current_target_emotion,
            'time_left': round(time_left, 1),
            'streak': self.accuracy_streak,
            'avg_reaction_time': round(sum(self.reaction_times) / len(self.reaction_times), 2) if self.reaction_times else 0
        }

# Global game instance and emotion detector
game = WebMoodBlasterGame()
emotion_detector = EmotionDetector()

@app.route('/')
def index():
    """Main game page."""
    return render_template('index.html')

@app.route('/api/game_state')
def get_game_state():
    """Get current game state."""
    game.check_timeout()  # Check for timeouts
    return jsonify(game.get_game_state())

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Start a new game."""
    game.start_game()
    return jsonify({'success': True})

@app.route('/api/submit_emotion', methods=['POST'])
def submit_emotion():
    """Submit an emotion guess."""
    data = request.get_json()
    detected_emotion = data.get('emotion')
    
    if game.state == "playing" and detected_emotion:
        match = game.check_emotion_match(detected_emotion)
        return jsonify({
            'success': True,
            'match': match,
            'game_state': game.get_game_state()
        })
    
    return jsonify({'success': False})

@app.route('/api/reset_game', methods=['POST'])
def reset_game():
    """Reset game to menu."""
    game.state = "menu"
    game.game_running = False
    return jsonify({'success': True})

@app.route('/api/analyze_frame', methods=['POST'])
def analyze_frame():
    """Analyze a camera frame for emotion detection."""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'})
        
        # Remove data URL prefix
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Convert PIL image to OpenCV format
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect emotion using our emotion detector
        if emotion_detector.face_mesh:
            emotion, confidence, landmarks = emotion_detector.detect_emotion(frame)
            
            # Calculate emotion percentages for all emotions
            emotion_percentages = {
                'happy': 0.0,
                'neutral': 0.0,
                'angry': 0.0
            }
            
            if emotion and confidence:
                # Simulate more realistic percentages based on detected emotion
                if emotion == 'happy':
                    emotion_percentages['happy'] = confidence * 100
                    emotion_percentages['neutral'] = max(0, (0.5 - confidence/2) * 100)
                    emotion_percentages['angry'] = max(0, (0.2 - confidence/5) * 100)
                elif emotion == 'neutral':
                    emotion_percentages['neutral'] = confidence * 100
                    emotion_percentages['happy'] = max(0, (0.4 - confidence/3) * 100)
                    emotion_percentages['angry'] = max(0, (0.3 - confidence/4) * 100)
                elif emotion == 'angry':
                    emotion_percentages['angry'] = confidence * 100
                    emotion_percentages['neutral'] = max(0, (0.3 - confidence/4) * 100)
                    emotion_percentages['happy'] = max(0, (0.1 - confidence/10) * 100)
            
            return jsonify({
                'emotion': emotion,
                'confidence': confidence if confidence else 0.0,
                'percentages': emotion_percentages,
                'success': True
            })
        else:
            # Fallback: simple mock detection based on current time for demo
            emotions = ['happy', 'neutral', 'angry']
            mock_emotion = emotions[int(time.time()) % len(emotions)]
            
            return jsonify({
                'emotion': mock_emotion,
                'confidence': 0.5,
                'success': True,
                'note': 'MediaPipe not available, using demo mode'
            })
            
    except Exception as e:
        print(f"Error analyzing frame: {e}")
        return jsonify({
            'error': 'Frame analysis failed',
            'emotion': None,
            'confidence': 0.0,
            'success': False
        })

if __name__ == '__main__':
    # Create templates directory and files
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)