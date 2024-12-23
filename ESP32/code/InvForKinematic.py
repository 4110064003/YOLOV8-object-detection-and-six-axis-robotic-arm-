# Import necessary modules
import math
import ArmInversekinematics as ArmIK

# Function to generate the DH transformation matrix
def dh_matrix(alpha, a, d, theta):
    theta = math.radians(theta)  # Convert angle to radians
    alpha = math.radians(alpha)  # Convert angle to radians
    
    #從{坐標系i-1}轉換到{坐標系i}的轉換矩陣
    return [
        [math.cos(theta)                  , -math.sin(theta)                 ,       0         ,         a           ],
        [math.sin(theta) * math.cos(alpha), math.cos(theta) * math.cos(alpha), -math.sin(alpha), -d * math.sin(alpha)],
        [math.sin(theta) * math.sin(alpha), math.cos(theta) * math.sin(alpha),  math.cos(alpha),  d * math.cos(alpha)],
        [                                0,                                 0,                0,                    1]
    ]

# Function to perform matrix multiplication
def matrix_multiply(A, B):
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(4))
    return result

# Inverse kinematics function to calculate DH parameters
def dh_params(coordinate):
    corrected_coordinate = [ coordinate[0], coordinate[1], coordinate[2]]
    angle = ArmIK.CalcAngle(X = corrected_coordinate[0], Y = corrected_coordinate[1], Z = corrected_coordinate[2]) 
    print(angle)
    if angle == False:
        return False
    
    # Set DH parameters for the robotic arm
    # DH parameters: [alpha, a, d, theta]
    return [
        [0 , 0    , 73.5, angle[0]],
        [90, 0    , 0   , angle[1]],
        [0 , 100.5, 0   , angle[2]],
        [0 , 96   , 0   , angle[3]],
        [0 , 160  , 0   , 0       ]
    ]
    

# Forward kinematics function to calculate the end effector pose
def forward_kinematics(dh_params):
    # Initialize homogeneous transformation matrix (identity matrix)
    T = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    # Accumulate transformation matrices based on DH parameters
    for param in dh_params:
        alpha, a, d, theta = param
        T_i = dh_matrix(alpha, a, d, theta)
        T = matrix_multiply(T, T_i)
    
    return T

# Main program to calculate and display the position of the end effector
coordinate = [100, 180, 200]#可修改成任意座標

# Calculate DH parameters using inverse kinematics
DH_params = dh_params(coordinate)

# If DH parameters are successfully calculated, perform forward kinematics
if DH_params:
    # Calculate forward kinematics
    T_end_effector = forward_kinematics(DH_params)
    
    # Display the transformation matrix of the end effector
    # print("末端執行器的轉換矩陣:")
    # for row in T_end_effector:
        # print(row)
    
    # Display the position of the end effector
    position = [T_end_effector[0][3], T_end_effector[1][3], T_end_effector[2][3]]
    print("\n末端執行器的位置 (x, y, z):")
    print(position)#如果輸出結果與coordinate座標吻合表示參數無誤
else:
    print("無法計算此坐標的角度")



