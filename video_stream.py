import cv2
import time


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
        print(since)
        return frame

    def release(self):
        self.__capture.release()

    def is_opened(self):
        return self.__capture.isOpened()
