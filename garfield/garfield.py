from pylx16a.lx16a import *
import serial.tools.list_ports
import serial.serialutil
import subprocess
import time
import os
import math
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
from gcommands import speech_to_command
from gkinematics import *

ports = serial.tools.list_ports.comports()
LX16A.initialize(ports[1].device, 0.1)

# LX16A.initialize("/dev/ttyUSB0", 0.1)

# initialize imu
# cmd_str = "ldto enable i2c-ao ;i2cdetect -y 1"
# subprocess.run(cmd_str, shell=True)

class Garfield():

    # Servos
    l_hip = None
    l_knee = None
    l_calf = None
    r_hip = None
    r_knee = None
    r_calf = None

    # motion

    # Voice control
    wake_phrase = "hey garfield"

    def __init__(self):
        self._start_up()

    def _start_up(self):
        # load in servos; quit program if fails
        self._load_servos()

        # #move to homing position
        self.move_l_leg(0,0,0,600)
        self.move_r_leg(0,0,0,600)

        # speak active
        # self.speak("Hello world, I am garfield")
        
        # slepp for a sec
        time.sleep(2)

        # start walk
        self.walk_forward()

        # listen for commands
        # self.listen()

    def _load_servos(self):
        # ----- init l_hip ----- #
        try:
            self.l_hip = LX16A(0)
            self.l_hip.set_angle_limits(0, 240)
            # self.l_hip.set_angle_offset(20, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init l_knee ----- #
        try:
            self.l_knee = LX16A(1)
            self.l_knee.set_angle_limits(0, 240)
            # self.l_knee.set_angle_offset(-30, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init l_calf ----- #
        try:
            self.l_calf = LX16A(2)
            self.l_calf.set_angle_limits(0, 240)
            self.l_calf.set_angle_offset(-30, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init r_hip ----- #
        try:
            self.r_hip = LX16A(10)
            self.r_hip.set_angle_limits(0, 240)
            # self.r_hip.set_angle_offset(0, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init r_knee ----- #
        try:
            self.r_knee = LX16A(11)
            # self.r_knee.set_angle_limits(0, 240)
            # self.r_knee.set_angle_offset(0, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init r_calf ----- #
        try:
            self.r_calf = LX16A(12)
            # self.r_calf.set_angle_limits(0, 240)
            # self.r_calf.set_angle_offset(-20, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()
    
    # consider base pose 0 and mask offsets
    def move_l_leg(self,x,y,z,speed=0):
        min = 76 #76mm min z 
        # hip_offest = 0
        knee_offset = 26.6
        calf_offset = 35.1
        self.l_hip.move(50,speed)

        # Adjust for X 
        knee_angle_x_delta = math.atan(x/(z+min))
        z_delta = z+min/math.cos(knee_angle_x_delta)

        # Calc Z
        knee_angle = knee_angle_z_ik(z_delta) + knee_offset - math.degrees(knee_angle_x_delta)
        calf_angle = calf_angle_z_ik(z_delta)+ calf_offset 

        self.l_knee.move(knee_angle,speed)
        self.l_calf.move(calf_angle,speed)

    # move right leg add x,y later
    def move_r_leg(self,x,y,z,speed=0):
        min = 76 #76mm min z 
        # hip_offest = 0
        knee_offset = -33.4
        calf_offset = 151
        self.r_hip.move(37,speed)
        # Knee Delta
        knee_angle_x_delta = math.atan(x/(z+min))
        z_delta = z+min/math.cos(knee_angle_x_delta)

        # becuase the servo is physically flipped but the IK remains the same
        knee_base = knee_angle_z_ik(min)+ knee_offset
        calf_base = calf_angle_z_ik(min)+ calf_offset

        knee_angle = knee_base + (knee_base - (knee_angle_z_ik(z+min)+ knee_offset)) + math.degrees(knee_angle_x_delta)
        calf_angle = calf_base + (calf_base - (calf_angle_z_ik(z+min)+ calf_offset)) 
        
        self.r_knee.move(knee_angle,speed)
        self.r_calf.move(calf_angle,speed)

    def walk_forward(self,stride_length=50,walk_rate=.6):
        # redementary walk
        arc_phase_array = []
        state = 0
        
        while True:
            print(60*math.sin(state)-28)
            state+=.05
            self.move_l_leg(60*math.sin(state)-28,0,0)
            time.sleep(.01)
            # self.move_l_leg(55,0,25,600)
            # if state == 1:
            #     self.move_l_leg(55,0,25,600)
            #     # self.move_r_leg(-80,0,50,600)
            #     state = 2
            # elif state == 2:
            #     self.move_l_leg(-100,0,40,600)
            #     # self.move_r_leg(0,0,0,600)
            #     state = 3
            # step_size = stride_length//walk_rate
            # for i in range(0,stride_length+step_size,step_size):
            #     x = i 
            #     z = math.sqrt(pow((stride_length/2),2) - pow((i - (stride_length/2)),2))
            #     self.move_l_leg(x,0,z)
            #     time.sleep(walk_rate)
            #     print("x:",x,"z:",z)

            # #phase 2 come back
            # for i in range(stride_length,0-step_size,-step_size):
            #     self.move_l_leg(x,0,0)
            #     print("x:",i)
            #     time.sleep(walk_rate)
        # while True:
        #     if state == 0:
        #         self.move_l_leg(0,0,0,600)
        #         self.move_r_leg(50,0,30,600)
        #         state = 1
        #     elif state == 1:
        #         self.move_l_leg(50,0,30,600)
        #         self.move_r_leg(-80,0,50,600)
        #         state = 2
        #     elif state == 2:
        #         self.move_l_leg(-80,0,50,600)
        #         self.move_r_leg(0,0,0,600)
        #         state = 0
        #     else:
        #         break
        #     time.sleep(.6)
        

    def print_physical_angles(self): # debugging
        print("l_hip:", self.l_hip.get_physical_angle(),
                "l_knee:", self.l_knee.get_physical_angle(),
                "l_calf:", self.l_calf.get_physical_angle(),
                "r_hip:", self.r_hip.get_physical_angle(),
                "r_knee:", self.r_knee.get_physical_angle(),
                "r_calf:", self.r_calf.get_physical_angle())
    
    def speak(self,text):
        audio = pyttsx3.init()
        audio.setProperty("rate", 150)
        audio.setProperty("volume", 1)
        audio.say(text)
        audio.runAndWait()

    def _get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
                audio = r.listen(source)
                said = ""
                try:
                    said = r.recognize_google(audio)
                except Exception as e: 
                    print("Expection:" + str(e))
        return said.lower()


    def listen(self): #implement alsways listen on different thread with wake word
        while True:
            wakeword = self._get_audio()
            if wakeword.count(self.wake_phrase) > 0:
                self.speak("You may speak")
                command = self._get_audio()
                speech_to_command(self, command)

    

            
            

