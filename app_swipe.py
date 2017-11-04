# Author: AdrianZhang
# Coding Time: 2017/11/03
# Script Function: 一个实现“获取手机屏幕分辨率、上滑、下滑、左滑、右滑”功能的脚本。

import os
import time


class AppSwipe(object):

    def get_screen_size(self):
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

    def swipe_up(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.5
        y_start = location[-1] * 0.75
        x_end = location[0] * 0.5
        y_end = location[-1] * 0.25
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))

    def swipe_down(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.5
        y_start = location[-1] * 0.25
        x_end = location[0] * 0.5
        y_end = location[-1] * 0.75
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))

    def swipe_left(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.75
        y_start = location[-1] * 0.5
        x_end = location[0] * 0.25
        y_end = location[-1] * 0.5
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))

    def swipe_right(self):
        location = self.get_screen_size()
        x_start = location[0] * 0.25
        y_start = location[-1] * 0.5
        x_end = location[0] * 0.75
        y_end = location[-1] * 0.5
        os.popen("adb shell input swipe {} {} {} {}".format(x_start, y_start, x_end, y_end))

if __name__ == '__main__':
    os.popen("adb shell am start -W -n com.qiyi.video/.WelcomeActivity")
    time.sleep(10)
    swipe = AppSwipe()
    swipe.get_screen_size()
    swipe.swipe_up()
    time.sleep(3)
    swipe.swipe_down()
    time.sleep(3)
    swipe.swipe_left()
    time.sleep(3)
    swipe.swipe_right()
    time.sleep(3)
    os.popen("adb shell am force-stop com.qiyi.video")

