# 视频流 URL
video_stream_paths_dict = {
    # 'houban': 'E:/Datasets/XIO/intrusion_detection/mix_video.avi',
    # 'xiazhewan': 'E:/Datasets/XIO/intrusion_detection/mix_video.avi',
    'houban': 'rtsp://user:xiolift123@10.19.31.154/Streaming/Channels/102',
    'xiazhewan': 'rtsp://user:xiolift123@10.19.31.136/Streaming/Channels/102',
    'shangpenfen': 'rtsp://user:xiolift123@10.19.31.139/Streaming/Channels/102',
}

# 视频帧的形状
frame_shape = (480, 640)

# 各视频流是否检测的开关，1 表示检测， 0 表示不检测
switch_mask = (1, 1, 1, 0, 0)

# 需要显示的视频流名称
vis_name = 'houban'


# 禁区掩码图像路径
masks_paths_dict = {
    'houban': 'images/masks/houban.jpg',
    'xiazhewan': 'images/masks/xiazhewan.jpg',
    'shangpenfen': 'images/masks/shangpenfen.jpg',
}

# 判断人的边界框进入禁区的阈值
inter_threshold = 0.3

# 设定待检测目标物体最大边界框面积，
# 排除模型误检中较大的物体
max_object_bbox_area_dict = {
    'houban': 20000,
    'xiazhewan': 20000,
    'shangpenfen': 20000,
}
# 设定待检测目标物体最小边界框面积，
# 排除模型误检中较小的物体
min_object_bbox_area_dict = {
    'houban': 500,
    'xiazhewan': 500,
    'shangpenfen': 500,
}

# 排除掉可能被错识别为人的目标物体区域
excluded_objects_dict = {
    'houban': [],
    'xiazhewan': [],
    'shangpenfen': [],
}

# 是否连接OPC服务器，执行紧急停机
open_opc = True

# OPC 服务器 URL
opc_url = 'opc.tcp://10.19.3.35:49320'

# 机器工位节点
nodes_dict = {
    'houban': 'ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志',
    'xiazhewan': 'ns=2;s=laozhuanjixian.shangpenfenxiazhewanCJ2M.下折弯光幕报警',
    'shangpenfen': 'ns=2;s=laozhuanjixian.shangpenfenxiazhewanCJ2M.上喷粉光幕报警',
}

# detection model configuration, the values are default below
img_size = 416  # size of each image dimension
config_path = 'config/yolov3.cfg'  # path to model config file
weights_path = 'weights/yolov3.weights'  # path to weights file
class_path = 'config/coco.names'  # path to class label file
conf_thres = 0.8  # object confidence threshold
nms_thres = 0.4  # iou threshold for non-maximum suppression
device_name = 'cuda'  # use cuda if available
