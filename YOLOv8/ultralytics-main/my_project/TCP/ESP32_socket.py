import machine ,network,socket,gc,utime
#connect to wifi
def go_wifi():
    try:
        wifi.active(False)
        wifi.active(True)
        wifi.connect('realme 7 5G','376bb77cf2a3')
        print('start to connect wifi')
        for i in range(20):
            print('try to connect wifi in {}s'.format(i))
            utime.sleep(1)
            if wifi.isconnected():
                break
        if wifi.isconnected():
            print('Wifi connection OK!')
            print('Network config=',wifi.ifconfig())
        else:
            print('Wifi connection failed!')
    except Exception as e:print(e)
#create socket 
gc.collect()
wifi=network.WLAN(network.STA_IF)
go_wifi()
hostip = wifi.ifconfig()[0]
tcp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_server.bind((hostip,1000))
tcp_server.listen(1)

print('Waiting for connection...')

def handle_move_command(command):
    #realize the actual moving process
    print('Moving the red box',command)

while True:
    print("tcp server is listening ...")
    tcp_conn,client_addr=tcp_server.accept()
    print(client_addr,"client connects sucessfully")
    while True:
        command = tcp_conn.recv(1024).decode().strip()
        if not command :
            break
        print('Received command :',command)
        if command.startswith('MOVE_RED_BOX'):
            handle_move_command(command)
        else:
                print('This comannd can not be recognized')
    tcp_conn.close()
    print('Client disconnected')

server_socket.close()


