from machine import Pin, PWM
import time
# 初始化PWM，Pin()为所要调用的IO口，freq为PWM的频率，freq=200为频率200Hz，
# duty代表PWM占空比范围为0-1023
led =  PWM(Pin(2), freq=200, duty=0)
time.sleep_ms(1000)
# 先以蜂鸣器来演示一下，这里duty代表的是音量
Buzzer = PWM(Pin(15), freq=200, duty=512) # 引脚是25，在同一语句下创建和配置 PWM
# 蜂鸣器会从200、400、600、800、1000Hz各响600ms
for i in range(200,1200,200):
  Buzzer.freq(i)
  time.sleep_ms(600)
# 关闭蜂鸣器
Buzzer.duty(0)
# 再以LED来演示一下，这里duty代表的是亮度，以下程序会让LED灯逐渐的从暗到亮再从亮到暗，也就是呼吸灯。
for i in range(0,1024,1):
  led.duty(i)
  time.sleep_ms(1)
for i in range(1023,0,-1):
  led.duty(i)
  time.sleep_ms(1)
time.sleep_ms(100)
led.duty(0)


