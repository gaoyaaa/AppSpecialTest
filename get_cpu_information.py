# Author: AdrianZhang
# Coding Time: 2017/11/29
# Script Function: 获取app的CPU占用率统计，并进行数据可视化。

import os
import csv

def connect_device():
    try:
        log = os.popen("adb kill-server && adb devices").read()
        split_log = log.split('\n')
        for each in split_log:
            if '\t' in each:
                device_name = each.split('\t')[0]
                return "Device name is: {}".format(device_name)
    except Exception as e:
        print(e)

def get_once_cpu_data():
    cpu_data_list = []
    try:
        cpu_data = os.popen('adb shell "top -n 1 -d 1 | grep com.snda.wifilocating"').read()
        split_cpu_data = cpu_data.strip().split('\n\n')
        for each in split_cpu_data:
            split_each = each.split()
            clean_each = ",".join(split_each)
            cpu_data_list.append(clean_each.split(','))
        return cpu_data_list
    except Exception as e:
        print(e)

def format_data(cpu_data_list):
    """
    PID: 应用程序ID
    S: 进程状态(S:休眠; R:正在运行; Z:僵死状态; N:进程优先值为负数)
    #THR: 程序所用线程数
    VSS: 虚拟耗用内存
    RSS: 实际使用物理内存
    UID: 用户身份ID
    Name: 应用程序名称
    """
    formatted_data = [
        ["PID",
         "PR",
         "CPU%",
         "S",
         "#THR",
         "VSS",
         "RSS",
         "PCY",
         "UID",
         "Name"],
    ]

    for each in cpu_data_list:
        formatted_data.append(each)
    return formatted_data

def write_csv(formatted_data):
    file = open("result.csv", "w+", newline='')
    writer = csv.writer(file)
    for unit in formatted_data:
        writer.writerow(unit)
    file.close()

if __name__ == '__main__':
    log = connect_device()
    cpu_data_list = get_once_cpu_data()
    format_data = format_data(cpu_data_list)
    write_csv(format_data)

