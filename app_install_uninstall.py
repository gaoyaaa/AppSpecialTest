# Author: AdrianZhang
# Coding Time: 2017/10/25
# Script function: 一个实现Android APK自动化的安装、卸载测试脚本。

import os
import time

class AppTest(object):
    def __init__(self):
        self.apk_path = "C:\\Users\\Adrian\\Desktop\\qiyi.apk"        # 使用爱奇艺的apk进行测试，apk文件放在windows桌面。
        self.apk_package_name = "com.qiyi.video"

    def install(self):
        cmd_install = "adb install {}".format(self.apk_path)
        install_log_content = os.popen(cmd_install).read()
        return install_log_content

    def uninstall(self):
        cmd_uninstall = "adb uninstall {}".format(self.apk_package_name)
        uninstall_log_content = os.popen(cmd_uninstall).read()
        return uninstall_log_content

class Control(object):
    def __init__(self, count):
        self.app_test = AppTest()
        self.counter = count

    def single_test(self):
        print("--> {} Starts install {}".format(self.get_time(), self.app_test.apk_path))
        self.app_test.install()
        time.sleep(10)
        print("--> {} Starts uninstall {}".format(self.get_time(), self.app_test.apk_package_name))
        self.app_test.uninstall()
        time.sleep(10)

    def many_times_test(self):
        while self.counter > 0:
            self.single_test()
            self.counter -= 1

    def get_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time

if __name__ == '__main__':
    do_test = Control(10)           # 设定执行安装、卸载的次数，此处为10次。
    do_test.many_times_test()


