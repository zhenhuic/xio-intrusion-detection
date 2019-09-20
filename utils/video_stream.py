import cv2
import time
from queue import LifoQueue
from threading import Thread


class VideoStream:
    def __init__(self, video_path, stream_name, queue_maxsize=20):
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
        # assert frame.shape == (480, 640, 3)
        if frame.shape != (480, 640, 3):
            frame = cv2.resize(frame, (640, 480))
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


class VideoLoader:
    def __init__(self, video_streams_path_dict, queue_maxsize=50):
        self.queue_maxsize = queue_maxsize
        self.video_streams_dict = self.__video_captures(video_streams_path_dict)
        self.queues_dict = self.queues()
        self.start()

    @staticmethod
    def __video_captures(video_streams_path_dict):
        video_streams_dict = {}

        for name in video_streams_path_dict.keys():
            path = video_streams_path_dict[name]
            stream = VideoStream(path, name)
            video_streams_dict[name] = stream
        return video_streams_dict

    def start(self):
        th1 = Thread(target=self.update, args=('sawanini_1',))
        th1.daemon = True
        th2 = Thread(target=self.update, args=('sawanini_2',))
        th2.daemon = True
        th3 = Thread(target=self.update, args=('zhuanjixia',))
        th3.daemon = True
        th4 = Thread(target=self.update, args=('penfenshang',))
        th4.daemon = True
        th5 = Thread(target=self.update, args=('baobantongyong',))
        th5.daemon = True

        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th5.start()

    def queues(self):
        queues_dict = {}
        for name in self.video_streams_dict.keys():
            q = LifoQueue(maxsize=self.queue_maxsize)
            queues_dict[name] = q
        return queues_dict

    def update(self, name):
        while True:
            if not self.queues_dict[name].full():
                capture = self.video_streams_dict[name]
                frame = capture.robust_read()

                self.queues_dict[name].put(frame)
            else:
                with self.queues_dict[name].mutex:
                    self.queues_dict[name].queue.clear()

    def getitem(self):
        # return next frame in the queue
        frames_dict = {}
        for name in self.queues_dict.keys():
            frames_dict[name] = self.queues_dict[name].get()
        return frames_dict
