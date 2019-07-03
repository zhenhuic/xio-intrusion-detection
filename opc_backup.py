from opcua import Client
from opcua import ua


client = Client("ocp.tcp://10.19.3.35:49320")
node_info = "ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志"
client.connect()
node = client.get_node(node_info)
isStopFlag = node.get_value()
node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
