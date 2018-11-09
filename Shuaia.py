# 下载 帅啊网上的图片
# 2018-11-09
# sunjingpeng6@126.com
# Python 3.6.1 |Anaconda 4.4.0 (64-bit)| [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux
import requests
import os
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

class Shuaia():
    def __init__(self, max_num_page=3, file_folder_name='images'):
        # 图片所在页的url
        self.list_url = []
        # 下载的最大页数
        self.max_num_page = max_num_page
        # 保存文件夹的名字
        self.file_folder_name = file_folder_name
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" }
        self._get_url()

    # 获取每张图片所在网页的url
    def _get_url(self):
        for num_page in range(1, self.max_num_page):
            if num_page == 1:
                url = 'http://www.shuaia.net/index.html'
            else:
                url = 'http://www.shuaia.net/index_%d.html' %num_page
            req = requests.get(url, headers=self.headers)
            req.encoding = 'utf-8'
            html = BeautifulSoup(req.text, 'lxml')
            # 图片页的url的class为item-img
            target_url = html.find_all(class_='item-img')
            for each in target_url:
                # self.list_url = ['身材匀称的美女=http://www.shuaia.net/meinv/2018-10-10/16172.html', ... ,]
                self.list_url.append(each.img.get('alt') + '=' + each.get('href'))

    # 下载每一张图片
    # url 图片所在网页的url， filename 图片名称
    # 一个网页有多张图片， 用 图片名称_.jpg 图片名称_2.jpg 图片名称._3.jpg 区分
    def _download_each(self, url, filename):
        img_req = requests.get(url, headers=self.headers)
        img_req.encoding = 'utf-8'
        img_html = BeautifulSoup(img_req.text, 'lxml')
        img_html = img_html.find('div', class_='wr-single-content-list')
        img_urls = img_html.find_all('img')
        for i,url in enumerate(img_urls):
            img_url = url.get('src')
            # filename images/陈乔恩登台颁奖笑容_2.jpg
            img_filename = self.file_folder_name + '/' + filename + '_' + str(i+1) + '.jpg'
            # 保存图片
            urlretrieve(url=img_url, filename=img_filename)
            print("下载完图片：" + img_filename)
            time.sleep(1)

    def download(self):
        # 创建文件夹
        if self.file_folder_name not in os.listdir():
            os.makedirs(self.file_folder_name)
        # each_url '身材匀称，极具诱惑力的美女=http://www.shuaia.net/meinv/2018-10-10/16172.html'
        for each_url in self.list_url:
            filename, url = each_url.split('=')
            # 下载
            self._download_each(url, filename)
        return True

if __name__ == '__main__':
    # download website
    # url = 'http://www.shuaia.net/index.html'
    pic = Shuaia()
    # 在当前目录下 images/xx.jpg
    pic.download()
