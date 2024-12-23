from machine import Pin
import time#, _thread
from micropython import const



BUTTON_DOWN_UP          = const(1)
BUTTON_DOWN_LONG        = const(2)

class Key:
  
  
  def __init__(self, io = 0):
    self.key = Pin(io, Pin.IN)
    self.msg = []
    self.time_last = time.ticks_ms()
    self.count = 0
    
  def run_loop(self):
    if time.ticks_ms() - self.time_last >= 20:
      self.time_last = time.ticks_ms()
      if self.key.value() == 1:
        if self.count > 3 and self.count < 25:
          self.count = 0
          self.msg.append(BUTTON_DOWN_UP)
        else:
          self.count = 0
      if self.key.value() == 0:
        self.count += 1
        if self.count == 50:
          self.msg.append(BUTTON_DOWN_LONG)
      
      
  def down_up(self):
    if len(self.msg) > 0:
      if self.msg[0] == BUTTON_DOWN_UP:
        self.msg.pop(0)
        return True
    return False
    
  def down_long(self):
    if len(self.msg) > 0:
      if self.msg[0] == BUTTON_DOWN_LONG:
        self.msg.pop(0)
        return True
    return False  


