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

class Door:
    def __init__ (self, gpio_pin, lock_file_path, wait_to_close_time, btn_press_time):
        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.HIGH)
        self.gpio_pin = gpio_pin
        self.lock_file_path = lock_file_path
        self.wait_to_close_time = wait_to_close_time
        self.btn_press_time = btn_press_time
    
    def press_button(self): #Presses the door button
        # print("Btn")
        GPIO.output(self.gpio_pin, GPIO.LOW)
        sleep(self.btn_press_time)
        GPIO.output(self.gpio_pin, GPIO.HIGH)

    def press_button_with_locking(self): #Presses the door button and locks and unlocks at start and end, respectively, the lockFile
        if not os.path.isfile(self.lock_file_path):
            with open(self.lock_file_path, 'w') as f: 
                pass
            self.press_button()
            os.remove(self.lock_file_path)


    def open(self, wait_to_close_time=None): #Opens door and closes it after specified time
        if wait_to_close_time == None:
            wait_to_close_time = self.wait_to_close_time
        
        if not os.path.isfile(self.lock_file_path):
            with open(self.lock_file_path, 'w') as f: 
                pass

            self.press_button()
            sleep(wait_to_close_time)
            self.press_button()
    
            os.remove(self.lock_file_path)

    #Extra things a smart door should do vvvvvvv

    def play_audio_file(self, file_path): #Plays the audio file specified
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(1.0) 
            pygame.mixer.music.play()
        except pygame.error: #Don't blame if the file doesn't exists, as is posible that people remove their file if they want. Also aplicable if no speaker because not wanting speaker features.
            pass


    def take_photo(self, photo_path="doorPhoto.jpg"): #Takes a photo to the specified path
        # print("Photo")
        try:
         camera.capture(photo_path)
        except:
            pass


