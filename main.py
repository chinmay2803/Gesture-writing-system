import cv2
from hand_detector import HandDetector
from drawing_board import DrawingBoard

def main():
    cap = cv2.VideoCapture(0)
    hand_detector = HandDetector()
    drawing_board = DrawingBoard()

    # Ask user if they want to open a previously saved file
    # drawing_board.open_canvas()

    new_width = 900
    new_height = 700

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (new_width, new_height))
        frame = cv2.flip(frame, 1)

        hand_landmarks = hand_detector.find_hands(frame)

        if hand_landmarks:
            if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y:
                drawing_board.track_finger(hand_landmarks, frame)
            else:
                drawing_board.previous_position = None

        canvas = drawing_board.get_canvas()
        drawing_board.draw_color_boxes(frame)

        cv2.imshow("Whiteboard", canvas)
        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
