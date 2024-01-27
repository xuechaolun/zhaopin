import json
import os
import time
from typing import Iterable

import scrapy
from scrapy import Request


class TencentSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["careers.tencent.com"]

    headers = {
        "authority": "careers.tencent.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://careers.tencent.com/search.html",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def start_requests(self) -> Iterable[Request]:
        url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&pageIndex={}&pageSize=10"

        for page in range(102):
            yield Request(url=url.format(int(time.time() * 1000), str(page + 1)), headers=self.headers)

    def parse(self, response, **kwargs):
        # print(response.text)
        detail_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?&postId={}'
        ret = json.loads(response.body.decode('utf-8'))
        posts = ret['Data']['Posts']
        for post in posts:
            # print('post_url:', post['PostURL'])
            # print('post_id:', post['PostId'])
            yield Request(url=detail_url.format(post['PostId']), headers=self.headers, callback=self.detail_parse)

    def detail_parse(self, response, **kwargs):
        # print(response.text)
        data = json.loads(response.text).get('Data')
        yield {
            'recruit_post_name': data.get('RecruitPostName'),
            'category_name': data.get('CategoryName'),
            'product_name': data.get('ProductName'),
            'requirement': data.get('Requirement'),
            'responsibility': data.get('Responsibility'),
            'location_name': data.get('LocationName'),
            'last_update_time': data.get('LastUpdateTime'),
        }


if __name__ == '__main__':
    os.system('scrapy crawl tencent --nolog')
