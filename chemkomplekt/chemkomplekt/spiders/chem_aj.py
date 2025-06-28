import scrapy
from scrapy.selector import Selector
import json


class ChemKomplektSpider(scrapy.Spider):
    name = "chem_aj"
    allowed_domains = ["chemkomplekt.ru"]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,  # задержка, чтобы не гонять сервер сильно
        "COOKIES_ENABLED": True,
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
    }

    def start_requests(self):
        url_main = "https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"
        yield scrapy.Request(
            url=url_main,
            callback=self.parse_main,
            dont_filter=True,
        )

    def parse_main(self, response):
        cookies = {}
        for cookie_header in response.headers.getlist('Set-Cookie'):
            cookie_str = cookie_header.decode('utf-8')
            cookie_key_value = cookie_str.split(';')[0]
            if '=' in cookie_key_value:
                key, value = cookie_key_value.split('=', 1)
                cookies[key] = value

        self.logger.info(f"Cookies из ответа: {cookies}")

        csrf_token = cookies.get('csrftoken')
        self.logger.info(f"CSRF Token найден: {csrf_token}")

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/137.0.0.0 Safari/537.36",
            "Referer": response.url,
            "Accept": "application/json",
        }
        if csrf_token:
            headers["X-CSRFToken"] = csrf_token

        yield scrapy.Request(
            url=self.build_url(1, ""),
            headers=headers,
            cookies=cookies,
            callback=self.parse_ajax,
            cb_kwargs={"portion": 1, "headers": headers, "cookies": cookies, "nextGoodsBackData": ""}
        )

    def build_url(self, portion, nextGoodsBackData):
        return (
            f"https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"
            f"?_common-data=1&ajax=1&portionNumber={portion}&nextGoodsBackData={nextGoodsBackData}"
        )

    def parse_ajax(self, response, portion, headers, cookies, nextGoodsBackData):
        if response.status == 419:
            self.logger.warning(f"Порция {portion}: Получен 419 статус — возможно, сессия устарела.")
            return

        try:
            data = json.loads(response.text)
            html = data.get("html", "")
            next_goods_data = data.get("nextGoodsBackData", "")
        except json.JSONDecodeError:
            self.logger.warning(f"Порция {portion}: ответ не JSON, прекращаем.")
            return

        selector = Selector(text=html)
        product_links = selector.css("a.lnk.goods__img-link::attr(href)").getall()

        if not product_links:
            self.logger.info(f"Порция {portion}: ссылки не найдены, завершение парсинга.")
            return

        self.logger.info(f"Порция {portion}: найдено {len(product_links)} ссылок.")

        for link in product_links:
            yield {"link": response.urljoin(link)}

        if not next_goods_data:
            self.logger.info("Данные закончились, парсинг завершен.")
            return

        next_portion = portion + 1
        next_url = self.build_url(next_portion, next_goods_data)

        yield scrapy.Request(
            url=next_url,
            headers=headers,
            cookies=cookies,
            callback=self.parse_ajax,
            cb_kwargs={"portion": next_portion, "headers": headers, "cookies": cookies, "nextGoodsBackData": next_goods_data}
        )
