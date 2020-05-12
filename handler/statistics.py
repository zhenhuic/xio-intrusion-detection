import time
import threading

from handler.send_email import Email
from handler.database import MySql


class IntrusionStatistics:
    def __init__(self, video_stream_dict: dict, report_interval: int):
        self.epoch_start: str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.report_interval: int = report_interval
        self.prev_intrusion_timestamp: dict = dict(zip(video_stream_dict.keys(), [0] * len(video_stream_dict)))
        self.lock = threading.Lock()

        self.number_intrusion: dict = dict(zip(video_stream_dict.keys(), [0] * len(video_stream_dict)))
        # 记录闯入图片的路径
        self.intrusion_records: dict = dict(zip(video_stream_dict.keys(), [[]] * len(video_stream_dict)))

        self.subthread_report_with_email()

    def add_one_record(self, name: str, img_path: str):
        curr_time = time.time()
        if curr_time - self.prev_intrusion_timestamp[name] > 60:  # 同一个工位一分钟之内的所有闯入算一次
            self.lock.acquire()
            try:
                self.number_intrusion[name] += 1
                self.intrusion_records[name].append(img_path)
                self.prev_intrusion_timestamp[name] = curr_time
                # MySql.add_record(name)
            finally:
                self.lock.release()

    def subthread_report_with_email(self):
        th = threading.Thread(target=self.__report_with_email)
        th.start()

    def __report_with_email(self):
        while True:
            time.sleep(self.report_interval)

            strftime = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
            for i in self.number_intrusion.values():
                if i > 0:
                    text = str(self.epoch_start) + '-' + strftime + '\n'
                    for name in self.number_intrusion.keys():
                        text = text + '\t' + name + ': ' + str(self.number_intrusion[name]) + '次\n'
                    Email.send_email("安全监测系统异常闯入记录报告", text)

                    self.lock.acquire()
                    try:
                        for name in self.number_intrusion.keys():
                            self.number_intrusion[name] = 0
                            self.intrusion_records[name] = []
                    finally:
                        self.lock.release()
                    break
            self.epoch_start = strftime


