from machine import Timer
import time,gc

from RobotControl import RobotControl
from BusServo import BusServo
from Buzzer import Buzzer
from Touch_sensor import TOUCH

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
Robot = RobotControl(bus_servo = bus_servo)


buzzer = Buzzer()
# 初始化蜂鸣器
touch = TOUCH(32)
# 初始化触摸传感器
time_count = 0
count = 0
flag = False

Robot.runActionGroup('00.rob')
time.sleep_ms(1000)
# 执行起始位置动作组

def br():
# 控制蜂鸣器响一声
  buzzer.on()
  time.sleep_ms(100)
  buzzer.off()

def touch_run():
  global time_count,count,flag
  # 触摸传感器需要先运行run_loop()后才可判断
  if touch.down_long():
    # 判断函数有两个down_long()、down_up()分别是检测长按、短按。
    # 如果您不需要检测触摸传感器是否被长按，也请运行下down_long()这个函数。
    # 否则无法清除标志位，同理不需要检测短按时也是如此。
    print('long')
  elif time.ticks_ms() - time_count < 2000 and count == 1:
  # 当距离第一次按下按键时间在2秒以内时
    if touch.down_up():
      # 检测是否有第二次按键按下
      count = 2
      br()
      print(count)
      flag = True
      # 第二次按键按下
  elif touch.down_up() and count == 0:
    # 注意使用down_up()、down_long()时调用过一次后会擦除缓存中的值。
    # 例如当你短暂触摸一下后调用down_up()会返回True而第二次调用时会返回False
    time_count = time.ticks_ms()
    # 开始计时
    count = 1
    # 记录按了一下
    br()
    # 蜂鸣器响一声
    print(count)
    
  elif time.ticks_ms() - time_count > 2000 and count == 1:
    flag = True
  if flag:
    if count  == 1:
      # 根据按键次数执行相应动作组
      Robot.runActionGroup('31.rob')
    elif count == 2:
      Robot.runActionGroup('32.rob')
    flag = False
    count = 0
    # 清除按键计数
  time.sleep_ms(10) 


def main(t):
  #在定时器中断中完成的，不要出现死循环和过大的延时函数

  gc.collect()
  Robot.run_loop()
  touch.run_loop()
  touch_run()
  
print("Start")
tim = Timer(2)
tim.init(period=10, mode=Timer.PERIODIC, callback=main)






