# Author: AdrianZhang
# Coding Time: 2017/10/29
# Script Function:
#   一个实现“查找本目录下的apk文件、设备连接、安装app、启动app、获取分辨率、
#   上滑、下滑、左滑、右滑、退出app、卸载app、断开设备连接”并可以自己设置执行次数的脚本。

import os
import time


class AppOperation(object):

    def get_apk_path(self):
        current_path = os.getcwd()              # 获取当前路径
        lists = os.listdir(current_path)        # 获得目录中的内容
        apk_lists = []
        for file in lists:
            if ".apk" in file:
                apk_lists.append(file)
        apk_lists.sort(key=lambda nf: os.path.getmtime(current_path + "\\" + nf))       # 重新按时间对目录下文件进行排序
        recent_apk = os.path.join(current_path, apk_lists[-1])                          # 把目录和文件名合成一个路径
        print("Get The Apk Path: {} Success!\n".format(recent_apk))
        return recent_apk

    def device_connect(self):
        device_connect_cmd = "adb connect {}".format(device_name)
        try:
            connect_log = os.popen(device_connect_cmd).read()
            if "connected to" in connect_log:
                return True
            else:
                return False
        except Exception as message:
            print(message)

    def install_app(self):
        install_app_cmd = "adb -s {} install {}".format(device_name, self.get_apk_path())
        device_status = self.device_connect()
        if device_status:
            try:
                install_app_log = os.popen(install_app_cmd).read()
                if "Success" in install_app_log:
                    print(install_app_log, end="")
                    print("Install {} Success!\n".format(self.get_apk_path()))
            except Exception as message:
                print(message)
        else:
            self.device_connect()

    def start_app(self):
        start_app_cmd = "adb shell am start -W -n {}".format(apk_package_activity)
        start_app_log = os.popen(start_app_cmd).read().replace("\n", ",")
        for log in start_app_log.split(",,"):
            print(log)

    def get_screen_size(self):
        try:
            displays_content = os.popen("adb shell dumpsys window displays").readlines()
            for displays_size in displays_content:
                if "cur=" in displays_size:
                    resolution = displays_size.split(" ")[6].split("=")[-1]
                    x_axis = int(resolution.split("x")[0])
                    y_axis = int(resolution.split("x")[-1])
                    print("The Screen Size is: {} x {}\n".format(x_axis, y_axis))
                    return x_axis, y_axis
                else:
                    try:
                        size_content = os.popen("adb shell wm size")
                        for wm_size in size_content:
                            if "Physical size:" in wm_size:
                                resolution = wm_size.split(": ")[-1]
                                x_size = int(resolution.split("x")[0])
                                y_size = int(resolution.split("x")[-1])
                                print("The Screen Size is: {} x {}\n".format(x_size, y_size))
                                return x_size, y_size
                    except Exception as error:
                        print(error)
        except Exception as error:
            print(error)

    def swipe_up(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.5
        y_start = location[-1] * 0.75
        x_end = location[0] * 0.5
        y_end = location[-1] * 0.25
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))
        print("Swipe Up Success!\n")

    def swipe_down(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.5
        y_start = location[-1] * 0.25
        x_end = location[0] * 0.5
        y_end = location[-1] * 0.75
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))
        print("Swipe Down Success!\n")

    def swipe_left(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.75
        y_start = location[-1] * 0.5
        x_end = location[0] * 0.25
        y_end = location[-1] * 0.5
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))
        print("Swipe Left Success!\n")

    def swipe_right(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.25
        y_start = location[-1] * 0.5
        x_end = location[0] * 0.75
        y_end = location[-1] * 0.5
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))
        print("Swipe Right Success!\n")

    def quit_app(self):
        quit_app_cmd = "adb shell am force-stop {}".format(apk_package_name)
        quit_app_log = os.popen(quit_app_cmd).read()
        if quit_app_log == "":
            print("Quit APP Success!\n")

    def uninstall_app(self):
        uninstall_app_cmd = "adb -s {} uninstall {}".format(device_name, apk_package_name)
        try:
            uninstall_app_log = os.popen(uninstall_app_cmd).read().replace("\n", "")
            if "Success" in uninstall_app_log:
                print("Uninstall {} {}!\n".format(apk_package_name, uninstall_app_log))
        except Exception as message:
            print(message)

    def device_disconnect(self):
        try:
            cmd = "adb disconnect {}".format(device_name)
            disconnect_log = os.popen(cmd).read()
            if "disconnected" in disconnect_log:
                print("Disconnect Device Success!\n")
        except Exception as error:
            print(error)


class TimesControl(object):
    def __init__(self, count):
        self.app_operation = AppOperation()
        self.initial = 1
        self.counter = count

    def single_test(self):
        # 开始
        print("{:^30}{:^25}{:^30}{}".format(">" * 30, "Start Test: " + str(self.initial), "<" * 30, "\n" * 1))
        time.sleep(1)
        # 获取脚本目录下的Apk文件
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Get Apk Path:", "=" * 30))
        self.app_operation.get_apk_path()
        # 连接设备
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Connect Device:", "=" * 30))
        print("{}\n".format(self.app_operation.device_connect()))
        # 安装APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Install APP:", "=" * 30))
        self.app_operation.install_app()
        # 启动APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Start App:", "=" * 30))
        self.app_operation.start_app()
        time.sleep(10)
        # 获取屏幕分辨率
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Get Screen Size:", "=" * 30))
        self.app_operation.get_screen_size()
        # 屏幕上滑
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Swipe Up:", "=" * 30))
        self.app_operation.swipe_up()
        time.sleep(3)
        # 屏幕下滑
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Swipe Down:", "=" * 30))
        self.app_operation.swipe_down()
        time.sleep(3)
        # 屏幕左滑
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Swipe Left:", "=" * 30))
        self.app_operation.swipe_left()
        time.sleep(3)
        # 屏幕右滑
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Swipe Right:", "=" * 30))
        self.app_operation.swipe_right()
        time.sleep(3)
        # 关闭APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Quit App:", "=" * 30))
        self.app_operation.quit_app()
        time.sleep(1)
        # 卸载APP
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Uninstall APP:", "=" * 30))
        self.app_operation.uninstall_app()
        # 断开设备连接
        print("{:^30}{:^25}{:^30}".format("=" * 30, "Disconnect Device:", "=" * 30))
        self.app_operation.device_disconnect()
        # 结束
        print("{:^30}{:^25}{:^30}{}".format(">" * 30, "End Test!", "<" * 30, "\n" * 5))

    def many_times_test(self):
        while self.initial <= self.counter:
            self.single_test()
            self.initial += 1

if __name__ == '__main__':
    device_name = "127.0.0.1:7555"
    apk_package_name = "com.qiyi.video"
    apk_package_activity = "com.qiyi.video/.WelcomeActivity"
    do_test = TimesControl(10)
    do_test.many_times_test()

