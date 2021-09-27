from sqlite3.dbapi2 import connect
import cv2
import numpy as np
import sqlite3
from time import strftime
from datetime import date,time


def getProfile(Id):
    conn = sqlite3.connect("staff.db")
    cmd = "SELECT * FROM staffs WHERE id="+str(Id)
    cur = conn.execute(cmd)
    profile = None
    for row in cur:
        profile= row
    conn.close()
    return profile




    

def detector():
    faceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/trainingData.yml")
    id = 0
    font = cv2.FONT_HERSHEY_SIMPLEX                       
    while(True):
        ret,img= cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces =faceDetect.detectMultiScale(gray,1.4,7)
        for(x,y,w,h) in faces:
        
        
            cv2.rectangle(img,(x,y),(x+w+60,y+h+40),(100,255,0),8)
            id,conf = recognizer.predict(gray[y:y+h,x:x+w])
            profile = getProfile(id)
            if(profile!=None):
                cv2.putText(img,str(profile[1]), (x,y+h+90), font, 2, 90)
                # conn = sqlite3.connect("staff.db")
                
                # conn.execute('INSERT INTO attendence VALUES (?)',(profile[1],))
                # conn.commit()
                # conn.close()
                

                
            else:
                cv2.putText(img,"Unknown Face", (x,y+h+90), font, 2, 90)
          

 
            

        cv2.imshow("Face",img)
        if(cv2.waitKey(1)==ord('q')):
            break
    cam.release()
    cv2.destroyAllWindows()

detector()

