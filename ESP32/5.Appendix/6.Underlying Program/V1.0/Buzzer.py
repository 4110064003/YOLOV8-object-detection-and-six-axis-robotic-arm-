from machine import Pin, PWM




class Buzzer:
  
  def __init__(self, io = 15, freq=2500):
    self.buzzer = PWM(Pin(io), freq=freq, duty=0)
    
  def on(self):
    self.buzzer.duty(300)
  
  def off(self):
    self.buzzer.duty(0)
    
    
    
if __name__ == '__main__':
  buzzer = Buzzer()
