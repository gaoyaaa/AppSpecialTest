# Author: AdrianZhang
# Coding Time: 2017/12/11
# Script Function: This Script was written for "the management who looks like a dog", This script can "install app" and "uninstall app".
# Prompt: If you want to run this script, Your computer must be have "MonkeyRunner" environment first.

import time
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage


class AppTest(object):
    def __init__(self, apk_path, package_name, data_app_name):
        self.apk_path = apk_path
        self.package_name = package_name
        self.data_app_name = data_app_name
        self.device = MonkeyRunner.waitForConnection()

    def install_uninstall(self):
        self.device.installPackage(self.apk_path)
        MonkeyRunner.sleep(8)

        log_info = '/data/app/' + self.data_app_name + ': No such file or directory'

        install_result = self.device.shell('ls /data/app/' + self.data_app_name)
        if log_info in install_result:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  Install Test Failed !')
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  Install Test Passed !')

        self.device.removePackage(self.package_name)
        MonkeyRunner.sleep(5)

        uninstall_result = self.device.shell('ls /data/app/' + self.data_app_name)
        if log_info in uninstall_result:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  Uninstall Test Passed !\n')
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  Uninstall Test Failed !\n')


class Control(object):
    def __init__(self, count):
        self.app_test = AppTest(apk_path, package_name, data_app_name)
        self.initial = 1
        self.counter = count

    def single(self):
        self.app_test.install_uninstall()

    def many_times(self):
        while self.initial <= self.counter:
            print('Now, Test Times: ' + str(self.initial))
            self.single()
            self.initial += 1
        print('End...')

if __name__ == '__main__':
    apk_path = 'C:/Users/username/Desktop/app-debug.apk'
    package_name = 'com.geenk.zto.sys'
    data_app_name = 'com.geenk.zto.sys-1.apk'
    count = 10
    do_test = Control(count)
    do_test.many_times()

