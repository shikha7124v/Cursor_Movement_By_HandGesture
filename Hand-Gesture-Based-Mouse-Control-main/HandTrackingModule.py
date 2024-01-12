import cv2  # Can be installed using "pip install opencv-python"
import mediapipe as mp  # Can be installed using "pip install mediapipe"
import time
import math
import numpy as np


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=False, trackCon=0.5):         # initializer that sets various parameters for hand tracking
                                                                                          # It initializes :- mpHands (MediaPipe hands module), hands (MediaPipe hands object), mpDraw (MediaPipe drawing utilities)
                                                                                          # and tipIds (list of finger tip indices) attributes.
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):    # Finds all hands in a frame
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      # findHands method Takes img as input, and converts it to RGB format
        self.results = self.hands.process(imgRGB)          # Further processing that RGB img using the 'hands' object to detect hands

        if self.results.multi_hand_landmarks:              # If hands are detected
            for handLms in self.results.multi_hand_landmarks:   # for each detected hand
                if draw:                                        # mpDraw is used to draw landmarks and connections on the image
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):   # Fetches the position of hands
        xList = []                     # for the storage of x coordinate of the detected landmarks
        yList = []                     # for the storage of y coordinate of the detected landmarks
        bbox = []                      # empty list to store the bounding box coordinates (xmin, ymin, xmax, ymax)
        self.lmList = []               # is an empty list to store the landmark information in the format [id, cx, cy]

        if self.results.multi_hand_landmarks:          # Check for detected hands, It extracts landmarks and calculates their coordinates.
            myHand = self.results.multi_hand_landmarks[handNo]      # It extracts the landmark of specified hand
            for id, lm in enumerate(myHand.landmark):  # it iterates through each landmark, extracting the id, and calculating the corresponding pixel coordinates (cx and cy) based on the image dimensions (c,w.h)
                h, w, c = img.shape
                print(h)
                print(w)
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:  # it draws circle at each landmark position on the image using open cv
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax       # calculating the bounding box around the detected hand

            if draw:    # it draws a rectangle around the hand
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox        # return self.lmList containing landmark information and bbox containing the bounding box coordinates

    def fingersUp(self):    # Checks which fingers are up
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):   # Finds distance between two fingers
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    pTime = 0           # Previous Time
    cTime = 0           # Current Time
    cap = cv2.VideoCapture(0)                # Default webcam of laptop
    detector = handDetector()
    while True:
        success, img = cap.read()             # It reads frame from webcam using cap
        img = detector.findHands(img)         # findHands method - to detect and draw landmarks on the hand in the frame
        lmList, bbox = detector.findPosition(img)         # this findPosition method is used to get the landmark positions and bounding box
        if len(lmList) != 0:                  # If landmarks are detected, it prints the information of the 5Th landmark (index 4)
            print(lmList[4])

        cTime = time.time()                   # Calculating frame per second (fps)
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,      # Displaying the fps
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)     # Shows the image using OpenCV
        cv2.waitKey(1)


if __name__ == "__main__":
    main()