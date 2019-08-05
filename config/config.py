
# 视频流 URL
video_stream_paths_dict = {
        # 'houban': 'E:/Datasets/XIO/intrusion_detection/mix_video.avi',
        'houban': 'rtsp://user:xiolift123@10.19.31.154/Streaming/Channels/102',
        'xiazhewan': 'rtsp://user:xiolift123@10.19.31.136/Streaming/Channels/102',
        'shangpenfen': 'rtsp://user:xiolift123@10.19.31.139/Streaming/Channels/102',
        # '4': 'rtsp://user:xiolift123@10.19.31.137',
        # '5': 'rtsp://user:xiolift123@10.19.31.138',
    }

# 视频帧的形状
frame_shape = (480, 640)

# 各视频流是否检测的开关，1 表示检测， 0 表示不检测
switch_mask = (1, 1, 1, 0, 0)

# 需要显示的视频流名称
vis_name = 'houban'

# 安全禁区
restricted_areas_dict = {
    'houban': [(250, 230, 1500, 900), ],  # (left, top, right, bottom)
    'xiazhewan': [],
    'shangpenfen': [(175, 320, 1370, 1079), ],
    '4': [],
    '5': [],
}

# 从禁区中排除掉的区域
tolerated_areas_dict = {
    'houban': [(250, 230, 580, 430), ],  # (left, top, right, bottom)
    'xiazhewan': [],
    'shangpenfen': [(175, 320, 530, 470), ],
    '4': [],
    '5': [],
}

# 排除掉可能被错识别为人的目标物体区域
excluded_objects_dict = {
    'houban': [(690, 200, 880, 500), ],
    'xiazhewan': [],
    'shangpenfen': [],
    '4': [],
    '5': [],
}

# OPC 服务器 URL
opc_url = 'opc.tcp://10.19.3.35:49320'

# 机器工位节点
nodes_dict = {
    'houban': 'ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志',
    'xiazhewan': 'ns=2;s=laozhuanjixian.shangpenfenxiazhewanCJ2M.下折弯光幕报警',
    'shangpenfen': 'ns=2;s=laozhuanjixian.shangpenfenxiazhewanCJ2M.上喷粉光幕报警',
}
