# Author: AdrianZhang
# Coding Time: 2018/01/02
# Script Function: A script for scan web address status code.

import csv
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_web_address(web_address_file):
    with open(web_address_file) as csvfile:
        reader = csv.reader(csvfile)
        web_address = []
        for item in reader:
            for strings in item:
                web_address.append(strings)
    return web_address

def write_status_code(web_address, headers):
    result_file_name = 'result_'+web_address_file
    with open(result_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Web Address', 'Test Time', 'Status Code'])
        for item in web_address:
            try:
                status_code_value = requests.get(item, headers=headers, timeout=30).status_code
                writer.writerow([item, time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), status_code_value])

            except Exception as e:
                print(e)
    return result_file_name

def send_mail(result_file_name, subject, smtp_server, sender, receiver, username, password):
    msg_root = MIMEMultipart('related')
    msg_root["Subject"] = subject

    msg_text = MIMEText("""
        <html>
          <body>
            <p style="font-size:20px">{}：</p>
            <p style="font-size:16px;color:red">测试结果已生成，请查收邮件附件！</p>
          </body>
        </html>""".format(subject), "html", "utf-8")
    msg_root.attach(msg_text)

    with open(result_file_name, 'rb') as fp:
        msg_log = MIMEText(fp.read(), 'base64', 'utf-8')
    msg_log["Content-Type"] = "application/octet-stream"
    msg_log["Content-Disposition"] = "attachment; filename=result_web_address.csv"
    msg_root.attach(msg_log)

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=10)
        server.set_debuglevel(0)
        server.login(username, password)
        server.sendmail(sender, receiver, msg_root.as_string())
        server.quit()
    except smtplib.SMTPException as msg:
        print(msg)

if __name__ == '__main__':
    web_address_file = 'web_address.csv'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    web_address = get_web_address(web_address_file)
    result_file_name = write_status_code(web_address, headers)

    subject = "Web Address Scan测试结果"
    smtp_server = "smtp.qq.com"
    sender = "sender@qq.com"
    receiver = "receiver@163.com"
    username = "sender@qq.com"
    password = "********"
    send_mail(result_file_name, subject, smtp_server, sender, receiver, username, password)


