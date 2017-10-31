# Author: AdrianZhang
# Coding Time: 2017/10/19
# Script Function: 统计被测APP的“冷启动”时间，并对启动耗时进行数据可视化。

import os
import time
import matplotlib.pyplot as plt

class AppTest(object):
    def __init__(self):
        self.log_content = ""
        self.launch_time = 0

    def launch_app(self, activity):
        launch_cmd = "adb shell am start -W -n {}".format(activity)
        self.log_content = os.popen(launch_cmd).readlines()     # 返回一个list

    def quit_app(self, package):
        force_stop_cmd = "adb shell am force-stop {}".format(package)
        os.popen(force_stop_cmd)

    def get_launch_time(self):
        for log in self.log_content:
            if "ThisTime" in log:
                self.launch_time = log.split(":")[-1]
                return int(self.launch_time)

class Control(object):
    def __init__(self, count, apk_activity, apk_package):
        self.app_test = AppTest()
        self.activity = apk_activity
        self.package = apk_package
        self.initial = 1
        self.counter = count
        self.time_list = []

    def single_test(self):
        system_time = self.get_time_hms()
        self.app_test.launch_app(self.activity)
        time.sleep(5)
        app_launch_time = self.app_test.get_launch_time()
        self.app_test.quit_app(self.package)
        time.sleep(5)
        self.time_list.append((system_time, app_launch_time))

    def many_times_test(self):
        while self.initial <= self.counter:
            self.single_test()
            self.initial += 1

    def get_time_ymd(self):
        current_time_ymd = time.strftime("%Y-%m-%d", time.localtime())
        return current_time_ymd

    def get_time_hms(self):
        current_time_hms = time.strftime("%H:%M:%S", time.localtime())
        return current_time_hms

    def data_visualization(self):
        time_list = self.time_list
        x_system_time = []
        y_app_launch_time = []
        z_average_time = []
        z_total_time = 0
        for x in range(self.counter):                   # 提取每一次启动APP时的系统时间
            x_system_time.append(time_list[x][0])

        for y in range(self.counter):                   # 提取每一次APP启动的耗时
            y_app_launch_time.append(time_list[y][1])

        for z in range(self.counter):                   # 累加每一次APP启动耗时
            z_total_time += y_app_launch_time[z]

        average_time = int(z_total_time / self.counter)     # APP启动的平均耗时
        for num in range(self.counter):
            z_average_time.append(average_time)

        plt.figure(figsize=(25, 10))         # 设置图的范围
        plt.plot(y_app_launch_time, 'b', linewidth=1.5, label='Actual Value')      # y轴，线宽为1.5个点的蓝色线条
        plt.plot(x_system_time, y_app_launch_time, 'ro')                      # 'r': 红色; 'o': 圆标记
        plt.plot(z_average_time, 'r', linewidth=1.5, label='Average Value')        # y轴，线宽为1.5个点的红色线条
        plt.plot(x_system_time, z_average_time, 'yo')                         # 'y': 黄色; 'o': 圆标记
        plt.xticks(x_system_time, rotation=270)             # 设置x轴文本显示角度，0为水平，90为逆时针旋转90°，以此类推

        # tidy up the figure
        plt.grid(True)                                  # 添加网格线
        plt.legend(loc=0)                               # 图例，0为最佳位置，即不覆盖数据
        plt.axis('tight')                               # 使所有数据可见（缩小限值）
        plt.title('{} Total "{} Times" Cold Boot App Launch Time Test Result:'.format(self.get_time_ymd(), self.counter))
        plt.xlabel('System Time(Hours:minutes:seconds)')
        plt.ylabel('App Launch Time Value(Milliseconds)')
        plt.savefig('{}_ColdBootAppLaunchTimeTestResult.png'.format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())))

if __name__ == '__main__':
    apk_activity = "com.qiyi.video/.WelcomeActivity"
    apk_package = "com.qiyi.video"
    count = 30
    control = Control(count, apk_activity, apk_package)
    control.many_times_test()
    control.data_visualization()
