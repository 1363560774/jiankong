import paho.mqtt.client as mqtt
import json


class Message:
    def __init__(self, cpu_percent, virtual_memory, ip_v4, nvme_temperature, cpu_temperature, gpu_temperature):
        # 下面定义 2 个实例变量
        self.cpu_percent = cpu_percent
        self.virtual_memory = virtual_memory
        self.ip_v4 = ip_v4
        self.nvme_temperature = nvme_temperature
        self.cpu_temperature = cpu_temperature
        self.gpu_temperature = gpu_temperature


# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('monitor')


# 消息接收回调
def on_message(client, userdata, msg):
    obj = json.loads(msg.payload)
    cpu_percent = obj['cpu_percent']
    virtual_memory = obj['virtual_memory']
    ip_v4 = obj['ip_v4']
    nvme_temperature = obj['nvme_temperature']
    cpu_temperature = obj['cpu_temperature']
    gpu_temperature = obj['gpu_temperature']
    print(cpu_percent, virtual_memory, ip_v4, nvme_temperature, cpu_temperature, gpu_temperature)


print('开始')

client = mqtt.Client()

# 指定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立连接
client.connect('10.168.1.182', 1883, 60)
client.loop_forever()
