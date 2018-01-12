# waitting for write...
#
#

import os
import time
import pygal

def get_total_memory():
    lines = os.popen('adb shell cat /proc/meminfo').readlines()
    for line in lines:
        if 'MemTotal' in line:
            memory = line.split(' ')[-2]
            return memory

def get_total_pss(package_name):
    lines = os.popen('adb shell dumpsys meminfo {}'.format(package_name)).readlines()
    for line in lines:
        if "TOTAL" in line and "TOTAL:" not in line:
            line = line.strip().split(' ')
            while '' in line:
                line.remove('')
            pss_value = line[1]
            return pss_value

def get_cpu(package_name):
    lines = os.popen('adb shell "top -n 1 -d 1 | grep {}"'.format(package_name)).readlines()
    for line in lines:
        if 'push' not in line:
            line = line.strip().split(' ')
            while '' in line:
                line.remove('')
            for item in line:
                if "%" in item:
                    cpu_value = item.split('%')[0]
                    return cpu_value

def data_chart(wifi_pss_list, wifi_cpu_list, tencent_pss_list, tencent_cpu_list, times):
    line_chart = pygal.Line()
    line_chart.title = 'WiFi Key / Tencent Pss and CPU chart (in %)'
    line_chart.x_labels = map(str, range(1, times+1))
    line_chart.add('WiFi Pss', wifi_pss_list)
    line_chart.add('WiFi CPU', wifi_cpu_list)
    line_chart.add('Tencent Pss', tencent_pss_list)
    line_chart.add('Tencent CPU', tencent_cpu_list)
    line_chart.render_to_file('pss_cpu_chart.svg')

if __name__ == '__main__':
    package_name = ['com.snda.wifilocating', 'com.tencent.wifimanager']
    total_memory = get_total_memory()
    times = 10

    wifi_pss_list = []
    wifi_cpu_list = []
    tencent_pss_list = []
    tencent_cpu_list = []
    for num in range(1, times+1):
        print(num, '-->', time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
        for pkg in range(len(package_name)):
            pss_value = get_total_pss(package_name[pkg])
            cpu_percent = get_cpu(package_name[pkg])
            pss_mem_percent = float(pss_value) / float(total_memory) * 100
            wifi_pss_list.append(float('%.2f' % pss_mem_percent))
            wifi_cpu_list.append(float('%.2f' % float(cpu_percent)))
            tencent_pss_list.append(float('%.2f' % pss_mem_percent))
            tencent_cpu_list.append(float('%.2f' % float(cpu_percent)))

    print('WiFi Pss list: ', wifi_pss_list)
    print('WiFi CPU list: ', wifi_cpu_list)
    print('Tencent Pss list: ', tencent_pss_list)
    print('Tencent CPU list: ', tencent_cpu_list)
    data_chart(wifi_pss_list, wifi_cpu_list, tencent_pss_list, tencent_cpu_list, times)


