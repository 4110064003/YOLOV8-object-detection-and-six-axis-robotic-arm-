from machine import UART
import time
# 创建发送信息
sendbuffer = "Hiwonder\r\n"
# 注意串口0被repl占用无法使用 串口1没有引出串口1引脚为 tx=10, rx=9 
uart = UART(2,115200, tx=17, rx=16)
# 请大家自行购买USB转串口模块，将USB转串口模块上
# 的TX与esp32上的rx、RX与esp32上的tx相连,串口2引脚为 tx=17, rx=16 
# 如需对串口参数进行修改请参照以下参数，此参数为默认参数。
# UART(2, baudrate=115201, bits=8, parity=None, stop=1, tx=17, rx=16,
# rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=1)
# 打印串口参数
print(uart)
# 死循环中每隔1000ms输出一句Hiwonder，并把串口接收到的数据以bytes的形式打印出来。
while True:
  uart.write(sendbuffer)
  readbuffer = uart.readline()
  if readbuffer is not None:
    print(readbuffer)
  time.sleep_ms(1000)

