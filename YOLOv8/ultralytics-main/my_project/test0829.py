import socket

server_ip = '192.168.213.19'  # 替換為您的伺服器 IP
server_port = 1000        # 替換為您的伺服器端口

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)  # 設置超時時間
        s.connect((server_ip, server_port))
        print("成功連接到伺服器")
except socket.error as e:
    print(f"連接失敗: {e}")
