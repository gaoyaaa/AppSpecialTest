# Author: AdrianZhang
# Coding Time: 2017/10/27
# Script Function: App启动耗时统计并自动发送报告的主执行脚本。

import os
import time
import launch_time
import data_processing
import send_mail

def get_current_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return current_time

def device_connect(device_name):
    try:
        cmd = "adb connect {}".format(device_name)
        connect_log = os.popen(cmd).read()
        if "connected to" in connect_log:
            print("\t{} Connected Device Success!".format(get_current_time()))
    except Exception as error:
        print(error)

def device_disconnect(device_name):
    try:
        cmd = "adb disconnect {}".format(device_name)
        disconnect_log = os.popen(cmd).read()
        if "disconnected" in disconnect_log:
            print("\t{} Disconnect Device Success!".format(get_current_time()))
    except Exception as error:
        print(error)

def execute_launch_time(count, app_activity, app_package):
    control = launch_time.Control(count, app_activity, app_package)
    control.get_log()
    time_list = control.many_times_test()
    return time_list

def execute_data_processing(count, app_version, launch_time_list):
    data_image = data_processing.DataProcessing(count, app_version, launch_time_list)
    data_image.get_data_visualization_image()
    data_report = data_image.get_data_report()
    recent_image_path = data_image.get_recent_image_path()
    recent_log_path = data_image.get_recent_log_path()
    return data_report, recent_image_path, recent_log_path

def execute_send_mail(smtp_server, sender, receiver, username, password, data_content, app_version, app_package, app_activity):
    execute_send = send_mail.SendMail(smtp_server, sender, receiver, username, password, data_content, app_version, app_package, app_activity)
    execute_send.mail_text()
    execute_send.mail_image()
    execute_send.mail_log_attachment()
    execute_send.send_mail()

if __name__ == '__main__':
    print("1. Start connecting device.")
    device_name = "127.0.0.1:7555"
    device_connect(device_name)

    print("2. Execute testing: launch_time.py")
    count = 25
    app_version = "V8.10.0"
    app_activity = "com.qiyi.video/.WelcomeActivity"
    app_package = "com.qiyi.video"
    launch_time_list = execute_launch_time(count, app_activity, app_package)
    print("\t", launch_time_list)

    print("3. Execute testing: data_processing.py")
    data_content = execute_data_processing(count, app_version, launch_time_list)
    print("\t", data_content[0], "\n\t", data_content[1], "\n\t", data_content[-1])

    print("4. Execute testing: send_mail.py")
    smtp_server = "smtp.qq.com"
    sender = "********@qq.com"
    receiver = "********@163.com"       # 群发可使用列表模式 ["********@163.com", "********@163.com", ...]
    username = "********@qq.com"
    password = "********"       # 此处的密码为邮箱的“授权码”，而非登录密码！
    execute_send_mail(smtp_server, sender, receiver, username, password, data_content, app_version, app_package, app_activity)

    print("5. Disconnect device.")
    device_disconnect(device_name)

    print("6. Tests complete, Please check the mail!")

