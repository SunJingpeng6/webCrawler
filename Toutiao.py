import requests
from urllib.parse import urlencode
import os
from hashlib import md5

# 爬取今日头条上关键字为 街拍 的图片
class Toutiao():

    def __init__(self, keyword='街拍', max_page=2):
        # max_page 爬取的最大页数
        self.max_page = max_page
        # 搜索的关键字
        self.keyword = keyword
        # 每张图片的title 和 url
        self.images = []
        base_url = 'https://www.toutiao.com/search_content/?'
        params = {
            'format': 'json',
            'keyword': self.keyword,
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
            'from': 'search_tab'
        }
        self.url = base_url + urlencode(params)

    # 获取每一页的Json数据
    def _get_page(self, offset):
        url = self.url + '&offset=' + str(offset)
        try:
            response = requests.get(url)
            if 200 == response.status_code:
                return response.json()
        except requests.ConnectionError:
            return None

    # 得到json数据中图片的url和title
    def _get_images(self, json):

        def image2target(image):
            # image   //p3-tt.bytecdn.cn/list/pgc-image/15300150331111dc5c695c9
            # target http://p3.pstatp.com/origin/pgc-image/15300150331111dc5c695c9
            image_parts = image.split('/')
            target_img = 'http://p3.pstatp.com/origin/pgc-image/' + image_parts[-1]
            return target_img

        if json.get('data'):
            data = json.get('data')
            for item in data:
                # 只对‘open_url’类型解析
                if item.get('open_url') is  None:
                    continue
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    img = {}
                    # 转化网址
                    target_img = image2target(image['url'])
                    img['image_url'] = target_img
                    img['title'] = title
                    self.images.append(img)

    # 保存图片
    def _save_image(self, image):
        # file holder path 文件夹名字
        img_path = 'img' + os.path.sep + image.get('title')
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        try:
            response = requests.get(image.get('image_url'))
            if 200 == response.status_code:
                # 文件名字
                file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(file_name=md5(response.content).hexdigest(), file_suffix='jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
        except requests.ConnectionError:
            print('Failed to Save Image，item %s' % item)

    # 下载一页的所有图片
    def _download_one_page(self, offset):
        # 获取json数据
        image_json = self._get_page(offset)
        # 获取图片的url
        self._get_images(image_json)
        # 下载
        for image in self.images:
            self._save_image(image)

    # 下载多页
    def download(self):
        for page in range(self.max_page):
            offset = page * 20
            self._download_one_page(offset)
            self.images = []
            print('第 %d 页保存完成，共%d页！' %(page+1, self.max_page))

if __name__ == "__main__":
    Jiepai = Toutiao(keyword='秋天美景')
    Jiepai.download()
