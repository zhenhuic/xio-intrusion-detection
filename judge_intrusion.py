from opcua import Client
from opcua import ua


class OpcClient:
    def __init__(self, opc_url):
        self.opc_url = opc_url
        self.client = None
        self.node = None
        self.connect()

    def connect(self):
        self.client = Client(self.opc_url)
        print("OPC server 连接成功")

    def disconnect(self):
        self.client.disconnect()

    def node_value(self, node_id):
        node = self.client.get_node(node_id)
        value = node.get_value()
        return value

    def stop_it(self):
        self.node.set_attribute(ua.AttributeIds.Value,
                                ua.DataValue(variant=ua.Variant(True)))


def judge(predictions, open_opc=False, opc_client=None):
    pass

