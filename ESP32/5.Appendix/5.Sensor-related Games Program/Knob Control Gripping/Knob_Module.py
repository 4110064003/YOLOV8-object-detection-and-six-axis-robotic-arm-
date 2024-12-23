
from machine import ADC,Pin

class KNOB:
  
  def __init__(self,io = 32):
    self.Knob = ADC(Pin(io))
    self.Knob.atten(ADC.ATTN_11DB)# 设置衰减比 满量程3.3v
    self.Knob.width(ADC.WIDTH_10BIT)# 设置数据宽度为10bit 满量程1023

  def get_Knob(self):
    return self.Knob.read()
    
  

if __name__ == '__main__':
  import time
  knob = KNOB()
  # 输出数值范围为0-1023 
  while True:
    print('旋钮数据:',knob.get_Knob())
    time.sleep_ms(100) 













