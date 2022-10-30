import cv2
import sys
import numpy
import maskpass
import random
from hashlib import sha256
import os
import pickle

class FacialRecognition():
    # Get user supplied images
    cascPath = sys.argv[1]


    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    
    faces = []

    def SaveFace(self):
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
                path = './known/'+str(random.getrandbits(10))+'.png'
                cv2.imwrite(path, gray)
                break
        # When everything is done, release the capture
        self.faces = face
        video_capture.release()
        cv2.destroyAllWindows()
        return path
    
    def ScanFace(self):
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

class SteamFace():
    
    usernames = {
        
    }
    
    passwords = {
        
    }
    facialRecognition = FacialRecognition()
    
    def register(self):
        # Create salt to make password authentication truly secure
        salt = str(random.randbytes(10))
        # Ask user to enter their Steam username
        user = input("Enter your steam username: ")
        # Ask user to enter their Steam password
        password = maskpass.askpass(prompt= "Enter the password to your steam account: ", mask="#")
        # Hash it using the salt and password
        passwordencoded = (password+salt).encode("utf8")
        hashedPassword = sha256(passwordencoded)
        # Get the user's face image path by saving their face.
        imagepath = self.facialRecognition.SaveFace()
        # Save username to dictionary linking the username to the image path
        self.usernames[user] = imagepath
        # Do the same with the hashed password
        self.passwords[hashedPassword] = imagepath
        # Save the dictionaries locally to the root folder of the program
        with open("./savedvars.pkl", "wb+") as f:
            pickle.dump(str(self.usernames), f)
            pickle.dump(str(self.passwords), f)

    def login(self, username, password):
        with open("./savedvars.pkl", "rb") as f:
            self.usernames = pickle.load(f)
            self.usernames = dict(self.usernames)
            self.passwords = pickle.load(f)
            self.passwords = dict(self.passwords)
        
        
            
                
        
        
steamface = SteamFace()

steamface.register()