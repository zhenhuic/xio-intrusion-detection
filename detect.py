import time
import logging

import cv2
import torch
from PyQt5.QtGui import QImage

from model.models import Darknet
from video_stream.visualize import Visualize
from handler.opc_client import OpcClient
from configs.config import *
from utils.utils import non_max_suppression, load_classes, calc_fps
from model.transform import transform, stack_tensors, preds_postprocess
from handler.intrusion_handling import IntrusionHandling
from handler.send_email import Email
from video_stream.video_stream import VideoLoader
from configs.config import patrol_opc_nodes_interval, update_detection_flag_interval,\
    open_email_warning
# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


def get_model(config_path, img_size, weights_path, device):
    model = Darknet(config_path, img_size=img_size)
    model.load_darknet_weights(weights_path)

    model = model.to(device)
    model.eval()  # Set in evaluation mode
    return model


def inference(model, input_tensor, device, num_classes, conf_thres, nms_thres):
    try:
        torch.cuda.empty_cache()  # 修复 RuntimeError: cuDNN error: CUDNN_STATUS_EXECUTION_FAILED
        input_tensor = input_tensor.to(device)
        # print(input_tensor.shape)

        output = model(input_tensor)
        preds = non_max_suppression(output, conf_thres, nms_thres)
    except RuntimeError as e:
        torch.cuda.empty_cache()
        preds = [None for _ in range(input_tensor.shape[0])]
        print(e)
        logging.error(e)
    # preds = non_max_suppression(output, num_classes, conf_thres, nms_thres)
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
    global prevs_vis_name

    prevs_vis_name = vis_name
    vis_name = list(video_stream_paths_dict.keys())[index]


@torch.no_grad()
def detect_main(qthread):
    device = torch.device(device_name)
    model = get_model(config_path, img_size, weights_path, device)
    logging.info('Model initialized')

    if open_opc:
        opc_client = OpcClient(opc_url, nodes_dict)
        strftime = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
        qthread.text_append.emit(strftime + ' OPC 服务器已连接')
        logging.info('OPC Client created')

    else:
        opc_client = None
        strftime = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
        qthread.text_append.emit(strftime + ' OPC 服务器未连接')
        logging.warning('OPC Client does not create')
    if open_email_warning:
        warning_email = Email()
    else:
        warning_email = None

    visualize = Visualize(masks_paths_dict)
    handling = IntrusionHandling(masks_paths_dict, opc_client)

    qthread.status_update.emit('读取视频流')
    video_loader = VideoLoader(video_stream_paths_dict)
    logging.info('Video streams create: ' + ', '.join(n for n in video_stream_paths_dict.keys()))

    classes = load_classes(class_path)  # Extracts class labels from file
    qthread.status_update.emit('准备就绪')

    # 计时器开始的变量
    since = patrol_opc_nodes_clock_start = update_detection_flag_clock_start = time.time()

    # 用于后续计算检测FPS
    accum_time, curr_fps = 0, 0
    show_fps = 'FPS: ??'

    logging.info('Enter detection main loop process')
    exception_flag = False
    while not exception_flag:
        # 当前次循环的时间戳
        curr_time = time.time()

        if curr_time - update_detection_flag_clock_start > update_detection_flag_interval:
            update_detection_flag_clock_start = curr_time
            qthread.detection_flag.value = 1  # 更新 detection_flag
            # time.sleep(10)  # 模拟检测程序卡住 10s

        # 隔一段时间轮巡读取一遍OPC状态信息，确认OPC服务正常与否
        # if open_opc and curr_time - patrol_opc_nodes_clock_start > patrol_opc_nodes_interval:
        if curr_time - patrol_opc_nodes_clock_start > patrol_opc_nodes_interval:
            patrol_opc_nodes_clock_start = curr_time
            try:
                opc_client.patrol_nodes()
            except RuntimeError as er:
                strftime = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                msg = strftime + ' OPC服务失效,无法获取节点数据！！'
                qthread.text_append.emit(msg)
                print(msg)
                logging.error('OPC服务失效,无法获取节点数据！！')
                qthread.popup_message_box.emit("OPC服务异常，无法获取机器人节点数据, 系统失效！！\n请排查OPC软件异常后，重启系统\n\n联系电话: 13429129739")
                if open_email_warning and warning_email is not None:
                    warning_email.subthread_email_warning("OPC服务失效,无法获取节点数据", "检查时间:" + strftime)

            except Exception as ex:
                strftime = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                msg = strftime + ' OPC服务失效,无法获取节点数据！！未知错误'
                qthread.text_append.emit(msg)
                print(msg + str(ex))
                logging.error('OPC服务无法获取节点数据！！未知错误' + str(ex))
                qthread.popup_message_box.emit("无法获取OPC服务节点数据, 系统失效！！\n请排查OPC软件问题，重启系统\n\n联系电话: 13429129739")
                if open_email_warning and warning_email is not None:
                    warning_email.subthread_email_warning("OPC服务失效,无法获取节点数据", "检查时间:" + strftime)

        # prepare frame tensors before inference
        frames_dict = video_loader.getitem()
        input_tensor = []
        for name in frames_dict.keys():
            tensor = transform(frames_dict[name], img_size)
            input_tensor.append(tensor)
        input_tensor = stack_tensors(input_tensor)

        # model inference and postprocess
        preds = inference(model, input_tensor, device, 80, conf_thres, nms_thres)
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
        try:
            handling.handle_judgement(judgements_dict, vis_imgs_dict)
        except RuntimeError as e:
            print(e)

        # emit the information to the front end
        img = vis_imgs_dict[vis_name]
        qimage = array_to_QImage(img, (780, 430))
        qthread.video_1_change_pixmap.emit(qimage)

        for name in judgements_dict.keys():
            if judgements_dict[name]:
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + name + ' 启动联锁保护')
                # show intrusion record
                img = vis_imgs_dict[name]
                qimage = array_to_QImage(img, (358, 243))
                qthread.record_change_pixmap.emit(qimage)

        prevs_img = vis_imgs_dict[prevs_vis_name]
        vis_imgs_dict[vis_name] = prevs_img
        vis_imgs_dict.pop(prevs_vis_name)

        for i, img in enumerate(vis_imgs_dict.values()):
            qimage = array_to_QImage(img, (204, 155))
            if i == 0:
                qthread.video_2_change_pixmap.emit(qimage)
            elif i == 1:
                qthread.video_3_change_pixmap.emit(qimage)
            elif i == 2:
                qthread.video_4_change_pixmap.emit(qimage)
            elif i == 3:
                qthread.video_5_change_pixmap.emit(qimage)
            else:
                raise RuntimeError("No so many QLabel!")


if __name__ == '__main__':
    detect_main(None)
