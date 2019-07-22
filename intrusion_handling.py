from opcua import Client
from opcua import ua

from config.config import restricted_areas_dict, \
    tolerated_areas_dict, excluded_objects_dict


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


def handle_judgement(judgements_dict, opc_client):
    for name in judgements_dict.keys():
        if judgements_dict[name]:
            opc_client.stop_it_if_working(name)
    print('处理完成')


def judge_intrusion(preds_dict):
    judgements_dict = {}
    for name in preds_dict.keys():
        if name == 'houban':
            result = strategy_1(preds_dict[name])
            judgements_dict[name] = result
        elif name == '2':
            result = strategy_2(preds_dict[name])
            judgements_dict[name] = result
        elif name == '3':
            result = strategy_3(preds_dict[name])
            judgements_dict[name] = result
        else:
            raise RuntimeError('流水线名称不匹配')
    return judgements_dict


def strategy_1(bboxes):
    if bboxes is None:
        return False
    restricted_areas = restricted_areas_dict['houban']
    tolerated_areas = tolerated_areas_dict['houban']
    excluded_objects = excluded_objects_dict['houban']

    for restr_rect in restricted_areas:
        for bbox in bboxes:
            inter_area, inter_rect = bbox_inter_area(bbox, restr_rect)
            if inter_area > 0 and not is_inside(tolerated_areas, inter_rect) and \
                    not is_them(excluded_objects, bbox):
                return True
    return False


def strategy_2(bboxes):
    if bboxes is None:
        return False

    return True


def strategy_3(bboxes):
    if bboxes is None:
        return False

    return True


def bbox_inter_area(box1, box2):
    # Get the coordinates of bounding boxes
    b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
    b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]

    # get the corrdinates of the intersection rectangle
    inter_rect_x1 = max(b1_x1, b2_x1)
    inter_rect_y1 = max(b1_y1, b2_y1)
    inter_rect_x2 = min(b1_x2, b2_x2)
    inter_rect_y2 = min(b1_y2, b2_y2)
    inter_rect = (inter_rect_x1, inter_rect_y1, inter_rect_x2, inter_rect_y2)

    # Intersection area
    inter_area = max(inter_rect_x2 - inter_rect_x1 + 1, 0) * \
                 max(inter_rect_y2 - inter_rect_y1 + 1, 0)

    return inter_area, inter_rect


def is_inside(big_boxes, box):
    x1, y1, x2, y2 = box
    for big_box in big_boxes:
        bx1, by1, bx2, by2 = big_box
        if bx1 <= x1 and by1 <= y1 and bx2 >= x2 and by2 >= y2:
            return True
    return False


def is_them(excluded_objects, box, thres=0.8):
    max_iou = 0
    for exc_obj in excluded_objects:
        inter_area, inter_rect = bbox_inter_area(exc_obj, box)

        # Get the coordinates of bounding boxes
        exc_obj_x1, exc_obj_y1, exc_obj_x2, exc_obj_y2 = exc_obj[0], exc_obj[1], exc_obj[2], exc_obj[3]

        iou = inter_area / ((exc_obj_x2 - exc_obj_x1) * (exc_obj_y2 - exc_obj_y1))
        max_iou = max(iou, max_iou)

    if max_iou > thres:
        return True
    else:
        return False
