DSD V 2.4.0 分析功能

# Dockerfile中已经配置了数据库地址，database, user, password, host, port

# 路由为 总路由"" + 子路由"api/v2/analysis"，

在Analysis_Predict/Analysis_Predict/urls.py 文件中配置总路由。

在Analysis_Predict/analysis/utils.py中配置数据库连接的ip地址和端口号。