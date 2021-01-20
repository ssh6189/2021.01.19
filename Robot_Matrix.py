import numpy as np
import math


def robot_Mat(X, Y, Z, roll, pitch, yaw):
    
    B = np.zeros((4, 4))

    B[0][0] = math.cos(roll)*math.cos(pitch)
    B[0][1] = math.cos(roll)*math.sin(pitch)*math.sin(yaw) - math.sin(roll)*math.cos(yaw)
    B[0][2] = math.cos(roll)*math.sin(pitch)*math.cos(yaw) + math.sin(roll)*math.sin(yaw)
    B[1][0] = math.sin(roll)*math.cos(pitch)
    B[1][1] = math.sin(roll)*math.sin(pitch)*math.sin(yaw) + math.cos(roll)*math.sin(yaw)
    B[1][2] = math.sin(roll)*math.sin(pitch)*math.cos(yaw) - math.cos(roll)*math.sin(yaw)
    B[2][0] = -math.sin(pitch)
    B[2][1] = -math.cos(pitch)*math.sin(yaw)
    B[2][2] = math.cos(pitch)*math.cos(yaw)

    B[0][3] = X
    B[1][3] = Y
    B[2][3] = Z
    B[3][3] = 1

    return B

if __name__ == "__main__":
    print(robot_Mat(1, 2, 3, 10, 20, 30))
