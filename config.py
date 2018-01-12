# coding:utf-8
# 图片路径
image_path = 'question.png'

http_port = '80'

server_host = ''

socket_port = '443'

server_host = 'free.ngrok.cc:16902' # '47.100.175.121'
# 从代理ip网站上总共要爬取的ip页数。一般每页20条，小项目(20-30个代理ip即可完成的)可以设置为1-2页。
page_num = 1

# 对已经检测成功的ip测试轮次。普通爬虫服务设置1轮足矣，若希望减少抓取数据缺失，可适当提高轮次，然而可能ip也将更少。
examine_round = 1

# 超时时间。代理ip在测试过程中的超时时间。
timeout = 0.6

database_name = 'ip_pool.db'

# 表名
TABLE_NAME = 'valid_ip'

# 数据库字符
charset = 'utf8'
