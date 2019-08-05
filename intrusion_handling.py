import os
import cv2

from config.config import excluded_objects_dict, inter_threshold


def bbox_inter_area(box1, box2):
    # Get the coordinates of bounding boxes
    b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
    b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]

    # get the coordinates of the intersection rectangle
    inter_rect_x1 = max(b1_x1, b2_x1)
    inter_rect_y1 = max(b1_y1, b2_y1)
    inter_rect_x2 = min(b1_x2, b2_x2)
    inter_rect_y2 = min(b1_y2, b2_y2)
    inter_rect = (inter_rect_x1, inter_rect_y1, inter_rect_x2, inter_rect_y2)

    # Intersection area
    inter_area = max(inter_rect_x2 - inter_rect_x1 + 1, 0) * \
                 max(inter_rect_y2 - inter_rect_y1 + 1, 0)

    return inter_area, inter_rect


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


class IntrusionHandling:

    def __init__(self, opc_client, masks_path_dict):
        self.opc_client = opc_client
        self.masks_dict = self.get_mask(masks_path_dict)

    @staticmethod
    def get_mask(masks_path_dict):
        masks_dict = {}
        for name in masks_path_dict.keys():
            if not os.path.exists(masks_path_dict[name]):
                raise RuntimeError(str(name) + "mask路径不存在")
            mask = cv2.imread(masks_path_dict[name])
            mask = mask[:, :, 2]  # only want red channel array
            masks_dict[name] = mask

        return masks_dict

    def judge_intrusion(self, preds_dict):
        judgements_dict = {}
        for name in preds_dict.keys():
            result = self.judge_strategy(preds_dict[name], self.masks_dict[name],
                                         excluded_objects_dict[name], inter_threshold)
            judgements_dict[name] = result
        return judgements_dict

    @staticmethod
    def judge_strategy(bboxes, mask, excluded_objects, thresh):
        if bboxes is None:
            return False
        for box in bboxes:
            x1, y1, x2, y2 = box
            box_area = (x2 - x1) * (y2 - y1)
            inter = np.sum(mask[y1:y2, x1:x2] == 255)
            ratio = inter / box_area
            if ratio >= thresh and not is_them(excluded_objects, box):
                return True
        return False

    def handle_judgement(self, judgements_dict):
        for name in judgements_dict.keys():
            if judgements_dict[name]:
                self.opc_client.stop_it_if_working(name)
        print('处理完成')

    def subprocess_handle_judgement(self, judgements_dict):
        from multiprocessing import Process
        func = lambda name: self.opc_client.stop_it_if_working(name)
        for name in judgements_dict.keys():
            if judgements_dict[name]:
                p = Process(target=func, args=(name, ))
                p.start()


if __name__ == '__main__':
    import numpy as np

    mask = cv2.imread('images/masks/xiazhewan.jpg')
    mask = mask[:, :, 2]
    print(mask.shape)

    mask = mask[0:400, 300:400]

    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
