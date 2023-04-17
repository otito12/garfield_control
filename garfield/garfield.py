from pylx16a.lx16a import *
# import serial.tools.list_ports
import serial.serialutil
# import subprocess
import time
# import os
import math
# import playsound
# import speech_recognition as sr
# from gtts import gTTS
# import pyttsx3
# from gcommands import speech_to_command
from gkinematics import *

# ports = serial.tools.list_ports.comports()
# LX16A.initialize(ports[1].device, 0.1)

LX16A.initialize("/dev/ttyUSB0", 0.1)

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

        # implement health check
        # self._health_check()

        # #move to homing position
        # decided to abandon ik for hip
        self.l_hip.move(50, 600)
        self.r_hip.move(37, 600)
        self.move_l_leg(0, 0, 0, 600)
        self.move_r_leg(0, 0, 0, 600)

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
    def move_l_leg(self, x, y, z, speed=0):
        min = 76  # 76mm min z
        # hip_offest = 0
        knee_offset = 26.6
        calf_offset = 35.1

        # Adjust for X
        knee_angle_x_delta = math.atan(x/(z+min))
        z_delta = z+min/math.cos(knee_angle_x_delta)

        # Calc Z
        knee_angle = knee_angle_z_ik(
            z_delta) + knee_offset - math.degrees(knee_angle_x_delta)
        calf_angle = calf_angle_z_ik(z_delta) + calf_offset

        self.l_knee.move(knee_angle, speed)
        self.l_calf.move(calf_angle, speed)

    # move right leg add x,y later
    def move_r_leg(self, x, y, z, speed=0):
        min = 76  # 76mm min z
        # hip_offest = 0
        knee_offset = -33.4
        calf_offset = 151
        # Knee Delta
        knee_angle_x_delta = math.atan(x/(z+min))
        z_delta = z+min/math.cos(knee_angle_x_delta)

        # becuase the servo is physically flipped but the IK remains the same
        knee_base = knee_angle_z_ik(min) + knee_offset
        calf_base = calf_angle_z_ik(min) + calf_offset

        knee_angle = knee_base + \
            (knee_base - (knee_angle_z_ik(z+min) + knee_offset)) + \
            math.degrees(knee_angle_x_delta)
        calf_angle = calf_base + \
            (calf_base - (calf_angle_z_ik(z+min) + calf_offset))

        self.r_knee.move(knee_angle, speed)
        self.r_calf.move(calf_angle, speed)

    def walk_forward(self, stride_length=50, walk_rate=.6):
        # redementary walk
        arc_phase_array = []

        # #move to ready position
        # self.l_hip.move(60, 600)
        # self.r_hip.move(27, 600)
        self.move_l_leg(0, 0, 85, 600)
        self.move_r_leg(0, 0, 85, 600)

        time.sleep(1)
        speed = 1000
        state = 0

        while True:
            if state == 0:
                # self.move_l_leg(0, 0, 85, speed//2)
                # self.move_r_leg(0, 0, 40, speed)
                self.move_l_leg(0, 0, 85, speed)
                self.move_r_leg(0, 0, 85, speed)
                state = 1
            elif state == 1:
                # self.move_l_leg(0, 0, 40, speed)
                # self.move_r_leg(0, 0, 85, speed//2)
                self.move_l_leg(0, 0, 0, speed)
                self.move_r_leg(0, 0, 0, speed)
                state = 0
            time.sleep(speed*0.001)

        # while True:
        #     if state == 0: # key frame
        #         self.move_l_leg(-60,0,85,speed)
        #         self.move_r_leg(20,0,55,speed)
        #         state = 1
        #     elif state == 1: # inbetween
        #         self.move_l_leg(0,0,55,speed)
        #         self.move_r_leg(10,0,75,speed)
        #         state = 2
        #     elif state == 2: # key frame
        #         self.move_l_leg(20,0,55,speed)
        #         self.move_r_leg(-60,0,85,speed)
        #         state = 3
        #     elif state == 3: # inbetween
        #         self.move_r_leg(0,0,55,speed)
        #         self.move_l_leg(10,0,75,speed)
        #         state = 0
        #     else:
        #         break
        #     time.sleep(speed*0.001)

    def print_physical_angles(self):  # debugging
        print("l_hip:", self.l_hip.get_physical_angle(),
              "l_knee:", self.l_knee.get_physical_angle(),
              "l_calf:", self.l_calf.get_physical_angle(),
              "r_hip:", self.r_hip.get_physical_angle(),
              "r_knee:", self.r_knee.get_physical_angle(),
              "r_calf:", self.r_calf.get_physical_angle())

    # def speak(self, text):
    #     audio = pyttsx3.init()
    #     audio.setProperty("rate", 150)
    #     audio.setProperty("volume", 1)
    #     audio.say(text)
    #     audio.runAndWait()

    # def _get_audio(self):
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         audio = r.listen(source)
    #         said = ""
    #         try:
    #             said = r.recognize_google(audio)
    #         except Exception as e:
    #             print("Expection:" + str(e))
    #     return said.lower()

    # def listen(self):  # implement alsways listen on different thread with wake word
    #     while True:
    #         wakeword = self._get_audio()
    #         if wakeword.count(self.wake_phrase) > 0:
    #             self.speak("You may speak")
    #             command = self._get_audio()
    #             speech_to_command(self, command)

    def shutdown(self):
        # to implement
        pass

    def _health_check(self):
        # to implement
        pass


# def marh(self,stride_length=50,walk_rate=.6):
#         # redementary walk
#         arc_phase_array = []
#         state = 0
#         # #move to ready position
#         self.l_hip.move(65,600)
#         self.r_hip.move(22,600)
#         self.move_l_leg(0,0,85,600)
#         self.move_r_leg(0,0,85,600)

#         time.sleep(2)
#         speed = 300
#         while True:
#             if state == 0:
#                 self.move_l_leg(0,0,85,speed//2)
#                 self.move_r_leg(0,0,10,speed)
#                 state = 1
#             elif state == 1:
#                 self.move_l_leg(0,0,0,speed)
#                 self.move_r_leg(0,0,85,speed//2)
#                 state = 0
#             time.sleep(speed*0.001)
