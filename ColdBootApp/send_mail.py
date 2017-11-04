# Author: AdrianZhang
# Coding Time: 2017/10/19
# Script Function: 汇总App启动耗时测试数据，并发送测试报告。

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class SendMail(object):
    def __init__(self, smtp_server, sender, receiver, username, password, data_content, app_version, app_package, app_activity):
        self.subject = "APP冷启动耗时测试结果"
        self.smtp_server = smtp_server
        self.sender = sender
        self.receiver = receiver
        self.username = username
        self.password = password
        self.data_result = data_content[0]
        self.recent_image_path = data_content[1]
        self.recent_log_path = data_content[2]
        self.app_version = app_version
        self.app_package = app_package
        self.app_activity = app_activity
        self.msg_root = MIMEMultipart('related')        # 使用related定义内嵌资源的邮件体
        self.msg_root["Subject"] = self.subject

    def mail_text(self):
        msg_text = MIMEText("""
        <html>
          <body>
            <p style="font-size:20px">{}：</p>
            <p style="font-size:16px;color:red">如果图中出现较大耗时情况，
            请根据X轴的系统时间点，参照邮件的log附件，查看对应系统时间点打印的日志。</p>
            <P style="font-size:16px">[ APP Version ]： {}</P>
            <P style="font-size:16px">[ APP Package Name ]： {}</P>
            <P style="font-size:16px">[ APP Activity Name ]： {}</P>
            <p style="font-size:16px">[ 平均耗时 ]： {}毫秒</p>
            <p style="font-size:16px">[ 最小耗时 ]： {}毫秒</p>
            <p style="font-size:16px;color:red">[ 最大耗时 ]： {}毫秒</p>
            <p style="font-size:16px">[ 总共测试次数 ]： {}次</p>
            <p style="font-size:16px">[ 低于平均耗时的次数 ]： {}次</p>
            <p style="font-size:16px;color:red">[ 超出平均耗时的次数 ]： {}次</p><br>
            <p><img src="cid:image1" width="1000" height="500" /></p><br>
          </body>
        </html>""".format(self.subject, self.app_version, self.app_package, self.app_activity,
                          self.data_result[0], self.data_result[1], self.data_result[2],
                          self.data_result[3], self.data_result[4], self.data_result[5]), "html", "utf-8")
        self.msg_root.attach(msg_text)

    def mail_image(self):
        with open(self.recent_image_path, 'rb') as fp:
            msg_image = MIMEImage(fp.read())
        msg_image.add_header('Content-ID', '<image1>')
        self.msg_root.attach(msg_image)

    def mail_log_attachment(self):
        with open(self.recent_log_path, 'rb') as fp:
            msg_log = MIMEText(fp.read(), 'base64', 'utf-8')
        msg_log["Content-Type"] = "application/octet-stream"
        msg_log["Content-Disposition"] = "attachment; filename=log.txt"
        self.msg_root.attach(msg_log)

    def send_mail(self):
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, 465, timeout=10)
            server.set_debuglevel(0)
            server.login(self.username, self.password)
            server.sendmail(self.sender, self.receiver, self.msg_root.as_string())
            server.quit()
        except smtplib.SMTPException as msg:
            print(msg)

