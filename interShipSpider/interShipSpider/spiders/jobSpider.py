import scrapy
from scrapy import Selector


class JobspiderSpider(scrapy.Spider):
    name = "jobSpider"
    # allowed_domains = ["jobs.bytedance.com"]
    start_urls = ["https://jobs.bytedance.com/campus/position/"]

    def parse(self, response, **kwargs):
        sel = Selector(response)
        as_list = sel.xpath('//*[@id="bd"]/section/section/main/div/div/div[2]/div[3]/div[1]/div[2]/a')
        for a in as_list:

            job_name = a.xpath('./div/div[1]/span/text()').get()
            work_address = a.xpath('./div/div[2]/span/text()').get()
            job_content = a.xpath('./div/div[3]/text()').get()
            print(job_name,work_address,job_content)
            break

