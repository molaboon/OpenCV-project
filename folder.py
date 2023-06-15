import os
import cv2

    
def creatList(folderName):
    List = []
    listFolder = os.listdir(folderName)
    
    for object in listFolder:
        List.append(cv2.imread(f'{folderName}/{object}', cv2.IMREAD_UNCHANGED))
    
    return List
        
        