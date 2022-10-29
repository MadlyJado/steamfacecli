import cv2
import sys
import numpy
import hashlib

facetouser = {
    "superjadon121224": "known/face5464",
}

facetopassword = {
    "1234": "known/face5464",
}

class FacialRecognition():
    # Get user supplied images
    cascPath = sys.argv[1]


    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    
    faces = []

    def GetFace(self):
        video_capture = cv2.VideoCapture(0)
        while True:

            # Capture webcam frame by frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = self.faceCascade.detectMultiScale(
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
        # When everything is done, release the capture
        self.faces = face
        video_capture.release()
        cv2.destroyAllWindows()

    # Return the amount of faces found by the facial recognition cascade
    def __str__(self):
        global faces
        Faces = self.faces
        return "Found {0} faces!".format(len(Faces))
    
    
   

facialrecognition = FacialRecognition()

facialrecognition.GetFace()
print(facialrecognition)