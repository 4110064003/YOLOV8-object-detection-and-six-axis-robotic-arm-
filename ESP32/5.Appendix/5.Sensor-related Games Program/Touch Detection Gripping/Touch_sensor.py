from machine import Pin
import time#, _thread
from micropython import const

TOUCH_DOWN_UP          = const(1)
TOUCH_DOWN_LONG        = const(2)

class TOUCH:
  
  def __init__(self, io = 16):
    self.touch = Pin(io, Pin.IN, Pin.PULL_UP)
    self.msg = []
    self.time_last = time.ticks_ms()
    self.keep_time = 0 
    self.threshold_value = 500 
    
  def run_loop(self):
    if time.ticks_ms() - self.time_last >= 20:
      self.time_last = time.ticks_ms()
      if self.touch.value() == 1:
        if time.ticks_ms() - self.keep_time >= 10 and time.ticks_ms() - self.keep_time <= self.threshold_value:
          self.keep_time = 0
          self.msg.append(TOUCH_DOWN_UP)
        else:
          self.keep_time = 0
      if self.touch.value() == 0:
        if self.keep_time == 0:
          self.keep_time = time.ticks_ms()
        elif time.ticks_ms() - self.keep_time >= self.threshold_value:
          self.msg.append(TOUCH_DOWN_LONG)
    
  def down_up(self):
    if len(self.msg) > 0:
      if self.msg[0] == TOUCH_DOWN_UP:
        self.msg.pop(0)
        return True
    return False
    
  def down_long(self):
    if len(self.msg) > 0:
      if self.msg[0] == TOUCH_DOWN_LONG:
        self.msg.pop(0)
        return True
    return False  
    
  def set_long_press_time(self, value):
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
  touch = TOUCH()
  while True:
    touch.run_loop()
    if touch.down_up():
      print('short')
    if touch.down_long():
      print('long')
      break
    time.sleep_ms(10) 







