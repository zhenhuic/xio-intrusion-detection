import pymysql
import time
from configs.config import mysql_host, mysql_user,\
    mysql_password, mysql_db


class MySql:
    server = mysql_host
    port = 3306
    user = mysql_user
    password = mysql_password
    db = mysql_db

    @staticmethod
    def connect_mysql():
        return pymysql.Connect(
            host=MySql.server,
            port=MySql.port,
            user=MySql.user,
            password=MySql.password,
            database=MySql.db
        )

    @staticmethod
    def add_record(table: str):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        print(datetime)
        conn = None
        cursor = None
        try:
            conn = MySql.connect_mysql()
            cursor = conn.cursor()
            sql = "INSERT INTO {} (datetime) values ('{}')".format(table, datetime)
            print(sql)
            cursor.execute(sql)
            conn.commit()

            cursor.close()
            conn.close()
        except pymysql.err.MySQLError as e:
            print(e)
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.rollback()
                conn.close()

    @staticmethod
    def count_records_between_datetime(cursor: pymysql.cursors.Cursor,
                                       table: str, start: str, end: str) -> int:
        sql = "SELECT count(*) FROM {} WHERE datetime >= '{}' AND datetime <= '{}'".format(table, start, end)
        # print(sql)
        cursor.execute(sql)
        cnt = cursor.fetchone()[0]
        return int(cnt)

    @staticmethod
    def count_records_multi_datetime_periods(table: str, datetime_periods: [[str, str]]) -> [int]:
        conn = None
        cursor = None
        result = []
        try:
            conn = MySql.connect_mysql()
            cursor = conn.cursor()
            for period in datetime_periods:
                cnt = MySql.count_records_between_datetime(cursor, table, period[0], period[1])
                result.append(cnt)
            conn.commit()

            cursor.close()
            conn.close()
        except pymysql.err.MySQLError as e:
            print(e)
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
        except Exception as e:
            print(e)
        finally:
            return result


if __name__ == '__main__':
    # MySql.add_record('sawanini_1')
    res = MySql.count_records_multi_datetime_periods('sawanini_2', [['2020-05-07 20:18:16', '2020-05-09 22:00:10'],
                                                                    ['2020-05-09 22:00:10', '2020-05-07 20:18:16']])
    print(res)

