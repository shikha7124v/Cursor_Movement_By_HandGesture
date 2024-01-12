import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
import HandDistance as hd
import ZoomCamera as zs


wCam,hCam=640,480
frameR=170
smoothening = 4
buttondelay = 21
buttoncounter=0
buttonpressd=False


pTime=0
plocX=0
plocY=0
clocX,clocY=0,0

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(maxHands=1)
wScr,hScr =autopy.screen.size()

while True:
    success,img=cap.read()
    new_img=img
    distance = hd.distance(img)
    if distance>100:
        img=zs.zoomat(img)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x4, y4 = lmList[4][1:]
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 0, 255), 2)
        # img=img[bbox[1]:bbox[3] , bbox[0]:bbox[2]]
        # img=cv2.resize(img,(500,800))

        # 3 check which finger are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4 only index finger : moving mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # 5 convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6 smooth values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7 move mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8 both index and middel fingers are up : clicking mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # 9 find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # 10 click mouse if distence short
            if length < 45:
                buttonpressd = True
                # cv2.circle(img,(lineInfo[4],lineInfo[5]),5,(0,255,0),cv2.FILLED)
                pyautogui.click(button='left')
                # autopy.mouse.click()

        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            length, img, lineInfo = detector.findDistance(8, 20, img)
            if length < 100:
                pyautogui.click(button='right')

        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            length, img, lineInfo = detector.findDistance(4, 8, img)

            if length < 115:
                speedup = length
                speedup = int(speedup)
                speedup = speedup * 5
                pyautogui.scroll(speedup)

            if length > 120:
                speeddown = length
                speeddown = int(speeddown)
                speeddown = speeddown * 2
                pyautogui.scroll(-speeddown)

        # tack screenshots
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 0 and fingers[4] == 0:
            lengthscroll1, img, lineInfo1 = detector.findDistance(8, 12, img)
            lengthscroll2, img, lineInfo2 = detector.findDistance(12, 16, img)

            if lengthscroll1 < 70 and lengthscroll2 < 70:
                cv2.circle(img, (lineInfo1[4], lineInfo1[5]), 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (lineInfo2[4], lineInfo2[5]), 5, (0, 255, 0), cv2.FILLED)
                ss = pyautogui.screenshot()
                ss.save(r"D:\Machine Learning\Object detection\virtual mouse control\screenshort.png")


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    img = cv2.flip(img, 1)
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("images",img)
    key=cv2.waitKey(30)
    if key==27:
        cap.release()
        cv2.destroyAllWindows()
        break
    