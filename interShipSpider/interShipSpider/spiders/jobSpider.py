import scrapy


class JobspiderSpider(scrapy.Spider):
    name = "jobSpider"
    allowed_domains = ["jobs.bytedance.com"]
    start_urls = ["http://jobs.bytedance.com/"]

    def parse(self, response):
        pass
