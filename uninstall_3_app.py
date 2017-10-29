# Author: AdrianZhang
# Coding Time: 2017/10/25
# Script Function: 一个实现“卸载当前已连接的Android手机中所有第三方包”的脚本。

import os

class Uninstall3App(object):
    def __init__(self):
        self.device_name = ""
        self.package_name = []

    def get_devices_name(self):
        try:
            device_list = os.popen("adb devices").read().split("\n")
            for device in device_list:
                if "\t" in device:
                    self.device_name = device.split("\t")[0]
        except Exception as msg:
            print(msg)

    def get_3_app_packages_name(self):
        try:
            package_list = os.popen("adb -s {} shell pm list packages -3".format(self.device_name)).readlines()
            for package in package_list:
                self.package_name.append(package.split(":")[-1].replace("\n", ""))
        except Exception as msg:
            print(msg)

    def uninstall_3_app(self):
        for package in self.package_name:
            try:
                log_info = os.popen("adb -s {} uninstall {}".format(self.device_name, package)).read()
                content = log_info.replace("\n", "")
                if "Success" in content:
                    print("{}: {} uninstall {}!".format(self.device_name, package, content))
            except Exception as msg:
                print(msg)

if __name__ == '__main__':
    do_test = Uninstall3App()
    do_test.get_devices_name()
    do_test.get_3_app_packages_name()
    do_test.uninstall_3_app()

