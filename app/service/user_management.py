# Standard library imports.
import os
import re
import sqlite3
import json
import time
import datetime
from threading import Thread

from logging import getLogger

# Related third party imports.

# Local application/library specific imports.
from jobcan import Jobcan

logger = getLogger(__name__)


db_name = "user.sqlite"
db_path = f"{os.getcwd()}/db/{db_name}".replace('/', os.sep)

STATUS_UNREGISTERED = "UNREGISTERED"
STATUS_REGISTERED = "REGISTERED"

MESSAGE_UNREGISTERED = "未登録です"
MESSAGE_ALREADY_REGISTERED = "登録済みです"
MESSAGE_REGISTRATION = "メールアドレスとパスワードを入力してください(例: test@test.com 12345678)"
MESSAGE_REGISTERED = "登録しました"

class UserManagement:

    def __init__(self):
        # データベースファイルのパス
        # データベース接続とカーソル生成
        logger.info(db_path)
        self.connection = sqlite3.connect(db_path)
        # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        # connection.isolation_level = None
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def start_registration(self, user_id):
        self._create_tables()

        sql = f"SELECT status from users WHERE user_id==\"{user_id}\""
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data is None:
            logger.info(f"The user \"{user_id}\" is not in table.\nInsert this user.")
            self._insert_user(user_id)
            return(MESSAGE_REGISTRATION)
        else:
            if data[0] == STATUS_REGISTERED:
                return(MESSAGE_ALREADY_REGISTERED)
            else: # STATUS_UNREGISTERED
                return(MESSAGE_REGISTRATION)

    def user_ragistration(self, user_id, email, password):
        email = self.__convert_mailto2email(email)

        sql = f"SELECT status from users WHERE user_id==\"{user_id}\""
        logger.info(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data is None:
            return(MESSAGE_UNREGISTERED)
        else:
            if data[0] == STATUS_REGISTERED:
                return(MESSAGE_ALREADY_REGISTERED)
            else: # STATUS_UNREGISTERED
                sql = f"UPDATE users set email = \"{email}\", password = \"{password}\", status = \"{STATUS_REGISTERED}\" WHERE user_id==\"{user_id}\""
                self.cursor.execute(sql)
                return(MESSAGE_REGISTERED)

    def work(self, user_id, work_type):
        sql = f"SELECT email, password from users WHERE user_id==\"{user_id}\""
        logger.info(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data is None:
            return(MESSAGE_UNREGISTERED)
        else:
            if (work_type == "start"):
                return Jobcan.work_start(data[0], data[1])
            elif(work_type == "end"):
                return Jobcan.work_end(data[0], data[1])

    def make_reservation(self, user_id, work_type, time):
        thread = Thread(target=self._reservation_thread, args=(user_id, work_type, time))
        thread.start()

    def _reservation_thread(self, user_id, work_type, time):
        now = datetime.datetime.now()
        reservation_time = self._calc_resavation_time(now, time)

        td = reservation_time - now

        while td.seconds > 5:
            time.sleep(5)
            td = reservation_time - datetime.datetime.now()

        self.work(user_id, work_type)       

    def _calc_resavation_time(self, now, time):
        reservation_hour = int(time.split(':')[0])
        reservation_min = int(time.split(':')[1])

        if reservation_hour > now.hour or reservation_hour == now.hour and reservation_min >= now.minute:
            reservation_time = datetime.datetime.strptime(f"{now.year}/{now.month}/{now.day} {reservation_hour}:{reservation_min}", '%Y/%m/%d %H:%M')
        else:
            reservation_time = datetime.datetime.strptime(f"{now.year}/{now.month}/{now.day+1} {reservation_hour}:{reservation_min}", '%Y/%m/%d %H:%M')

        logger.info(f"Reservation time is {reservation_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return reservation_time

    def _create_tables(self):
        try:
            # CREATE
            self.cursor.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    email TEXT,
                    password TEXT,
                    status TEXT)''')
    
        except sqlite3.Error as e:
            print('sqlite3.Error occurred:', e.args[0])
    
    def _insert_user(self, user_id):
        sql = f"INSERT INTO users VALUES (\"{user_id}\", \"\", \"\",  \"{STATUS_UNREGISTERED}\")"
        logger.info(sql)
        self.cursor.execute(sql)

    def release(self):
        # 保存を実行（忘れると保存されないので注意）
        self.connection.commit()
        
        # 接続を閉じる
        self.connection.close()

    def __convert_db2jsonlist(self, rowdata):
        resjsonlist = []
        for data in rowdata:
            cols = data.keys()
            pos = 0
            json = {}
            for col in cols:
                d = {col : data[pos]}
                json.update(d)
                pos += 1
            resjsonlist.append(json)

        return resjsonlist

    def __convert_mailto2email(self, mail):
        pattern = r"\A<mailto:(.+\@.+\..+)\|.+\>"
        result = re.match(pattern, mail)
        correct_key = result.group(1)
        return correct_key
