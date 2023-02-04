import requests
import csv

url = 'http://www.xinfadi.com.cn/getPriceData.html'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
    'Referer': 'http://www.xinfadi.com.cn/priceDetail.html'
}
data = {
    'current': 1,
    'limit': 20,
    'prodPcatid': 1187,
    'prodCatid': 1201
}
resp = requests.post(url, headers=header, data=data)
price_list = resp.json()['list']
prodName = []
lowPrice = []
avgPrice = []
highPrice = []
specInfo = []
place = []
unitInfo = []
pubDate = []
for i in range(1, len(price_list)):
    info = price_list[i]
    prodName.append(info.get('prodName'))
    lowPrice.append(info.get('lowPrice'))
    avgPrice.append(info.get('avgPrice'))
    highPrice.append(info.get('highPrice'))
    specInfo.append(info.get('specInfo'))
    place.append(info.get('place'))
    unitInfo.append(info.get('unitInfo'))
    pubDate.append(info.get('pubDate'))

with open('新发地菜价.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["品名", "最低价", "平均价", "最高价", "规格", "产地", "单位", "发布日期"])
    rows = zip(prodName, lowPrice, avgPrice, highPrice, specInfo, place, unitInfo, pubDate)
    for row in rows:
        writer.writerow(row)

print('all over!!!')