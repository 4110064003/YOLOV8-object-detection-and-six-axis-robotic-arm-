import network,socket,gc,utime
import time
from test8 import ArmController
# 創建一個全局變數來存儲接收到的資料
received_data = None

def go_wifi():
    try:
        wifi.active(False)
        wifi.active(True)
        # wifi.connect('iiphone','Phantom0818')
        #wifi.connect('realme 7 5G','376bb77cf2a3')
        wifi.connect('angela','27332039')
        print('start to connect wifi')
        for i in range(20):
            print('try to connect wifi in {}s'.format(i))
            utime.sleep(1)
            if wifi.isconnected():
                break          
        if wifi.isconnected():
            print('WiFi connection OK!')
            print('Network Config=',wifi.ifconfig())
        else:
            print('WiFi connection Error') 
    except Exception as e: print(e)
    
gc.collect()
wifi= network.WLAN(network.STA_IF)
def start_socket_server():
  go_wifi()
  hostip = wifi.ifconfig()[0]
  global received_data
  tcp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  #tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  tcp_server.bind((hostip,1000))            #server ip and port
  tcp_server.listen(1)                     #listen only 1 connection
  rev_num=0                                #calculate the message number 
  while 1:
      print("tcp server is listening")
      client ,client_addr = tcp_server.accept() 
      print(client_addr, "Client connects sucessfully")
      while 1: 
          msg=client.recv(128).decode()#receave the message and decode
          if len(msg) > 0:         
              #msg=msg.decode()        #convert bytes to strings
              print("Client recv data : ", msg) 
              received_data = msg  # 更新全局變數
              rev_num +=1
              client.send('the server has received your msg {}'.format(rev_num))
              time.sleep_ms(1000)  # 防止 CPU 過度占用
          else :
              print('client socket is disconnected')
              break

def main():
  start_socket_server()
  arm_controller = ArmController()
  
  if received_data:
        data_list = received_data.split()
        if len(data_list) == 8:
            object_label = data_list[0]
            object_coordinates = list(map(int, data_list[1:4]))
            destination_label = data_list[4]
            destination_coordinates = list(map(int, data_list[5:8]))

            arm_controller.execute_arm_sequence(object_label,destination_label,object_coordinates, destination_coordinates)

if __name__ == '__main__':
    main()






