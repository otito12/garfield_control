def knee_angle_z_ik(x):
    # approximate Knee pose formular from z axis ik
    return -8.102e-05*pow(x,3) + 0.03254*pow(x,2) - 4.848*x + 250.5

def calf_angle_z_ik(x):
    # approximate Knee pose formular from z axis ik
    return -1.736e-05*pow(x,3) + 0.006582*pow(x,2) - 1.417*x + 102.2

def knee_angle_x_ik(x):
    # approximate Knee pose formular from z axis ik
    return -8.102e-05*pow(x,3) + 0.03254*pow(x,2) - 4.848*x + 250.5

def calf_angle_x_ik(x):
    # approximate Knee pose formular from z axis ik
    return -1.736e-05*pow(x,3) + 0.006582*pow(x,2) - 1.417*x + 102.2