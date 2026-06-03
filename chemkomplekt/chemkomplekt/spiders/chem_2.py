import scrapy
from scrapy_playwright.page import PageMethod

class ChemSpider(scrapy.Spider):
    name = "chem_2"
    allowed_domains = ["chemkomplekt.ru", "localhost"]
    start_urls = ["https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"]

    def start_requests(self):
        url = "https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "div.goods__item"),

            ],
    errback=self.errback,))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        links = response.css("a.lnk.goods__img-link ::attr(href)").getall()
        print(links, len(links))
        
        
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        
    