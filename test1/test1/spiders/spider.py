# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import os
import re
import codecs
import sys


class lufiSpider(scrapy.Spider):
    reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
    sys.setdefaultencoding('utf-8')
    name = 'baoliny'
    allowed_domains = ['www.baoliny.com']
    start_urls = ['http://www.baoliny.com/']

    def parse(self, response):
        link_url = 'http://blog.wuzhenyu.com.cn'
        link_url = link_url.replace('\x0a', '')
        request = scrapy.Request(link_url, callback=self.parse_book_item)
        yield request

    def parse_book_item(self, response):

        sel = Selector(response)
        # xpathbookname = '//*[@id=\"breadCrumb\"]/font/text()';  # 书籍名称规则
        # print xpathbookname
        xpathbookchs = "//*[@class=\"t z\"]//tr/td/h3"  # 章节URL
        # bookname = sel.xpath(xpathbookname).extract()[0]
        # print bookname
        bookchs = sel.xpath(xpathbookchs).extract();
        link_url = response.meta["link"]
        for ch in bookchs:
            if ch == '':
                continue;
            regroup = re.findall("href=\"(.+)\">(.+)</a>", ch);  # 章节的链接和章节名称的正则表达式
            if not regroup:
                continue;
            chUrl_lufi = "http://www.baoliny.com/" + regroup[0][0];  # group 0的第一个位置[0]是链接
            chUrl = chUrl_lufi.split('"')[0]
            # chname = regroup[0][1];  # group 0的第一个位置[1]是章节名
            request = scrapy.Request(chUrl, meta={'chUrl': chUrl}, callback=self.parse_book_chapter)
            yield request;