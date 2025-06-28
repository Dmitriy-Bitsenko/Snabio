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
                # PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                # PageMethod("wait_for_selector", "div.goods__item(10)"),  # 10 per page
            ],
    errback=self.errback,))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

    # def parse(self, response):
        links = response.css("a.lnk.goods__img-link ::attr(href)").getall()
        #for link in links:
        print(links, len(links))
        
        
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        
    # async def parse_(self, response):
    #     page = response.meta["playwright_page"]
    #     screenshot = await page.screenshot(path="example.png", full_page=True)
    # 	# screenshot contains the image's bytes
    #     await page.close()
    