#!/usr/bin/env python

from Rediscli import RedisClient

from crawler import Crawler
import sys


POOL_UPPER_THRESHOLD = 1000
class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    def is_over_threshold(self):
        '''
        判断代理池是否是满了
        :return:
        '''
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    def run(self):
        print('代理池开始执行获取。。。。')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback=self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies=self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
# if __name__ == '__main__':
#     C = Getter()
#     C.run()
