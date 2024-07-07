import scrapy


class OkachimspiderSpider(scrapy.Spider):
    name = "okachimspider"
    allowed_domains = ["okachim.ru"]
    start_urls = ["https://okachim.ru/catalog/"]

    def parse(self, response):
        products = response.css('div.letter-block ul li a::attr(href)').getall()
        for product in products:
            product_url = 'https://okachim.ru'+ product
            print(product_url)
            yield scrapy.Request(url=product_url, callback=self.parse_product)

    def parse_product(self, response):
        name = response.css('h1.pagetitle.h2 ::text').get()
        CAS = response.css('div.td::text').getall()[8].lstrip().rstrip()
        yield{'name': name, 'CAS': CAS}
