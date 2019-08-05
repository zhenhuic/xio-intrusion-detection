from opcua import Client
from opcua import ua


class OpcClient:
    def __init__(self, opc_url, nodes_dict):
        self.opc_url = opc_url
        self.nodes_dict = nodes_dict
        self.client = None
        self.connect()

    def connect(self):
        self.client = Client(self.opc_url)
        print("OPC server 连接成功")

    def disconnect(self):
        self.client.disconnect()

    def node_value(self, name):
        node_id = self.nodes_dict[name]
        node = self.client.get_node(node_id)
        value = node.get_value()
        return node, value

    @staticmethod
    def stop_it(node):
        node.set_attribute(ua.AttributeIds.Value,
                           ua.DataValue(variant=ua.Variant(True)))

    def stop_it_if_working(self, name):
        node, value = self.node_value(name)
        if not value:  # Value 为 False 表示机器正在运作，否则表示机器静止
            self.stop_it(node)
            print(name + ' 有人闯入，主动停机！！')
        else:
            print('有人闯入，机器静止')