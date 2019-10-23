import logging
import threading
import sys
import time
from socket import timeout

from opcua import Client
from opcua import ua
from opcua.common.node import Node


class OpcClient:
    def __init__(self, opc_url, nodes_dict):
        self.opc_url = opc_url
        self.nodes_dict = nodes_dict
        self.client = None
        self.connect()
        self.just_reconnected = False

    def connect(self):
        self.client = Client(self.opc_url)
        try:
            self.client.connect()
            logging.info("OPC 服务器已连接")
        except timeout:
            raise TimeoutError("OPC服务器连接超时！")
        except Exception as e:
            print(e)
            print("OPC 服务器连接失败，系统自动退出！")
            print("")
            sys.exit(1)

    def reconnect(self):
        self.client.disconnect()
        self.connect()
        self.just_reconnected = True

    def node_value(self, name):  # TODO 重写
        node_id = self.nodes_dict[name]
        node = self.client.get_node(node_id)
        try:
            value = node.get_value()
        except Exception:
            msg = '获取{}状态信息失败'.format(name)
            print(msg)
            logging.warning(msg)
            value = False
        return node, value

    @staticmethod
    def stop_it(node: Node):
        node.set_attribute(ua.AttributeIds.Value,
                           ua.DataValue(variant=ua.Variant(True)))

    @staticmethod
    def reset(node: Node) -> None:
        node.set_attribute(ua.AttributeIds.Value,
                           ua.DataValue(variant=ua.Variant(False)))

    def stop_it_if_working(self, name):
        try:
            node, value = self.node_value(name)

            if self.just_reconnected:  # 如果重新连接后成功读取节点信息，则标志置 False
                self.just_reconnected = False

            if name == 'zhuanjixia' or name == 'penfenshang':  # 先写 0，再写 1
                self.reset(node)
                time.sleep(0.2)
                self.stop_it(node)
                logging.warning(name + ' 工位' + ' 安全系统主动停机')
                print(name + ' 异常闯入，安全系统主动停机！！')
            else:
                if not value:  # Value 为 False 表示机器正在运作，否则表示机器静止
                    self.stop_it(node)
                    logging.warning(name + ' 工位' + ' 安全系统主动停机')
                    print(name + ' 异常闯入，安全系统主动停机！！')
                else:
                    print('异常闯入，机器静止')
                    logging.warning(name + ' 工位' + ' 机器静止')

        except ConnectionResetError:
            # 如果刚刚没有重连过，那么尝试重新连接，
            # 否则表示刚刚重新连接过仍然出现异常，则退出程序
            if not self.just_reconnected:
                self.reconnect()
                self.stop_it_if_working(name)
            else:
                msg = '无法连接工位{}节点'.format(name)
                print(msg)
                logging.error(msg)
                sys.exit(1)

