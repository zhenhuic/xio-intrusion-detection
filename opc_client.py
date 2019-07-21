from opcua import Client
from opcua import ua


class OpcClient:
    def __init__(self, opc_url, node_id):
        self.opc_url = opc_url
        self.node_id = node_id
        self.client = None
        self.node = None

    def connect(self):
        self.client = Client(self.opc_url)
        self.node = self.client.get_node(self.node_id)

    def disconnect(self):
        self.client.disconnect()

    def node_value(self):
        value = self.node.get_value()
        return value

    def stop_it(self):
        self.node.set_attribute(ua.AttributeIds.Value,
                                ua.DataValue(variant=ua.Variant(True)))

