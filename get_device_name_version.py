# Author: AdrianZhang
# Coding Time: 2017/11/19
# Script Function: 一个获取Android手机设备名称、系统版本号的脚本。

import os

def get_device_name():
    try:
        content = os.popen("adb devices").readlines()
        for each in content:
            if "\t" in each:
                device_name = each.split("\t")[0]
                return device_name
    except Exception as error:
        print(error)

def get_platform_version():
    try:
        content = os.popen("adb shell cat /system/build.prop").readlines()
        for each in content:
            if "version.release" in each:
                device_version = each.split("=")[-1].replace("\n", "")
                return device_version
    except Exception as error:
        print(error)

if __name__ == '__main__':
    device_name = get_device_name()
    device_version = get_platform_version()
    print("The device name is '{}', and device version is '{}'".format(device_name, device_version))

