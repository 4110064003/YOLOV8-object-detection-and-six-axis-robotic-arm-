# ESP32 as a tcp server for remote control
# the details in https://jimirobot.tw 
import machine,network,socket,gc,utime
from machine import Pin
led=Pin(14,Pin.OUT)

def go_wifi():
    try:
        wifi.active(False)
        wifi.active(True)
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
go_wifi()
hostip = wifi.ifconfig()[0]
tcp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDER,1)
#tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind((hostip,1000))            #server ip and port
tcp_server.listen(1)                     #listen only 1 connection
rev_num=0                                #calculate the message number 

while 1:
    print("tcp server is listening")
    tcp_conn,client_addr = tcp_server.accept() 
    print(client_addr, "Client connects sucessfully")
    while 1:       
        msg=tcp_conn.recv(128)
        if len(msg) > 0:          
            msg=msg.decode()        #convert bytes to strings
            if msg[0:4]=="led=":
                if(msg[4]=='1'):
                    led.value(1)
                else: 
                    led.value(0)
            else:
                print('This comannd can not be recognized')    
            rev_num +=1
            tcp_conn.send('the server has received your msg {}'.format(rev_num))
        else :
            print('client socket is disconnected')
            break