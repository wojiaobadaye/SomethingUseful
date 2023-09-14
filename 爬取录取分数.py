import requests
from lxml import etree
import re
# 1 下载解析网页
target_url = "https://yjsy.swupl.edu.cn/zsgl/qrzssszlxx/index.html"
resp = requests.get(target_url)
resp.encoding='utf-8'
html = etree.HTML(resp.text)
li_list = html.xpath('/html/body/div[2]/article/section/div/div[2]/ul/li')

for li in li_list:
    year_month = li.xpath('./a/div[1]/span/text()')
    day = li.xpath('./a/div[1]/em/text()')
    text = li.xpath('./a/div[2]/text()')
    date = '.'.join(year_month+day)
    print(date)
# 2 对比信息
# 3 如果满足条件，则发送消息给我，
# 4 设置定时

# 发送消息
# key = 'PDU20716TZ4QHUXWH12stzo90lAJu97MIRRisiINQ'
# my_url = "https://api2.pushdeer.com/message/push?"
# param = {
#     "pushkey": key,
#     "text": "要发送的内容"
# }
# resp = requests.get(my_url, params=param)

