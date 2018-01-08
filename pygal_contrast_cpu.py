# Author: AdrianZhang
# Coding Time: 2018/01/03
# Script Function: contrast 'snda wifi' and 'tencent wifi' cpu usage rate .

import os
import time
import pygal

def get_screen_size():
    try:
        displays_content = os.popen("adb shell dumpsys window displays").readlines()
        for displays_size in displays_content:
            if "cur=" in displays_size:
                resolution = displays_size.split(" ")[6].split("=")[-1]
                x_axis = int(resolution.split("x")[0])
                y_axis = int(resolution.split("x")[-1])
                return x_axis, y_axis
            else:
                try:
                    size_content = os.popen("adb shell wm size")
                    for wm_size in size_content:
                        if "Physical size:" in wm_size:
                            resolution = wm_size.split(": ")[-1]
                            x_size = int(resolution.split("x")[0])
                            y_size = int(resolution.split("x")[-1])
                            return x_size, y_size
                except Exception as error:
                    print(error)
    except Exception as error:
        print(error)

def swipe_down():
    location = get_screen_size()
    x_start = location[0] * 0.5
    y_start = location[-1] * 0.25
    x_end = location[0] * 0.5
    y_end = location[-1] * 0.75
    os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))

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

def data_chart(snda_cpu_list, tencent_cpu_list, times):
    line_chart = pygal.Line()
    line_chart.title = 'Snda/Tencent App CPU Contrast Result (in %)'
    line_chart.x_labels = map(str, range(1, times+1))
    line_chart.add('Snda CPU (%)', snda_cpu_list)
    line_chart.add('Tencent CPU (%)', tencent_cpu_list)
    line_chart.render_to_file('pygal_contrast_cpu.svg')

def test_snda(count, times):
    package_name = 'com.snda.wifilocating'
    package_activity_name = 'com.snda.wifilocating/com.lantern.launcher.ui.MainActivity'
    snda_cpu_list = []
    os.popen('adb shell am start -W -n {}'.format(package_activity_name))
    time.sleep(2)
    while count < times:
        connect_button = 'adb shell input tap 135 1741'
        os.popen(connect_button)
        swipe_down()
        snda_cpu_percent = get_cpu(package_name)
        snda_cpu_list.append(float('%.2f' % float(snda_cpu_percent)))
        count += 1
    os.popen('adb shell am force-stop {}'.format(package_name))
    return snda_cpu_list

def test_tencent(count, times):
    package_name = 'com.tencent.wifimanager'
    package_activity_name = 'com.tencent.wifimanager/com.tencent.server.fore.QuickLoadActivity'
    tencent_cpu_list = []
    os.popen('adb shell am start -W -n {}'.format(package_activity_name))
    time.sleep(2)
    wifi_button = 'adb shell input tap 540 1743'
    os.popen(wifi_button)
    while count < times:
        swipe_down()
        tencent_cpu_percent = get_cpu(package_name)
        tencent_cpu_list.append(float('%.2f' % float(tencent_cpu_percent)))
        count += 1
    os.popen('adb shell am force-stop {}'.format(package_name))
    return tencent_cpu_list

def main():
    count = 0
    times = 60
    snda_cpu_list = test_snda(count, times)
    time.sleep(2)
    tencent_cpu_list = test_tencent(count, times)
    data_chart(snda_cpu_list, tencent_cpu_list, times)

if __name__ == '__main__':
    main()

