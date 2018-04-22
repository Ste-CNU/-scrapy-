# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QidianPipeline(object):

    def process_item(self, item, spider):
        path = '斗罗大陆.txt'
        with open(path, 'a', encoding='utf-8') as f:
            f.write(item['chapter'] + '\n')
            for each in item['text']:
                if each == '\r':
                    f.write('\n')
                f.write(each)
            f.write('\n\n')
        return item
