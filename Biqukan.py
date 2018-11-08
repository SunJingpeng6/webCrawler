# email： sunjingpeng6@126.com
# time: 2018-11-08
import requests
from bs4 import BeautifulSoup
import os
from collections import OrderedDict

"""
类说明:下载《笔趣看》网小说: url:https://www.biqukan.com/
"""
class DownloadBiqukan():

    def __init__(self, url, max_chapter_num=3):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166', }
        # 所有小说的url
        self.novel_urls = []
        # 每一个小说不同章节的url，为一个有序字典
        self.download_urls = OrderedDict()
        # 获取所有小说的url
        self._get_url()
        # 每本下载的最大章节数
        self.max_chapter_num = max_chapter_num

    # 获取所有小说的url
    def _get_url(self):
        index_html = requests.get(self.url, headers = self.headers)
        index_html = BeautifulSoup(index_html.text, 'lxml')
        # print(index_html)
        novel_list = index_html.find('div', class_='up')
        novel_list = novel_list.find('div', class_='l bd')
        for child in novel_list.ul.children:
            if child != '\n':
                url_html = child.find('span', attrs={'class':'s2'})
                url = self.url + url_html.a.get('href')
                self.novel_urls.append(url)

    # 获取每一本小说不同章节的url，为一个有序字典
    def _get_charpters(self, url):
        target_html = requests.get(url, headers=self.headers)
        list_html = BeautifulSoup(target_html.text, 'lxml')
        chapters = list_html.find_all('div', class_='listmain')
        download_soup = BeautifulSoup(str(chapters), 'lxml')

        begin_flag = False
        # 小说的名字
        self.novel_name = str(download_soup.dl.dt.string).split("》")[0][1:]
        # 保存小说的文件名字
        self.file_name = self.novel_name + '.txt'
        flag_name = "《" + self.novel_name + "》" + "正文卷"
        for child in download_soup.dl.children:
            if child != '\n':
                if child.string == flag_name:
                    begin_flag = True
                if begin_flag == True and child.a != None:
                    url = self.url +  child.a.get('href')
                    self.download_urls[child.string] = url

    # 获取小说每一章节的内容， 返回每一章节的文本
    def _get_text(self, download_url):
        html = requests.get(download_url, headers=self.headers)
        texts_html = BeautifulSoup(html.text, 'lxml')
        text_html = texts_html.find_all(id='content', class_='showtxt')
        text_html = BeautifulSoup(str(text_html), 'lxml')
        text = ''
        # \xa0 替换乱码字符
        for each in text_html.div.text.replace('\xa0', ''):
            if each == 'h':
                continue
            elif  each == '\r':
                text += '\n'
            else:
                text += each
        return text

    # 在当前目录下保存 每一本小说
    def _download_each(self, url):
        with open(self.file_name, 'w') as f:
            index = 0
            for key, value in self.download_urls.items():
                text = self._get_text(value)
                f.write(str(key) + '\n')
                f.write(str(text))
                f.write('\n\n')
                index += 1
                if index > self.max_chapter_num: break

    # 下载所有小说
    def download(self):
        for i in range(len(self.novel_urls)):
            # 获取第i本小说不同章节的url，为一个有序字典
            self._get_charpters(self.novel_urls[i])
            # 在当前目录下 保存每一本小说
            self._download_each(self.novel_urls[i])
            print('第' + str(i+1) + '本小说: ' + str(self.novel_name) +'下载完成！')
            # 为保存下一本小说做准备
            self.download_urls = OrderedDict()

if __name__ == "__main__":
    url = 'http://www.biqukan.com'
    novel = DownloadBiqukan(url)
    novel.download()
