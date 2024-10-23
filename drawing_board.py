import numpy as np
import cv2
from tkinter import filedialog, Tk

class DrawingBoard:
    def __init__(self):
        # Create a blank white canvas (whiteboard) for drawing
        self.canvas = np.ones((520, 680, 3), dtype="uint8") * 255  # White background
        self.previous_position = None
        self.color = (255, 0, 0)  # Default color (Red)

        # Define button boxes and their positions, adjusted for vertical alignment and width increased
        self.color_boxes = {
            "Red": ((10, 10), (120, 50), (0, 0, 255)),        # Red box (increased width)
            "Green": ((10, 70), (120, 110), (0, 255, 0)),     # Green box (increased width)
            "Blue": ((10, 130), (120, 170), (255, 0, 0)),     # Blue box (increased width)
            "Yellow": ((10, 190), (120, 230), (0, 255, 255)), # Yellow box (increased width)
            "Clear All": ((10, 250), (120, 290), (0, 0, 0)),  # Clear All box (Black, increased width)
            "Open": ((10, 310), (120, 350), (0, 0, 139)),     # Open button (Dark Blue, increased width)
            "Save": ((10, 370), (120, 410), (139, 69, 19)),   # Save button (Brown, increased width)
            "Save As": ((10, 430), (120, 470), (128, 0, 128)) # Save As button (Purple, increased width)
        }

    def track_finger(self, hand_landmarks, frame):
        x, y = hand_landmarks.landmark[8].x * 900, hand_landmarks.landmark[8].y * 700  # Match your resized frame dimensions

        # Check if the fingertip is inside any of the button boxes
        for button, ((x1, y1), (x2, y2), _) in self.color_boxes.items():
            if x1 < x < x2 and y1 < y < y2:
                if button == "Clear All":
                    self.clear_canvas()  # Clear the canvas
                elif button == "Open":
                    self.open_file()  # Open an existing drawing
                elif button == "Save":
                    self.save_file()  # Save the current drawing
                elif button == "Save As":
                    self.save_as_file()  # Save As functionality
                else:
                    self.color = self.color_boxes[button][2]  # Change color

        # Draw a marker on the frame to show fingertip position
        cv2.circle(frame, (int(x), int(y)), 20, (0, 255, 255), -1)  # Yellow circle to mark the fingertip

        # Draw a line on the canvas from the previous position to the current position
        if self.previous_position is not None:
            cv2.line(self.canvas, self.previous_position, (int(x), int(y)), self.color, thickness=4)

        self.previous_position = (int(x), int(y))

    def open_file(self):
        # Open an image file and set it as the canvas
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            loaded_image = cv2.imread(file_path)
            if loaded_image is not None:
                self.canvas = cv2.resize(loaded_image, (680, 520))  # Resize to fit canvas size
        root.destroy()

    def save_file(self):
        # Save the current drawing to an existing file
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, self.canvas)
        root.destroy()

    def save_as_file(self):
        # Save As functionality to save the canvas to a new file
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, self.canvas)
        root.destroy()

    def clear_canvas(self):
        # Clear the canvas (reset to white)
        self.canvas = np.ones((520, 680, 3), dtype="uint8") * 255  # White background
        self.previous_position = None  # Reset previous position

    def draw_color_boxes(self, frame):
        # Draw button boxes on the frame (camera feed)
        for label, ((x1, y1), (x2, y2), box_color) in self.color_boxes.items():
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, -1)  # Draw filled rectangle
            cv2.putText(frame, label, (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # Label the buttons

    def get_canvas(self):
        return self.canvas
