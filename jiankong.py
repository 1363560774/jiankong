import psutil
import paho.mqtt.client as mqtt
import time
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


class Temperature:
    def __init__(self, name, hardware):
        # 下面定义 2 个实例变量
        self.name = name
        self.hardware = hardware


def getIP():
    """获取ipv4地址"""
    dic = psutil.net_if_addrs()
    ipv4_list = []
    for adapter in dic:
        snicList = dic[adapter]
        for snic in snicList:
            # if snic.family.name in {'AF_LINK', 'AF_PACKET'}:
            #     mac = snic.address
            if snic.family.name == 'AF_INET':
                ipv4 = snic.address
                if ipv4 != '127.0.0.1':
                    ipv4_list.append(ipv4)
            # elif snic.family.name == 'AF_INET6':
            #     ipv6 = snic.address
    if len(ipv4_list) >= 1:
        return ipv4_list[0]
    else:
        return 'None'


def loadTemperature():
    """获取硬件温度"""
    hardware = psutil.sensors_temperatures()
    hardware_list = []
    for adapter in hardware:
        hard = hardware[adapter]
        for h in hard:
            t = Temperature(adapter, h.current)
            hardware_list.append(t)
    return hardware_list


# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    # client.subscribe('testtopic/#')


# # 消息接收回调
# def on_message(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))


# # 1. 获取CPU的完整信息
# print(psutil.cpu_times())
#
# # 2. 获取CPU的逻辑个数
# print(psutil.cpu_count())
#
# # 3. 获取CPU的物理个数
# print(psutil.cpu_count(logical=False))
#
# # 4. psutil获取系统CPU使用率的方法是cpu_percent(),其有两个参数，分别是interval和percpu
# # interval指定的是计算cpu使用率的时间间隔，percpu则指定是选择总的使用率还是每个cpu的使用率
# for x in range(10):
#     print(psutil.cpu_percent(interval=1))
#
#     print(psutil.cpu_percent(interval=1, percpu=True))
#
# # 1. 获取系统内存的使用情况
# print(psutil.virtual_memory())
#
# # 2. 获取系统交换内存的统计信息
# print(psutil.swap_memory())
#
# # 1. 获取磁盘分区的信息
# print(psutil.disk_partitions())
# # 2. 获取磁盘的使用情况
# print(psutil.disk_usage('/'))
# # 3. 获取磁盘的IO统计信息（读写速度等）
# print(psutil.disk_io_counters())
#
# # 1. 获取总的网络IO信息
# print(psutil.net_io_counters())
# # 2. 获取网卡的IO信息
# print(psutil.net_io_counters(pernic=True))
# # 3. 获取网络接口信息
# print(psutil.net_if_addrs())
# print(psutil.sensors_temperatures())
# # 4. 获取网络接口状态信息
# print(psutil.net_if_stats())
#
# # 获取系统的开机时间，并转化为自然的格式
# print(psutil.boot_time())
# # 获取连接系统的用户列表
# print(psutil.users())
# # 获取系统全部的进程信息
# print(psutil.pids())
# 获取单个进程的信息, 获取指定进程ID=780
# print(psutil.Process(780))

# print(psutil.test())


# for proc in psutil.process_iter(['pid', 'name']):
#     print(proc.info)


print('开始')

client = mqtt.Client()

# 指定回调函数
client.on_connect = on_connect
# client.on_message = on_message

# 建立连接
client.connect('10.168.1.182', 1883, 60)


while True:
    cpu_percent = psutil.cpu_percent(0)
    virtual_memory = psutil.virtual_memory().percent

    ip_v4 = getIP()
    c = loadTemperature()
    nvme_temperature = None
    cpu_temperature = None
    gpu_temperature = None
    for cn in c:
        # print(cn.name, cn.hardware)
        if cn.name == 'nvme':
            nvme_temperature = cn.hardware
        if cn.name == 'k10temp':
            cpu_temperature = cn.hardware
        if cn.name == "amdgpu":
            gpu_temperature = cn.hardware
    message = Message(cpu_percent, virtual_memory, ip_v4, nvme_temperature, cpu_temperature, gpu_temperature)

    # 对象转化为字典
    # 字典转化为json
    jsonStr = json.dumps(message.__dict__)

    # 发布消息
    client.publish('monitor', payload=jsonStr, qos=0)
    time.sleep(3)
    # client.loop_forever()

