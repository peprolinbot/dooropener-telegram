from time import sleep
import os

#Initializes pygame
import pygame
pygame.init()

#Sets up gpio
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Tries setting up piCamera
try:
    from picamera import PiCamera
    camera = PiCamera()
except:
    pass

class door:
    def __init__ (self, gpioPin, lockFilePath, waitToCloseTime, btnPressTime):
        GPIO.setup(gpioPin, GPIO.OUT)
        GPIO.output(gpioPin, GPIO.HIGH)
        self.gpioPin = gpioPin
        self.lockFilePath = lockFilePath
        self.waitToCloseTime = waitToCloseTime
        self.btnPressTime = btnPressTime
    
    def pressButton(self): #Presses the door button
        # print("Btn")
        GPIO.output(self.gpioPin, GPIO.LOW)
        sleep(self.btnPressTime)
        GPIO.output(self.gpioPin, GPIO.HIGH)

    def pressButtonWithLocking(self): #Presses the door button and locks and unlocks at start and end, respectively, the lockFile
        if not os.path.isfile(self.lockFilePath):
            with open(self.lockFilePath, 'w') as f: 
                pass
            self.pressButton()
            os.remove(self.lockFilePath)


    def open(self, waitToCloseTime=None): #Opens door and closes it after specified time
        if waitToCloseTime == None:
            waitToCloseTime = self.waitToCloseTime
        
        if not os.path.isfile(self.lockFilePath):
            with open(self.lockFilePath, 'w') as f: 
                pass

            self.pressButton()
            sleep(waitToCloseTime)
            self.pressButton()
    
            os.remove(self.lockFilePath)

    #Extra things a smart door should do vvvvvvv

    def playAudioFile(self, filePath): #Plays the audio file specified
        try:
            pygame.mixer.music.load(filePath)
            pygame.mixer.music.set_volume(1.0) 
            pygame.mixer.music.play()
        except pygame.error: #Don't blame if the file doesn't exists, as is posible that people remove their file if they want. Also aplicable if no speaker because not wanting speaker features.
            pass


    def takePhoto(self, photoPath="doorPhoto.jpg"): #Takes a photo to the specified path
        # print("Photo")
        try:
         camera.capture(photoPath)
        except:
            pass


