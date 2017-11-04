ColdBootApp文件夹下的脚本，是为了测试App启动耗时，并将耗时统计分析形成坐标图，然后汇总形成测试报告并自动发送至指定的邮箱。  
使用前，请先阅读以下注意点：  
1. launch_time.py，data_processing.py，send_mail.py，test_main.py必须在同一个目录下；  
2. 电脑已配置好Python3.x开发环境，已安装Matplotlib库（安装方法：pip install matplotlib）；  
3. 本人在自己的环境中，脚本测试通过。（以“mumu模拟器”作为测试机器，“爱奇艺”作为测试app）；  
mumu模拟器设备地址:  
(windows): adb connect 127.0.0.1:7555  
(Mac)    : adb connect 127.0.0.1:5555  
