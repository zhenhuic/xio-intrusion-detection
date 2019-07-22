import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config.config import restricted_areas_dict, tolerated_areas_dict
from utils.utils import plot_one_box


def draw_static_contents(img_array, name):
    # draw restricted area rectangles
    restricted_rects = restricted_areas_dict[name]
    line_thickness = round(0.001 * max(img_array.shape[0:2])) + 1
    for rect in restricted_rects:
        img_array = cv2.rectangle(img_array, (rect[0], rect[1]), (rect[2], rect[3]),
                                  (0, 0, 255), thickness=line_thickness)

    # draw tolerated area rectangles
    tolerated_rects = tolerated_areas_dict[name]
    for rect in tolerated_rects:
        img_array = cv2.rectangle(img_array, (rect[0], rect[1]), (rect[2], rect[3]),
                                  (0, 255, 0), thickness=(line_thickness - 1), lineType=cv2.LINE_4)

    # draw introduction words
    # img_array = draw_Chinese_words(img_array, '视觉安全检测', (900, 50), ())

    return img_array


def draw_fps(img_array, show_fps):
    img_array = cv2.putText(img_array, text=show_fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5, color=(255, 200, 0), thickness=2)
    return img_array


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


def draw(name, frames_dict, preds_dict, judgements_dict, fps):
    frame = frames_dict[name]
    pred = preds_dict[name]
    judgement = judgements_dict[name]

    img = draw_static_contents(frame, name)
    img = draw_fps(img, fps)

    label = 'person 0.99'
    if pred is not None:
        for x1, y1, x2, y2 in pred:
            plot_one_box((x1, y1, x2, y2), img, label=label, color=(225, 225, 0))

    if judgement:
        img = cv2.putText(img, text='Kick your head!!!', org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                          fontScale=2, color=(0, 0, 255), thickness=4)
    else:
        img = cv2.putText(img, text='Safe working', org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                          fontScale=2, color=(0, 255, 0), thickness=4)
    return img

