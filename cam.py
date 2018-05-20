from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
for i in range(5):
    sleep(0.1)
    camera.capture('/home/pi/Adafruit-Motor-HAT-Python-Library/Adafruit_MotorHAT/pic/a'+str(i)+'.jpg' )
camera.stop_preview()