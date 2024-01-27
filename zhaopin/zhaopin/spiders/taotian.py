import json
import os
import time
from typing import Iterable

import scrapy
from scrapy import Request


class TaoTianSpider(scrapy.Spider):
    name = "taotian"
    allowed_domains = ["talent.taotian.com"]

    # start_urls = ["https://talent.taotian.com"]
    def start_requests(self) -> Iterable[Request]:
        url = 'https://talent.taotian.com/position/search?_csrf=9023ad04-2b7f-420a-a39a-0813260f2cb9'
        headers = {
            "authority": "talent.taotian.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "bx-v": "2.2.3",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://talent.taotian.com",
            "pragma": "no-cache",
            "referer": "https://talent.taotian.com/off-campus/position-list?lang=zh&search=",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        cookies = {
            "XSRF-TOKEN": "9023ad04-2b7f-420a-a39a-0813260f2cb9",
            "SESSION": "MzBDMDlGNDYxMkQ1M0M2MTdGREQ5MUY3N0I3MjBEMTA=",
            "xlly_s": "1",
            "prefered-lang": "zh",
            "isg": "BDY2XHqzTzU8PjtW-UzmDj4jh2o4V3qR7MwEd6AeHJil49R9COTQo8PV-r-P-HKp"
        }
        for page in range(143):
            data = {
                "channel": "group_official_site",
                "language": "zh",
                "batchId": "",
                "categories": "",
                "deptCodes": [],
                "key": "",
                "pageIndex": page + 1,
                "pageSize": 10,
                "regions": "",
                "subCategories": "",
                "shareType": "",
                "shareId": "",
                "myReferralShareCode": ""
            }
            yield scrapy.http.JsonRequest(url=url, data=data, headers=headers, cookies=cookies)

    def parse(self, response):
        json_content = json.loads(response.text)
        datas = json_content['content']['datas']
        for data in datas:
            yield {
                'name': data.get('name'),
                'categories': data.get('categories'),
                'requirement': data.get('requirement'),
                'description': data.get('description'),
                'work_locations': data.get('workLocations'),
                'modify_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get('modifyTime') // 1000))
            }


if __name__ == '__main__':
    os.system('scrapy crawl taotian --nolog')
