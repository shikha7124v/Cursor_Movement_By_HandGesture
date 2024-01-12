import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
import HandDistance as hd
import ZoomCamera as zs
import os
from datetime import datetime
#####################################################
         #mouse variable
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

# cap=cv2.VideoCapture(1)
# cap.set(3,wCam)
# cap.set(4,hCam)
detector=htm.handDetector(maxHands=1)
wScr,hScr =autopy.screen.size()

count=0
flag=0
drawing_flag=0
#########################################################



#########################################################
              # virtual drawing variable
brushthickness=25
erasethickness=100

imagcanvas=np.zeros((480,640,3),np.uint8)

folderpath="Colors"
mylist=os.listdir(folderpath)
overlayList=[]
for imPath in mylist:
    image=cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

header=overlayList[0]
drawcolor=(255,255,255)
detector=htm.handDetector(detectionCon=0.85)


##########################################################


def open_camera(img):
    global flag,count,drawcolor,drawing_flag,xp,yp,plocX,plocY
    #cv2.flip(img,1)
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

        fingers = detector.fingersUp()

        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1:
            time.sleep(1)
            for i in range(1):
                count+=1

        if count%2==1:
            flag=1
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                drawing_flag=1
                xp, yp = 0, 0
                if y1 < 65:
                    if x1 < 106:
                        drawcolor = (0, 0, 0)
                    elif 107 < x1 < 212:
                        drawcolor = (0, 255, 255)
                    elif 213 < x1 < 318:
                        drawcolor = (0, 255, 0)
                    elif 319 < x1 < 424:
                        drawcolor = (255, 0, 0)
                    elif 425 < x1 < 530:
                        drawcolor = (0, 0, 255)
                    elif x1 > 531:
                        drawcolor = (255, 255, 255)

                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)

            if drawing_flag==1:
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    if drawcolor == (0, 0, 0):
                        cv2.line(img, (xp, yp), (x1, y1), drawcolor, erasethickness)
                        cv2.line(imagcanvas, (xp, yp), (x1, y1), drawcolor, erasethickness)
                    else:
                        cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushthickness)
                        cv2.line(imagcanvas, (xp, yp), (x1, y1), drawcolor, brushthickness)

                    xp, yp = x1, y1

        if count%2==0:
            flag=0
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                length, img, lineInfo = detector.findDistance(4, 8, img)
                if length >83:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    autopy.mouse.move(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                if length < 80:
                    buttonpressd = True
                    pyautogui.click(button='left')

            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                length, img, lineInfo = detector.findDistance(8, 20, img)
                if length < 100:
                    pyautogui.click(button='right')

            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
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

            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                lengthscroll1, img, lineInfo1 = detector.findDistance(8, 12, img)
                lengthscroll2, img, lineInfo2 = detector.findDistance(12, 16, img)

                if lengthscroll1 < 70 and lengthscroll2 < 70:
                    cv2.circle(img, (lineInfo1[4], lineInfo1[5]), 5, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, (lineInfo2[4], lineInfo2[5]), 5, (0, 255, 0), cv2.FILLED)
                    ss = pyautogui.screenshot()
                    dates=datetime.now()
                    datesname=str(dates)
                    names="screenshots\\"+datesname+".png"
                    time.sleep(1)
                    ss.save(names)



        if flag==1:
            #cv2.flip(img,1)
            imggray = cv2.cvtColor(imagcanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imggray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            # img=cv.bitwise_and(img,imgInv)
            img = cv2.bitwise_or(img, imagcanvas)

            img[:50, :106] = overlayList[0]
            img[:50, 106:212] = overlayList[1]
            img[:50, 212:318] = overlayList[2]
            img[:50, 318:424] = overlayList[3]
            img[:50, 424:530] = overlayList[4]
            img[:50, 530:636] = overlayList[5]
            img = cv2.addWeighted(img, 1, imagcanvas, 1, 0)
        img = cv2.flip(img, 1)
    return img