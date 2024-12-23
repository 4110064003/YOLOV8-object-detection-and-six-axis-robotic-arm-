import math
import ArmInversekinematics as ArmIK

#根據DH參數生成齊次變換矩陣
def dh_matrix(alpha, a, d, theta):
  
  theta = math.radians(theta)  # 將角度轉為弧度
  alpha = math.radians(alpha)  # 將角度轉為弧度
    
  return [
    [math.cos(theta)                  , -math.sin(theta)                 , 0               , a                   ],
    [math.sin(theta) * math.cos(alpha), math.cos(theta) * math.cos(alpha), -math.sin(alpha), -d * math.sin(alpha)],
    [math.sin(theta) * math.sin(alpha), math.cos(theta) * math.sin(alpha), math.cos(alpha) , d * math.cos(alpha) ],
    [0                                , 0                                , 0               , 1                   ]
  ]
    

# 定義矩陣乘法函數
def matrix_multiply(A, B):
  result = [[0 for _ in range(4)] for _ in range(4)]
  for i in range(4):
    for j in range(4):
      result[i][j] = sum(A[i][k] * B[k][j] for k in range(4))
  return result

# 定義正向運動學的主要函數
def forward_kinematics(dh_params):
  #根據DH參數計算末端執行器的位姿
  T = [
    [1, 0, 0, 0],  # 初始齊次矩陣（單位矩陣）
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
  ]
    
  for param in dh_params:
    alpha, a, d, theta = param
    T_i = dh_matrix(alpha, a, d, theta)
    T = matrix_multiply(T, T_i)  # 累積變換矩陣
    
  return T
 
def dh_params(coordinate):
  angle = ArmIK.CalcAngle(X = coordinate[0], Y = coordinate[1], Z = coordinate[2]) 
  if angle == False:
    return False
  # 設定機械臂的 DH 參數
  # DH參數的順序：[theta, d, a, alpha]
  return [
    [0 , 0    , 73.5, angle[0]],  
    [90, 0    , 0   , angle[1]],
    [0 , 100.5, 0   , angle[2]],
    [0 , 96   , 0   , angle[3]],
    [0 , 160  , 0   , 0       ]
  ]
             
Coordinate = [100, 180, 200]           
DH_params = dh_params(Coordinate)

# 計算正向運動學
T_end_effector = forward_kinematics(DH_params)

# 顯示末端執行器的位姿
print("末端執行器的變換矩陣:")
for row in T_end_effector:
    print(row)

# 末端執行器的位置
position = [T_end_effector[0][3], T_end_effector[1][3], T_end_effector[2][3]]
print("\n末端執行器的位置 (x, y, z):")
print(position)




