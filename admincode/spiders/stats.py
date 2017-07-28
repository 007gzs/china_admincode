# -*- coding: utf-8 -*-
import scrapy
from admincode.items import AdmincodeItem


class StatsSpider(scrapy.Spider):
    name = 'stats'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html']

    def parse(self, response):
        for ret in self.parse_provincetr(response, response.selector.css(".provincetr")):
            yield ret
        for ret in self.parse_citytr(response, response.selector.css(".citytr")):
            yield ret
        for ret in self.parse_countytr(response, response.selector.css(".countytr")):
            yield ret
        for ret in self.parse_towntr(response, response.selector.css(".towntr")):
            yield ret
        for ret in self.parse_villagetr(response, response.selector.css(".villagetr")):
            yield ret

    def parse_provincetr(self, response, trs):
        for a in trs.xpath('td/a'):
            item = AdmincodeItem()
            item['codetype'] = 'province'
            item['name'] = a.xpath('text()')
            item['code'] = a.xpath('@href').extract()[0].split('.')[0] + ('0' * 10)
            item['url'] = response.urljoin(a.xpath('@href').extract()[0])
            yield item
            yield scrapy.Request(item['url'], callback=self.parse)

    def parse_citytr(self, response, trs):
        for tr in trs:
            item = AdmincodeItem()
            item['codetype'] = 'city'
            if not tr.xpath('td')[0].xpath('a'):
                item['name'] = tr.xpath('td')[1].xpath('text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('text()').extract()[0]
                item['parent_code'] = item.get_parent()
                yield item
            else:
                item['name'] = tr.xpath('td')[1].xpath('a/text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('a/text()').extract()[0]
                item['parent_code'] = item.get_parent()
                item['url'] = response.urljoin(tr.xpath('td')[0].xpath('a/@href').extract()[0])
                yield item
                yield scrapy.Request(item['url'], callback=self.parse)

    def parse_countytr(self, response, trs):
        for tr in trs:
            item = AdmincodeItem()
            item['codetype'] = 'county'
            if not tr.xpath('td')[0].xpath('a'):
                item['name'] = tr.xpath('td')[1].xpath('text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('text()').extract()[0]
                item['parent_code'] = item.get_parent()
                yield item
            else:
                item['name'] = tr.xpath('td')[1].xpath('a/text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('a/text()').extract()[0]
                item['parent_code'] = item.get_parent()
                item['url'] = response.urljoin(tr.xpath('td')[0].xpath('a/@href').extract()[0])
                yield item
                yield scrapy.Request(item['url'], callback=self.parse)

    def parse_towntr(self, response, trs):
        for tr in trs:
            item = AdmincodeItem()
            item['codetype'] = 'town'
            if not tr.xpath('td')[0].xpath('a'):
                item['name'] = tr.xpath('td')[1].xpath('text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('text()').extract()[0]
                item['parent_code'] = item.get_parent()
                yield item
            else:
                item['name'] = tr.xpath('td')[1].xpath('a/text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('a/text()').extract()[0]
                item['parent_code'] = item.get_parent()
                item['url'] = response.urljoin(tr.xpath('td')[0].xpath('a/@href').extract()[0])
                yield item
                yield scrapy.Request(item['url'], callback=self.parse)

    def parse_villagetr(self, response, trs):
        for tr in trs:
            item = AdmincodeItem()
            item['codetype'] = 'village'
            if not tr.xpath('td')[0].xpath('a'):
                item['name'] = tr.xpath('td')[2].xpath('text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('text()').extract()[0]
                item['parent_code'] = item.get_parent()
                yield item
            else:
                item['name'] = tr.xpath('td')[2].xpath('a/text()').extract()[0]
                item['code'] = tr.xpath('td')[0].xpath('a/text()').extract()[0]
                item['parent_code'] = item.get_parent()
                item['url'] = response.urljoin(tr.xpath('td')[0].xpath('a/@href').extract()[0])
                yield item
                yield scrapy.Request(item['url'], callback=self.parse)
