# Author: AdrianZhang
# Coding Time: 2017/10/25
# Script function: 一个实现“Android APK自动安装、卸载”的测试脚本。

import os
import time

class AppTest(object):
    def __init__(self):
        self.apk_path = "C:\\Users\\Adrian\\Desktop\\qiyi.apk"      # 使用爱奇艺的apk进行测试，apk文件放在windows桌面。
        self.apk_package_name = "com.qiyi.video"
        self.install_result = ""
        self.uninstall_result = ""

    def install(self):
        cmd_install = "adb install {}".format(self.apk_path)
        self.install_result = os.popen(cmd_install).read()
        return self.install_result

    def uninstall(self):
        cmd_uninstall = "adb uninstall {}".format(self.apk_package_name)
        self.uninstall_result = os.popen(cmd_uninstall).read()
        return self.uninstall_result

class Control(object):
    def __init__(self, count):
        self.app_test = AppTest()
        self.initial = 1
        self.counter = count

    def single_test(self):
        print("{} [ No. {} ] {}".format("*" * 35, self.initial, "*" * 35))
        print("### {} ###\n### Starts install {} ###".format(self.get_time(), self.app_test.apk_path))
        self.app_test.install()
        print("{}".format(self.app_test.install_result))
        time.sleep(1)
        print("### {} ###\n### Starts uninstall {} ###".format(self.get_time(), self.app_test.apk_package_name))
        self.app_test.uninstall()
        print("{}".format(self.app_test.uninstall_result))
        time.sleep(1)

    def many_times_test(self):
        while self.initial <= self.counter:
            self.single_test()
            self.initial += 1

    def get_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time

if __name__ == '__main__':
    do_test = Control(10)           # 设定执行安装、卸载的次数，此处为10次。
    do_test.many_times_test()

