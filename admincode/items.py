# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AdmincodeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    code = scrapy.Field()
    codetype = scrapy.Field()
    parent_code = scrapy.Field()
    towntypecode = scrapy.Field() # 城乡分类代码为：   100 城镇   110 城区   111 主城区    112 城乡结合区   120 镇区    121 镇中心区   122 镇乡结合区   123 特殊区域   200 乡村   210 乡中心区   220 村庄

    def get_parent(self):
        if codetype == 'province':
            return ('0' * 12)
        elif codetype == 'city':
            return code[0:2] + ('0' * 10)
        elif codetype == 'county':
            return code[0:4] + ('0' * 8)
        elif codetype == 'town':
            return code[0:6] + ('0' * 6)
        elif codetype == 'village':
            return code[0:9] + ('0' * 3)
        else:
            raise