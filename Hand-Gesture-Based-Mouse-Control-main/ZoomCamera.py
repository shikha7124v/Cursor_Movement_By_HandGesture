import cv2
import mediapipe as mp
import platform

gb_zoom = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
handNo = 0
device_val = None

def zoom_frame(image,same_image,coord):
    zoom_type="transitioin"
    global gb_zoom
    # If zoom_type is transition check if Zoom is already done else zoom by 0.1 in current frame
    if zoom_type == 'transition' and gb_zoom < 3.0:
        gb_zoom = gb_zoom + 0.1

    # If zoom_type is normal zoom check if zoom more than 1.4 if soo zoom out by 0.1 in each frame
    if gb_zoom != 1.4 and zoom_type is None:
        gb_zoom = gb_zoom - 0.1

    zoom = gb_zoom
    # If coordinates to zoom around are not specified, default to center of the frame.
    cy, cx = [i /2 for i in image.shape[:-1]] if coord is None else coord[::-1]

    # Scaling the image using getRotationMatrix2D to appropriate zoom.
    rot_mat = cv2.getRotationMatrix2D((cx, cy), 0, 1.5)

    # Use warpAffine to make sure that  lines remain parallel
    result1 = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    result2 = cv2.warpAffine(same_image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result2


def zoomat(img):
    unl_image=img
    lmList = []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    coordinates = None
    zoom_transition = None
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            height, width, channels = img.shape
            cx, cy = int(lm.x * width), int(lm.y * height)
            lmList.append([id, cx, cy])
            # Fetch coordinates of nose, right ear and left ear
        nose = lmList[9][1:]
        right_ear = lmList[20][1:]
        left_ear = lmList[4][1:]
        # print("nose=",nose,"\nright finger=",right_ear,"\nleft finger=",left_ear)

        #  get coordinates for right ear and left ear
        right_ear_x = int(right_ear[0] * width)
        left_ear_x = int(left_ear[0] * width)

        # Fetch coordinates for the nose and set as center
        center_x = int(right_ear[0])
        center_y = int(left_ear[1])
        coordinates = [center_x, center_y]

        # Perform zoom on the image
        img = zoom_frame(img,unl_image,coordinates)
    return img