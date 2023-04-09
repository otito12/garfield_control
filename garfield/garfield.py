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
        # load in servos quit program if fails
        # self.speak("Hello world, I am garfield")
        self._load_servos()
        self.move_l_leg(0,0,0)
        self.move_r_leg(0,0,0)
        time.sleep(2)
        # for i in range(50):
        #     self.move_l_leg(0,0,i)
        #     self.move_r_leg(0,0,i)
        #     print()
        # time.sleep(2)
        t = 0
        while True:
            # redementary walk
            if t == 0:
                self.move_l_leg(0,0,0,600)
                # self.move_r_leg(0,0,0)
                t = 1
            elif t == 1:
                self.move_l_leg(50,0,30,600)
                # self.move_r_leg(0,0,0)
                t = 2
            elif t == 2:
                self.move_l_leg(-80,0,50,600)
                # self.move_r_leg(0,0,50)
                t = 0
            else:
                break
            time.sleep(.6)
        # self.move_r_leg(0,0,0) #should produce origin pose
        # speech_to_command(self, "move to base origin pose")
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
    
    # move left leg 
    # add x,y later
    # consider base pose 0 and mask offsets
    def move_l_leg(self,x,y,z,speed=600):
        min = 76 #76mm min z 
        # hip_offest = 0
        knee_offset = 26.6
        calf_offset = 35.1
        self.l_hip.move(50,speed)

        # Adjust for X 
        knee_angle_x_delta = math.atan(x/(z+min))
        print("DD:",knee_angle_x_delta)
        print("AASC:",math.degrees(knee_angle_x_delta))

        z_delta = z+min/math.cos(knee_angle_x_delta)
        print("DDAA:",z_delta)

        # Calc Z
        knee_angle = knee_angle_z_ik(z_delta) + knee_offset - math.degrees(knee_angle_x_delta)
        calf_angle = calf_angle_z_ik(z_delta)+ calf_offset 

        self.l_knee.move(knee_angle,speed)
        self.l_calf.move(calf_angle,speed)
        print("l_k:",knee_angle_z_ik(z+min)+ knee_offset)
        print("l_c:",calf_angle_z_ik(z+min)+ calf_offset)

    # move right leg add x,y later
    def move_r_leg(self,x,y,z,speed=600):
        min = 76 #76mm min z 
        # hip_offest = 0
        knee_offset = -33.4
        calf_offset = 151
        self.r_hip.move(37,speed)
        # becuase the servo is physically flipped but the IK remains the same
        knee_base = knee_angle_z_ik(min)+ knee_offset
        calf_base = calf_angle_z_ik(min)+ calf_offset
        self.r_knee.move(knee_base + (knee_base - (knee_angle_z_ik(z+min)+ knee_offset)),speed)
        self.r_calf.move(calf_base + (calf_base - (calf_angle_z_ik(z+min)+ calf_offset)),speed)
        print("r_k:",knee_base + (knee_base - (knee_angle_z_ik(z+min)+ knee_offset)))
        print("r_c:",calf_base + (calf_base - (calf_angle_z_ik(z+min)+ calf_offset)))


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
        # tts = gTTS(text=text, lang="en")
        # file = "voice.mp3"
        # tts.save(file)
        # playsound.playsound(file)

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

    

            
            

