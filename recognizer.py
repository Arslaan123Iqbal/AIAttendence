import os
import cv2
import numpy as np

from PIL import Image

def recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = "dataSet"


    def getImagesId(path):
        imgePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faces = []
        ids = []
        
        for imagePath in imgePaths:
            faceImg =  Image.open(imagePath).convert("L")
            faceNp = np.array(faceImg,'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[0])
            faces.append(faceNp)
            ids.append(ID)
            cv2.imshow("Training",faceNp)
            cv2.waitKey(10)
        return ids,faces

    Ids,faces = getImagesId(path)
    recognizer.train(faces,np.array(Ids))
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()





