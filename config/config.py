import collections


# 视频流 URL
video_stream_paths_dict = {
    'sawanini_1': 'rtsp://user:xiolift123@10.19.31.138/Streaming/Channels/102',
    'sawanini_2': 'rtsp://user:xiolift123@10.19.31.154/Streaming/Channels/102',
    'zhuanjixia': 'rtsp://user:xiolift123@10.19.31.136/Streaming/Channels/102',
    'penfenshang': 'rtsp://user:xiolift123@10.19.31.139/Streaming/Channels/102',
    'baobantongyong': 'rtsp://user:xiolift123@10.19.31.137/Streaming/Channels/102',
}

# for local test
# video_stream_paths_dict = {
#     'sawanini_1': 'E:/Datasets/XIO/intrusion_detection/mix_video.avi',
#     'sawanini_2': 'E:/Datasets/XIO/intrusion_detection/outputhou.avi',
#     'zhuanjixia': 'E:/Datasets/XIO/intrusion_detection/still_1.avi',
#     'penfenshang': 'E:/Datasets/XIO/intrusion_detection/still_2.avi',
#     'baobantongyong': 'E:/Datasets/XIO/intrusion_detection/mix_video.avi',
# }

# 视频帧的形状
frame_shape = (480, 640)

# 各视频流是否检测的开关，1 表示检测， 0 表示不检测
switch_mask = (1, 1, 1, 1, 1)

# 需要显示的视频流名称
vis_name = 'sawanini_1'


# 禁区掩码图像路径
masks_paths_dict = {
    'sawanini_1': 'images/masks/sawanini_1.jpg',
    'sawanini_2': 'images/masks/sawanini_2.jpg',
    'zhuanjixia': 'images/masks/zhuanjixia.jpg',
    'penfenshang': 'images/masks/penfenshang.jpg',
    'baobantongyong': 'images/masks/baobantongyong.jpg',
}

# 判断人的边界框进入禁区的阈值
inter_threshold = 0.2

# 设定待检测目标物体最大边界框面积，
# 排除模型误检中较大的物体
max_object_bbox_area_dict = {
    'sawanini_1': 15000,
    'sawanini_2': 12000,
    'zhuanjixia': 12000,
    'penfenshang': 20000,
    'baobantongyong': 20000,  # TODO
}
# 设定待检测目标物体最小边界框面积，
# 排除模型误检中较小的物体
min_object_bbox_area_dict = {
    'sawanini_1': 500,
    'sawanini_2': 500,
    'zhuanjixia': 500,
    'penfenshang': 500,
    'baobantongyong': 500,
}

# 排除掉可能被错识别为人的目标物体区域
excluded_objects_dict = {
    'sawanini_1': [],
    'sawanini_2': [],
    'zhuanjixia': [(175, 130, 200, 155), ],
    'penfenshang': [],
    'baobantongyong': [],
}

# 是否连接OPC服务器，执行紧急停机
open_opc = True

# OPC 服务器 URL
opc_url = 'opc.tcp://10.19.3.35:49320'

# 机器工位节点
nodes_dict = {
    'sawanini_1': 'ns=2;s=sawaninigaopin.OP30-S71214C.轿壁小车2光幕被报警',
    'sawanini_2': 'ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志',
    'zhuanjixia': 'ns=2;s=laozhuanjixian.shangpenfenxiazhewanCJ2M.下折弯光幕报警',
    'penfenshang': 'ns=2;s=laozhuanjixian.shangpenfenxiazhewanCJ2M.上喷粉站报警',  # TODO 同时给两个点位置 1
    'baobantongyong': 'ns=2;s=weibentongyongxian.S7300.机器人停止',
}

# -------------- detection model configuration -----------------
img_size = 416  # size of each image dimension
config_path = 'config/yolov3.cfg'  # path to model config file
weights_path = 'weights/yolov3.weights'  # path to weights file
class_path = 'config/coco.names'  # path to class label file
conf_thres = 0.8  # object confidence threshold
nms_thres = 0.4  # iou threshold for non-maximum suppression
device_name = 'cuda:0'  # use cuda if available
