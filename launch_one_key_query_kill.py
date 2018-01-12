# Author: AdrianZhang
# Coding Time: 2017/12/11
# Script Function: launch app and do 'one key query', then, kill app.

import time
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage


class AppTest(object):
    def __init__(self, package, activity, second, device_name):
        self.device = MonkeyRunner.waitForConnection()
        self.package = package
        self.activity = activity
        self.screen_advertising_time = second
        self.device_name = device_name
        self.connect_coordinate = 135, 1850
        self.one_key_query_coordinate = 540, 555

    def launch_app(self):
        run_component = self.package + '/' + self.activity
        self.device.startActivity(run_component)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "Begin to launch app.")

        MonkeyRunner.sleep(self.screen_advertising_time)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "Display 5 seconds launch page advertisement.")

    def touch_connect(self):
        MonkeyRunner.sleep(5)
        self.device.touch(self.connect_coordinate[0], self.connect_coordinate[1], MonkeyDevice.DOWN_AND_UP)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "Touch 'Connect' menu.")

    def touch_one_key_query(self):
        MonkeyRunner.sleep(3)
        self.device.touch(self.one_key_query_coordinate[0], self.one_key_query_coordinate[1], MonkeyDevice.DOWN_AND_UP)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "Touch 'One key query' button.")

    def kill_app(self):
        MonkeyRunner.sleep(3)
        self.device.shell('am force-stop ' + self.package)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "Force stop app.")
        print('\n')


class Control(object):
    def __init__(self, count, device_name):
        self.app_test = AppTest(package, activity, second, device_name)
        self.initialise = 1
        self.counter = count
        self.device_name = device_name

    def get_log(self):
        time_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        os.popen('adb logcat -v time > D:/' + self.device_name + '_' + time_name + '.txt')
        print('\n')
        print(">>> Grab log and save at D:/" + self.device_name + '_' + time_name + ".txt, please check it.")
        print('\n')

    def single(self):
        self.app_test.launch_app()
        self.app_test.touch_connect()
        self.app_test.touch_one_key_query()
        self.app_test.kill_app()

    def many_times(self):
        try:
            while self.initialise <= self.counter:
                print("> No. ", self.initialise)
                self.single()
                self.initialise += 1
        except:
            print('Error!!!')

        print("End...")

if __name__ == '__main__':
    package = 'com.snda.wifilocating'
    activity = 'com.lantern.launcher.ui.MainActivity'
    second = 5
    device_name = 'OPPO_A77'

    count = 10
    do_test = Control(count, device_name)
    do_test.get_log()
    do_test.many_times()

