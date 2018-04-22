# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import collections
from QiDian.items import QidianItem
import time


class QidianSpider(scrapy.Spider):
    name = 'Qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://book.qidian.com/info/1115277']
#    path = ''

    def parse(self, response):
        #global path
        pattern = 'https://read.qidian.com/chapter.*$'
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        download_dict = collections.OrderedDict()
#        path = response.xpath('')
        for link in links:
            if link.text:
                time.sleep(0.5)  # 时间要设置，因为yield之后就进习行下一个循环，所以下载并不是顺序的
                download_dict[link.url] = link.text
                yield scrapy.Request(link.url, callback=self.parse_text)

    def parse_text(self, response):
        item = QidianItem()
        item['chapter'] = response.xpath('//h3[@class="j_chapterName"]/text()').extract_first()
        text = response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()
        item['text'] = ''.join(text).replace('\u3000\u3000', '\n  ')
        yield item
