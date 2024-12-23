import network, socket, gc, utime
import time
from test8 import ArmController

class SocketServer:
    def __init__(self):
        self.received_data = None

    def go_wifi(self):
        wifi = network.WLAN(network.STA_IF)
        try:
            wifi.active(False)
            wifi.active(True)
            wifi.connect('realme 7 5G','376bb77cf2a3')
            print('Start to connect to WiFi')
            for i in range(20):
                print('Trying to connect to WiFi in {}s'.format(i))
                utime.sleep(1)
                if wifi.isconnected():
                    break          
            if wifi.isconnected():
                print('WiFi connection OK!')
                print('Network Config=', wifi.ifconfig())
            else:
                print('WiFi connection Error') 
        except Exception as e: 
            print(e)

        return wifi

    def start_socket_server(self):
        wifi = self.go_wifi()
        hostip = wifi.ifconfig()[0]
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcp_server.bind((hostip, 2000))  # Server IP and port
        tcp_server.listen(1)  # Listen only 1 connection
        rev_num = 0  # Calculate the message number 
        print("TCP server is listening")

        while True:
            client, client_addr = tcp_server.accept() 
            print(client_addr, "Client connects successfully")
            while True: 
                msg = client.recv(128).decode()  # Receive the message and decode
                if len(msg) > 0:         
                    print("Client received data: ", msg) 
                    self.received_data = msg  # Store received data
                    rev_num += 1
                    client.send('The server has received your msg {}'.format(rev_num))
                    time.sleep_ms(1000)  # Prevent CPU overuse
                else:
                    print('Client socket is disconnected')
                    break

            # Process the received data after client disconnects
            if self.received_data:
                self.process_received_data()

    def process_received_data(self):
        arm_controller = ArmController()

        data_list = self.received_data.split()
        if len(data_list) == 8:
            object_label = data_list[0]
            object_coordinates = list(map(int, data_list[1:4]))
            destination_label = data_list[4]
            destination_coordinates = list(map(int, data_list[5:8]))

            arm_controller.execute_arm_sequence(
                object_label, destination_label, object_coordinates, destination_coordinates
            )

def main():
    server = SocketServer()
    server.start_socket_server()

if __name__ == '__main__':
    main()


