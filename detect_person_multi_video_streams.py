from models import *
from utils.utils import *
from utils.datasets import *

import os
import sys
import time
import datetime
import argparse
from opcua import Client
from opcua import ua

import torch
import cv2
import threading


def image_preprocess(img):
    img = pad_and_resize(img, opt.img_size)
    # Channels-first
    input_img = np.transpose(img, (2, 0, 1))
    input_img = np.expand_dims(input_img, axis=0)
    # As pytorch tensor
    input_tensor = torch.from_numpy(input_img).float()
    input_tensor = input_tensor.to(device)
    return input_tensor


def visualize_detections(frame, detections):
    """
    在原图中画出检测结果（person）
    并返回画好的图和检测到person的bounding boxes
    :param frame:
    :param detections:
    :return:
    """
    # The amount of padding that was added
    pad_x = max(frame.shape[0] - frame.shape[1], 0) * \
            (opt.img_size / max(frame.shape))
    pad_y = max(frame.shape[1] - frame.shape[0], 0) * \
            (opt.img_size / max(frame.shape))
    # Image height and width after padding is removed
    unpad_h = opt.img_size - pad_y
    unpad_w = opt.img_size - pad_x

    detections = detections[0]
    # Draw bounding boxes and labels of detections
    person_bboxes = []
    if detections is not None:
        unique_labels = detections[:, -1].cpu().unique()
        n_cls_preds = len(unique_labels)
        bbox_colors = random.sample(colors, n_cls_preds)
        for *xyxy, conf, cls_conf, cls_pred in detections:
            if classes[int(cls_pred)] != 'person':  # 只检测人
                continue
            # print('\t+ Label: %s, Conf: %.5f' %
            #       (classes[int(cls_pred)], cls_conf.item()))

            # Rescale coordinates to original dimensions
            box_h = ((xyxy[3] - xyxy[1]) / unpad_h) * frame.shape[0]
            box_w = ((xyxy[2] - xyxy[0]) / unpad_w) * frame.shape[1]
            y1 = ((xyxy[1] - pad_y // 2) / unpad_h) * frame.shape[0]
            x1 = ((xyxy[0] - pad_x // 2) / unpad_w) * frame.shape[1]

            label = '%s %.2f' % (classes[int(cls_pred)], cls_conf)
            plot_one_box((x1, y1, x1 + box_w, y1 + box_h), frame, label=label, color=colors[int(cls_pred)])
            person_bbox = (x1, y1, x1 + box_w, y1 + box_h)
            person_bboxes.append(person_bbox)
    return frame, person_bboxes


def stop_it(node):
    node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
    print("机器人运行被中止！！")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str,
                        default='rtsp://user:xiolift123@10.19.31.154:554/ch2', help='path to video')
    parser.add_argument('--config_path', type=str,
                        default='config/yolov3.cfg', help='path to model config file')
    parser.add_argument('--weights_path', type=str,
                        default='weights/yolov3.weights', help='path to weights file')
    parser.add_argument('--class_path', type=str,
                        default='data/coco.names', help='path to class label file')
    parser.add_argument('--conf_thres', type=float, default=0.8,
                        help='object confidence threshold')
    parser.add_argument('--nms_thres', type=float, default=0.4,
                        help='iou threshold for non-maximum suppression')
    parser.add_argument('--n_cpu', type=int, default=8,
                        help='number of cpu threads to use during batch generation')
    parser.add_argument('--img_size', type=int, default=416,
                        help='size of each image dimension')
    parser.add_argument('--use_cuda', type=bool, default=True,
                        help='whether to use cuda if available')
    opt = parser.parse_args()
    print(opt)

    device = torch.device("cuda:0" if torch.cuda.is_available() and opt.use_cuda else "cpu")
    # Set up model
    model = Darknet(opt.config_path, img_size=opt.img_size)
    model.load_weights(opt.weights_path)

    model = model.to(device)
    model.eval()  # Set in evaluation mode

    # Extracts class labels from file
    classes = load_classes(opt.class_path)
    # Bounding-box colors
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]

    client = Client("opc.tcp://10.19.3.35:49320")
    node_info = "ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志"
    client.connect()
    node = client.get_node(node_info)
    print('opc connected')

    stream_1 = 'rtsp://user:xiolift123@10.19.31.154:554/ch2'
    # stream_1 = 'E:/datasets/XIO/still_1.avi'
    stream_2 = 'rtsp://user:xiolift123@10.19.31.136:554/ch2'
    # stream_3 = 'rtsp://user:xiolift123@10.19.31.137:554/ch2'
    # Get video capture
    cap_1 = cv2.VideoCapture(stream_1)
    print(cap_1.get(cv2.CAP_PROP_FPS))
    # cap_1.set(cv2.CAP_PROP_BUFFERSIZE, 0)
    # cap_1.set(cv2.CAP_PROP_FPS, fps)
    # cap_2 = cv2.VideoCapture(stream_2)
    # cap_2.set(cv2.CAP_PROP_FPS, fps)
    # cap_3 = cv2.VideoCapture(stream_3)
    # cap_3.set(cv2.CAP_PROP_FPS, fps)

    prev_time = time.time()
    num_frame = 0
    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    while cap_1.isOpened():
        try:
            ret_1, frame_1 = cap_1.read()
            # ret_2, frame_2 = cap_2.read()
            # ret_3, frame_3 = cap_3.read()
            while ret_1 is False:
                print("视频流不稳定")
                cap_1.release()
                # cap_2.release()
                # cap_3.release()
                cap_1 = cv2.VideoCapture(stream_1)
                # cap_1.set(cv2.CAP_PROP_FPS, fps)
                # cap_2 = cv2.VideoCapture(stream_2)
                # cap_2.set(cv2.CAP_PROP_FPS, fps)
                # cap_3 = cv2.VideoCapture(stream_3)
                # cap_3.set(cv2.CAP_PROP_FPS, fps)

                ret_1, frame_1 = cap_1.read()
                # ret_2, frame_2 = cap_2.read()
                # ret_3, frame_3 = cap_3.read()
        except Exception as e:
            print("读帧异常", e)
            break

        num_frame += 1
        input_tensor_1 = image_preprocess(frame_1)
        # input_tensor_2 = image_preprocess(frame_2)
        # input_tensor_3 = image_preprocess(frame_3)

        # Get detections
        with torch.no_grad():
            detections_1 = model(input_tensor_1)
            detections_1 = non_max_suppression(
                detections_1, 80, opt.conf_thres, opt.nms_thres)

            # detections_2 = model(input_tensor_2)
            # detections_2 = non_max_suppression(
            #     detections_2, 80, opt.conf_thres, opt.nms_thres)
            #
            # detections_3 = model(input_tensor_3)
            # detections_3 = non_max_suppression(
            #     detections_3, 80, opt.conf_thres, opt.nms_thres)

        # Log progress
        current_time = time.time()
        exec_time = current_time - prev_time
        prev_time = current_time
        accum_time = accum_time + exec_time
        curr_fps = curr_fps + 1
        if accum_time > 1:
            accum_time = accum_time - 1
            fps = "FPS: " + str(curr_fps)
            curr_fps = 0
        cv2.putText(frame_1, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5, color=(255, 200, 0), thickness=2)
        # inference_time = datetime.timedelta(seconds=current_time - prev_time)
        # print('\t+ Frame %d, Inference Time: %s' % (num_frame, inference_time))

        result_img_1, person_bboxes_1 = visualize_detections(frame_1, detections_1)
        # result_img_2, person_bboxes_2 = visualize_detections(frame_2, detections_2)
        # result_img_3, person_bboxes_3 = visualize_detections(frame_3, detections_3)
        danger_box = [(350, 210), (1500, 1000)]  # [(x1, y1), (x2, y2)]

        tl = round(0.001 * max(result_img_1.shape[0:2])) + 1  # line thickness
        cv2.rectangle(result_img_1, danger_box[0], danger_box[1], (0, 0, 255), thickness=tl)
        somebody_in_danger = False
        for i in person_bboxes_1:
            x = int((i[2] + i[0]) / 2)
            y = int((i[3] + i[1]) / 2)
            box_width = int(i[2] - i[0])
            box_height = int(i[3] - i[1])
            # print(x)

            if danger_box[0][0] < x < danger_box[1][0] and danger_box[0][1] < y < danger_box[1][1]:
                if i[2] < 570 and i[3] < 430:  # secure area 左上角(570, 430) 判断目标框的右下角是否进入
                    recent_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                    cv2.imwrite('records/uncertain_imgs/' + 'sec' + recent_time + '.jpg', result_img_1)
                    print(recent_time, '进入设定安全区域图像已保存')
                    continue
                if box_width < 80 and box_height < 80:  # 过滤小物体误检
                    recent_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                    cv2.imwrite('records/uncertain_imgs/' + 'small' + recent_time + '.jpg', result_img_1)
                    print(recent_time, '小目标过滤图像已保存')
                    continue
                if 765 < x < 792 and 330 < y < 365:  # 机器人误检区域
                    recent_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                    cv2.imwrite('records/uncertain_imgs/' + 'rob' + recent_time + '.jpg', result_img_1)
                    print(recent_time, '机器人误检区域图像已保存', str((x, y, box_width, box_height)))
                    continue

                cv2.putText(result_img_1, text='Kick your head!!!', org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=2, color=(0, 0, 255), thickness=4)
                somebody_in_danger = True
                print("目标框坐标", str((x, y, box_width, box_height)))
                break

        if not somebody_in_danger:
            cv2.putText(result_img_1, text='Safe working', org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=2, color=(0, 255, 0), thickness=4)
        else:
            recent_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            isStopFlag = node.get_value()
            if not isStopFlag:
                print(recent_time, '有人闯入，主动停机！！')
                try:
                    halt_thread = threading.Thread(target=stop_it, args=(node,))
                    halt_thread.start()
                    # node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
                except Exception as e:
                    print("OPC异常", e)
            else:
                print(recent_time, '有人闯入，机器静止')

            cv2.imwrite('records/halt_imgs/' + 'halt' + recent_time + '.jpg', result_img_1)
            print('图像已保存')

        cv2.namedWindow('Security detection Stream 1', cv2.WINDOW_NORMAL)
        # cv2.namedWindow('Security detection Stream 2', cv2.WINDOW_NORMAL)
        # cv2.namedWindow('Security detection Stream 3', cv2.WINDOW_NORMAL)
        cv2.imshow('Security detection Stream 1', result_img_1)
        # cv2.imshow('Security detection Stream 2', result_img_2)
        # cv2.imshow('Security detection Stream 3', result_img_3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap_1.release()
    # cap_2.release()
