#import for GPIO
import RPi.GPIO as gp
#import for MotorHat
from Adafruit_MotorHAT_Motors import Adafruit_MotorHAT,\
    Adafruit_DCMotor, Adafruit_StepperMotor

#import for cam and laser
from subprocess import call
import time

"""TODO: add calibration , and distance functions"""

#******************************************************IMPORTANT


#laser control 25 dgree
LAS_20 = 4
#laser control 60 dgree
LAS_60 = 22
#laser control 80 dgree
LAS_85 = 23

#Global objects for motor
mh = Adafruit_MotorHAT(addr=0x60)
#1st motor circular
G_myStepper2 = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
G_myStepper2.setSpeed(30)  # 30 RPM
#2 motor linier
G_myStepper1 = mh.getStepper(200, 2)  # 200 steps/rev, motor port #1
G_myStepper1.setSpeed(3000)
#******************************************************IMPORTANT
MOTOR_CONST_STEP_TO_ANGLE = 200
NUM_OF_PICS = 30
STEP_SIZE   = MOTOR_CONST_STEP_TO_ANGLE // NUM_OF_PICS
#Globals for GPIO
gp.setmode(gp.BCM)
gp.setwarnings(False)
#laser Globals
gp.setup(LAS_20, gp.OUT)
gp.setup(LAS_60, gp.OUT)
gp.setup(LAS_85, gp.OUT)
LASER_2_STRING = {LAS_20: "20_", LAS_60: "60_", LAS_85: "85_"}

"""function in charge of taking a picture ,
 immbedding string in its name and saving it"""
def take_picture(string ):
    timeStamp = time.strftime("%Y%m%d_%H%M%S")
    condition =True
    while(True):
        try:
            call(['fswebcam', '-S', '2',  '-p', 'YUYV', '-d','/dev/video0', '-r', '320X240',
              '/home/pi/Adafruit-Motor-HAT-Python-Library/Adafruit_MotorHAT/pic/' + string + '.jpg'])
            print "worked"
            time.sleep(3)

        except :
            print "didnt go"
            return
"""all motors need to be taken off"""
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

"""responsible to operate a laser,
laser param is wich laser to oparate
and the on param is to indicte requiered 
laser stete in\off = True\False"""
def Laser(laser, on):
    #if LAS_25 laser turns on  on False else laser turns on on True
    gp.output(laser, (gp.LOW if on else gp.HIGH)if
    (laser == LAS_20) else
    (gp.HIGH if on else gp.LOW))

"""incharge of moving circular Motor  num_of_steps 
    indicates how many steps to take"""
def circularMotor(num_of_steps):
    G_myStepper2.step(num_of_steps, Adafruit_MotorHAT.FORWARD
                      , Adafruit_MotorHAT.DOUBLE)
    turnOffMotors()

"""incharge of moving linier motor """
def liniarMotor(num_of_steps, direction):
    G_myStepper1.step(num_of_steps, Adafruit_MotorHAT.FORWARD if direction else
    Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    turnOffMotors()

""""distance measuring func"""
def meassureDistance():
    pass

"""findes wright dpot and moves there"""
def moveLinier():
    pass

"""Go function runs floe takes NUM_OF_PICS amount 
    of pictures , in each step it turn on all 3 lasers
    one ate a time takes a pic and closes laser , after
    taking 3 photos it takes another step until it finishes
    a 360 degree full circle """
def Go():
    for step in range(NUM_OF_PICS):
        for laser in [LAS_20, LAS_60, LAS_85]:
            Laser(laser, True)
            take_picture(LASER_2_STRING[laser] + str(step))
            time.sleep(0.3)
            Laser(laser, False)
        circularMotor(STEP_SIZE)
    #add last pic marker

"""a calibration function"""
def calibration():
    pass


def main():
    #circularMotor(100000)

    Laser(LAS_20,True)
    # Laser(LAS_60, True)
    #Laser(LAS_85, True)
    #
     #Laser(LAS_20, False)
     #Laser(LAS_60, False)
    Laser(LAS_85, False)
    take_picture("25_3test")
    #Go()
    #Go()

if __name__ == "__main__":
    main()
