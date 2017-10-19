# Author: AdrianZhang
# Script function: 统计被测APP的启动时间，作为参考。
# Coding Time: 2017/10/19

import time
import os
import re
import csv

class AppTest(object):
    def __init__(self):
        self.log_content = ""
        self.launch_time = 0

    def launch(self):
        launch_cmd = "adb shell am start -W -n com.moretv.android/.testActivity"
        self.log_content = os.popen(launch_cmd)

    def quit(self):
        quit_cmd = "adb shell am force-stop com.moretv.android/.testActivity"       # 停止APP，作为冷启动APP测试用。
        # quit_cmd = "adb shell input keyevent 'KEYCODE_HOME'"                      # 退出APP，作为热启动APP测试用。
        os.popen(quit_cmd)

    def get_launch_time(self):
        r = re.split("\n", self.log_content)
        for element in r:
            if "ThisTime" in element:
                self.launch_time = element.split(":")[1].replace(" ", "")
                break
        return self.launch_time         # 返回的"self.launch_time"类型为：<class 'str'>

class Control(object):
    def __init__(self, count):
        self.app_test = AppTest()
        self.count = count
        self.test_time = [("CurrentTime", "ConsumeTime")]

    def single_test(self):
        self.app_test.launch()
        time.sleep(3)
        consume_time = self.app_test.get_launch_time()
        self.app_test.quit()
        time.sleep(3)
        current_time = self.get_time()
        self.test_time.append((current_time, consume_time))

    def many_times_test(self):
        if self.count > 0:
            self.single_test()
            self.count -= 1

    def data_save(self):
        csv_file = open("E:\\LaunchTime.csv", "w")              # 数据文件保存在E盘（根据自己电脑修改）
        write_data = csv.writer(csv_file)
        write_data.writerows(self.test_time)
        csv_file.close()

    def get_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time

if __name__ == '__main__':
    control = Control(10)               # 执行10次测试（根据自己需求而修改数值）
    control.many_times_test()
    control.data_save()

