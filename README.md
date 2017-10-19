# AppSpecialTest

# 本目录下的脚本，皆为Android APP的专项测试代码（样例皆以电视猫为参考）

# 【Android App“启动时间”监控】相关知识点：
# -----------------------------------------------------------------------------------------
# 1. 获取 package/activity 方式：
  adb logcat | grep START
# 2. 启动 app 应用：
  adb shell am start -W -n com.xxx.xxx/.xxxActivity
# 3. 停止（冷启动） app 应用：
  adb shell am force-stop com.xxx.xxx
# 4. 停止（热启动） app 应用：
  adb shell input keyevent 3     # keyevent 3为“返回键”
# -----------------------------------------------------------------------------------------

# 【】相关知识点：
