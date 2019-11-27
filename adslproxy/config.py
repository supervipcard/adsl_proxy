# coding=utf-8
# 拨号间隔
ADSL_CYCLE = 30

# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 1

# ADSL命令
ADSL_BASH = 'pppoe-stop;pppoe-start'

# 代理账号
PROXY_USERNAME = 'xiangchen'

# 代理密码
PROXY_PASSWORD = 'pl1996317'

# 代理运行端口
PROXY_PORT = 3129

# 客户端唯一标识
CLIENT_NAME = 'adsl1'

# 拨号网卡
ADSL_IFNAME = 'ppp0'

# Redis数据库IP
REDIS_HOST = '101.132.71.2'

# Redis数据库密码, 如无则填None
REDIS_PASSWORD = 'pl1996317'

# Redis数据库端口
REDIS_PORT = 6379

# Redis数据库db
REDIS_DB = 1

# 代理池键名
REDIS_KEY = 'adsl'

# 测试URL
TEST_URL = 'https://www.weibo.com'

# 测试超时时间
TEST_TIMEOUT = 10
