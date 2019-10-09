import time
from multiprocessing import Process, Value
from gui_main import gui_main
from monitor import is_alive


def start_detect(detection_flag):
    p = Process(target=gui_main, args=(detection_flag,))
    p.start()
    return p


if __name__ == '__main__':
    detection_flag = Value('i', 0)
    p = start_detect(detection_flag)

    while True:
        time.sleep(10)
        if is_alive(detection_flag):
            print('The process is <alive>')
        else:
            print('The process is <dead>!')
            p.terminate()
            print('reboot')
            time.sleep(3)
            detection_flag = Value('i', 0)
            p = start_detect(detection_flag)
