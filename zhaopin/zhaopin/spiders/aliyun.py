import json
import os, time
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse, JsonRequest, FormRequest


class AliyunSpider(scrapy.Spider):
    name = "aliyun"
    allowed_domains = ["careers.aliyun.com"]

    def start_requests(self) -> Iterable[Request]:
        url = "https://careers.aliyun.com/position/search?_csrf=7d18cb4f-c74e-433f-a088-832fe4c4895a"
        headers = {
            "authority": "careers.aliyun.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "bx-v": "2.2.3",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://careers.aliyun.com",
            "pragma": "no-cache",
            "referer": "https://careers.aliyun.com/off-campus/position-list?lang=zh",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        }
        cookies = {
            "XSRF-TOKEN": "7d18cb4f-c74e-433f-a088-832fe4c4895a",
            "arms_uid": "7c4a6086-61df-4e22-bd4a-bc12917a39ed",
            "SESSION": "QzdCRDhFQjU2OTk2QkUwNTg0NURGOUQ5N0UxODI4RkU=",
            "isg": "BC8v-PCClhK0VJIpGHqkktGXvkU51IP2PX8taEG-Nx9vkEeSSacLRM4GE4Cu7ltu",
            "tfstk": "edvBSJNk0UpNshF352iwf2hVE36WAeMVJusJm3eU29BdPTtWlBSP83BSVe-QT_---U95WFAyaH3hFLtkcJ7dU97-FnYC8_-pzY_Jm9CkTa7FPTtklcuq3x-HxTf-uqkquG6QFTLpnEDexHXujlz-gCK3FmmCFiXIiYyrr3u_QR2JY80fLJTiQhsCOaeP58s6p-55kK_tkoaVf6NevNw8edsPT-7jajF7fs25fZosf7VlvehmkBVD5g5djM9qfcaLZ6IGfGmsf7Vl9GjaNci_J7f.."
        }
        for page in range(51):
            data = {
                "channel": "group_official_site",
                "language": "zh",
                "batchId": "",
                "categories": "",
                "deptCodes": [],
                "key": "",
                "pageIndex": page+1,
                "pageSize": 10,
                "regions": "",
                "subCategories": ""
            }
            yield JsonRequest(url=url, headers=headers, data=data, cookies=cookies)

    def parse(self, response, **kwargs):
        # print(response.text)
        json_content = json.loads(response.text)
        datas = json_content['content']['datas']
        for data in datas:
            yield {
                'name': data.get('name'),
                'categories': data.get('categories'),
                'requirement': data.get('requirement'),
                'description': data.get('description'),
                'work_locations': data.get('workLocations'),
                'modify_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get('modifyTime')//1000))
            }


if __name__ == '__main__':
    os.system('scrapy crawl aliyun --nolog')
