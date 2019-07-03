import cv2


class VideoStream:
    def __init__(self, video_path, cap_buffer_size):
        self.video_path = video_path
        self.cap_buffer_size = cap_buffer_size

        self.capture = self._create_video_capture()

    def _create_video_capture(self):
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, self.cap_buffer_size)
        return cap

    def reconnect(self):
        self.capture.release()
        self.capture = self._create_video_capture()

    def read(self):
        ret, frame = self.capture.read()
        return ret, frame

    def release(self):
        self.capture.release()

    def is_opened(self):
        return self.capture.isOpened()
