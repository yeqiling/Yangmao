### 一、zk_monitor.py
zk论坛关键字监控，实时邮箱提醒

1. 邮箱配置

    发送者邮箱账号开启客户端授权码，更安全！！   
    接收者邮箱账号添加发送者进白名单，重要！！

2. 脚本配置
    ```
    # 监控关键字
    KEYWORD = {
        'include': '密令|红包|水|速度|神券|京豆',
        'exclude': '权限|水贴'
    }
    # 发送者
    SENDER = {
        'name': '小分队',
        'email': 'youremail@126.com',
        'smtp': 'smtp.126.com',
        'pass': 'yourpass'
    }
    # 接收者
    RECEIVERS = [
        {
            'name': 'username',
            'email': 'youremail@126.com',
        }
    ]
    ```

3. 脚本使用

    Windows平台：使用前提pip install pyquery，可以配合系统计划任务执行脚本，要求Python3.5   
    无服务云函数：免费运行资源，打包zip部署至云环境，打包步骤请看[这里](https://cloud.tencent.com/document/product/583/9702)，要求Python3.6


### 二、zk_monitor_wx.py
zk论坛关键字监控，实时机器人提醒

1. 脚本使用

    运行python zk_monitor_wx.py，微信扫描二维码登陆

### 三、懒人微信群
1. 有机器人实时发布监控消息   
![微信群](http://wx3.sinaimg.cn/bmiddle/800facaagy1fxv0rzfsh3j20q0114mzp.jpg)

2. 微信群已满100人，可以加 **我是机器人** 拉你们进群  
![我是机器人](http://wx3.sinaimg.cn/bmiddle/800facaagy1fy30smg9hrj20q00zkq5c.jpg)
