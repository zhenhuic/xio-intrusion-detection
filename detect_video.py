from models import *
from utils.utils import *
from utils.datasets import *

import os
import sys
import time
import datetime
from opcua import Client
from opcua import ua

import torch
import cv2

# model hyper-parameters
config_path = 'config/yolov3.cfg'  # path to model config file
weights_path = 'weights/yolov3.weights'  # path to weights file
class_path = 'data/coco.names'  # path to class label file
conf_thres = 0.8  # object confidence threshold
nms_thres = 0.4  # iou threshold for non-maximum suppression
img_size = 416  # size of each image dimension
use_cuda = True  # whether to use cuda if available

# video streams for detecting
video_paths = [
    'E:/datasets/XIO/still_1.avi',
    'E:/datasets/XIO/still_2.avi',
    # 'rtsp://user:xiolift123@10.19.31.154:554/ch2',
    # 'rtsp://user:xiolift123@10.19.31.136:554/ch2',
    # 'rtsp://user:xiolift123@10.19.31.137:554/ch2'
]

opc_paths = [

]

device = torch.device("cuda:0" if torch.cuda.is_available() and use_cuda else "cpu")
# Set up model
model = Darknet(config_path, img_size=img_size)
model.load_weights(weights_path)
model = model.to(device)
model.eval()  # Set in evaluation mode

classes = load_classes(class_path)  # Extracts class labels from file
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]  # Bounding-box colors




if __name__ == '__main__':
    pass
