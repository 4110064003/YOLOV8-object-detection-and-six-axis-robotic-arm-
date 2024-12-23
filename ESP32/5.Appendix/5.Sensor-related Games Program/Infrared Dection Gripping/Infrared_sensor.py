from machine import Pin
import time#, _thread
from micropython import const

INFRARED_DOWN_UP          = const(1)
INFRARED_DOWN_LONG        = const(2)

class INFRARED:
  
  def __init__(self, io = 16):
    self.infrared = Pin(io, Pin.IN, Pin.PULL_UP)
    self.msg = []
    self.time_last = time.ticks_ms()
    self.keep_time = 0 
    self.threshold_value = 500 
    
  def run_loop(self):
    if time.ticks_ms() - self.time_last >= 20:
      self.time_last = time.ticks_ms()
      if self.infrared.value() == 1:
        if time.ticks_ms() - self.keep_time >= 10 and time.ticks_ms() - self.keep_time <= self.threshold_value:
          self.keep_time = 0
          self.msg.append(INFRARED_DOWN_UP)
        else:
            self.keep_time = 0
      if self.infrared.value() == 0:
        if self.keep_time == 0:
          self.keep_time = time.ticks_ms()
        elif time.ticks_ms() - self.keep_time >= self.threshold_value:
          self.msg.append(INFRARED_DOWN_LONG)
    
  def close_short(self):
    if len(self.msg) > 0:
      if self.msg[0] == INFRARED_DOWN_UP:
        self.msg.pop(0)
        return True
    return False
    
  def close_long(self):
    if len(self.msg) > 0:
      if self.msg[0] == INFRARED_DOWN_LONG:
        self.msg.pop(0)
        return True
    return False  
  
  
  def set_long_close_time(self, value):
    if value<=10:
      print('设定值太低')
      return False
    elif value>=10000:
      print('设定值太高')
      return False
    else:
      self.threshold_value = value
      return True

if __name__ == '__main__':
  infrared = INFRARED()
  infrared.set_long_close_time(2000)
  while True:
    infrared.run_loop()
    if infrared.close_short():
      print('short')
    if infrared.close_long():
      print('long')
      break
    time.sleep_ms(10) 






