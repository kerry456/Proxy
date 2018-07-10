#!/usr/bin/env python

import json
from utils import get_page
import re
from pyquery import PyQuery as pq
from lxml import etree
from bs4 import BeautifulSoup as BS
import time

class ProxyMetaclass(type):
    def __new__(cls, name, bases,attrs):
        count = 0
        attrs['__CrawlFunc__']=[]
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object,metaclass=ProxyMetaclass):#
    def get_proxies(self,callback):
        proiex = []
        for prox in eval("self.{}()".format(callback)):
            print('成功获取代理',prox)
            proiex.append(prox)
        return proiex
    def crawl_kuaidaili(self):
        '''
        获取代理66
        :param page_count:页码
        :return: 代理
        '''
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1,100)]
        for url in urls:
            print('Crawling',url)
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                response = selector.xpath('//*[@id="list"]/table/tbody/tr')
                for item in response:
                    ip = item.xpath('./td[1]/text()')[0]
                    port = item.xpath('./td[2]/text()')[0]
                    # print(':'.join([ip,port]))
                    yield ':'.join([ip,port])
    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        dic = json.loads(html)
        for items in dic['RESULT']:
            ip = items['ip']
            port = items['port']
            l = ':'.join([ip,port])
            # print(l)
            yield ':'.join([ip,port])
    def crawl_ip3366(self):
        for page in range(1,11):
            start_url = f'http://www.ip3366.net/?stype=1&page={str(page)}'
            html = get_page(start_url)
            # print(html)
            selector = etree.HTML(html)
            respon =selector.xpath('//*[@id="list"]/table/tbody/tr')
            for item in respon:
                ip = item.xpath('./td[1]/text()')[0]
                port =  item.xpath('./td[2]/text()')[0]
                # l = ':'.join([ip, port])
                # print(l)
                yield ':'.join([ip, port])
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/free/ng'
        html = get_page(start_url)
        soup = BS(html, 'html.parser')
        text = soup.select('td')

        for items in [item.text for item in text]:
            # print(items)
            ips = re.findall('\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}\s',items,re.S)
            ports = re.findall('\s\d+\s',items,re.S)
            if ips:
                ip = ips[0].replace(' ','')
            elif ports:
                port = ports[0].replace(' ','')
            else:
                pass
                # print(ip + ':' + port)
                yield ip + ':' + port
    def crawl_89ip(self):
        for page in range(1,101):
            start_url = f'http://www.89ip.cn/index_{str(page)}.html'
            html = get_page(start_url)
            soup=BS(html, 'html.parser')
            text=soup.select('td')

            for items in [item.text for item in text]:
                ips=re.findall('\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}\s', items, re.S)
                ports=re.findall('\s\d+\s', items, re.S)
                if ips:
                    ip=ips[0].replace(' ', '').replace('\t','')
                elif ports:
                    port=ports[0].replace(' ', '').replace('\t','')
                else:
                    pass
                    # print(ip+':'+port)
                    yield ip + ':' + port

    def crawl_data5u(self):
        start_url='http://www.data5u.com/free/gngn/index.shtml'
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html=get_page(start_url, options=headers)
        if html:
            ip_address=re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address=ip_address.findall(html)
            for address, port in re_ip_address:
                result=address + ':' + port
                # print(result.replace(' ', ''))
                yield result.replace(' ', '')


# if __name__ == '__main__':
#     C = Crawler()
#     C.crawl_ip3366()
#





