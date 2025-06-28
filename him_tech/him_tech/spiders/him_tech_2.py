# import scrapy

# class HimTechSpider(scrapy.Spider):
#     name = "him_tech"
#     allowed_domains = ["him-tech.ru"]
#     # start_urls = ["https://him-tech.ru/catalog"]
#     start_urls = ['https://him-tech.ru/flokulyanty/']

#     def parse(self, response):
#         global start_urls
#         for i in start_urls: #Проходим по каждой ссылке
#             one_product = response.css("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link::attr(href)").getall()
#             print(len(one_product))
#                 # print(one_product)
#             for el in one_product:
#                 product_url = el
#                 yield scrapy.Request(url=product_url, callback=self.product)

#     def product(self, response):
#         category = response.css('nav.woocommerce-breadcrumb a::text').getall()[1]
#         name = response.css('h1 ::text').get().replace('"','')
#         price = response.css("p.price span ::text").get().replace("\xa0", "")
#         yield{'name': name, 'category': category, 'price': price}
        
#         next_page = response.css("a.page-numbers").attrib["href"]
#         if next_page:
#             page = next_page
#             yield response.follow(page, callback=self.product)


