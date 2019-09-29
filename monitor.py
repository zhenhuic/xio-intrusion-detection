import threading
import time

import pymysql
import serial


class MySql:
    def __init__(self):
        self.config = {
            'host': '10.19.3.35',
            'user': 'root',
            'password': '123456',
            'database': 'intrusion_detection'
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = pymysql.Connect(**self.config)
            print("MySQL已连接")
        except Exception as e:
            print('无法连接数据库！')

    def insert_timestamp(self):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                stamp = int(time.time())
                sql = "INSERT INTO monitor(timestamp) VALUES(%s)"
                cursor.execute(sql, stamp)
            self.conn.commit()
        except Exception:
            print('数据库写入失败！')
        finally:
            if self.conn is not None:
                self.conn.close()

    def asynchronous_insert_timestamp(self):
        th = threading.Thread(target=self.insert_timestamp)
        th.start()

    def read_latest_record(self) -> tuple:
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT timestamp FROM monitor ORDER BY id DESC LIMIT 1;"
                cursor.execute(sql)
                data = cursor.ferchone()
            return data
        except Exception:
            print('数据库写入失败！')
        finally:
            if self.conn is not None:
                self.conn.close()


class WarningLight:
    def __init__(self, port):
        self.port = port
        self.serial = None

    def __connect(self):
        ser = serial.Serial(self.port)
        return ser

    def alarm(self):
        self.serial.write([])  # TODO

    def shut_up(self):
        self.serial.write([])  # TODO


class Monitor:
    def __init__(self, database: MySql, warning_light: WarningLight):
        self.db = database
        self.light = warning_light

        self.previous_record = None

    def updated(self) -> bool:
        timestamp = self.db.read_latest_record()[0]
        if self.previous_record is None:
            self.previous_record = timestamp
            return True
        else:
            if timestamp <= self.previous_record:
                return False
            else:
                return True

    def run(self):
        while True:
            if self.updated():
                print('It is alive.')
            else:
                print('The process is dead!')
            time.sleep(60)


if __name__ == '__main__':
    mysql = MySql()
    light = WarningLight('COM4')
    monitor = Monitor(mysql, light)

    monitor.run()
