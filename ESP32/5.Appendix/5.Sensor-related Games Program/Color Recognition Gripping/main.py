from machine import Pin, I2C, Timer
import time, gc
from micropython import const

from Color_sensor import COLOR
from RobotControl import RobotControl
from BusServo import BusServo

from Oled import OLED_I2C
import utime
oled_flag = True
i2c = I2C(0, scl=Pin(27), sda=Pin(14), freq=100000)
try:
  oled = OLED_I2C(128, 32, i2c)
except OSError:
  print('没有检测到OLED模块')
  oled_flag = False
# 初始化OLED

RED = const(1)
GREEN = const(2)
BLUE = const(3)
WHITE = const(4)
#取黑白物体下的参数
R_F = const(8500)
G_F = const(13000)
B_F = const(16600)
r_f = const(140)
g_f = const(150)
b_f = const(140)


bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
Robot = RobotControl(bus_servo = bus_servo)

i2c = I2C(0, scl=Pin(27), sda=Pin(14), freq=100000)
color = COLOR(i2c)
color.enableLightSensor(False)
# 初始化颜色传感器
def Detection_color():
# 颜色检测函数
  c = color.readAmbientLight()
  r = color.readRedLight()
  g = color.readGreenLight()
  b = color.readBlueLight()
  
  #将参数范围浓缩至0~255
  r = int(255 * (r - r_f) / (R_F - r_f))
  g = int(255 * (g - g_f) / (G_F - g_f))
  b = int(255 * (b - b_f) / (B_F - b_f))
  
  if r > 25 and r > g and r > b:t = RED
  elif g > 25 and g > r and g > b:t = GREEN
  elif b > 25 and b > g and b > r:t = BLUE
  else:t = 0
  return t
  
Robot.runActionGroup('00.rob')
time.sleep_ms(1000)
# 执行起始位置动作组
time_count = 0
def color_run():
  global time_count,tim
  try:
    t = Detection_color()
    # 获得检测颜色 t为1时是红色、2是蓝色、3是绿色
    if time.ticks_ms() - time_count > 6000:
      if t != 0:
        if t == 1:
          if oled_flag:
            # 如果连接了OLED会在屏幕上显示颜色
            oled.fill(0)
            oled.text("RED", 50, 11)
            oled.show()
            utime.sleep_ms(1)
          Robot.runActionGroup('41.rob')
          time_count = time.ticks_ms()
        elif t == 2:
          if oled_flag:
            oled.fill(0)
            oled.text("GREEN", 50, 11)
            oled.show()
            utime.sleep_ms(1)
          Robot.runActionGroup('42.rob')
          time_count = time.ticks_ms()
        elif t == 3:
          if oled_flag:
            oled.fill(0)
            oled.text("BLUE", 50, 11)
            oled.show()
            utime.sleep_ms(1)
          Robot.runActionGroup('43.rob')
          time_count = time.ticks_ms()
      time.sleep_ms(100)
  except:
    tim.deinit()
    print("传感器可能断开连接，请连接后重启机械臂")


def main(t):
  #在定时器中断中完成的，不要出现死循环和过大的延时函数

  gc.collect()
  Robot.run_loop()
  color_run()
  
print("Start")
tim = Timer(2)
tim.init(period=10, mode=Timer.PERIODIC, callback=main)




