#Weather
##天气预报小脚本
=======

这是一个用于自动发送天气预报的小脚本
数据来源为www.weather.com.cn

##系统要求
	Python版本 >= 3.2 ( 暂时在3.2和3.3上测试过，可以使用 )

##配置文件weather.ini
    *Section info:
	email_from 这是配置邮件发送者显示的邮箱地址
	*Section emails:
	格式为:
	    [email1] = [cityid1]
		[email2] = [cityid1],[cityid2]...
	cityid的获取请看下面
##CityID如何获取
	访问www.weather.com.cn
	查看某地的天气，URL为http://www.weather.com.cn/weather/101210101.shtml
	大家可能已经猜到，后面那串数字就是CityID了
