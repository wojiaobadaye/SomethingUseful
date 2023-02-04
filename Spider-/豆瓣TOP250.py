import requests
import re
import csv
# get page
url = "https://movie.douban.com/top250"
obj = re.compile(r'<li>.*?<span class="title">(?P<name>.*?)</span>.*?导演:(?P<director>.*?)&nbsp'
                 r'.*?<br>(?P<year>.*?)&nbsp.*?<span class="rating_num" property="v:average">'
                 r'(?P<score>.*?)</span>.*?<span>(?P<people>.*?)人评价</span>', re.S)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "Safari/537.36 Edg/108.0.1462.76 "
}

param = {
    'start': None,
    'filter': None
}

for i in range(0, 226, 25):
    param['start'] = i
    resp = requests.get(url, headers=header, params=param)
    result = obj.finditer(resp.text)

    f = open('Top_250_Movies.csv', mode="a+", encoding='utf-8', newline='')
    writer = csv.writer(f)
    for it in result:
        # print(i.group('name'))
        # print(i.group('year').strip())
        # print(i.group('director').strip())
        # print(i.group('score'))
        # print(i.group('people'))
        dic = it.groupdict()
        dic['year'] = dic['year'].strip()
        dic['director'] = dic['director'].strip()
        writer.writerow(dic.values())
    f.close()
    resp.close()
    print(f'Top {i+25} is over!')

print('All write finished!')