import cv2
import sqlite3
from time import strftime
from datetime import date,time,datetime
faceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingData.yml")
id = 0
font = cv2.FONT_HERSHEY_SIMPLEX 
dt=datetime.strptime('01:45:56PM', '%I:%M:%S%p')
print(dt)
timez = dt.time()
today = date.today()
print("Today's date:", today)
now = datetime.now()

current_time = now.strftime("%H:%M:%S")

def getProfile(Id):
        conn = sqlite3.connect("staff.db")
        cmd = "SELECT * FROM staff WHERE id="+str(Id)
        cur = conn.execute(cmd)
        profile = None
        for row in cur:
            profile= row
        conn.close()
        return profile


class Video(object):
    def __init__(self):
        self.video= cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    

    def get_frame(self):
        ret,img = self.video.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces =faceDetect.detectMultiScale(gray,1.1, 5)
        for(x,y,w,h) in faces:
        
        
            cv2.rectangle(img,(x,y),(x+w+60,y+h+40),(100,255,0),8)
            id,conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf<70):
                profile=getProfile(id)
            else:
                id=0
                profile=getProfile(id)
            
            if(profile!=None):
                
               
                cv2.rectangle(img,(x,y-35),(x,y),(0,255,0))
                cv2.putText(img,profile[1],(x+6,y-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
               
                conn = sqlite3.connect("staff.db")
                # sqlite_insert_with_param =

                # data_tuple = ()
                cur = conn.cursor()
                cur.execute('SELECT * FROM attendence WHERE (id=? AND date=?)', (profile[0], today))
                entry = cur.fetchone()

                if entry is None:
                    conn.execute( """INSERT INTO attendence
                            ( name,register,department, date, time,status) 
                            VALUES (?, ?, ?,?,?,?) """, (profile[1], profile[2],profile[4] ,today, current_time,"Present"))
                    print("PResent")
                else:
                    print("ENtry found")

                # if(conn.execute('SELECT * FROM attendence WHERE (id=? AND date=?)', (profile[0], today))):
                #     print("already")
                # else:
                #     conn.execute( """INSERT INTO attendence
                #             (id, name, date, time) 
                #             VALUES (?, ?, ?, ?) """, (profile[0], profile[1], today, current_time))
                
                # conn.execute('INSERT INTO attendence values (?,?,?,?) where not exists(select * from attendence where id=?)',(profile[0],profile[1],today,dt))
                conn.commit()
                conn.close()
                

                
            else:
                
                
         
                cv2.putText(img,"Unknown Face", (x,y+h+90), font, 2, 90)
        ret,jpg=cv2.imencode('.jpg',img)
        return jpg.tobytes()        