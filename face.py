import cv2
def captureImage(id):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    sampleNum=0
    while True:
        ret,im = cam.read()
        gray= cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces =  detector.detectMultiScale(gray,1.3,5) 
        for(x,y,w,h) in faces:
            sampleNum = sampleNum+1
            cv2.imwrite("dataSet/"+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow('im',im)
        cv2.waitKey(100)
        if(sampleNum>20):
            cam.release()
            cv2.destroyAllWindows()
            break



        
        
        
            
        

                    

            
  





    
