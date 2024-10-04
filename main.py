import cv2
from hand_detector import HandDetector
from drawing_board import DrawingBoard

def main():
    cap = cv2.VideoCapture(0)
    hand_detector = HandDetector()
    drawing_board = DrawingBoard()

    # Define the new width and height for resizing the camera feed
    new_width = 900  # Set desired width
    new_height = 700  # Set desired height

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize the frame to the new dimensions
        frame = cv2.resize(frame, (new_width, new_height))

        # Flip the frame horizontally to correct mirror effect
        frame = cv2.flip(frame, 1)  # 1 means flipping around the y-axis

        hand_landmarks = hand_detector.find_hands(frame)

        # Check if the index finger is extended
        if hand_landmarks:
            # Check if the index finger tip is above a certain threshold (indicating it's raised)
            if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y:  # Finger raised
                drawing_board.track_finger(hand_landmarks,frame)
            else:
                # Reset previous position if finger is not extended
                drawing_board.previous_position = None  

        # Get the current canvas and overlay any drawing
        canvas = drawing_board.get_canvas()

        # Draw color boxes on the camera feed
        drawing_board.draw_color_boxes(frame)

        # Display both the whiteboard (canvas) and the camera feed
        cv2.imshow("Whiteboard", canvas)  # Display the canvas (whiteboard) as a separate window
        cv2.imshow("Camera Feed", frame)  # Display the resized camera feed for gesture tracking

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
