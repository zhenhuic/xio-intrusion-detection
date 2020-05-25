import smtplib
import time
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from threading import Thread

from configs.config import email_opc_warning_interval, email_address


class Email:
    def __init__(self):
        self.prev_send_timestamp = None
        self.email_warning_interval = email_opc_warning_interval

    @staticmethod
    def send_email(subject, content, imgpath=None, imgname=None, SMTP_host="smtp.qq.com",
                   from_account="1192317022@qq.com", from_password="fsaxnxeuabakfgbc",
                   to_account=email_address):
        """
        发送邮件
        :param subject: 邮件主题
        :param content: 邮件内容
        :param imgpath: 图片路径
        :param imgname: 发送图片名字
        :param SMTP_host: SMTP服务器地址，默认使用QQ
        :param from_account: 发送人邮箱账号
        :param from_password: 发送人邮箱密码(授权码)
        :param to_account: 收件人邮箱账号
        :return:
        """
        # 1. 实例化SMTP,创建对象
        smtp = smtplib.SMTP(timeout=1)
        # 2. 链接邮件服务器，若为QQ：smtp.qq.com,若为163：smtp.163.com
        smtp.connect(SMTP_host)
        # 3. 配置发送邮箱的用户名和密码(授权码)
        smtp.login(from_account, from_password)
        # 4. 配置发送对象msg及添加文字内容:
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, 'utf-8')  # 主题
        msg['From'] = from_account
        msg['To'] = to_account
        # # 添加内容到MIMEMultipart:
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        if imgpath is not None and imgname is not None:
            # 5. 添加图片附件
            with open(imgpath, 'rb') as f:
                # 设置附件的MIME和文件名
                img = MIMEBase('image', 'png',  filename=imgname)
                # 添加头信息
                img.add_header('Content-Disposition', 'attachment', filename=imgname)
                img.add_header('Content-ID', '<0>')
                img.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                img.set_payload(f.read())
                encode_base64(img)
                # 添加到MIMEMultipart:
                msg.attach(img)
        # 6. 配置发送邮箱，接受邮箱，以及发送内容
        smtp.sendmail(from_account, to_account, msg.as_string())
        # 7. 关闭邮件服务
        smtp.quit()

    def email_warning(self, subject, content=""):
        curr_time = time.time()
        if self.prev_send_timestamp is None or curr_time - self.prev_send_timestamp > self.email_warning_interval:
            try:
                self.send_email(subject, content)
                print("报警邮件发送成功")

                self.prev_send_timestamp = curr_time
            except smtplib.SMTPException as e:
                print("报警邮箱发送失败！", e)
                # raise e
            except Exception as ex:
                print("报警邮箱发送失败！", ex)

    def subthread_email_warning(self, subject, content):
        th = Thread(target=self.email_warning, args=(subject, content))
        th.start()
