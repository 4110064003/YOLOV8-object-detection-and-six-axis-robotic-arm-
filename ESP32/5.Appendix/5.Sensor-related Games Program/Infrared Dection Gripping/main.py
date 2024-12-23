from machine import Timer
import time,gc
from micropython import const

from Infrared_sensor import INFRARED
from RobotControl import RobotControl
from BusServo import BusServo


infrared = INFRARED(32)

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
Robot = RobotControl(bus_servo = bus_servo)

Robot.runActionGroup('00.rob')
time.sleep_ms(1000)
# 执行起始位置动作组
time_count = 0

def infrared_run():
  global time_count
  if time.ticks_ms() - time_count > 8000:
    infrared.run_loop()
    if infrared.close_short():
    # 红外避障传感器注意事项请参照触摸传感器玩法
    # 红外避障传感器与触摸传感器底层程序逻辑相同
      print("short")
    if infrared.close_long():
      Robot.runActionGroup('60.rob')
      time_count = time.ticks_ms()
      
def main(t):
  #在定时器中断中完成的，不要出现死循环和过大的延时函数

  gc.collect()
  Robot.run_loop()
  infrared_run()
  
print("Start")
tim = Timer(2)
tim.init(period=10, mode=Timer.PERIODIC, callback=main)




