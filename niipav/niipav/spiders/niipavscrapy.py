import scrapy


class NiipavscrapySpider(scrapy.Spider):
    name = "niipavscrapy"
    allowed_domains = ["niipav.ru"]
    start_urls = ["https://niipav.ru/production/"]

    def parse(self, response):
        products = response.css("div.elementor-widget-wrap.elementor-element-populated h5 a::attr(href)").getall()
        print(products)
        for product in products:
            product_url = product
            print(product_url)
            yield scrapy.Request(url=product_url, callback=self.parse_product)

    def parse_product(self, response):
        name = response.css("div.elementor-widget-container h1 strong ::text").getall()[1]
        CAS = response.css("div.elementor-widget-container h4 ::text").getall()[-1]
        yield {"name": name, "CAS": CAS}



