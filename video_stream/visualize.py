import os
import io

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from matplotlib.ticker import MaxNLocator

from utils.utils import plot_one_box
from configs.config import max_object_bbox_area_dict,\
    min_object_bbox_area_dict


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
        img_array = cv2.putText(img_array, text=show_fps, org=(2, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.2, color=(255, 200, 0), thickness=1)
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
        for name in preds_dict.keys():
            frame = frames_dict[name]
            pred = preds_dict[name]
            judgement = judgements_dict[name]

            img = self.draw_static_contents(frame, name)
            img = self.draw_fps(img, fps)

            label = 'person'
            if pred is not None:
                for x1, y1, x2, y2 in pred:
                    box_area = (x2 - x1) * (y2 - y1)
                    # 过滤掉过大和过小的识别框
                    if min_object_bbox_area_dict[name] <= box_area <= max_object_bbox_area_dict[name]:
                        plot_one_box((x1, y1, x2, y2), img, label=label, color=(225, 225, 0))

            if judgement:
                img = cv2.putText(img, text='Kick your head!!!', org=(30, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=1.2, color=(0, 0, 255), thickness=2)
            else:
                img = cv2.putText(img, text='Safe working', org=(30, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=1.2, color=(0, 255, 0), thickness=2)
            vis_imgs_dict[name] = img
        return vis_imgs_dict


def draw_bar_graph(names: [str], values: [int], title: str) -> np.ndarray:
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    fig, ax = plt.subplots()
    ax.bar(names, values)
    # ax.set_facecolor("darkgray")
    plt.xticks(rotation=60, fontsize=8)
    # ax.set_xlabel('')
    ax.set_title(title)
    ax.set_ylabel('异常记录次数')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    img = fig2img(fig)
    return img


def fig2img(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    return img


def array_to_QImage(img, size):
    rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgbImage.shape
    bytes_per_line = ch * w
    qimage = QImage(rgbImage.data, w, h, bytes_per_line, QImage.Format_RGB888)
    if isinstance(size, QSize):
        qimage = qimage.scaled(size)
    else:
        qimage = qimage.scaled(size[0], size[1])
    return qimage
