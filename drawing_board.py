import numpy as np
import cv2

class DrawingBoard:
    def __init__(self):
        # Create a blank white canvas (whiteboard) for drawing
        self.canvas = np.ones((520, 680, 3), dtype="uint8") * 255  # White background
        self.previous_position = None
        self.color = (255, 0, 0)  # Default color (Red)

        # Define color boxes and their positions, adjusted for 900x700 camera frame
        self.color_boxes = {
            "Red": ((10, 10), (130, 110), (0, 0, 255)),        # Red box
            "Green": ((150, 10), (270, 110), (0, 255, 0)),     # Green box
            "Blue": ((290, 10), (410, 110), (255, 0, 0)),      # Blue box
            "Yellow": ((430, 10), (550, 110), (0, 255, 255)),  # Yellow box
            "Clear All": ((570, 10), (820, 110), (0, 0, 0))  # Clear All box (White)
        }


    def track_finger(self, hand_landmarks, frame):
    # Extract fingertip position (index finger)
        x, y = hand_landmarks.landmark[8].x * 900, hand_landmarks.landmark[8].y * 700  # Match your resized frame dimensions

        # Check if the fingertip is inside any of the color boxes
        for color, ((x1, y1), (x2, y2), _) in self.color_boxes.items():
            if x1 < x < x2 and y1 < y < y2:
                if color == "Clear All":
                    self.clear_canvas()  # Clear the canvas
                else:
                    self.color = self.color_boxes[color][2]  # Change color

        # Draw the fingertip marker on the frame (camera feed), not on the canvas
        cv2.circle(frame, (int(x), int(y)), 20, (0, 255, 255), -1)  # Yellow circle to mark the fingertip

        # Draw a line on the canvas from the previous position to the current position
        if self.previous_position is not None:
            cv2.line(self.canvas, self.previous_position, (int(x), int(y)), self.color, thickness=4)

        self.previous_position = (int(x), int(y))



    def overlay_drawing(self, frame):
        # Overlay the drawing on the current frame (not needed anymore)
        pass

    def clear_canvas(self):
        # Clear the canvas (reset to white)
        self.canvas = np.ones((480, 640, 3), dtype="uint8") * 255  # White background
        self.previous_position = None  # Reset previous position

    def draw_color_boxes(self, frame):
        # Draw color boxes on the frame (camera feed)
        for color, ((x1, y1), (x2, y2), box_color) in self.color_boxes.items():
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, -1)  # Draw filled rectangle
            cv2.putText(frame, color, (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # Adjusted text position

    def get_canvas(self):
        return self.canvas
