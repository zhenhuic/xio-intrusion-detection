import time

import cv2
import torch
from PyQt5.QtGui import QImage

from models import Darknet
from visualize import Visualize
from opc_client import OpcClient
from config.config import *
from video_stream import initialize_video_streams, capture_one_frame
from utils.utils import non_max_suppression, load_classes, calc_fps
from utils.transform import transform, stack_tensors, preds_postprocess
from intrusion_handling import IntrusionHandling


def get_model(config_path, img_size, weights_path, device):
    model = Darknet(config_path, img_size=img_size)
    model.load_weights(weights_path)

    model = model.to(device)
    model.eval()  # Set in evaluation mode
    return model


def inference(model, input_tensor, device, num_classes, conf_thres, nms_thres):
    input_tensor = input_tensor.to(device)
    output = model(input_tensor)
    preds = non_max_suppression(output, num_classes, conf_thres, nms_thres)
    return preds


def array_to_QImage(img, size):
    rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgbImage.shape
    bytes_per_line = ch * w
    qimage = QImage(rgbImage.data, w, h, bytes_per_line, QImage.Format_RGB888)
    qimage = qimage.scaled(size[0], size[1])
    return qimage


def change_vis_stream(index):
    global vis_name
    vis_name = list(video_stream_paths_dict.keys())[index]


@torch.no_grad()
def detect_main(qthread):
    device = torch.device(device_name)
    model = get_model(config_path, img_size, weights_path, device)

    if open_opc:
        opc_client = OpcClient(opc_url, nodes_dict)
    else:
        opc_client = None

    video_streams_dict = initialize_video_streams(list(video_stream_paths_dict.values()),
                                                  list(video_stream_paths_dict.keys()),
                                                  switch_mask=switch_mask)
    visualize = Visualize(masks_paths_dict)
    handling = IntrusionHandling(masks_paths_dict, opc_client)

    # for calculating inference fps
    since = time.time()
    accum_time, curr_fps = 0, 0
    show_fps = 'FPS: ??'

    exception_flag = False
    while not exception_flag:
        # prepare frame tensors before inference
        frames_dict = capture_one_frame(video_streams_dict)
        input_tensor = []
        for name in frames_dict.keys():
            tensor = transform(frames_dict[name], img_size)
            input_tensor.append(tensor)
        input_tensor = stack_tensors(input_tensor)

        # model inference and postprocess
        preds = inference(model, input_tensor, device, 80, conf_thres, nms_thres)
        classes = load_classes(class_path)  # Extracts class labels from file
        preds_dict = preds_postprocess(preds, list(video_stream_paths_dict.keys()),
                                       frame_shape, img_size, classes)

        # judge whether someone breaks into
        judgements_dict = handling.judge_intrusion(preds_dict)

        # calculate inference fps
        since, accum_time, curr_fps, show_fps = calc_fps(since, accum_time, curr_fps, show_fps)
        # print(show_fps)

        # visualize detection results
        vis_imgs_dict = visualize.draw(frames_dict, preds_dict, judgements_dict, show_fps)

        # handle judgement results
        handling.handle_judgement(judgements_dict, vis_imgs_dict)

        img = vis_imgs_dict[vis_name]
        qimage = array_to_QImage(img, (780, 430))
        qthread.video_change_pixmap.emit(qimage)

        if judgements_dict[vis_name]:
            qimage = array_to_QImage(img, (358, 243))
            qthread.record_change_pixmap.emit(qimage)
        for name in judgements_dict.keys():
            if judgements_dict[name]:
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + name + ' 异常闯入')
