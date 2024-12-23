import network, socket, gc, utime
import time
import select
from test1106 import ArmController

class SocketServer:
    def __init__(self):
        self.received_data = None
        self.client = None

    def go_wifi(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect('realme 7 5G', '376bb77cf2a3')
        print('Connecting to WiFi...')
        for _ in range(20):
            if wifi.isconnected():
                print('WiFi connected:', wifi.ifconfig())
                return wifi
            utime.sleep(1)
        print('WiFi connection failed')
        return None

    def start_socket_server(self):
        wifi = self.go_wifi()
        if wifi is None:
            return
        hostip = wifi.ifconfig()[0]
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((hostip, 2000))
        tcp_server.listen(1)
        print("TCP server is listening")

        while True:
            try:
                # 接受新的 client 連線
                client, client_addr = tcp_server.accept()
                client.setblocking(False)  # 設置 client 為非阻塞模式
                print(client_addr, "Client connected")
                self.client = client
                self.handle_client()
            except Exception as e:
                print(e)
                # 若無新連線，繼續循環
                pass

            # 在主迴圈中處理機械手臂動作
            self.process_arm_controller(client)

    def handle_client(self):
        poller = select.poll()
        poller.register(self.client, select.POLLIN)
        rev_num = 0
        self.client.settimeout(5)  # 設置接收超時時間為 5 秒

        while True:
          events = poller.poll(0)  # 非阻塞地檢查是否有新訊息
          for sock, event in events:
              if event & select.POLLIN:
                  try:
                      msg = self.client.recv(128).decode()
                      if len(msg) > 0:
                          print("Received data:", msg)
                          self.received_data = msg
                          rev_num += 1
                          self.client.send('The server has received your msg {}'.format(rev_num).encode())
                          time.sleep_ms(1000)
                      else:
                          print('Client disconnected')
                          poller.unregister(self.client)
                          #self.client.close()
                          #self.client = None
                          return  # 結束此 client 的處理
                  except socket.timeout:
                      print("接收超時，結束等待")
                      poller.unregister(self.client)
                      self.client.close()
                      self.client = None
                      return  # 超時後結束等待

    def process_arm_controller(self,client):
        if not self.client:
          print("No client connected.")
          return

        if not self.received_data:
          print("No received data to process.")
          return
          
        if self.received_data:
            arm_controller = ArmController()
            data_list = self.received_data.split()
            if len(data_list) == 8:
                object_label = data_list[0]
                object_coordinates = list(map(int, data_list[1:4]))
                destination_label = data_list[4]
                destination_coordinates = list(map(int, data_list[5:8]))

                # 執行機械手臂指令
                arm_controller.execute_arm_sequence(
                    object_label, destination_label, object_coordinates, destination_coordinates
                )

                # 重置 received_data 並向 client 回傳 "complete" 訊息
              
              # 確認操作完成，然後發送 "complete" 訊息
                if self.client:
                    try:
                        self.client.send("complete".encode())
                        print("Sent 'complete' message to client")
                    except Exception as e:
                        print("Error sending 'complete' message:", e)
                else:
                    print("No client available to send 'complete' message.")
                
                self.client.close()
                self.client = None
                print('Client disconnected')
                
            self.received_data = None

def main():
    server = SocketServer()
    server.start_socket_server()

if __name__ == '__main__':
    main()

