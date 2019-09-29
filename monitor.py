import time

from config.config import monitor_flag
<<<<<<< Updated upstream
# import pymysql
=======
import pymysql
>>>>>>> Stashed changes


class MySql:
    def __init__(self):
        self.server = '10.19.3.35'
        self.port = 3306
        self.user = "root"
        self.password = "123456"
        self.db = "shijue"
        self.conn = self._connect()  # 在创建对象时就创建连接

    def _connect(self):
        # 如果连接断开，则重新连接
        conn = pymysql.Connect(host=self.server, port=self.port, user=self.user, password=self.password,
                               database=self.db)
        print("MySQL已连接")
        return conn

    def read_flag(self):
        self.conn.ping(reconnect=True)
        try:
            sql = ''
            cursor = self.conn.cursor()
            cursor.execute(sql)
            flag = cursor.fetchall()
            cursor.close()
            return flag
        except Exception as e:
            raise RuntimeError('数据库读取失败')


def monitor():
    started = False
    global monitor_flag
    while True:
        if not started:
            if monitor_flag:
                started = True
                print('The detection process start')
            else:
                time.sleep(5)
        else:
            if monitor_flag:
                monitor_flag = False
                # mysql TODO
                print("Is alive")
            else:
                print('The process is dead')

            time.sleep(10)


if __name__ == '__main__':
    monitor()
