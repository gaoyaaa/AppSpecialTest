# Author: AdrianZhang
# Coding Time: 2017/11/29
# Script Function: 获取app的CPU占用率统计，并进行数据可视化。

import os
import csv
import time
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

def get_top_data(test_time):
    start_time = time.time()
    format_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    print("Start Time: {} = {}".format(start_time, format_start_time))
    end_time = start_time + float(test_time)
    format_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
    print("End Time: {} = {}".format(end_time, format_end_time))

    top_data_list = []
    while start_time <= end_time:
        top_data = os.popen('adb shell "top -n 1 -d 1 | grep com.snda.wifilocating"').read()
        split_top_data = top_data.strip().split('\n\n')
        for each in split_top_data:
            split_each = each.split()
            clean_each = ",".join(split_each)
            top_data_list.append(clean_each.split(','))
            start_time = start_time + float(1)
            print("-->Time is: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))
    return top_data_list

def format_data(top_data_list):
    formatted_data = [
        ["PID", "PR", "CPU%", "S", "#THR", "VSS", "RSS", "PCY", "UID", "Name"],
    ]

    for each in top_data_list:
        formatted_data.append(each)
    return formatted_data

def write_csv(formatted_data):
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    file = open("{}_top_data.csv".format(current_time), "w+", newline='')
    writer = csv.writer(file)
    for unit in formatted_data:
        writer.writerow(unit)
    file.close()

def get_recent_csv_path():
    current_path = os.getcwd()
    lists = os.listdir(current_path)
    csv_lists = []
    for file in lists:
        if ".csv" in file:
            csv_lists.append(file)
    csv_lists.sort(key=lambda nf: os.path.getmtime(current_path + "\\" + nf))
    recent_csv_path = os.path.join(current_path, csv_lists[-1])
    return recent_csv_path

def get_cpu_value(recent_csv_path):
    csv_name = recent_csv_path.split('\\')[-1]
    dirty_cpu_value = []
    cpu_value = []
    with open(csv_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            dirty_cpu_value.append(row[2].split('%')[0])

    for num in range(len(dirty_cpu_value)):
        if num % 2 == 1:
            cpu_value.append(int(dirty_cpu_value[num]))
    return cpu_value

def visualization(cpu_value):
    list_x = []
    list_y1 = cpu_value
    for num in range(1, len(cpu_value)+1):
        list_x.append(num)
    plt.plot(list_x, list_y1, color="blue", linestyle="-", label="CPU%")
    plt.plot(list_x, list_y1, 'ro')
    plt.legend(loc=0)    # 图例，0为最佳位置，即不覆盖数据
    plt.axis('tight')    # 使所有数据可见（缩小限值）

    list_y2 = []
    total_value = 0
    for value in cpu_value:
        total_value += value
    cpu_average_value = int(total_value / len(cpu_value))
    for member in range(len(cpu_value)):
        list_y2.append(cpu_average_value)
    plt.plot(list_x, list_y2, color="red", linestyle=":", label="Average Value")

    plt.legend()
    boundary = len(list_y1) + 1
    plt.xlim(0, boundary)
    plt.ylim(0, 100)
    plt.title("WiFi Key: CPU Utilization Percentage")
    plt.xlabel("Number")
    plt.ylabel("CPU%")
    plt.savefig("WiFi_Key_CPU.png")

if __name__ == '__main__':
    log = connect_device()
    print(log)
    test_time = 60    # 测试时间（单位：秒）
    top_data_list = get_top_data(test_time)
    format_data = format_data(top_data_list)
    write_csv(format_data)
    csv_path = get_recent_csv_path()
    cpu_value = get_cpu_value(csv_path)
    visualization(cpu_value)



