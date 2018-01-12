# Author: AdrianZhang
# Coding Time: 2017/11/28
# Script Function: 获取apk包的版本信息。

import os

def get_log(apk_package_name):
    log_content = os.popen("adb shell dumpsys package {}".format(apk_package_name)).read()
    return log_content

def get_apk_info(log_content):
    split_data = log_content.split('\n')
    apk_info = []
    for each in split_data:
        if 'pkg=' in each:
            pkg = each.strip().split(' ')[-1].split('}')[0]
            apk_info.append(pkg)
        if 'userId=' in each:
            user_id = each.strip().split(' ')[0]
            apk_info.append(user_id)
        if 'versionCode=' in each:
            version_code = each.strip().split(' ')[0]
            apk_info.append(version_code)
        if 'versionName=' in each:
            version_name = each.strip()
            apk_info.append(version_name)
    return apk_info

if __name__ == '__main__':
    apk_package_name = "com.snda.wifilocating"
    log_content = get_log(apk_package_name)
    apk_info = get_apk_info(log_content)
    print(apk_info)

