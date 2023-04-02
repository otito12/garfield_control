from math import sin, cos
from pylx16a.lx16a import *
import serial.tools.list_ports
import serial.serialutil
import time

# ports = serial.tools.list_ports.comports()
# LX16A.initialize(ports[1].device, 0.1)

try:
    servo0 = LX16A(0)
    servo1 = LX16A(1)
    servo2 = LX16A(2)

    servo0.set_angle_limits(0, 30)
    servo1.set_angle_limits(0, 55)
    servo2.set_angle_limits(0, 60)

    servo0.set_angle_offset(-30, True)
    servo1.set_angle_offset(-30, True)
    servo2.set_angle_offset(-30, True)

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

t = 0
while True:
    servo0.move(abs(15*sin(-t) + 15))
    servo1.move(abs(22*sin(-t) + 22))
    servo2.move(abs(27*cos(-t) + 27))

    time.sleep(0.02)   
    t += 0.1
