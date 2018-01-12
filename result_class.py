# -*- coding=utf-8 -*-
import urllib
import logging
import time
import json
import logging
import random
#import pyautogui as pag
from scrapy.selector import Selector
from scrapy.http import Response
from urllib import request
from lxml import etree

from PIL import Image
from io import BytesIO
import base64
import requests
from multiprocessing.dummy import Pool as ThreadPool
import re

from ocr import normal_ocr
from ip_pool import ip_factory

# import objc, Quartz
# from AppKit import NSBitmapImageRep
# from Quartz.CoreGraphics import CGMainDisplayID

class Result(object):
    def __init__(self,image_path):
        self.keyword_in_results = {} #关键词在结果在出现次数
        self.message = ''
        self.image_path = image_path
        self.image_base64 = self.get_image_base64()
        self.question,self.keywords = self.analysis_image()
        for keyword in self.keywords:
            self.keyword_in_results[keyword]=0
        self.keywords_results_count = None
        if self.question and self.keywords:
            try:
                self.find_answer_from_baidu()
                self.read_result()
                self.write_msg()
            except:
                self.message = "无法在百度上搜索到问题，可能被封锁IP"
                self.write_msg()
            if self.page_urls:
                try:
                    self.add_answer_count_mul()
                    self.read_result()
                    self.write_msg()
                except:
                    self.message = "获取其他页的结果时出错"
                    self.add_msg()
            else:
                self.message = "无法获取其他页的结果"
                self.add_msg()
        else:
            self.message = "无法获取问题和选项"
            self.add_msg()

        try:
            self.keywords_results_count = self.results_count()
            self.read_result()
            self.add_msg()
        except:
            self.message = "无法获取搜索结果数"
            self.add_msg()


    def read_result(self):
        if self.keyword_in_results:
            results_string = ["搜索中出现次数\n"]
            for key in self.keyword_in_results:
                results_string.append(key)
                results_string.append(' : ')
                results_string.append(str(self.keyword_in_results[key]))
                results_string.append('\n')
        if self.keywords_results_count:
            results_string.append("搜索结果数\n")
            for result in self.keywords_results_count:
                results_string.append(list(result.keys())[0])
                results_string.append(' : ')
                results_string.append(str(list(result.values())[0]))
                results_string.append('\n')
        self.message = ''.join(results_string)

    def add_msg(self):
        print(self.message)
        with open("results.html",'a') as f:
            f.write(self.message)

    def write_msg(self):
        print(self.message)
        with open("results.html",'w') as f:
            f.write(self.message)

    def get_image_base64(self):
        with open(self.image_path,'rb') as f:
            imgbase64 = base64.b64encode(f.read())
        return imgbase64.decode()

    def analysis_image(self):
        res = normal_ocr.ocr(self.image_base64)
        try:
            rets = json.loads(res['outputs'][0]['outputValue']['dataValue'])['ret']
            row_number = rets.__len__()
            content = list(ret['word'] for ret in rets)
            question = ''.join(content[:(row_number-3)])
            keywords = content[(row_number-3):]
            return question,keywords
        except:
            return None,None

    def download_html(self,keywords):
        key = {'wd': keywords}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}
        url = "https://www.baidu.com/s?wd={}".format(keywords)
        web_content = requests.get(url, headers=headers, timeout=1.5)
        if web_content.text.__len__() < 250000:
            if ip_factory.ip_pool:
                proxy = random.choice(list(ip_factory.ip_pool))
                try:
                    proxy_url = {'http': 'http://'+proxy}
                    web_content = requests.get("https://www.baidu.com/s?", params=key, headers=headers, proxies=proxy_url,timeout=1)
                except:
                    print("不能获取网页内容，可能IP被封")
        return web_content.text

    def download_html_page(self,page_url):
        url = "https://www.baidu.com"+page_url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}
        url = "https://www.baidu.com{}".format(page_url)
        web_content = requests.get(url, headers=headers, timeout=1.5)
        if web_content.text.__len__() < 250000:
            if ip_factory.ip_pool:
                proxy = random.choice(list(ip_factory.ip_pool))
                try:
                    proxy_url = {'http': 'http://'+proxy}
                    web_content = requests.get(url, headers=headers, proxies=proxy_url,timeout=1)
                    return web_content.text
                except:
                    print("不能获取分页内容，可能IP被封")
        return web_content.text

    def find_answer_from_baidu(self):
        if self.question and self.keywords:
            html_doc = self.download_html(self.question)
            # with open('index.html','w') as f:
            #      f.write(html_doc)
            selector = etree.HTML(html_doc)
            xpath = '//div[@id="page"]//a/@href'
            self.page_urls = [page_url for page_url in selector.xpath(xpath)[:-1]]
            for id in range(1,11,1):
                xpath = '//*[@id="{}"]//div//text()'.format(id).format(id)
                for content in selector.xpath(xpath):
                    # print(content)
                    for keyword in self.keywords:
                        if keyword in content:
                            self.keyword_in_results[keyword] += 1



    def add_answer_count(self,page_number):
        if self.page_urls.__len__() < (page_number-1):
            return None
        page_url = self.page_urls[page_number-2]
        html_doc = self.download_html_page(page_url)

        selector = etree.HTML(html_doc)
        for id in range(10*page_number-9,10*page_number+1,1):
            xpath = '//*[@id="{}"]//div//text()'.format(id).format(id)
            for content in selector.xpath(xpath):
                for keyword in self.keywords:
                    if keyword in content:
                        self.keyword_in_results[keyword] += 1

    def add_answer_count_mul(self):
        pages = range(2,10,1)
        pool = ThreadPool()#机器是多少核便填多少，卤煮实在ubuntu14.04 4核戴尔电脑上跑的程序
        results = pool.map(self.add_answer_count, pages)
        pool.close()
        pool.join()

    def results_count_sub(self,keyword):
        keywords = '{} {}'.format(self.question,keyword)
        html_doc = self.download_html(keywords)
        selector = etree.HTML(html_doc)
        xpath = "//div[@class='nums']//text()"
        content = ''.join(selector.xpath(xpath))
        result = re.sub("\D",'',content)
        return {keyword:result}

    def results_count(self):
        pool = ThreadPool()#机器是多少核便填多少，卤煮实在ubuntu14.04 4核戴尔电脑上跑的程序
        results = pool.map(self.results_count_sub, self.keywords)
        pool.close()
        pool.join()
        return results
