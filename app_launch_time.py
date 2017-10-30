# Author: AdrianZhang
# Coding Time: 2017/10/19
# Script Function: 统计被测APP的启动时间，并进行数据可视化，作为参考。
# <以mumu模拟器作为测试机器，设备地址>:
#   (windows): adb connect 127.0.0.1:7555
#   (Mac)    : adb connect 127.0.0.1:5555

import os
import time
import matplotlib.pyplot as plt

class AppTest(object):
    def __init__(self):
        self.log_content = ""
        self.launch_time = 0

    def launch_app(self):
        launch_cmd = "adb shell am start -W -n {}".format(apk_package_activity_name)
        self.log_content = os.popen(launch_cmd).readlines()     # 返回一个list

    def quit_app(self):
        quit_cmd = "adb shell am force-stop {}".format(apk_package_name)
        # quit_cmd = "adb shell input keyevent 'KEYCODE_HOME'"
        os.popen(quit_cmd)

    def get_launch_time(self):
        for log in self.log_content:
            if "ThisTime" in log:
                self.launch_time = log.split(":")[-1]
                return int(self.launch_time)

class Control(object):
    def __init__(self, count):
        self.app_test = AppTest()
        self.initial = 1
        self.counter = count
        self.time_list = []

    def single_test(self):
        start_time = self.get_time_hms()
        self.app_test.launch_app()
        time.sleep(5)
        app_launch_time = self.app_test.get_launch_time()
        self.app_test.quit_app()
        time.sleep(5)
        end_time = self.get_time_hms()
        self.time_list.append((start_time, app_launch_time))

    def many_times_test(self):
        while self.initial <= self.counter:
            self.single_test()
            self.initial += 1

    def get_time_hms(self):
        current_time_hms = time.strftime("%H:%M:%S", time.localtime())
        return current_time_hms

    def get_time_ymd(self):
        current_time_ymd = time.strftime("%Y-%m-%d", time.localtime())
        return current_time_ymd

    def data_visualization(self):
        time_list = self.time_list
        x_test_time = []
        y_app_launch_time = []
        z_average_time = []
        z_total_time = 0
        for x in range(self.counter):
            x_test_time.append(time_list[x][0])

        for y in range(self.counter):
            y_app_launch_time.append(time_list[y][1])

        for z in range(self.counter):
            z_total_time += y_app_launch_time[z]
        average_time = int(z_total_time / self.counter)
        for num in range(self.counter):
            z_average_time.append(average_time)

        plt.figure(figsize=(10, 5))         # 设置比例：x轴为10， y轴为5
        plt.plot(y_app_launch_time, 'b', lw=1.5, label='result value')      # y轴，线宽为1.5个点的蓝色线条
        plt.plot(x_test_time, y_app_launch_time, 'ro')                      # 'r': 红色; 'o': 圆标记
        plt.plot(z_average_time, 'r', lw=1.5, label='average value')        # y轴，线宽为1.5个点的红色线条
        plt.plot(x_test_time, z_average_time, 'yo')                         # 'y': 黄色; 'o': 圆标记
        plt.xticks(x_test_time, rotation=0)             # 设置x轴文本显示角度，0为水平，90为逆时针旋转90°，以此类推
        plt.grid(True)                                  # 添加网格线
        plt.legend(loc=0)                               # 图例，0为最佳位置，即不覆盖数据
        plt.axis('tight')                               # 使所有数据可见（缩小限值）
        plt.title(self.get_time_ymd() + ' Test Result:')
        plt.xlabel('Time')
        plt.ylabel('Launch value')
        plt.savefig('app_launch_time_result.png')

if __name__ == '__main__':
    apk_package_activity_name = "com.qiyi.video/.WelcomeActivity"
    apk_package_name = "com.qiyi.video"
    control = Control(10)
    control.many_times_test()
    control.data_visualization()

