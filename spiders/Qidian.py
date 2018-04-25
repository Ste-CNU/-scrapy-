# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import collections
from QiDian.items import QidianItem
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time




title = input('please enter the book you want to download:')


def auto_get_url(arg):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 3)
    driver.get('https://www.qidian.com/')

    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#s-box'))
    )

    submit = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#search-btn > em'))
    )

    input.send_keys(arg)
    time.sleep(2)
    submit.click()
    driver.switch_to.window(driver.window_handles[1])
    if driver.find_elements_by_class_name('red-kw'):
        item = driver.find_element_by_xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h4/a').get_attribute(
            'href')
        return item


class QidianSpider(scrapy.Spider):
    name = 'Qidian'
    allowed_domains = ['qidian.com']
    start_urls = [auto_get_url(title)]

    def parse(self, response):

        pattern = 'https://read.qidian.com/chapter.*$'
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        download_dict = collections.OrderedDict()
#        path = response.xpath('')
        for link in links:
            if link.text:
                time.sleep(5)  # 时间要设置，因为yield之后就进习行下一个循环，所以下载并不是顺序的
                download_dict[link.url] = link.text
                yield scrapy.Request(link.url, callback=self.parse_text)

    def parse_text(self, response):
        item = QidianItem()
        item['chapter'] = response.xpath('//h3[@class="j_chapterName"]/text()').extract_first()
        text = response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()
        item['text'] = ''.join(text).replace('\u3000\u3000', '\n  ')
        item['title'] = response.xpath('//head/title/text()').extract_first().split('_')[0]
        yield item
