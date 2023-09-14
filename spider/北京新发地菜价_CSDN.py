import requests
import csv
import time


class price_spider(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)         AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.131 Safari/537.36",
            "Referer": "http://www.xinfadi.com.cn/priceDetail.html",
            "Cookie": "SHOP_MANAGE=c5dbec72-aa12-49b1-8557-ba67bad6bbb6"}

        self.prodName = []
        self.lowPrice = []
        self.avgPrice = []
        self.highPrice = []
        self.specInfo = []
        self.place = []
        self.unitInfo = []
        self.pubDate = []
        self.session = requests.session()

    def get_response(self, url, data):
        response = self.session.post(url, data=data, headers=self.headers)
        dic = response.json()
        return dic

    def parse_data(self, dic):
        price_list = dic['list']
        for test in range(1, len(price_list)):
            info = price_list[test]
            # print(info)
            self.prodName.append(info.get('prodName'))
            self.lowPrice.append(info.get('lowPrice'))
            self.avgPrice.append(info.get('avgPrice'))
            self.highPrice.append(info.get('highPrice'))
            self.specInfo.append(info.get('specInfo'))
            self.place.append(info.get('place'))
            self.unitInfo.append(info.get('unitInfo'))
            self.pubDate.append(info.get('pubDate'))

    def save_data(self):
        rows = zip(self.prodName, self.lowPrice, self.avgPrice, self.highPrice, self.specInfo, self.place,
                   self.unitInfo, self.pubDate)
        with open('price.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["品名", "最低价", "平均价", "最高价", "规格", "产地", "单位", "发布日期"])
            for row in rows:
                writer.writerow(row)

    def run(self):
        start = time.time()
        base_url = 'http://www.xinfadi.com.cn/getPriceData.html'
        for i in range(1, 10):
            d = {"current": f"{i}"}
            dic = self.get_response(base_url, data=d)
            self.parse_data(dic)
        self.save_data()
        end = time.time()
        print('Running time: %s Seconds' % (end - start))
    # def threadPool_run(self):
    #     start = time.clock()
    #     with ThreadPoolExecutor(50) as t:
    #         t.submit(self.run())
    #     end = time.clock()
    #     print('Running time: %s Seconds' % (end - start))


price_spider().run()


