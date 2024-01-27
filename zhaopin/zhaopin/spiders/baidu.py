import os
import json
import scrapy
from scrapy.http import Request, FormRequest, JsonRequest, Response
from typing import Iterable


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["talent.baidu.com"]
    start_urls = ["https://talent.baidu.com"]

    def start_requests(self) -> Iterable[Request]:
        for page in range(148):
            url = 'https://talent.baidu.com/httservice/getPostListNew'
            data = {
                "recruitType": "SOCIAL",
                "pageSize": "10",
                "keyWord": "",
                "curPage": str(page + 1),
                "projectType": ""
            }
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://talent.baidu.com",
                "Pragma": "no-cache",
                "Referer": "https://talent.baidu.com/jobs/social-list",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0.0.0 Safari/537.36",
                "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\""
            }
            yield FormRequest(url=url, formdata=data, headers=headers)

    def parse(self, response: Response, **kwargs):
        # print(type(response.text))
        # print(response.headers)
        res_dict = json.loads(response.text)
        job_list = res_dict['data']['list']
        for job in job_list:
            yield {
                'name': job.get('name'),
                'type': job.get('postType'),
                'serviceCondition': job.get('serviceCondition'),
                'workContent': job.get('workContent'),
                'workPlace': job.get('workPlace'),
                'updateDate': job.get('updateDate')
            }


if __name__ == '__main__':
    os.system('scrapy crawl baidu --nolog')
