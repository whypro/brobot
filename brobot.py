from __future__ import unicode_literals
import time
import sys
import os
import json
from collections import Counter
import signal
import sys

from lxml import etree
import requests


class UrlCounter(object):

    def __init__(self, json_file):
        self.counter = None
        self.json_file = json_file
        self.load_counter()

    def load_counter(self):
        if not os.path.exists(self.json_file):
            self.counter = Counter()
            return

        with open(self.json_file, 'r') as f:
            self.counter = Counter(json.load(f))
    
    def save_counter(self):
        if not self.counter:
            return 

        with open(self.json_file, 'w') as f:
            # print self.counter
            json.dump(self.counter, f, indent=4)

    def __setitem__(self, url, count):
        self.counter[url] = count

    def __getitem__(self, url):
        return self.counter[url]


class AutoHomeSpider(object):

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8',
        'cache-control': 'max-age=0',
        'connection': 'keep-alive',
        'host': 'k.autohome.com.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }
    
    url_template = 'http://www.autohome.com.cn/spec/{car_id}/index.html'

    page_access_freq = 1
    max_depth = 3

    def __init__(self, car_id, url_counter):
        self.last_access_page_time = time.time()
        self.car_id = car_id
        self.url_counter = url_counter

    def _download_image(self, url):
        # print url
        # print 'start download image...'
        r = requests.get(url, headers=self.headers)
        # print 'done.'
        return r.content

    def _download_page(self, url):
        # print url
        if time.time() - self.last_access_page_time < self.page_access_freq:
            time.sleep(self.page_access_freq)

        # print 'start download page...'
        r = requests.get(url, headers=self.headers)
        self.last_access_page_time = time.time()
        self.url_counter[url] += 1
        # print 'done.'
        return r.text


    def parse(self):
        url = self.url_template.format(car_id=self.car_id)
        self._parse_page(url)

    def _check_if_crawl_page(self, url):
        if self.car_id not in url:
            return False

        if not url.startswith('http'):
            return False

        if 'ComplaintMain' in url:
            return False

        return True

    def _check_if_crawl_image(self, url):
        if not url.startswith('http'):
            return False 

        return True


    def _parse_page(self, url, depth=0):
        if depth > self.max_depth:
            return

        print 'start download page <{0}>, depth <{1}>'.format(url, depth)
        text = self._download_page(url)
        root = etree.HTML(text)
        _pages = root.xpath('//a/@href')
        _images = root.xpath('//img/@src')
        pages = [u for u in _pages if self._check_if_crawl_page(u)]
        images = [i for i in _images if self._check_if_crawl_image(i)]

        print 'start download images...'
        for i in images:
            self._download_image(i)

        for u in pages:
            self._parse_page(u, depth+1)


uc = UrlCounter('counter.json')

def signal_handler(signal, frame):
        # print('You pressed Ctrl+C!')
        uc.save_counter()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: ./{0} [car_id]'.format(os.path.basename(sys.argv[0]))
        print '    example: ./{0} 25390'.format(os.path.basename(sys.argv[0]))
        exit(0)

    car_id = sys.argv[1]
    print 'got car_id <{0}>'.format(car_id)
    ah_spider = AutoHomeSpider(car_id, uc)
    ah_spider.parse()
