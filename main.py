import os
import random
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
import numpy as np
from folder import creatList
from obj import Obj

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)
idList = [0, 17, 78, 292]

eatables =  creatList('eatable')
nonEatables = creatList('noneatable')
Hearts = creatList('heart')


firstObj = Obj( [300, 0], eatables, nonEatables, eatables[random.randint(0, len(eatables)-1)], True)
secondObj = Obj( [600, 0], eatables, nonEatables, nonEatables[random.randint(0, len(nonEatables)-1)], False)
heartObj = Hearts[-1]
DoublePoint = eatables[5]

score = 0
gameOver = False
heart = 3

while True:
    success, img = cap.read()

    img = cv2.flip(img,1)
    
    if gameOver is False:

        img, faces = detector.findFaceMesh(img, draw=False)

        img = cvzone.overlayPNG(img, heartObj, (880,0))

        img = cvzone.overlayPNG(img, firstObj.currentObj, firstObj.pos)
        img = cvzone.overlayPNG(img, secondObj.currentObj, secondObj.pos)
        
        firstObj.fallDown(score)
        secondObj.fallDown(score)

        if faces:
            face = faces[0]

            up = face[idList[0]]
            down = face[idList[1]]

            upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
            leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])

            ## Distance of the Object
            cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
            distMouthObject, _ = detector.findDistance((cx, cy), 
                                                        (firstObj.pos[0] + 50, firstObj.pos[1] + 50))
            
            distMouthObject2, _ = detector.findDistance((cx, cy), 
                                                        (secondObj.pos[0] + 50, secondObj.pos[1] + 50))
            
            ratio = int((upDown / leftRight) * 100)
            
            if ratio > 60:
                mouthStatus = "Open"
            else:
                mouthStatus = "Closed"
            
            cv2.putText(img, mouthStatus, (0, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)

            if distMouthObject < 100 and ratio > 60:
                if firstObj.isEatable:
                    if np.array_equal(firstObj.currentObj, DoublePoint) : 
                        score += 2
                    else : 
                        score += 1
                    firstObj.resetObject()
                else:
                    heart -= 1
                    if heart == 0 : 
                        gameOver = True
                        continue
                    heartObj = Hearts[heart-1]
                    img = cvzone.overlayPNG(img, heartObj, (880,0))
                    firstObj.resetObject()

            if distMouthObject2 < 100 and ratio > 60:
                if secondObj.isEatable:
                    if np.array_equal(secondObj.currentObj, DoublePoint) : 
                        score += 2
                    else : 
                        score += 1
                    secondObj.resetObject()
                else:
                    heart -= 1
                    if heart == 0 : 
                        gameOver = True
                        continue
                    heartObj = Hearts[heart-1]
                    img = cvzone.overlayPNG(img, heartObj, (880,0))
                    secondObj.resetObject()
    
        cv2.putText(img, "score: "+str(score), (0, 125), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5)
    else:
        cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (0, 0, 255), 10)
        cv2.putText(img, "score: "+str(score), (425, 500), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        firstObj.resetObject()
        secondObj.resetObject()
        gameOver = False
        heart = 3
        heartObj = Hearts[heart-1]
        img = cvzone.overlayPNG(img, heartObj, (880,0))
        score = 0

    elif key == 27:
        break