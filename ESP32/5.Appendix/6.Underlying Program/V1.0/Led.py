from machine import Pin




class LED:
  
  def __init__(self, io = 2):
    self.led = Pin(io, Pin.OUT)
    self.on()
  def on(self):
    self.led.value(1)
  
  def off(self):
    self.led.value(0)
    
    
    
if __name__ == '__main__':
  led = LED()
  led.on()
