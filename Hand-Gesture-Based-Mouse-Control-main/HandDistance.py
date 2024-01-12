from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np

detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find Function
# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

def distance(img):
    hands= detector.findHands(img, draw=False)

    if hands:
        handlmlist = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1, _ = handlmlist[5]
        x2, y2, _ = handlmlist[17]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = int(A * distance ** 2 + B * distance + C)

        return distanceCM

    else:
        return 0


