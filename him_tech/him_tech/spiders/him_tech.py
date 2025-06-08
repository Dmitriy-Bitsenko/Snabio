import scrapy

class HimTechSpider(scrapy.Spider):
    name = "him_tech"
    allowed_domains = ["him-tech.ru"]
    # start_urls = ["https://him-tech.ru/catalog"]
    start_urls = ['https://him-tech.ru/flokulyanty/', 'https://him-tech.ru/tehnicheskaya-himiya/',
                  'https://him-tech.ru/activ/', 'https://him-tech.ru/ionoobmennye-smoly/',
                  'https://him-tech.ru/ingibitory-korrozii-i-soleotlozheniya/', 'https://him-tech.ru/silikageli/',
                  'https://him-tech.ru/czeolity/', 'https://him-tech.ru/koagulyanty/',
                  'https://him-tech.ru/kvarczevyj-pesok/', 'https://him-tech.ru/ksantanovaya-kamed/']

    def parse(self, response):
        categories = response.css("li.product-category a::attr(href)").getall() #Получаем ссылки на категории
        # print(categories)
        for product in categories: #Проходим по каждой категории
            product_url = product
            for i in product_url: #Проходим по каждой ссылке print("\n".join(my_list))
                one_product = response.css("h2 a::attr(href)").getall()
                # print(len(one_product))
                # print(one_product)
                for el in one_product:
                    product_url = el
                    yield scrapy.Request(url=product_url, callback=self.product)

    def product(self, response):
        category = response.css('nav.woocommerce-breadcrumb a::text').getall()[1]
        name = response.css('h1 ::text').get().replace('"','') #response.css("h2 a::text").get()#.replace("\t", "").replace("\r","").replace('\n',"")
        price = response.css("p.price span ::text").get().replace("\xa0", "")
        yield{'name': name, 'category': category, 'price': price}
            # response.css('a.bdt-link-reset ::text').get().replace('\t','').replace('\r','').replace('\n','')

    # def parse(self, response):
    #     categories = response.css("li.product-category a::attr(href)").getall() #Получаем ссылки на категории
    #     print(categories)
    #     print(len(categories))
    #     yield scrapy.Request(url=categories, callback=self.product)

    # def parse(self, response):
    #     for i in self.start_urls:
    #         name = response.css('a.bdt-link-reset::text').get().replace('\t','').replace('\r','').replace('\n','')
    #         print(name)
    #         # print(len(name))
    #         yield{'name': name}
            # print(products)
            # print(len(products))
            # for i in product:
            #     name = response.css('a.bdt-link-reset ::text').get().replace('\t','').replace('\r','').replace('\n','')
            #     print(name)
 # for el in one_product:
 #    ...:     name = response.css('a.bdt-link-reset ::text').get().replace('\t','').replace('\r','').replace('\n','')
 #    ...:     print(
