import sys

import cv2
import torch
from PIL import Image
import torchvision.transforms.functional as TF

from models import Darknet
from utils.utils import non_max_suppression
from video_stream import VideoStream


def get_model(config_path, img_size, weights_path, device):
    model = Darknet(config_path, img_size=img_size)
    model.load_weights(weights_path)

    model = model.to(device)
    model.eval()  # Set in evaluation mode
    return model


def transform(img_array, input_size):
    """

    :param img_array:
    :param input_size:
    :return:
    """
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img_array)

    width, height = img.size
    img = TF.resize(img, int(height / width * input_size))  # the smaller edge will be matched to input_size
    img = TF.pad(img, (0, int((img.size[0] - img.size[1]) / 2)))

    tensor = TF.to_tensor(img)
    tensor = TF.normalize(tensor, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    return tensor


def stack_tensors(tensors):
    stacked = torch.stack(tensors)
    return stacked


def initialize_video_streams(video_stream_paths, stream_names, switch_mask):
    video_stream_paths = [x for i, x in enumerate(video_stream_paths) if switch_mask[i]]
    stream_names = [x for i, x in enumerate(stream_names) if switch_mask[i]]

    video_streams_dict = {}
    for path, name in zip(video_stream_paths, stream_names):
        stream = VideoStream(path, name)
        video_streams_dict[name] = stream

    if video_streams_dict:
        print(str(list(video_streams_dict.keys())) + '视频流已初始化')
    else:
        print('无待检测视频流！')
        sys.exit()  # program process exit
    return video_streams_dict


def capture_one_frame(video_streams_dict):
    frames_dict = {}

    for name in video_streams_dict.keys():
        stream = video_streams_dict[name]
        frame = stream.robust_read()
        frames_dict[name] = frame

    return frames_dict


def inference(model, input_tensor, device, num_classes, conf_thres, nms_thres):
    input_tensor = input_tensor.to(device)
    output = model(input_tensor)
    preds = non_max_suppression(output, num_classes, conf_thres, nms_thres)
    # predictions = predictions.cpu()
    return preds


def preds_filter(preds):
    print(preds)
    print(type(preds))


@ torch.no_grad()
def main(args):
    device = torch.device(args.device)
    model = get_model(args.config_path, args.img_size, args.weights_path, device)

    video_stream_paths_dict = {
        'houban': 'E:/Datasets/XIO/still_1.avi',
        'zhewanji': 'E:/Datasets/XIO/still_2.avi',
    }

    video_streams_dict = initialize_video_streams(list(video_stream_paths_dict.values()),
                                                  list(video_stream_paths_dict.keys()),
                                                  switch_mask=(1, 1, 1))
    while True:
        frames_dict = capture_one_frame(video_streams_dict)

        input_tensor = []
        for name in frames_dict.keys():
            tensor = transform(frames_dict[name], args.img_size)
            input_tensor.append(tensor)
        input_tensor = stack_tensors(input_tensor)

        preds = inference(model, input_tensor, device, 80, args.conf_thres, args.nms_thres)
        preds_filter(preds)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, default='rtsp://user:xiolift123@10.19.31.154:554/ch2',
                        help='path to video')
    parser.add_argument('--open_opc', type=bool, default=False, help='whether to connect to opc server')

    # model config
    parser.add_argument('--img_size', type=int, default=416, help='size of each image dimension')
    parser.add_argument('--config_path', type=str, default='config/yolov3.cfg', help='path to model config file')
    parser.add_argument('--weights_path', type=str, default='weights/yolov3.weights', help='path to weights file')
    parser.add_argument('--class_path', type=str, default='data/coco.names', help='path to class label file')
    parser.add_argument('--conf_thres', type=float, default=0.8, help='object confidence threshold')
    parser.add_argument('--nms_thres', type=float, default=0.4, help='iou threshold for non-maximum suppression')
    parser.add_argument('--device', type=str, default='cuda:0', help='whether to use cuda if available')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    main(args)
