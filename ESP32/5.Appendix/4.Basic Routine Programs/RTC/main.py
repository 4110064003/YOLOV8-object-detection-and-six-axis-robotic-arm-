from machine import Pin,  RTC,Timer

# 定义星期和时间（时分秒）显示字符列表
week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
time_list = ['', '', '']
# 初始化RTC
rtc = RTC()
# 修改首次上电时RTC的时间，按顺序分别是：年，月，日，星期，时，分，秒，毫秒 第一次运行之后注释掉即可
rtc.datetime((2020, 1, 1, 0, 0, 0, 0, 0))
def RTC_Run(tim):
  # 获取当前时间
  datetime = rtc.datetime()  
  # 显示日期，字符串可以直接用“+”来连接
  print(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + week[datetime[3]])
  # 显示时间
  print(time_list[0] + str(datetime[4]) + ':' + time_list[1] + str(datetime[5]) + ':' + time_list[2] + str(datetime[6]))
# 开启RTOS定时器
tim = Timer(1)
# 设置定时器周期1000ms，重复执行，回调函数为RTC_Run
tim.init(period=1000, mode=Timer.PERIODIC, callback=RTC_Run) #周期300ms



