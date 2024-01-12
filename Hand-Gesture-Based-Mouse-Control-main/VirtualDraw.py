import cv2 as cv
import os
from HandTrackingModule import handDetector
import numpy as np

width, height = 1280,720

cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation images
# print(pathImages)

# variable
imgNumber = 0
hs, ws = int(120 * 1), int(213 * 1)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 10
annotations = [[]]
annotationNumber = 0
annotationStart = False

# HandDetector
detector = handDetector(detectionCon=0.8, maxHands=1)

folderPath = "icon"

while True:
    # import images
    success, img = cap.read()
    img = cv.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv.imread(pathFullImage)
    imgCurrent = cv.resize(imgCurrent, (1280, 720))

    hands, img = detector.findHands(img)
    cv.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        # Contrain Values for easier Drawing

        xVal = int(np.interp(lmList[8][0], [width // 2, w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [175, height - 175], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:
            annotationStart = False
            # gesture - 1 left
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                annotationStart = False
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber -= 1

            # gesture - 2 right
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                annotationStart = False
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber += 1

        # gesture - 3 Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv.FILLED)
            annotationStart = False

        # gesture - 4 Draw Pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        # Gesture 5 - Erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

    else:
        annotationStart = False

    # Button Pressed Iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv.line(imgCurrent, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 12)

    # Adding webcam image on slides
    imgSmall = cv.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall

    cv.imshow("Image", img)
    cv.imshow("Slides", imgCurrent)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv.destroyAllWindows()