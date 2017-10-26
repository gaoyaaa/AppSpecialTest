# Author: AdrianZhang
# Coding Time: 2017/10/25
# Script function: 一个实现“卸载多个Android手机中所有第三方包的脚本”。

import os

def get_devices_name():
    device_list = os.popen("adb devices").read().split("\n")
    devices = []
    for device in device_list:
        if "\t" in device:
            devices.append(device.split("\t")[0])
    return devices

def get_3_app_packages_name():
    package_list = os.popen("adb shell pm list packages -3").readlines()
    package_name = []
    for package in package_list:
        package_name.append(package.split(":")[-1].splitlines()[0])
    return package_name

def uninstall_3_app():
    device_name = get_devices_name()
    package_name = get_3_app_packages_name()
    for device in device_name:
        for package in package_name:
            try:
                content = os.popen("adb -s {} shell pm uninstall {}".format(device, package)).read().replace("\n", "")
                if "Success" in content:
                    print("{}: {} uninstall {}!".format(device, package, content))
                else:
                    print("{}: {} uninstall Fail! Details as Follows: {}".format(device, package, content))
            except Exception as msg:
                print(msg)

if __name__ == '__main__':
    uninstall_3_app()

