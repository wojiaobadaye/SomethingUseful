import csv
import requests
import json
import time
import pymysql
import pymongo
from random import uniform
from urllib.parse import unquote


class interShip:
    def __init__(self):
        self.headers = {
            'Host': 'jobs.bytedance.com',
            'Origin': 'https://jobs.bytedance.com',
            'Referer': 'https://jobs.bytedance.com/campus/position/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78'
        }
        self.token_data = {
            "portal_entrance":1
        }
        self.token_url = 'https://jobs.bytedance.com/api/v1/csrf/token'
        self.target_url = 'https://jobs.bytedance.com/api/v1/search/job/posts'
        self.session = requests.session()

    def get_cookie(self):
        """
        返回包含token的headers
        :return:
        """
        resp = self.session.post(self.token_url, headers=self.headers, data=self.token_data)
        cookie = self.session.cookies.get_dict()
        self.headers["x-csrf-token"] = unquote(cookie['atsx-csrf-token'])

    def get_data(self,data):
        """
        爬取一次数据，返回一个resp
        :param data: post请求参数
        :return: resp
        """
        resp = self.session.post(self.target_url, headers=self.headers, data=json.dumps(data))
        return resp

    def is_null(self, x):
        """
        处理 job_parent 字段
        :param x: 字典或者空值
        :return: x
        """
        if x is None:
            x = '无'
        else:
            x = x.get('name')
        return x

    def get_items(self,resp):
        """
        从响应中提取所需数据
        :param resp: requests.post(url, headers, data)
        :return: Items[list]
        """
        items = []
        for job in resp.json()['data']['job_post_list']:
            title = job.get('title')
            city = job['city_info'].get('name')
            job_parent = self.is_null(job['job_category']['parent'])
            job_type = job.get('job_category').get('name')
            recruit_type = job.get('recruit_type').get('name')
            requirement = job.get('requirement')
            description = job.get('description')
            hot_frag = job.get('job_hot_flag')

            job_item = [title, city, job_type, job_parent, hot_frag, recruit_type, requirement, description]
            items.append(job_item)
        return items

    def to_csv(self, items):
        with open('./data/job.csv', 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in items:
                writer.writerow(row)

    def to_musql(self, items):
        conn = pymysql.connect(host='212.64.23.2',
                                     user='inter',
                                     password='1234',
                                     database='intership',
                                     charset='utf8mb4',
                               )
        try:
            with conn.cursor() as cursor:
                # 创建一条新的记录
                sql = """INSERT INTO bytedance(title, city, job_type, job_parent, 
                hot_frag, recruit_type, requirements, descriptions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.executemany(sql, items)
            # 连接完数据库并不会自动提交，所以需要手动 commit 你的改动
            conn.commit()
        finally:
            conn.close()

    def get_newitems(self, items):
        """
        列表转字典（json）
        :param items: [[],[],...[]]
        :return: [{},{},...{}]
        """
        keys = ['title', 'city', 'job_type', 'job_parent',
                'hot_frag', 'recruit_type', 'requirement', 'description']
        new_itemlist = []
        for value in items:
            new_item = dict(zip(keys, value))
            new_itemlist.append(new_item)
        return new_itemlist

    def to_mongo(self, items):
        with pymongo.MongoClient("mongodb://inter:1234@212.64.23.2:27017/?"
                            "authMechanism=DEFAULT&authSource=intership") as client:
            db = client['intership']
            table = db['bytedance']
            table.insert_many(items)

    def logging(self):
        """
        随机时间爬取，防止被封ip
        """
        time.sleep(uniform(0.5,1.5))

    def run(self):
        try:
            self.get_cookie()
            for offset in range(0,691,10):
                data = {
                    "job_category_id_list": [],
                    "keyword": "数据分析",
                    "limit": 10,
                    "location_code_list": [],
                    "offset": offset,
                    "portal_entrance": 1,
                    "portal_type": 3,
                    "recruitment_id_list": ["202", "301"], # 实习岗位
                    "subject_id_list": []
                }
                job_list = self.get_items(self.get_data(data))

                # self.to_csv(job_list)
                self.to_musql(job_list)
                # self.to_mongo(self.get_newitems(job_list))

                print(f'第{int(offset/10+1)}页数据写入完成!')
                self.logging()
        finally:
            self.session.close()


inter = interShip()
inter.run()

# with open('result.json', 'w+', encoding='utf-8') as f:
#     json.dump(r_2.json()['data']['job_post_list'], f, ensure_ascii=False, indent=4)

