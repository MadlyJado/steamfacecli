import cv2
import sys
import numpy
import maskpass
import random
from hashlib import sha256
import os
import pickle


"""

    FacialRecognition:


    This class does exactly what you think it does.

    It recognizes faces!

    There are two functions in this class.

    SaveFace()

    and

    ScanFace()


    SaveFace:


        SaveFace gets the webcam of your computer, and goes through a while loop which turns on the webcam for you.

        It will then open a window where you can adjust your face if needed to be able to see your face properly.

        Once you can see your face in the window, press the Q button to close it.

        The SaveFace function then saves an image of the face it saw and then it will return the path to that image.

    ScanFace:


        ScanFace does the exact same thing as SaveFace but instead just scans the face so that way it can be compared to another face without
        returning anything.

"""

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
    
    def CompareFaces(self):
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

"""

    SteamFace:

    This class is the blueprints to make a SteamFace object, which uses the FacialRecognition class already made above. This SteamFace class is the main program class.
    While the FacialRecognition class is a class I adapted from a tutorial I found to work facial recognition on python to be used with object oriented programming.

    The class has two functions:

    register()

    and

    login()

    These functions do two things.

    register() registers the user with their steam username and password, which is saved locally for a more private experience(With the password being encrypted of course with
    sha256 + some salt)

    login() logins the user by first getting the dictionaries from the register() function from the usernames.pkl and passwords.pkl and then goes through the process of finding
    the sha256 + salt combination used to register the account. When a match is found by comparing the face to the other image, which is linked to the username and password, it opens
    steam and logs you in using a screen scraper.
    
    Disclaimer: (In order to use SteamFace you need to use email only verification through steam guard so that way when you say
    "Remember this computer" when you use your steam account on your pc for the first, it'll remember the computer and then it can log you in through SteamFace).

    Maybe someday I can figure out how to make it more secure without doing that but I don't want to risk anyone being hacked as turning off steam guard would just make
    things worse.



"""
class SteamFace():
    
    usernames = {
        
    }
    
    passwords = {
        
    }
    facialRecognition = FacialRecognition()
    
    """
        register(self)


        Description:

            This function registers your steam account into the SteamFace system, using two dictionaries, usernames, and passwords, to link the username and password to
            the image of your face, which will be used to log into Steam with your face, which is why the program is called steamfacecli :)
    """
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
        self.passwords[str(hashedPassword.digest())] = imagepath
        # Save the dictionaries locally to the root folder of the program
        with open("./usernames.pkl", "wb") as f:
            pickle.dump(self.usernames, f)
        with open("./passwords.pkl", "wb") as f:
            pickle.dump(self.passwords, f)
        with open("./faces.pkl", "wb") as f:
            pickle.dump(self.facialRecognition.faces, f)
        

    def login(self):

        with open("./usernames.pkl", "rb") as f:
            self.usernames = pickle.load(f)
        with open("./passwords.pkl", "rb") as f:
            self.passwords = pickle.load(f)
        orignalHashPassword = list(self.passwords.keys())[0]
        user = input("Enter steam username: ")
        password =  maskpass.askpass("Enter steam password: ", "#")
        while True:
            salt = str(random.randbytes(10))
            passwordpsalt = password+salt
            encodedPass = passwordpsalt.encode('utf8')
            hashPasswordCompare = str(sha256(encodedPass).digest())
            if(hashPasswordCompare == orignalHashPassword):
                print("Hashes Match!!")
                break
        
        
            
                
        
        
steamface = SteamFace()
steamface.login()