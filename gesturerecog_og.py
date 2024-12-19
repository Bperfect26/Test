import cv2;import mediapipe as mp;import math;import time;import pyautogui;import webbrowser
#Set up mediapipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
#Takes two landmarks and calculates the distance between them using pythagorean
def calculate_distance(landmark1, landmark2):
    return math.sqrt((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2)
#Using the landmark model on the mediapipe website, define each finger
def classify_gesture(landmarks):
    #Thumb
    thumb_is_up = landmarks[4].y < landmarks[3].y
    thumb_is_down = landmarks[4].y > landmarks[3].y
    #All fingers
    fingers_extended = [
        #Index Finger
        landmarks[8].y < landmarks[6].y,
        #Middle Finger
        landmarks[12].y < landmarks[10].y,
        #Ring Finger
        landmarks[16].y < landmarks[14].y,
        #Pinky Finger
        landmarks[20].y < landmarks[18].y,
    ]
    #Checks for basic gestures using all() function & the list
    all_fingers_extended = all(fingers_extended)
    no_fingers_extended = not any(fingers_extended)
    #Checks distance between tip of thumb and tip of index
    thumb_index_close = calculate_distance(landmarks[4], landmarks[8]) < 0.05
    #Check for distance between tip of thumb and middle finger, for closed fist
    thumb_middle_fist = calculate_distance(landmarks[4],landmarks[10]) < 0.5
    #Check for custom
    #~~GESTURE CHECKS~~
    if thumb_is_up and no_fingers_extended:
        return "Thumb Up"
    elif thumb_is_down and no_fingers_extended and not thumb_middle_fist:
        return "Thumb Down"
    elif all_fingers_extended:
        return "Open Palm"
    elif no_fingers_extended and thumb_middle_fist:
        return "Closed Fist"
    elif fingers_extended[0] and fingers_extended[1] and not any(fingers_extended[2:]):
        return "Peace"
    elif fingers_extended[0] and not any(fingers_extended[1:]):
        return "Pointing"
    elif thumb_index_close and not all_fingers_extended:
        return "OK Sign"
    else:
        return "Unknown Gesture"
#Calculates the size of the hand to filter out any hands in the background
def calculate_hand_size(landmarks, image_width, image_height):
    x_coords = [lm.x * image_width for lm in landmarks]
    y_coords = [lm.y * image_height for lm in landmarks]
    bbox_width = max(x_coords) - min(x_coords)
    bbox_height = max(y_coords) - min(y_coords)
    return bbox_width * bbox_height
#Constant used to filter based off proximity
MIN_HAND_SIZE = 9000

cap = cv2.VideoCapture(0)
#Processing using mediapipe
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break
        #Identifies the hand in the frame
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        left_hand_gesture = None
        right_hand_gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_size = calculate_hand_size(hand_landmarks.landmark, frame_width, frame_height)
                #Hand filtering
                if hand_size > MIN_HAND_SIZE:
                    hand_label = handedness.classification[0].label
                    hand_gesture = classify_gesture(hand_landmarks.landmark)
                    #Handedness check for display
                    if hand_label == "Left":
                        left_hand_gesture = hand_gesture
                    elif hand_label == "Right":
                        right_hand_gesture = hand_gesture
                #Display text
                    cv2.putText(
                        frame,f"{hand_label.capitalize()} Hand: {hand_gesture}",
                        (10, 30 + 40 * results.multi_hand_landmarks.index(hand_landmarks)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA
                    )
                #Draw landmarks onto the hands
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

        #Gesture based interactions (Opening/Closing tabs)
    
        '''if left_hand_gesture == "Pointing" and right_hand_gesture == "Pointing":
            pyautogui.hotkey('ctrl' , 't')
            time.sleep(1)
        elif left_hand_gesture == "Open Palm" and right_hand_gesture == "Open Palm":
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(1)
        elif left_hand_gesture == "Thumb Up" and right_hand_gesture == "Thumb Up":
            webbrowser.open("https://www.gmail.com")
            time.sleep(1)
            '''
        #Display processed frame into window
        #frame = cv2.resize(frame, (1000,1000), fx=1.5, fy=1.5)
        cv2.imshow("Hand Gesture Recognition", frame)
        #esc key to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()