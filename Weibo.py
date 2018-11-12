import requests
import json
import time
from pyquery import PyQuery as pq
from urllib.parse import urlencode

class Weibo():

    def __init__(self, max_page=10):
        self.max_page = max_page
        self.base_url = 'https://m.weibo.cn/api/container/getIndex?'
        # 保存微博信息
        self.weibos = []
        self.headers = {
            'Host': 'm.weibo.cn',
            'Referer': 'https://m.weibo.cn/u/2830678474',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like  Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    # 获取页面的json数据
    def _get_page(self, page):
        params = {
            'type': 'uid',
            'value': '2830678474',
            'containerid': '1076032830678474',
            'page': page+1
        }
        url = self.base_url + urlencode(params)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError as e:
            print('Error', e.args)

    # 解析json数据
    def _parse_page(self, json, page):
        if json:
            items = json.get('data').get('cards')
            for index, item in enumerate(items):
                if page == 0 and index == 1:
                    continue
                else:
                    item = item.get('mblog', {})
                    weibo = {}
                    weibo['id'] = item.get('id')
                    weibo['text'] = pq(item.get('text')).text()
                    weibo['attitudes'] = item.get('attitudes_count')
                    weibo['comments'] = item.get('comments_count')
                    weibo['reposts'] = item.get('reposts_count')
                    self.weibos.append(weibo)

    # 保存json数据到文件
    def _save_weibo(self):
        with open('weibo.json', 'a', encoding='utf-8') as f:
            for weibo in self.weibos:
                f.write(json.dumps(weibo, indent=2, ensure_ascii=False) + '\n')

    # 循环 保存 所有数据
    def save(self):
        for page in range(self.max_page):
            # 获取数据
            json = self._get_page(page)
            # 解析数据
            self._parse_page(json, page)
            # 保存
            self._save_weibo()
            # 为下一页做准备
            self.weibos = []
            time.sleep(1)
            print('第 %d 页保存完成，共%d页！' %(page+1, self.max_page))

if __name__ == '__main__':
    weibo = Weibo(max_page=5)
    weibo.save()
