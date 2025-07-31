#!/usr/bin/env python3
"""
Mood Blaster - Webcam Facial Expression Game
Main entry point for the game application.
"""

import cv2
import sys
from game import MoodBlasterGame

def main():
    """Main entry point for the Mood Blaster game."""
    try:
        # Initialize the game
        game = MoodBlasterGame()
        
        # Check if webcam is available
        if not game.emotion_detector.cap or not game.emotion_detector.cap.isOpened():
            print("Warning: No webcam detected. Running in demo mode with keyboard controls.")
            print("Demo Controls:")
            print("- Press 'h' for happy emotion")
            print("- Press 'a' for angry emotion") 
            print("- Press 'n' for neutral emotion")
            print("- SPACE: Start game / Restart")
            print("- ESC: Quit game")
            game.demo_mode = True
        else:
            print("Webcam detected! Show facial expressions to play.")
            game.demo_mode = False
        
        print("Starting Mood Blaster game...")
        print("Controls:")
        print("- SPACE: Start game / Restart")
        print("- ESC: Quit game")
        print("- Show different facial expressions to match the prompts!")
        
        # Run the game loop
        game.run()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    finally:
        # Cleanup
        cv2.destroyAllWindows()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
