import scrapy


class RushimSpider(scrapy.Spider):
    """Common class."""

    name = "rushim"
    allowed_domains = ["rushim.ru"]
    start_urls = ['https://rushim.ru/index.php?cat=2']

    def parse(self, response):
        """Parse one column."""
        reactives = response.css('div.thumbnail.text-center')
        print(reactives)
        for reactive in reactives:
            product_all_row = reactive.css('div.thumbnail.text-center a::text').get()
            print(product_all_row)
            product = product_all_row.split(',')[0]
            category = 'Реактивы и хим. сырье'
            trademark = None
            country = None
            description = None
            CAS = None
            INCI = None
            manufacturer = None
            packing = product_all_row.split(' ')
            for i in packing:
                if 'упак' in packing or 'упаковку' in packing:
                    packing = 'упаков'
                else:
                    packing = ''

            price = reactive.css('div.thumbnail.text-center span::text').get().replace('руб', '').lstrip().rstrip().replace('.00', '')

            if packing != '':
                price = price
            else:
                price = ''

            yield {'product': product, 'category': category, 'price': price,
                   'trademark': trademark, 'country': country,
                   'description': description, 'CAS': CAS,
                   'INCI': INCI, 'manufacturer': manufacturer,
                   'packing': packing}

            next_page = response.css('a.pageResults')[-1]
            if next_page:
                page = next_page
                yield response.follow(page, callback=self.parse)
