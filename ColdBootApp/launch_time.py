# Author: AdrianZhang
# Coding Time: 2017/10/19
# Script Function: 执行App的启动、退出操作，生成log日志，并获取每一次App的启动耗时。

import os
import time


class RunningApp(object):
    def __init__(self):
        self.log_content = ""
        self.launch_time = 0

    def launch_app(self, activity):
        launch_cmd = "adb shell am start -W -n {}".format(activity)
        self.log_content = os.popen(launch_cmd).readlines()

    def quit_app(self, package):
        force_stop_cmd = "adb shell am force-stop {}".format(package)
        os.popen(force_stop_cmd)

    def get_launch_time(self):
        for log in self.log_content:
            if "ThisTime" in log:
                self.launch_time = log.split(":")[-1]
                return int(self.launch_time)


class Control(object):
    def __init__(self, count, app_activity, app_package):
        self.running_app = RunningApp()
        self.counter = count
        self.activity = app_activity
        self.package = app_package
        self.time_list = []

    def get_time_ymd(self):
        current_time_ymd = time.strftime("%Y-%m-%d", time.localtime())
        return current_time_ymd

    def get_time_hms(self):
        current_time_hms = time.strftime("%H:%M:%S", time.localtime())
        return current_time_hms

    def get_log(self):
        clear_cmd = "adb logcat -c"
        os.popen(clear_cmd)
        time.sleep(3)
        log_cmd = "adb logcat -v time > LaunchTimeLog.txt"
        os.popen(log_cmd)

    def single_test(self):
        system_time = self.get_time_hms()
        self.running_app.launch_app(self.activity)
        time.sleep(6)
        app_launch_time = self.running_app.get_launch_time()
        self.running_app.quit_app(self.package)
        time.sleep(5)
        self.time_list.append((system_time, app_launch_time))
        for i in range(len(self.time_list)):
            if self.time_list[i][1] is None:
                self.time_list.remove(self.time_list[i])
                self.counter += 1

    def many_times_test(self):
        while self.counter > 0:
            self.single_test()
            self.counter -= 1
        return self.time_list

