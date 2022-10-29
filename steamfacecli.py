from tkinter import *
from tkinter import ttk
import cv2
import sys

class FacialRecognition():
    # Get user supplied images
    cascPath = sys.argv[1]


    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture webcam frame by frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
        
        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    def AmountOfFaces(self):
        Faces = self.faces
        print("Found {0} faces!".format(len(Faces)))
    
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
   

facialrecognition = FacialRecognition()

facialrecognition.AmountOfFaces()