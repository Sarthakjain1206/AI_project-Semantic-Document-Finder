# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

__author__ = "Sarthak Jain"
__copyright__ = "Copyright 2020, The Semantic Document Finder Project"
__version__ = "1.0"
__maintainer__ = "Rob Knight"
__email__ = "srkjain1147@gmail.com"
__status__ = "Under Development"

class BookSpider(CrawlSpider):
    name = 'wiki_parse'
    allowed_domains = ['en.wikipedia.org']

    start_urls = ['https://en.wikipedia.org/wiki/Coronavirus']

    rules = (Rule(LinkExtractor(allow_domains=('en.wikipedia.org'), deny=('index.php'), restrict_xpaths=('//p')),
                  callback='parse_page', follow=True),)


    def parse_page(self, response):
        # title = response.xpath('//h1//text()').extract_first()

        # There are lot of exceptions in Title, So we have to be very precise
        # For eg- Visit this link and Inspect --> https://en.wikipedia.org/wiki/Revenue and
        # https://en.wikipedia.org/wiki/List_of_American_Dad!_characters

        titles = response.xpath('//h1[@class="firstHeading"]//text()').extract()
        if len(titles) == 1:
            title = titles[0]
        else:
            title = " ".join(titles)
        # self.log(message="I am fetching wiki page...")

        # text = "\n".join(response.xpath('//p//text()|''//h2//text()').extract())
        text = '\n'.join(response.xpath('//p//text()|''//h2/text()|''//h3/text()|''//h3/following-sibling::dl//text()|''//p/following-sibling::ul//text()').extract())
        table_text = "\n".join(response.xpath('//table//text()').extract())
        url = response.url

        if len(re.findall(':', url)) >= 2:
            pass
        else:
            yield {
                'Title': title,
                'URL': url,
                'Text': text,
                'Table Text': table_text
            }

    # def close(spider, reason):
    #     csv_columns = ['Title', 'URL', 'Text', 'Table Text']
    #     csv_file = 'WikipediaArticles.csv'
    #     try:
    #         with open(csv_file, 'w', encoding='utf-8') as csvfile:
    #             writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #             writer.writeheader()
    #             for data in data_dict:
    #                 writer.writerow(data)
    #     except IOError:
    #         print("I/O error")
