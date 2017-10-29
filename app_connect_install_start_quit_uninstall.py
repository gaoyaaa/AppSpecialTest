# Author: AdrianZhang
# Coding Time: 2017/10/29
# Script Function: 一个实现“设备连接、安装app、启动app、退出app、卸载app”的脚本。

import os
import time

class AppOperation(object):

    def device_connect(self):
        device_connect_cmd = "adb connect {}".format(device_name)
        try:
            connect_log = os.popen(device_connect_cmd).read()
            if "connected to" in connect_log:
                return True
            else:
                return False
        except Exception as message:
            print(message)

    def install_app(self):
        install_app_cmd = "adb -s {} install {}".format(device_name, apk_path)
        device_status = self.device_connect()
        if device_status:
            try:
                install_app_log = os.popen(install_app_cmd).read()
                if "Success" in install_app_log:
                    print(install_app_log, end="")
                    print("Install {} Success!\n".format(apk_path))
            except Exception as message:
                print(message)
        else:
            self.device_connect()

    def start_app(self):
        start_app_cmd = "adb shell am start -W -n {}".format(apk_package_activity)
        start_app_log = os.popen(start_app_cmd).read().replace("\n", ",")
        for log in start_app_log.split(",,"):
            print(log)

    def quit_app(self):
        quit_app_cmd = "adb shell am force-stop {}".format(apk_package_name)
        quit_app_log = os.popen(quit_app_cmd).read()
        if quit_app_log == "":
            print("Quit APP Success!\n")

    def uninstall_app(self):
        uninstall_app_cmd = "adb -s {} uninstall {}".format(device_name, apk_package_name)
        try:
            uninstall_app_log = os.popen(uninstall_app_cmd).read().replace("\n", "")
            if "Success" in uninstall_app_log:
                print("Uninstall {} {}!\n".format(apk_package_name, uninstall_app_log))
        except Exception as message:
            print(message)

class TimesControl(object):
    def __init__(self, count):
        self.app_operation = AppOperation()
        self.initial = 1
        self.counter = count

    def single_test(self):
        # 开始
        print("{:^30}{:^25}{:^30}{}".format(">" * 30, "Start Test: " + str(self.initial), "<" * 30, "\n" * 1))
        time.sleep(1)
        # 连接设备
        self.app_operation.device_connect()
        print("{:^30}{:^25}{:^30}\n{}\n".format("=" * 30, "Connect Result:", "=" * 30, self.app_operation.device_connect()))
        # 安装APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Install APP Result:", "=" * 30))
        self.app_operation.install_app()
        # 启动APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Start App Result:", "=" * 30))
        self.app_operation.start_app()
        time.sleep(5)
        # 关闭APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Quit App Result:", "=" * 30))
        self.app_operation.quit_app()
        time.sleep(1)
        # 卸载APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Uninstall APP Result:", "=" * 30))
        self.app_operation.uninstall_app()
        # 结束
        print("{:^30}{:^25}{:^30}{}".format(">" * 30, "End Test!", "<" * 30, "\n" * 5))

    def many_times_test(self):
        while self.initial <= self.counter:
            self.single_test()
            self.initial += 1

if __name__ == '__main__':
    device_name = "127.0.0.1:7555"
    apk_path = "C:\\Users\\Adrian\\Desktop\\qiyi.apk"
    apk_package_name = "com.qiyi.video"
    apk_package_activity = "com.qiyi.video/.WelcomeActivity"
    do_test = TimesControl(10)
    do_test.many_times_test()


