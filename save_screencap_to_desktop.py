# Author: AdrianZhang
# Coding Time: 2017/11/28
# Script Function: get current phone screen and save to desktop

import os
import time

def connect_device():
    try:
        log = os.popen("adb kill-server && adb devices").read()
        return log
    except Exception as e:
        print(e)

def get_device_name(log):
    split_log = log.split('\n')
    for each in split_log:
        if '\t' in each:
            device_name = each.split('\t')[0]
            return device_name

def get_phone_image_path(device_name):
    if device_name:
        try:
            sdcard_folder = os.popen("adb shell ls /mnt/sdcard/").read()
            clean_sdcard_folder = sdcard_folder.strip().split('\n\n')
            if 'Pictures' in clean_sdcard_folder:
                pictures_folder = os.popen("adb shell ls /mnt/sdcard/Pictures/").read()
                clean_pictures_folder = pictures_folder.strip().split('\n\n')
                if 'Screenshots' in clean_pictures_folder:
                    screen_image_path = "/mnt/sdcard/Pictures/Screenshots/"
                    return screen_image_path
            else:
                os.popen("adb shell mkdir /mnt/sdcard/Pictures/")
                os.popen("adb shell mkdir /mnt/sdcard/Pictures/Screenshots/")
                screen_image_path = "/mnt/sdcard/Pictures/Screenshots/"
                return screen_image_path
        except Exception as e:
            print(e)

def get_pc_desktop_path():
    pc_desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    return pc_desktop_path

def screencap(screen_image_path):
    try:
        current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        os.popen("adb shell screencap -p {}{}.png".format(screen_image_path, current_time))
    except Exception as e:
        print(e)

def pull_to_desktop(screen_image_path, pc_desktop_path):
    try:
        info = os.popen("adb pull {} {}".format(screen_image_path, pc_desktop_path)).read()
        return info
    except Exception as e:
        print(e)


if __name__ == '__main__':
    log = connect_device()
    device_name = get_device_name(log)
    screen_image_path = get_phone_image_path(device_name)
    pc_desktop_path = get_pc_desktop_path()
    screencap(screen_image_path)
    pull_to_desktop(screen_image_path, pc_desktop_path)

