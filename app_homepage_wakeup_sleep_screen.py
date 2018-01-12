# Author: AdrianZhang
# Coding Time: 2018/01/12
# Script Function: App home page, wakeup screen and sleep screen.

import os
import time

def wakeup_sleep_screen(times):
    count = 0
    activity = 'com.snda.wifilocating/com.lantern.launcher.ui.MainActivity'
    os.popen('adb shell am start -W -n {}'.format(activity))
    time.sleep(5)
    adb_content = os.popen('adb shell dumpsys power | findstr "Display Power:"').readlines()
    for line in adb_content:
        if 'Display Power: state=' in line:
            screen_status = line.strip().split('=')[-1]

    if "OFF" in screen_status:
        while count < times:
            os.popen('adb shell input keyevent KEYCODE_POWER')
            time.sleep(3)
            os.popen('adb shell input swipe 504 1440 504 480')
            time.sleep(3)
            os.popen('adb shell input keyevent KEYCODE_POWER')
            time.sleep(3)
            count += 1

    else:
        while count < times:
            os.popen('adb shell input swipe 504 1440 504 480')
            time.sleep(3)
            os.popen('adb shell input keyevent KEYCODE_POWER')
            time.sleep(3)
            os.popen('adb shell input keyevent KEYCODE_POWER')
            time.sleep(3)
            count += 1

if __name__ == '__main__':
    times = 30
    wakeup_sleep_screen(times)

  
