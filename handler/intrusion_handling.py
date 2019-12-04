import os
import time
import random
import threading
import logging

import cv2
import numpy as np

from handler.wechat import WeChat
from configs.config import excluded_objects_dict, inter_threshold,\
    video_stream_paths_dict, max_object_bbox_area_dict, \
    min_object_bbox_area_dict, open_wechat_bot, wechat_group


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
    inter_area = max(inter_rect_x2 - inter_rect_x1 + 1, 0) * max(
        inter_rect_y2 - inter_rect_y1 + 1, 0)

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

    def __init__(self, masks_path_dict, opc_client, records_root='images/records/'):
        self.masks_dict = self.__get_mask(masks_path_dict)
        self.opc_client = opc_client
        self.records_root = records_root
        self.lock = threading.Lock()
        if open_wechat_bot:
            self.wechat = WeChat(wechat_group, video_stream_paths_dict)

    @staticmethod
    def __get_mask(masks_path_dict):
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
            result = self.__judge_strategy(preds_dict[name], self.masks_dict[name],
                                           max_object_bbox_area_dict[name],
                                           min_object_bbox_area_dict[name],
                                           excluded_objects_dict[name], inter_threshold)
            judgements_dict[name] = result
        return judgements_dict

    @staticmethod
    def __judge_strategy(bboxes, mask, max_bbox_area, min_bbox_area, excluded_objects, thresh):
        if bboxes is None:
            return False
        for box in bboxes:
            x1, y1, x2, y2 = box
            box_area = (x2 - x1) * (y2 - y1)

            # 过滤掉过大和过小的识别框
            if min_bbox_area <= box_area <= max_bbox_area:
                num_inter = np.count_nonzero(mask[y1:y2, x1:x2])
                ratio = num_inter / box_area
                if ratio >= thresh and not is_them(excluded_objects, box):
                    return True
        return False

    def handle_judgement(self, judgements_dict, vis_imgs_dict):
        for name in judgements_dict.keys():
            if judgements_dict[name]:
                logging.warning(name + ' 工位' + ' 异常闯入')
                if self.opc_client is not None:
                    th1 = threading.Thread(target=self.__thread_safe_stop_working, args=(name,))
                    th1.start()
                th2 = threading.Thread(target=self.__save_record, args=(name, vis_imgs_dict[name]))
                th2.start()

    def __thread_safe_stop_working(self, name):
        self.lock.acquire()
        self.opc_client.stop_it_if_working(name)
        self.lock.release()

    def __save_record(self, name, img_array, event='intrusion'):
        strftime = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        img_name = event + '_' + strftime + '.jpg'

        # img_dir = self.records_root + name + '/'
        # if os.path.exists(img_dir + img_name):
        #     img_name = event + '_' + strftime + '_' + str(random.randint(0, 100)) + '.jpg'

        img_dir = os.path.join(self.records_root, name)
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img_path = os.path.join(img_dir, img_name)

        cv2.imwrite(img_path, img_array)
        logging.info(name + ' 工位' + ' 异常图片已保存')

        if open_wechat_bot:
            self.wechat.send_image(img_path, name)


