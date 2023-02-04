import requests
import re
import csv
# 1.从主页面提取子页面
# 2.从子页面提取子页面链接
# 3.从新的链接页面提取名字和下载链接

domain = 'https://dy.dytt8.net/html/gndy/jddy/20160320/50523.html'
# 请求头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                  'Safari/537.36 Edg/108.0.1462.76 '
}
# 提取子页面的 re模块
obj1 = re.compile(r'更新至: <strong>(?P<update_time>.*?)</strong></font></p>'
                  r'.*?<p><br />(?P<ul>.*?)<p><br />187', re.S)
# 提取子链接的 re模块
obj2 = re.compile(r'<a href="(?P<child_href>.*?)">', re.S)
# 提取电影名，年份，磁力链接
obj3 = re.compile(r'◎译　　名(?P<movie_name>.*?)/.*?◎年　　代(?P<year>.*?)<br />'
                  r'.*?magnet:(?P<download>.*?)">', re.S)

# 实现目标1
resp = requests.get(domain, headers=header)
resp.encoding = 'gb2312'
result1 = obj1.search(resp.text)
update_time = result1.group('update_time')
ul = result1.group('ul')
resp.close()
# 实现目标2
result2 = obj2.finditer(ul)
child_href_list = []
for j in result2:
    child_href_list.append(j.group('child_href'))

# 测试前50个
child_href_list = child_href_list[0:50]

# 实现目标3
f = open('IMDB8分以上电影下载地址.csv', 'a+', encoding='utf-8', newline='')
# 构造写入器
writer = csv.writer(f)
# 写入更新时间
writer.writerow([f"更新时间: {update_time}"])
error_times = 0 # 用于计算失败次数
repeat_time = 0 # 用于计算重复次数
name_verify = [] # 用于验证是否重复

try:
    for href in child_href_list:
        try:
            child_resp = requests.get(href, headers=header, verify=False)
            child_resp.encoding = 'gb2312'
            result3 = obj3.search(child_resp.text)
            # 使用re 模块提取信息
            dic = result3.groupdict()
            dic['movie_name'] = dic['movie_name'].strip()
            # 验证是否之前提取过同名电影，如果否，写入csv；如果是，跳过。
            if dic['movie_name'] not in name_verify:
                name_verify.append(dic['movie_name'])
                dic['year'] = dic['year'].strip()
                dic['download'] = 'magnet:' + dic['download'].strip()
                writer.writerow(dic.values())
                child_resp.close()
                print(dic['movie_name'], 'get!')
            else:
                child_resp.close()
                repeat_time += 1
                print(dic['movie_name'], 'already got!')
        # 排除 re 模块找不到信息导致的NoneType 错误
        except AttributeError:
            error_times += 1
            continue
        # 排除 请求不稳定导致的“远程客户端强行关闭了一个链接”错误。
        except requests.exceptions.ProxyError:
            error_times += 1
            continue
finally:
    f.close()

print(f'All over! and {repeat_time} repeated! and {error_times} filed!')