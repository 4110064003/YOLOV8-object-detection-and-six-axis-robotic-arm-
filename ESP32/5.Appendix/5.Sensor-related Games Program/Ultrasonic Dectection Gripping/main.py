from machine import Pin, I2C, Timer
import time, gc

from RobotControl import RobotControl
from BusServo import BusServo
from Ultrasonic import ULTRASONIC

i2c = I2C(0, scl=Pin(27), sda=Pin(14), freq=100000)
hwsr06 = ULTRASONIC(i2c)
# 初始化超声波

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
Robot = RobotControl(bus_servo = bus_servo)
# 初始化动作组

Robot.runActionGroup('00.rob')
time.sleep_ms(1000)
# 执行起始位置动作组

time_count = 0
def ultrasonic_run():
  global time_count,tim
  try:
    if time.ticks_ms() - time_count > 5500:
      t=0
      time.sleep_ms(200)
      Distance = hwsr06.getDistance()
      # 获得距离信息
      # 串口输出距离
      if Distance >160 and Distance <180:
      # 判断是否在远端
        print(Distance)
        time.sleep_ms(100)
        Distance = hwsr06.getDistance()
        if Distance >160 and Distance <180:
        # 延时后再次判断，减少误差。
          t = 1
          # 对标志位进行赋值
      elif Distance >95 and Distance <110:
        print(Distance)
        time.sleep_ms(100)
        Distance = hwsr06.getDistance()
        if Distance >95 and Distance <110:
          t = 2
      elif Distance >40 and Distance <60:
        print(Distance)
        time.sleep_ms(100)
        Distance = hwsr06.getDistance()
        if Distance >40 and Distance <60:
          t = 3
      if t != 0:
        # 根据标志位执行不同动作组
        if t == 1:
          Robot.runActionGroup('51.rob')
          time_count = time.ticks_ms()
        elif t == 2:
          Robot.runActionGroup('52.rob')
          time_count = time.ticks_ms()
        elif t == 3:
          Robot.runActionGroup('53.rob')
          time_count = time.ticks_ms()
  except:
    tim.deinit()
    print("传感器可能断开连接，请连接后重启机械臂")


def main(t):
  #在定时器中断中完成的，不要出现死循环和过大的延时函数

  gc.collect()
  Robot.run_loop()
  ultrasonic_run()
  
print("Start")
tim = Timer(2)
tim.init(period=10, mode=Timer.PERIODIC, callback=main)





