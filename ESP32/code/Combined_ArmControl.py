
import math
import ArmInversekinematics as ArmIK
import time

# Function from ForwardKinematicTest for calculating DH matrix
def dh_matrix(alpha, a, d, theta):
    theta = math.radians(theta)  # Convert degrees to radians
    alpha = math.radians(alpha)  # Convert degrees to radians
    return [
        [math.cos(theta), -math.sin(theta), 0, a],
        [math.sin(theta) * math.cos(alpha), math.cos(theta) * math.cos(alpha), -math.sin(alpha), -d * math.sin(alpha)],
        [math.sin(theta) * math.sin(alpha), math.cos(theta) * math.sin(alpha), math.cos(alpha), d * math.cos(alpha)],
        [0, 0, 0, 1]
    ]

# Matrix multiplication function from ForwardKinematicTest
def matrix_multiply(A, B):
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(4))
    return result

# Forward kinematics function
def forward_kinematics(dh_params):
    T = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    for param in dh_params:
        alpha, a, d, theta = param
        T_i = dh_matrix(alpha, a, d, theta)
        T = matrix_multiply(T, T_i)
    return T

# Function to extract DH parameters
def dh_params(coordinate):
    angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2]) 
    if angle == False:
        return False
    return [
        [0, 0, 73.5, angle[0]],  
        [90, 0, 0, angle[1]],
        [0, 100.5, 0, angle[2]],
        [0, 96, 0, angle[3]],
        [0, 160, 0, 0]
    ]

# ArmControl class from version8.py
class ArmControl:
    def __init__(self, bus_servo):
        self.bus_servo = bus_servo

    def convert_input_to_arm_coordinates(self, x, y):
        # Conversion logic to arm coordinates
        converted_x = x * 10  # Placeholder conversion
        converted_y = y * 10  # Placeholder conversion
        return converted_x, converted_y

    def adjust_z_based_on_distance(self, x, y, z):
        # Adjust the Z height based on distance
        return z + 10  # Placeholder adjustment

    def AngleConvert(self, angle, middle_angle=90, flip=False):
        # Convert an angle into servo value, considering middle_angle and flip
        if flip:
            return middle_angle - angle
        return middle_angle + angle

    def ArmControl_grab(self, object_coordinates, _time):
        # Grabbing action implementation
        converted_x, converted_y = self.convert_input_to_arm_coordinates(object_coordinates[0], object_coordinates[1])
        adjusted_z = self.adjust_z_based_on_distance(object_coordinates[0], object_coordinates[1], object_coordinates[2])
        angle = ArmIK.CalcAngle(X=converted_x, Y=converted_y, Z=adjusted_z)

        if angle == False:
            return False

        # Perform forward kinematic check before actual movement
        dh_param_values = dh_params([converted_x, converted_y, adjusted_z])
        if dh_param_values:
            T_ee = forward_kinematics(dh_param_values)
            print("Pre-move End-Effector Position (from Forward Kinematics):")
            print([T_ee[0][3], T_ee[1][3], T_ee[2][3]])

        # Actual movement
        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90, flip=False), _time)
        self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
        self.bus_servo.run(4, self.AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
        self.bus_servo.run(1, 600, 1000)
        time.sleep(_time / 1500.0)
        self.bus_servo.run(1, 300, 1000)
        return True

    def ArmControl_release(self, destination_coordinates, _time):
        # Releasing action implementation
        converted_x, converted_y = self.convert_input_to_arm_coordinates(destination_coordinates[0], destination_coordinates[1])
        adjusted_z = self.adjust_z_based_on_distance(destination_coordinates[0], destination_coordinates[1], destination_coordinates[2])
        angle = ArmIK.CalcAngle(X=converted_x, Y=converted_y, Z=adjusted_z)

        if angle == False:
            return False

        # Perform forward kinematic check before actual movement
        dh_param_values = dh_params([converted_x, converted_y, adjusted_z])
        if dh_param_values:
            T_ee = forward_kinematics(dh_param_values)
            print("Pre-release End-Effector Position (from Forward Kinematics):")
            print([T_ee[0][3], T_ee[1][3], T_ee[2][3]])

        # Actual movement
        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90, flip=False), _time)
        self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
        self.bus_servo.run(4, self.AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
        self.bus_servo.run(1, 600, 1000)
        time.sleep(_time / 1000.0)
        self.bus_servo.run(1, 300, 1000)
        return True

    def execute_arm_sequence(self, object_label, destination_label, object_coordinates, destination_coordinates):
        # Execute grab and release sequence
        print("Moving toward object {}".format(object_label))
        success_grab = self.ArmControl_grab(object_coordinates, 2500)

        if success_grab:
            print("Move object {} to destination {}".format(object_label, destination_label))
            self.ArmControl_release(destination_coordinates, 2500)
