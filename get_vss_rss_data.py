# Author: AdrianZhang
# Coding Time: 2017/11/29
# Script Function: 获取app的CPU占用率统计，并进行数据可视化。

import os
import csv
import matplotlib.pyplot as plt

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

def get_once_top_data():
    top_data_list = []
    try:
        top_data = os.popen('adb shell "top -n 1 -d 1 | grep com.snda.wifilocating"').read()
        split_top_data = top_data.strip().split('\n\n')
        for each in split_top_data:
            split_each = each.split()
            clean_each = ",".join(split_each)
            top_data_list.append(clean_each.split(','))
        return top_data_list
    except Exception as e:
        print(e)

def format_data(top_data_list):
    formatted_data = [
        ["PID", "PR", "CPU%", "S", "#THR", "VSS", "RSS", "PCY", "UID", "Name"],
    ]

    for each in top_data_list:
        formatted_data.append(each)
    return formatted_data

def write_csv(formatted_data):
    file = open("result.csv", "w+", newline='')
    writer = csv.writer(file)
    for unit in formatted_data:
        writer.writerow(unit)
    file.close()

def get_vss():
    pass

def get_rss():
    pass

def visualization(vss_list, rss_list):
    list_x1 = [1, 5, 7, 9, 13, 16]
    list_y1 = [15, 50, 80, 40, 70, 50]
    plt.plot(list_x1, list_y1, color="blue", linestyle="-", label="Python")

    list_x2 = [2, 6, 8, 11, 14, 16]
    list_y2 = [10, 40, 30, 50, 80, 60]
    plt.plot(list_x2, list_y2, color="red", linestyle="--", label="Java")

    list_x3 = [3, 7, 9, 12, 15, 17]
    list_y3 = [12, 45, 35, 55, 85, 65]
    plt.plot(list_x3, list_y3, color="yellow", linestyle=":", label="Swift")

    plt.legend()
    plt.xlim(0, 20)
    plt.ylim(0, 100)
    plt.title("People's Like")
    plt.xlabel("Number")
    plt.ylabel("Times")
    plt.show()

if __name__ == '__main__':
    log = connect_device()
    cpu_data_list = get_once_cpu_data()
    format_data = format_data(cpu_data_list)
    write_csv(format_data)

    play = visualization()
    print(play)

