import math

L1 = 101 #連桿1長度
L2 = 95  #連桿2長度
L3 = 165 #連桿3長度(含夾爪閉合後長度)
baseHeight = 65 #基座的高度
cubeHalfHeight = 15 #方塊一半的高度

def angle(dist):
    #計算theta1
    distance_project_part1  = 0.25 * dist
    print(" 0.25*d = ",distance_project_part1)
    distance_project_part2  = 0.75 * dist
    print(" 0.75*d = ",distance_project_part2)
    height1 = math.sqrt(L1 ** 2 - distance_project_part1  ** 2)#L1 * cos(180-theta1)
    print("a = ",height1)
    theta1_sup = (L1** 2 + distance_project_part1  ** 2 - height1 **2)/(2*L1*distance_project_part1 )#theta1補角-餘弦公式-三邊長求夾角
    print("180-theta1 = ",theta1_sup)
    theta1_sup_angle = math.degrees(math.acos(theta1_sup))
    print("180-theta1 = ",theta1_sup_angle)
    theta1 = 180  - theta1_sup_angle
    print("theta1 = ",theta1)

    #計算theta3
    height2 = height1 + baseHeight
    print("b = ",height2)
    height3 = height2 - cubeHalfHeight
    print("c = ",height3)
    hyp1 = math.sqrt(height3 ** 2 + distance_project_part2  ** 2)
    print("d = ",hyp1)
    theta3_sup = (L3** 2 + L2  ** 2 - hyp1 **2)/(2*L3*L2 )#theta3補角-餘弦公式-三邊長求夾角
    print("180-theta3 = ",theta3_sup)
    theta3_sup_angle = math.degrees(math.acos(theta3_sup))
    print("180-theta3 = ",theta3_sup_angle)
    theta3 = 180  - theta3_sup_angle
    print("theta3 = ",theta3)

    #計算theta2
    theta2_sup1 = (L1** 2 + height1 ** 2 - distance_project_part1 **2)/(2 * L1 * height1 )#theta3補角-餘弦公式-三邊長求夾角
    print("o1 = ",theta2_sup1)
    theta2_sup1_angle = math.degrees(math.acos(theta2_sup1))
    print("o1 = ",theta2_sup1_angle)
    theta2_sup2 = (hyp1** 2 + height3 ** 2 - distance_project_part2 **2)/(2 * hyp1 * height3 )#theta3補角-餘弦公式-三邊長求夾角
    print("o2 = ",theta2_sup2)
    theta2_sup2_angle = math.degrees(math.acos(theta2_sup2))
    print("o2 = ",theta2_sup2_angle)
    theta2_sup3 = (L2** 2 + hyp1 ** 2 - L3 **2)/(2 * L2 * hyp1 )#theta3補角-餘弦公式-三邊長求夾角
    print("o3 = ",theta2_sup3)
    theta2_sup3_angle = math.degrees(math.acos(theta2_sup3))
    print("o3 = ",theta2_sup3_angle)
    theta2 = 180  - theta2_sup1_angle - theta2_sup2_angle - theta2_sup3_angle
    print("theta2",theta2)

    # return theta1,theta2,theta3

if __name__ == '__main__':
  while True:
    dist = int(input("distance"))
    # coor.append(int(input("請輸入x座標: ")))
    # coor.append(int(input("請輸入y座標: ")))
    # coor.append(int(input("請輸入z座標: ")))
    angle(dist)