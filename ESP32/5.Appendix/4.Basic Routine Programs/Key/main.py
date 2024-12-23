from machine import Pin
import time
# ESP32拓展板上的按键K1是连接到IO13上的，且按下K1后为低电平，所以我们要先设置IO13的引脚为上拉输入模式。
key = Pin(13, Pin.IN, Pin.PULL_UP)
# 进入死循环一直判断按键是否按下
while True:
  # 当按键按下时，为低电平
  if key.value() == 0:
    # 延时10ms消除抖动
    time.sleep_ms(10)
    # 再次判断按键是否按下
    if key.value() == 0:
      # 串口输出hello world
      print("hello world")
      # 跳出死循环结束程序
      led = Pin(2,Pin.OUT)
# 为了点亮LED要调用on函数使IO2为高电平，这时LED亮起
      led.on()
      break



