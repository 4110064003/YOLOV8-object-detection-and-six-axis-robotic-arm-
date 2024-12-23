import paho.mqtt.client as mqtt

# MQTT Broker 設置
MQTT_BROKER = '172.20.10.13'  # Broker 地址，例如 'localhost' 或 '192.168.x.x'
MQTT_PORT = 1883                     # MQTT 默認埠號
MQTT_TOPIC = 'esp32/commands'         # 要訂閱的主題
USERNAME = 'james03'            # 如果 Broker 有帳號密碼，則設置帳號
PASSWORD = '0303zz'            # 設置密碼

# 當客戶端連接到 Broker 時的回呼函數
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully")
        client.subscribe(MQTT_TOPIC)  # 訂閱主題
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

# 當接收到訊息時的回呼函數
def on_message(client, userdata, msg):
    print("Message received from topic {}: {}".format(msg.topic, msg.payload.decode()))

# 建立 MQTT 客戶端
client = mqtt.Client()

# 如果需要帳號密碼，使用下列行設置
client.username_pw_set(username=USERNAME, password=PASSWORD)

# 設置回呼函數
client.on_connect = on_connect
client.on_message = on_message

# 連接到 Broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print("Could not connect to MQTT broker:", e)
    exit(1)

# 開始等待訊息
client.loop_forever()