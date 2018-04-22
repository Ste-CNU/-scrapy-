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
        pattern = 'https://read.qidian.com/chapter.*$' # 用正则选取所有需要的免费章节的url，因为vip章节看不了
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        download_dict = collections.OrderedDict() # 生成按照顺序存储的字典
#        path = response.xpath('')
        for link in links:
            if link.text: # 如果章节名字存在，就进行下载，因为有的link.text为空，说明该link里面没有正文
                time.sleep(0.5)  # 因为yield之后就进行下一个循环，下载并不是按照顺序完成地，所以时间要设置，确保上一个完成之后下一个开始
                download_dict[link.url] = link.text
                yield scrapy.Request(link.url, callback=self.parse_text)

    def parse_text(self, response):
        item = QidianItem()
        item['chapter'] = response.xpath('//h3[@class="j_chapterName"]/text()').extract_first()
        text = response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()
        item['text'] = ''.join(text).replace('\u3000\u3000', '\n  ') # 对正文进行规范
        yield item
