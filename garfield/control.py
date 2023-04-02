from math import sin, cos
from pylx16a.lx16a import *
import serial.tools.list_ports
import serial.serialutil
from garfield import Garfield
import time

t = 0

garfiled = Garfield()

# while True:
#     servo0.move(abs(15*sin(-t) + 15))
#     servo1.move(abs(22*sin(-t) + 22))
#     servo2.move(abs(27*cos(-t) + 27))

#     time.sleep(0.02)
#     t += 0.1
