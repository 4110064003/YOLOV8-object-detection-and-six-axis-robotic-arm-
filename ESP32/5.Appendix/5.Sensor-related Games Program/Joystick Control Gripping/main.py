from machine import Timer
import time,gc

from RobotControl import RobotControl
from BusServo import BusServo, have_got_servo_pos
from Joystick import JOYSTICK

joystick = JOYSTICK()
# 初始化摇杆
bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
Robot = RobotControl(bus_servo = bus_servo)

Robot.runActionGroup('00.rob')
time.sleep_ms(1000)
# 执行起始位置动作组
time_count = time.ticks_ms()

def joystick_run():
  # 摇杆控制函数
  global time_count
  x = joystick.get_original_x_axis()
  y = joystick.get_original_y_axis()
  if time.ticks_ms() - time_count > 5000:
    if x < 5:

      Robot.runActionGroup('31.rob')
      time_count = time.ticks_ms()
    elif x>1000:
      Robot.runActionGroup('32.rob')
      time_count = time.ticks_ms()
    elif y<5:
      Robot.runActionGroup('33.rob')
      time_count = time.ticks_ms()
    elif y>1000:
      Robot.runActionGroup('34.rob')
      time_count = time.ticks_ms()


def main(t):
  #在定时器中断中完成的，不要出现死循环和过大的延时函数

  gc.collect()
  Robot.run_loop()
  joystick_run()
  
print("Start")
tim = Timer(2)
tim.init(period=10, mode=Timer.PERIODIC, callback=main)










