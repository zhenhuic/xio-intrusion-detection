
# 视频流URL
video_stream_paths_dict = {
        'houban': 'E:/Datasets/XIO/still_1.avi',
        '2': 'E:/Datasets/XIO/still_2.avi',
    }

# 安全禁区
restricted_areas_dict = {
    'houban': [(250, 230, 1500, 900), ],  # (left, top, right, bottom)

}

# 从禁区中排除掉的区域
tolerated_areas_dict = {
    'houban': [(250, 230, 580, 430), ],

}

# 排除掉可能被错识别为人的目标物体区域
excluded_objects_dict = {
    'houban': [(690, 200, 880, 500), ],

}

# OPC 服务器 URL
opc_url = 'opc.tcp://10.19.3.35:49320'

# 机器工位节点
nodes_dict = {
    'houban': 'ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志',

}
