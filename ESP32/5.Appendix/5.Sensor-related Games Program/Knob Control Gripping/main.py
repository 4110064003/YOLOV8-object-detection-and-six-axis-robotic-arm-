from machine import Pin, ADC
import time

import ArmInversekinematics as ArmIK
from BusServo import BusServo
from Knob_Module import KNOB

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
knob = KNOB()


def AngleConvert(angle, middle_angle, flip):
  # 进行舵机角度与控制信号之间的转换
  # 0~240° ————> 0~1000
  p = 500 + (angle - middle_angle) * 25 / 6
  if p < 0:
    p = 0
  elif p > 1000:
    p = 1000
  if flip: return 1000 - int(p)
  return int(p)


def ArmControl(coordinate, _time=0):
  angle = ArmIK.CalcAngle(X = None, Y = coordinate[1], Z = coordinate[2])
  # 坐标通过逆运动学运算后返回的舵机角度
  if angle == False:
    return False
  # angle[0]为6号舵机旋转角度，当X为正时顺时针旋转，为负时逆时针旋转。
  # angle[1]为5号舵机臂与转台的内侧夹角（内侧为初始状态时有控制板的一侧）。
  # angle[2]为4号舵机臂与5号舵机到4号舵机延长线的夹角。
  # angle[3]为3号舵机臂与4号舵机到3号舵机延长线的夹角。
  # 由于存在回程误差且不同位置舵机的承重不同，为保证机械臂水平需要减去一个常量。
  # bus_servo.run(6, AngleConvert(angle[0] , middle_angle=90, flip=False), _time)
  bus_servo.run(5, AngleConvert(angle[1] - 3, middle_angle=90, flip=True), _time)
  bus_servo.run(4, AngleConvert(angle[2] - 2, middle_angle=0, flip=False), _time)
  bus_servo.run(3, AngleConvert(angle[3] - 1, middle_angle=0, flip=True), _time)
  return True
 
Coordinate = [0, 180, 200]#坐标 x, y, z

ArmControl(Coordinate, _time=1000)
bus_servo.run(6, 500, 1000)
bus_servo.run(2, 500, 1000)
bus_servo.run(1, 500, 1000)
# 初始化舵机位置
while True:
  if knob.get_Knob() < 400:
    Coordinate[2] += 1
    if ArmControl(Coordinate,10) == False or Coordinate[2] > 250: Coordinate[2] -= 1
    time.sleep_ms(10)
  elif knob.get_Knob() > 800:
    Coordinate[2] -= 1
    if ArmControl(Coordinate,10) == False or Coordinate[2] < 165: Coordinate[2] += 1
    time.sleep_ms(10)






