import scrapy
from scrapy.linkextractors import LinkExtractor


class MySpider(scrapy.Spider):
    name = 'myspider'

    start_urls = ['https://niipav.ru/production/']

    def parse(self, response):
        link_extractor = LinkExtractor()
        links = link_extractor.extract_links(response)
        for link in links:
            yield {'link': link}
