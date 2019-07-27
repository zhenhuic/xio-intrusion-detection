import time
import cv2
from multiprocessing import Process, Queue
from video_stream import VideoStream


def read_frame(queue):
    video_path = 'E:/Datasets/XIO/safe_detection/still_1.avi'
    vs = VideoStream(video_path, 'test')
    while True:
        frame = vs.robust_read()
        queue.put(frame)
        print("read a frame")


def process(queue):
    while True:
        for _ in range(15):
            frame = queue.get(True)
        time.sleep(0.1)
        cv2.imshow('show', frame)
        print("show")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    q = Queue(50)
    pr = Process(target=read_frame, args=(q,))
    pp = Process(target=process, args=(q,))

    pr.start()
    pp.start()

    pp.join()
