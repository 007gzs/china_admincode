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

    def get_text_href(self, td):
        if not td.xpath('a'):
            return td.xpath('text()').extract()[0], None
        else:
            return td.xpath('a/text()').extract()[0], td.xpath('a/@href').extract()[0]

    def parse_provincetr(self, response, trs):
        for td in trs.xpath('td'):
            item = AdmincodeItem()
            item['codetype'] = 'province'
            item['name'], href = self.get_text_href(td)
            if href:
                item['code'] = href.split('.')[0] + ('0' * 10)
                item['parent_code'] = item.get_parent()
                item['url'] = response.urljoin(href)
            yield item
            if item['url']:
                yield scrapy.Request(item['url'], callback=self.parse)

    def parse_2td(self, response, trs, codetype):
        for tr in trs:
            item = AdmincodeItem()
            item['codetype'] = codetype
            item['code'], href = self.get_text_href(tr.xpath('td')[0])
            item['parent_code'] = item.get_parent()
            if href:
                item['url'] = response.urljoin(href)
            item['name'], href = self.get_text_href(tr.xpath('td')[1])
            if href:
                item['url'] = response.urljoin(href)
            yield item
            if item['url']:
                yield scrapy.Request(item['url'], callback=self.parse)

    def parse_citytr(self, response, trs):
        return self.parse_2td(response, trs, 'city')

    def parse_countytr(self, response, trs):
        return self.parse_2td(response, trs, 'county')

    def parse_towntr(self, response, trs):
        return self.parse_2td(response, trs, 'town')

    def parse_villagetr(self, response, trs):
        for tr in trs:
            item = AdmincodeItem()
            item['codetype'] = 'village'
            item['code'], href = self.get_text_href(tr.xpath('td')[0])
            item['parent_code'] = item.get_parent()
            if href:
                item['url'] = response.urljoin(href)
            item['towntypecode'], href = self.get_text_href(tr.xpath('td')[1])
            if href:
                item['url'] = response.urljoin(href)
            item['name'], href = self.get_text_href(tr.xpath('td')[2])
            if href:
                item['url'] = response.urljoin(href)
            yield item
            if item['url']:
                yield scrapy.Request(item['url'], callback=self.parse)
