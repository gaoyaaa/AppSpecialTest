## AppSpecialTest  
`本目录下的脚本，皆为Android APP的专项测试代码。`  
  
#### 1. <Android APP 启动时间监控>相关知识点:  
* ##### 获取 package/activity 方式：
```adb logcat | grep START```  
* ##### 启动 app 应用：
```adb shell am start -W -n com.xxx.xxx/.xxxActivity```  
* ##### 停止（冷启动） app 应用：
```adb shell am force-stop com.xxx.xxx```  
* ##### 停止（热启动） app 应用：
```adb shell input keyevent 3     # keyevent 3为“按键Home”，等同于：adb shell input keyevent "KEYCODE_HOME"```  
  
#### 2. <Android App 内存监控>相关知识点：
* ##### xxx
