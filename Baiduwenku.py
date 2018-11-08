# email： sunjingpeng6@126.com
# time: 2018-11-08
from selenium import webdriver
import re

# 百度文库爬取文章
class BaiduWenku():
    def __init__(self, url):
        # 请求头
        options = webdriver.ChromeOptions()
        options.add_argument('User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)')
        self.url = url
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.url)
        # 等文章加载完毕
        self.driver.implicitly_wait(15)
        # page_count 文章的页数
        self.page_count = int(self.driver.find_element_by_xpath('/html/body/div[18]/div/div/div[2]/div[1]/div/span').text[1:])
        # title 文章标题
        self.title = str(self.driver.find_element_by_xpath('//*[@id="doc-tittle-0"]').text)
        # file 保存时的文件名
        self.file = self.title + '.txt'
        # 初始化每一页的内容
        self.text = ''
        # 执行JavaScipt 等价 点击 ‘阅读更多’
        js = 'document.getElementsByClassName("moreBtn goBtn")[0].click();'
        self.driver.execute_script(js)
        # 等文章加载完毕
        self.driver.implicitly_wait(10)

    # 获取每一页的内容
    def _get_each_text(self, num_page):
        # 每一页的Xpath路径
        xpath = "//*[@id='pageNo-" + str(num_page + 1) + "']/div/div/div/div/div/p"
        # paragraphs = [paragraph1, paragraph2, ... , paragraph_last]
        paragraphs = self.driver.find_elements_by_xpath(xpath)
        for paragraph in paragraphs:
            # 获取每一段的内容
            try:
                m = re.search(r'(\w*)(?P<sign>.*)(\w*)', paragraph.text)
                if m:
                    self.text += m.group()
            except:
                pass

    # 下载文章
    def download(self):
        print('文章共' + str(self.page_count) + '页。')
        with open(self.file, 'w') as f:
            for i in range(self.page_count):
                # 获取每一页的内容
                self._get_each_text(i)
                # 把每一页写入文件
                f.write(self.text)
                # 重置 self.text = ''
                self.text = ''
                print('第' + str(i+1) + "页已经写入文件！")
        return True

if __name__ == '__main__':
    # 要下载文章的url
    url = 'https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html'
    wenku = BaiduWenku(url)
    text = wenku.download()
    print(text)
