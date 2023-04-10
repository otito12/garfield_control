from math import sin, cos
from pylx16a.lx16a import *
import serial.tools.list_ports
import serial.serialutil
from garfield import Garfield
import time
garfiled = Garfield()

#for developing the IK Delete later
count = 0
# def knee_angle_fit_z(x):
#     # approximate Knee pose formular from z axis ik
#     return -8.102e-05*pow(x,3) + 0.03254*pow(x,2) - 4.848*x + 250.5

# def calf_angle_fit_z(x):
#     # approximate Knee pose formular from z axis ik
#     return -1.736e-05*pow(x,3) + 0.006582*pow(x,2) - 1.417*x + 102.2

# # time.sleep(2)
# # offset = 40.8
# # l_c_angle = offset +  calf_angle_fit_z(150)
# # l_k_angle = offset +  knee_angle_fit_z(150)
# # garfiled.l_calf.move(l_c_angle,2000)
# # garfiled.l_knee.move(l_k_angle,2000)

# # # Right leg
# # offset_c = 154.8
# # offset_c = 154.8
# # offset_k = -20
# # r_c_angle = offset_c +  calf_angle_fit_z(150)
# # r_k_angle = offset_k +  knee_angle_fit_z(150)
# # garfiled.r_calf.move(r_c_angle,2000)
# # garf iled.r_knee.move(r_k_angle,2000)
