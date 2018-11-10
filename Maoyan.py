import json
import requests
from requests.exceptions import RequestException
import re, time
# 获取猫眼电影的信息
class Maoyan():

    def __init__(self, max_page=5):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; max_pageexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166', }
        self.films = []
        self.max_page = max_page

    # 获取每一页的html
    def _get_one_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None

    # 把页面上的电影信息保存到列表里
    def _parse_one_page(self, html):
        pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
        items = re.findall(pattern, html)
        for item in items:
            film = {}
            film['index'] = item[0]
            film['image'] = item[1]
            film['title'] = item[2],
            film['actor'] = item[3].strip()[3:]
            film['time'] = item[4].strip()[5:]
            film['score'] = item[5] + item[6]
            self.films.append(film)

    # self.film中的电影信息保存到文件中
    def _write_one_page(self):
        with open('result.text', 'a', encoding='utf-8') as f:
            for film in self.films:
                film_json = json.dumps(film, ensure_ascii=False)
                f.write(film_json + '\n')


    def write_file(self):
        for i in range(self.max_page):
            offset = i * 10
            # 每一页的url
            url = 'http://maoyan.com/board/4?offset=' + str(offset)
            # 获取 html
            html = self._get_one_page(url)
            # 获取电影信息
            self._parse_one_page(html)
            # 保存
            self._write_one_page()
            print('第 %d 页保存完成，共%d页！' %(i+1, self.max_page))
            # 为下一页做准备
            self.films = []
            time.sleep(1)

if __name__ == '__main__':
    film = Maoyan()
    film.write_file()
