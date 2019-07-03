from opcua import Client
from opcua import ua
import time
import threading


def stop_it(node):
    node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
    print("机器人运行被中止！！")


client = Client("opc.tcp://10.19.3.35:49320")
node_info = "ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志"

since = time.time()
client.connect()

node = client.get_node(node_info)
print("connection", time.time() - since)

since = time.time()
halt_thread = threading.Thread(target=stop_it, args=(node,))
halt_thread.start()
print("thread", time.time() - since)

since = time.time()
isStopFlag = node.get_value()
print("get value", time.time() - since)
print(isStopFlag)

since = time.time()
node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
print("set attr", time.time() - since)
