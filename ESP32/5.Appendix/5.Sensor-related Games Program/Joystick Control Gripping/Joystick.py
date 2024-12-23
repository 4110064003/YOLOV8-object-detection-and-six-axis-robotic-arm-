from machine import ADC,Pin

class JOYSTICK:
  
  def __init__(self,x_axisio = 32,y_axisio = 33):
    self.x_axis = ADC(Pin(x_axisio))
    self.y_axis = ADC(Pin(y_axisio))
    self.x_axis.atten(ADC.ATTN_11DB)# 设置衰减比 满量程3.3v
    self.x_axis.width(ADC.WIDTH_10BIT)# 设置数据宽度为10bit 满量程1023
    self.y_axis.atten(ADC.ATTN_11DB)# 设置衰减比 满量程3.3v
    self.y_axis.width(ADC.WIDTH_10BIT)# 设置数据宽度为10bit 满量程1023
    self.x_threshold = 500
    self.y_threshold = 500
    self.x_axis_centre = self.x_axis.read()
    self.y_axis_centre = self.y_axis.read()

  def get_original_x_axis(self):
    return self.x_axis.read()
    
  def get_original_y_axis(self):
    return self.y_axis.read()
    
  def get_original_xy_axis(self):
    return self.x_axis.read(),self.y_axis.read()

  def get_x_axis(self):
    if self.x_axis.read() > self.x_axis_centre:
      return int(512*(1+(self.x_axis.read() - self.x_axis_centre)/(1023-self.x_axis_centre)))
    else:
      return int(512*(1-(self.x_axis_centre - self.x_axis.read())/(self.x_axis_centre)))

      
  def get_y_axis(self):
    if self.y_axis.read() > self.y_axis_centre:
      return int(512*(1+(self.y_axis.read() - self.y_axis_centre)/(1023-self.y_axis_centre)))
    else:
      return int(512*(1-(self.y_axis_centre - self.y_axis.read())/(self.y_axis_centre)))

  def get_xy_axis(self):
    return self.get_x_axis(),self.get_y_axis()

  
  

if __name__ == '__main__':
  import time
  joystick = JOYSTICK()
  # 输出数值范围为0-1023 
  while True:
    print('X轴数据:',joystick.get_original_x_axis())
    time.sleep_ms(100) 
    print('Y轴数据:',joystick.get_original_y_axis())
    time.sleep_ms(100) 











