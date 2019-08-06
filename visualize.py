import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from utils.utils import plot_one_box


class Visualize:

    def __init__(self, masks_path_dict):
        self.masks_dict = self.get_mask(masks_path_dict)

    @staticmethod
    def get_mask(masks_path_dict):
        masks_dict = {}
        for name in masks_path_dict.keys():
            if not os.path.exists(masks_path_dict[name]):
                raise RuntimeError(str(name) + "mask路径不存在")
            mask = cv2.imread(masks_path_dict[name])
            masks_dict[name] = mask

        return masks_dict

    def draw_static_contents(self, img_array, name):
        mask = self.masks_dict[name]
        overlap = cv2.addWeighted(img_array, 1, mask, 0.6, 0)
        return overlap

    @staticmethod
    def draw_fps(img_array, show_fps):
        img_array = cv2.putText(img_array, text=show_fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.5, color=(255, 200, 0), thickness=2)
        return img_array

    @staticmethod
    def draw_Chinese_words(img_array, contents, coord, color):
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img_array)

        # PIL图片上打印汉字
        draw = ImageDraw.Draw(img)  # 图片上打印
        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
        draw.text(coord, contents, color, font=font)

        # PIL 图片转 cv2 图片
        img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_array

    def draw(self, frames_dict, preds_dict, judgements_dict, fps):
        vis_imgs_dict = {}
        for name in frames_dict.keys():
            frame = frames_dict[name]
            pred = preds_dict[name]
            judgement = judgements_dict[name]

            img = self.draw_static_contents(frame, name)
            img = self.draw_fps(img, fps)

            label = 'person'
            if pred is not None:
                for x1, y1, x2, y2 in pred:
                    plot_one_box((x1, y1, x2, y2), img, label=label, color=(225, 225, 0))

            if judgement:
                img = cv2.putText(img, text='Kick your head!!!', org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=2, color=(0, 0, 255), thickness=4)
            else:
                img = cv2.putText(img, text='Safe working', org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=2, color=(0, 255, 0), thickness=4)
            vis_imgs_dict[name] = img
        return vis_imgs_dict
