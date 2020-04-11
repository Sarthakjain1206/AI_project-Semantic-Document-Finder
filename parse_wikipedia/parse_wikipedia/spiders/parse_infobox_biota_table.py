# -*- coding: utf-8 -*-
import scrapy


class ParseInfoboxBiotaTableSpider(scrapy.Spider):
    name = 'parse_infobox_biota_table'
    allowed_domains = ['en.wikipedia.org']
    # start_urls = ['https://en.wikipedia.org/wiki/Human_coronavirus_HKU1']
    # start_urls = ['https://en.wikipedia.org/wiki/Coronavirus']
    # start_urls = ['https://en.wikipedia.org/wiki/Bird']
    start_urls = ['https://en.wikipedia.org/wiki/Bat']


    def parse(self, response):

        table = response.xpath('//table[@class="infobox biota"]')[0]
        trs = table.xpath('.//tr')[2:]
        flag = False
        # classification_dict = {}
        for tr in trs:

            if flag == False:

                classification = tr.xpath('.//a[contains(text(),"classification")]/text()').extract_first()
                if classification != None:
                    flag = True
                    continue
            else:
                col = tr.xpath('.//td')
                if col == []:
                    flag = False
                    continue
                key = col[0].xpath('.//text()').extract_first().strip()[:-1]
                value = col[1].xpath('.//text()').extract_first().strip()
                # classification_dict.update({key: value})
                yield {key: value}
