from machine import Pin
import time
# 按照基础教程1、2中初始化led和按键
led = Pin(2,Pin.OUT)
key = Pin(13, Pin.IN, Pin.PULL_UP)
# 定义按键中断回调函数
def fun(key):
    time.sleep_ms(10) 
    if key.value()==0: 
        led.on()
        time.sleep_ms(1000)
#定义按键中断下降沿触发，并设置fun为回调函数。
key.irq(fun,Pin.IRQ_FALLING) 
#死循环中led灯为长灭状态，当按下按键led亮起1000ms。
while True:
  led.off()
  time.sleep_ms(10) 

