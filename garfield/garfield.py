from pylx16a.lx16a import *
import serial.tools.list_ports
import serial.serialutil
import subprocess

ports = serial.tools.list_ports.comports()
LX16A.initialize(ports[1].device, 0.1)

# LX16A.initialize("/dev/ttyUSB0", 0.1)

# initialize imu
# cmd_str = "ldto enable i2c-ao ;i2cdetect -y 1"
# subprocess.run(cmd_str, shell=True)


class Garfield():

    l_hip = None
    l_knee = None
    l_calf = None
    r_hip = None
    r_knee = None
    r_calf = None

    def __init__(self):
        self._start_up()

    def _start_up(self):
        # load in servos quit program if fails
        self._load_servos()

        # send garfield to base pose
        self._base_pose()

    def _load_servos(self):
        # ----- init l_hip ----- #
        try:
            self.l_hip = LX16A(0)
            self.l_hip.set_angle_limits(0, 240)
            # self.l_hip.set_angle_offset(-30, True)

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
            # self.l_calf.set_angle_offset(-30, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init r_hip ----- #
        try:
            self.r_hip = LX16A(10)
            self.r_hip.set_angle_limits(0, 240)
            # self.r_hip.set_angle_offset(-30, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init r_knee ----- #
        try:
            self.r_knee = LX16A(11)
            # self.r_knee.set_angle_limits(0, 240)
            # self.r_knee.set_angle_offset(-30, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()

        # ----- init r_calf ----- #
        try:
            self.r_calf = LX16A(12)
            # self.r_calf.set_angle_limits(0, 240)
            # self.r_calf.set_angle_offset(-30, True)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()
        print("l_hip:", self.l_hip.get_physical_angle(),
                "l_knee:", self.l_knee.get_physical_angle(),
                "l_calf:", self.l_calf.get_physical_angle(),
                "r_hip:", self.r_hip.get_physical_angle(),
                "r_knee:", self.r_knee.get_physical_angle(),
                "r_calf:", self.r_calf.get_physical_angle())
    def _base_pose(self):
        # l_hip: 50.64 l_knee: 30.0 l_calf: 32.16 r_hip: 30.48 r_knee: 29.76 r_calf: 150.0
        self.l_hip.move(50.64,time=600)
        self.l_knee.move(60.0,time=600)
        self.l_calf.move(34,time=600)
        self.r_hip.move(36,time=600)
        self.r_knee.move(0,time=600)
        self.r_calf.move(150.7,time=600)

        
