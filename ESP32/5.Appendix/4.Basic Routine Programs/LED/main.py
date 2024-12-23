from machine import Pin
import time
# ESP32上的LED灯是连接到IO2上的，所以我们要先设置IO2的引脚为输出模式
led = Pin(2,Pin.OUT)
# 为了点亮LED要调用on函数使IO2为高电平，这时LED亮起
led.on()



