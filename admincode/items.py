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