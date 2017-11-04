# Author: AdrianZhang
# Coding Time: 2017/10/19
# Script Function: 绘制App启动耗时的坐标图，返回关键测试数据、坐标图地址、log文件地址。

import os
import time
import matplotlib.pyplot as plt


class DataProcessing(object):
    def __init__(self, count, app_version, time_list):
        self.counter = count
        self.app_version = app_version
        self.time_list = time_list
        self.x_system_time = []
        self.y_app_launch_time = []
        self.z_average_time = []
        self.average_time = 0

    def get_data_visualization_image(self):
        z_total_time = 0
        for x in range(self.counter):                            # 提取每一次启动APP时的系统时间
            self.x_system_time.append(self.time_list[x][0])
        for y in range(self.counter):                            # 提取每一次APP启动的耗时
            self.y_app_launch_time.append(self.time_list[y][1])
        for z in range(self.counter):                            # 累加每一次APP启动耗时
            z_total_time += self.y_app_launch_time[z]
        self.average_time = int(z_total_time / self.counter)     # APP启动的平均耗时
        for num in range(self.counter):
            self.z_average_time.append(self.average_time)
        # 图形绘制
        plt.figure(figsize=(20, 10))                                              # 设置比例：x轴为20， y轴为10
        plt.plot(self.y_app_launch_time, 'b', linewidth=1.5, label='Actual Value')     # y轴，线宽为1.5个点的蓝色线条
        plt.plot(self.x_system_time, self.y_app_launch_time, 'ro')                          # 'r': 红色; 'o': 圆标记
        plt.plot(self.z_average_time, 'r', linewidth=1.5, label='Average Value')       # y轴，线宽为1.5个点的红色线条
        plt.plot(self.x_system_time, self.z_average_time, 'yo')                             # 'y': 黄色; 'o': 圆标记
        plt.xticks(self.x_system_time, rotation=270)             # 设置x轴文本显示角度，0为水平，90为逆时针旋转90°，以此类推
        plt.grid(True)                        # 添加网格线
        plt.legend(loc=0)                     # 图例，0为最佳位置，即不覆盖数据
        plt.axis('tight')                     # 使所有数据可见（缩小限值）
        plt.title('{} Version "{} Times" Cold Boot App Launch Time Image ({})'.format(self.app_version, self.counter,
                                                                                      time.strftime("%Y-%m-%d", time.localtime())))
        plt.xlabel('System Time (Hours:minutes:seconds)')
        plt.ylabel('App Launch Time Value (Milliseconds)')
        plt.savefig('ColdBootAppLaunchTimeImage.png')

    def get_data_report(self):
        data_result = []
        self.y_app_launch_time.sort()
        min_time = self.y_app_launch_time[0]
        max_time = self.y_app_launch_time[-1]
        above_average_time_count = 0
        under_average_time_count = 0
        for time_value in self.y_app_launch_time:
            if time_value > self.average_time:
                above_average_time_count += 1
            else:
                under_average_time_count += 1
        data_result.insert(0, self.average_time)
        data_result.insert(1, min_time)
        data_result.insert(2, max_time)
        data_result.insert(3, self.counter)
        data_result.insert(4, under_average_time_count)
        data_result.insert(5, above_average_time_count)
        return data_result

    def get_recent_image_path(self):
        current_path = os.getcwd()              # 获取当前路径
        lists = os.listdir(current_path)        # 获得目录中的内容
        image_lists = []
        for file in lists:
            if ".png" in file:
                image_lists.append(file)
        image_lists.sort(key=lambda nf: os.path.getmtime(current_path + "\\" + nf))     # 重新按时间对目录下文件进行排序
        recent_image = os.path.join(current_path, image_lists[-1])                         # 把目录和文件名合成一个路径
        return recent_image

    def get_recent_log_path(self):
        current_path = os.getcwd()              # 获取当前路径
        lists = os.listdir(current_path)        # 获得目录中的内容
        txt_lists = []
        for file in lists:
            if ".txt" in file:
                txt_lists.append(file)
        txt_lists.sort(key=lambda nf: os.path.getmtime(current_path + "\\" + nf))       # 重新按时间对目录下文件进行排序
        recent_txt = os.path.join(current_path, txt_lists[-1])                             # 把目录和文件名合成一个路径
        return recent_txt

