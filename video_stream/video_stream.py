import ctypes
import inspect
import time
from queue import LifoQueue, Empty, Queue
from threading import Thread

import cv2
from configs.config import switch_dict


class VideoStream:
    def __init__(self, video_path, stream_name):
        self.video_path = video_path
        self.stream_name = stream_name
        self.capture = self.get_video_capture()

    def reconnect(self):
        if self.capture is not None:
            self.capture.release()
        self.capture = self.get_video_capture()

    def robust_read(self):
        if self.capture is None:
            return None

        ret, frame = self.capture.read()
        reconn_flag = False
        since = time.time()
        while not ret or frame is None:
            self.reconnect()
            if self.capture is None:
                return None
            ret, frame = self.capture.read()
            reconn_flag = True
        if reconn_flag:
            time_consume = time.time() - since
            print('视频流"{}"不稳定,重新连接 {:.2f}'.format(self.stream_name, time_consume))
        # assert frame.shape == (480, 640, 3)
        if frame.shape != (480, 640, 3):
            frame = cv2.resize(frame, (640, 480))
        return frame

    def release(self):
        if self.capture is not None:
            self.capture.release()

    def is_opened(self):
        if self.capture is not None:
            return self.capture.isOpened()

    def get_video_capture(self, timeout=3):
        if not switch_dict[self.stream_name]:
            return None
        res_queue = Queue()
        th = VideoCaptureDaemon(self.video_path, res_queue)
        th.start()
        try:
            return res_queue.get(block=True, timeout=timeout)
        except Empty:
            print('无法连接 {} Timeout occurred after {:.2f}s'.format(self.video_path, timeout))
            return None


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
            if stream.capture is not None:
                print(name, "视频流已创建")
            video_streams_dict[name] = stream
        return video_streams_dict

    def start(self):
        """
        如果某个视频流连接不上，就没必要创建线程，不然会进入死循环会严重影响性能
        """
        if self.video_streams_dict["sawanini_1"].capture is not None:
            th1 = Thread(target=self.update, args=('sawanini_1',))
            th1.daemon = True
            th1.start()

        if self.video_streams_dict["sawanini_2"].capture is not None:
            th2 = Thread(target=self.update, args=('sawanini_2',))
            th2.daemon = True
            th2.start()

        if self.video_streams_dict["zhuanjixia"].capture is not None:
            th3 = Thread(target=self.update, args=('zhuanjixia',))
            th3.daemon = True
            th3.start()

        if self.video_streams_dict["penfenshang"].capture is not None:
            th4 = Thread(target=self.update, args=('penfenshang',))
            th4.daemon = True
            th4.start()

        if self.video_streams_dict["baobantongyong"].capture is not None:
            th5 = Thread(target=self.update, args=('baobantongyong',))
            th5.daemon = True
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
                if frame is not None:
                    self.queues_dict[name].put(frame)
            else:
                with self.queues_dict[name].mutex:
                    self.queues_dict[name].queue.clear()

    def getitem(self):
        # return next frame in the queue
        frames_dict = {}
        for name in self.queues_dict.keys():
            if self.video_streams_dict[name].capture is not None:
                try:
                    # 设置timeout，否则一直返回None，主线程陷入死循环导致程序崩溃
                    frames_dict[name] = self.queues_dict[name].get(timeout=2)
                except Empty:
                    frames_dict[name] = None
            else:
                frames_dict[name] = None
        return frames_dict


class VideoCaptureDaemon(Thread):
    """
    由于 cv2.VideoCapture在找不到资源时会一直阻塞，
    而且没有设置timeout的方式，
    所以只能单独创建一个线程来尝试连接
    """
    def __init__(self, video, result_queue):
        super().__init__()
        self.setDaemon(True)
        self.video = video
        self.result_queue = result_queue

    def run(self):
        self.result_queue.put(cv2.VideoCapture(self.video))
