import time
from threading import Thread
from wxpy import Bot, ensure_one, ResponseError
from configs.config import video_stream_paths_dict, send_interval


class WeChat:
    def __init__(self, group_name: str, video_stream_dict: dict):
        self.bot = None
        self.group = None
        self._login()
        self._search_group(group_name)
        self.prev_send_timestamp = dict(zip(video_stream_dict.keys(),
                                            [0] * len(video_stream_dict)))  # 发送时间间隔的标志

    def _login(self):
        try:
            bot = Bot(cache_path=True)
            self.bot = bot
        except KeyError:
            raise ConnectionRefusedError("网页版微信登录被拒绝！")

    def _search_group(self, group_name):
        if self.bot is not None:
            groups = self.bot.groups().search(group_name)
            # groups = self.bot.friends().search(group_name)
            if len(groups) < 1:
                raise RuntimeError("未能找到该微信群组或群组未被添加到通讯录！")
            group = ensure_one(groups)
            self.group = group
        else:
            raise RuntimeError('请先登录微信机器人！')

    def _sendable(self, node: str) -> bool:
        curr = int(time.time())
        prev = self.prev_send_timestamp[node]
        interval = prev - curr

        if interval > send_interval:
            self.prev_send_timestamp[node] = curr
            return True
        else:
            return False

    def send_msg(self, msg: str, node: str):
        if not self._sendable(node):
            return
        if self.group is not None:
            try:
                self.group.send_msg(msg)
            except ResponseError as e:
                print(e.err_code, e.err_msg, "微信机器人发送消息失败")
        else:
            raise RuntimeError("没有微信群聊对象")

    def send_image(self, img_path: str, node: str):
        if not self._sendable(node):
            return
        if self.group is not None:
            try:
                self.group.send_image(img_path)
                # self._wait_minute(node)  # TODO
            except ResponseError as e:
                print(e)
                print(e.err_code, e.err_msg, "微信机器人发送图片失败")
        else:
            raise RuntimeError("没有微信群聊对象")

    def async_send_msg(self, msg: str, node: str):
        th = Thread(target=self.send_msg, args=[msg, node])
        th.start()

    def async_send_image(self, img_path: str, node: str):
        th = Thread(target=self.send_image, args=[img_path, node])
        th.start()


if __name__ == '__main__':
    wechat = WeChat("陈振辉", video_stream_paths_dict)
    wechat.async_send_msg('..\\images\\records\\vlcsnap-2019-08-02-16h02m31s252.png', 'sawanini_1')
    wechat.async_send_image('..\\images\\records\\vlcsnap-2019-08-02-16h02m31s252.png', 'sawanini_1')
    # wechat._send_image('..\\images\\records\\vlcsnap-2019-08-02-16h02m31s252.png', 'sawanini_1')
    wechat.bot.join()

