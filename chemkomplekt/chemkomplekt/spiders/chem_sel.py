import time
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ChemSpider(scrapy.Spider):
    name = "chem_sel"
    allowed_domains = ["chemkomplekt.ru"]
    start_urls = ["https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"]

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.scroll_and_collect,
            wait_time=3,
            screenshot=False
        )

    def scroll_and_collect(self, response):
        driver = response.request.meta["driver"]

        collected_links = set()
        prev_count = 0
        same_count_times = 0
        MAX_ATTEMPTS = 80

        for i in range(MAX_ATTEMPTS):
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(3)

            try:
                WebDriverWait(driver, 10).until(
                    lambda d: len(Selector(text=d.page_source).css(".goods__item")) > prev_count
                )
            except:
                print("Подгрузка остановилась или ничего нового не появилось.")
                same_count_times += 1

            selector = Selector(text=driver.page_source)
            links = selector.css("a.lnk.goods__img-link::attr(href)").getall()

            new_links = set(links) - collected_links
            collected_links.update(new_links)

            print(f"[{i+1}] Собрано ссылок: {len(collected_links)}")

            curr_count = len(collected_links)

            if curr_count == prev_count:
                same_count_times += 1
            else:
                same_count_times = 0
                prev_count = curr_count

            if same_count_times >= 5:
                print("Подгрузка завершена.")
                break

        links  = list(collected_links)
        print(links)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        country = response.css('div.info-table__value::text').get()
        title = response.css('div.title.section__title h1::text').get()
        category = response.xpath('//*[@id="reactRootElem"]/div[2]/div/div/main/div[3]/div/div/div[2]/div/div/div[2]/div[2]/text()').get() # response.xpath('//*[@id="reactRootElem"]/div[2]/div/div/main/div[3]/div/div/div[1]/div/div/div[1]/div[2]/text()').get()            
        price = response.css('.break-word::text').get().replace('₽', '')
        if country == "химические индикаторы":
            country = None
        yield {'title': title,
               'category': category,
               'country': country ,                 
               'price': price}
        