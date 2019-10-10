import time
from multiprocessing import Process, Value
from gui_main import gui_main
from monitor import is_alive


def subprocess_run(detection_flag: Value) -> Process:
    p = Process(target=gui_main, args=(detection_flag,))
    p.start()
    return p


if __name__ == '__main__':
    detection_flag = Value('i', 0)  # variable with shared memory between multi processes
    p = subprocess_run(detection_flag)

    while True:
        time.sleep(10)
        if is_alive(detection_flag):
            print('The detection process is <alive>')
        else:
            print('The detection process is <dead>!')
            p.terminate()  # kill the subprocess
            time.sleep(2)
            print('reboot')
            detection_flag = Value('i', 0)
            p = subprocess_run(detection_flag)