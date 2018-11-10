from bs4 import BeautifulSoup
import subprocess as sp
from lxml import etree
import requests
import random
import re
# 从西刺网获取免费可用代理 http://www.xicidaili.com
class Proxys():
    def __init__(self):
        # ip列表
        self.proxys_list = []
        # notice： 不同系统平台的正则是不一样的 程序平台为 CentOS Linux 7
        # --- 0.0.0.0 ping statistics ---
        # 16 packets transmitted, 16 received, 0% packet loss, time 14999ms
        # rtt min/avg/max/mdev = 0.076/0.106/0.134/0.014 ms
        # 正则匹配收包数
        self.re_receive_num = re.compile(u"(\d+) received", re.IGNORECASE)
        # 正则匹配平均时间
        self.re_average_time = re.compile(u"/(\d+.\d+)/", re.IGNORECASE)
        # 获取代理100个ip
        self._get_enough_proxys()

    # 获取代理ip
    def _get_proxys(self, page):
        s = requests.Session()
        target_url = 'http://www.xicidaili.com/nn/%d' %page
        target_headers = {'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer':'http://www.xicidaili.com/nn/',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
        }

        target_response = s.get(target_url, headers=target_headers)
        target_response.encoding = 'utf-8'
        target_html = target_response.text
        ip_list_html = BeautifulSoup(target_html, 'lxml')
        ip_list_html = ip_list_html.find(id='ip_list')
        ip_list = ip_list_html.find_all('tr')
        for index in range(len(ip_list)):
            if index % 2 == 1 and index != 1:
                dom = etree.HTML(str(ip_list[index]))
                ip = dom.xpath('//td[2]')
                port = dom.xpath('//td[3]')
                protocol = dom.xpath('//td[6]')
                self.proxys_list.append([protocol[0].text.lower(), ip[0].text, port[0].text])

    # 获取100个ip
    def _get_enough_proxys(self):
        for page in range(1, 100):
            print(page)
            self._get_proxys(page)
            if len(self.proxys_list) > 100:
                break

    # 检查ip是否可用
    def _check_ip(self, ip):
        # 命令 -c 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
        # 不同平台的ping命令可能不同
        # CentOS Linux 7
        cmd = "ping -c 3 -w 3 %s"
        p = sp.Popen(cmd %ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out = p.stdout.read().decode('gbk')
        # re_average_time.findall 的返回值是list类型
        rece_num = int(self.re_receive_num.findall(out)[0])
        avg_time = self.re_average_time.findall(out)
        # IP选取规则是，如果丢包数大于2个，则认为ip不能用，ping通的平均时间大于200ms也认为ip不能用
        if rece_num < 2 or not avg_time :
            return False
        else:
            return float(avg_time[0]) <= 200

    # 获取可用ip
    def get_ip(self):
        while True:
            proxy = random.choice(self.proxys_list)
            # proxy = [protocol, ip, port]
            _, ip , port = proxy
            if not self._check_ip(ip):
                self.proxys_list.remove(proxy)
                print("ip连接超时, 重新获取中!")
                # 代理池中ip小于20个时，重新获取100个代理ip
                if len(self.proxys_list) < 20:
                    self._get_enough_proxys()
            else:
                return str(ip) + ':' + str(port)

if __name__ == '__main__':
    proxy = Proxys()
    ip = proxy.get_ip()
    print(ip)
