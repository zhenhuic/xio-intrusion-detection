import cv2
import time
import sys


class VideoStream:
    def __init__(self, video_path, stream_name):
        self.video_path = video_path
        self.stream_name = stream_name

        self.__capture = self.__create_video_capture()

    def __create_video_capture(self):
        cap = cv2.VideoCapture(self.video_path)
        return cap

    def reconnect(self):
        self.__capture.release()
        self.__capture = self.__create_video_capture()

    def robust_read(self):
        ret, frame = self.__capture.read()

        reconn_flag = False
        since = time.time()
        while not ret or frame is None:
            self.reconnect()
            ret, frame = self.__capture.read()
            reconn_flag = True
        if reconn_flag:
            time_consume = time.time() - since
            print('视频流"{}"不稳定,重新连接 {:.2f}'.format(self.stream_name, time_consume))
        return frame

    def release(self):
        self.__capture.release()

    def is_opened(self):
        return self.__capture.isOpened()


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
        raise RuntimeError('无待检测视频流！')
    return video_streams_dict


def capture_one_frame(video_streams_dict):
    frames_dict = {}

    for name in video_streams_dict.keys():
        stream = video_streams_dict[name]
        frame = stream.robust_read()
        frames_dict[name] = frame

    return frames_dict
