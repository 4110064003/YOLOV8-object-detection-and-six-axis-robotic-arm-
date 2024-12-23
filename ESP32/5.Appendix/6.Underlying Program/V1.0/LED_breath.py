from machine import Pin, PWM
import time

class LED:
    #使用GPIO 2控制LED
    def __init__(self, io=2):
        #將GPIO引腳設置為PWM模式
        self.led = PWM(Pin(io))
        #控制LED的亮度變化
        self.led.freq(1000)
    #完成一次呼吸的週期2秒，從亮到暗的步數為50(數量越多亮度變化越平滑)
    def breathe(self, duration=30, steps=100):
        #每個step執行的時間=週期/總步數(2*50 暗到亮 亮到暗)
        step_time = duration / (2 * steps)
        # 漸亮
        #i逐步從0增加到step
        for i in range(steps):
            #設置PWM的duty值
            self.led.duty(int(i * (1023 / steps)))
            print(i)
            time.sleep(step_time)
        # 漸暗
        for i in range(steps, -1, -1):
            self.led.duty(int(i * (1023 / steps)))
            print(i)
            time.sleep(step_time)
    
    def on(self):
        #LED全亮
        self.led.duty(1023)
    
    def off(self):
        #LED全暗
        self.led.duty(0)

if __name__ == '__main__':
    led = LED()
    while True:
        led.breathe()


