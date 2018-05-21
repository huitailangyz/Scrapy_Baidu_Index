# 接口 
>百度账号和密码：`openbrowser`函数中的 `account` 和 `passwd`

>关键词：`main.py` 中的 `key_word`

>起止时间：`main.py` 中的 `from_time` 和 `end_time`

# 方法
>使用 python + selenium 模拟网页操作，通过逐个月截取指数曲线，分别识别坐标轴数字和指数曲线，拟合得到每日的百度指数，精度较高

# 注意事项
>在 `get_value` 和 `get_axis` 函数中需要根据实际窗口大小调整 `top/width/height/left` 参数，可通过 `value.png` 以及 `axis*.png` 查看窗口大小调整效果

>测试时间为 `2018.5.21`，百度指数页面架构可能随时调整
