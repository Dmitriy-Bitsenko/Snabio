# import scrapy
# from scrapy_splash import SplashRequest
#
# # Улучшенный Lua-скрипт с обработкой ошибок
# scroll_script = """
# function main(splash)
#     -- Настройки
#     splash.resource_timeout = 30.0
#     splash.images_enabled = false
#     splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#
#     -- Открытие страницы с обработкой ошибок
#     local ok, message = pcall(function()
#         assert(splash:go(splash.args.url))
#     end)
#
#     if not ok then
#         splash:log("Failed to load page: " .. message)
#         return {error=message}
#     end
#
#     splash:wait(3)
#
#     -- Функция для прокрутки
#     local scroll_to = splash:jsfunc("window.scrollTo")
#     local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
#
#     local last_height = get_body_height()
#     local scroll_attempts = 0
#     local max_attempts = 15
#
#     while scroll_attempts < max_attempts do
#         scroll_to(0, last_height)
#         splash:wait(3)
#
#         local new_height = get_body_height()
#
#         if new_height == last_height then
#             scroll_attempts = scroll_attempts + 1
#         else
#             scroll_attempts = 0
#             last_height = new_height
#         end
#
#         -- Проверяем наличие элементов
#         local items = splash:evaljs("document.querySelectorAll('.goods-item').length")
#         splash:log("Loaded items: " .. items)
#     end
#
#     return splash:html()
# end
# """
# class ChemSpider(scrapy.Spider):
#     name = "chem"
#     allowed_domains = ["chemkomplekt.ru", "localhost"]
#     start_urls = ["https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"]
#
#     def start_requests(self):
#         for url in self.start_urls:
#             yield SplashRequest(
#                 url,
#                 self.parse,
#                 endpoint='execute',
#                 args={'lua_source': scroll_script, 'wait': 2, 'timeout': 90},
#             )
#         # for url in self.start_urls:
#         #     yield SplashRequest(url, self.parse, args={'wait': 2}) # Увеличьте 'wait' если нужно больше времени для загрузки
#
#     def parse(self, response):
#         links = response.css("a.lnk.goods__img-link ::attr(href)").getall()
#         #for link in links:
#         print(links, len(links))
#

# import scrapy
# from scrapy_splash import SplashRequest
# import time
# from urllib.parse import urljoin
#
#
# class ChemSpider(scrapy.Spider):
#     name = "chem"
#     allowed_domains = ["chemkomplekt.ru"]
#     start_urls = ["https://chemkomplekt.ru/products/novoe-postuplenie-f66875838/"]
#
#     custom_settings = {
#         'DOWNLOAD_DELAY': 3,
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'RETRY_TIMES': 3,
#         'CONCURRENT_REQUESTS': 1,
#         'SPLASH_URL': 'http://localhost:8050',
#     }
#
#     def start_requests(self):
#         script = """
#         function main(splash)
#             splash:set_user_agent(splash.args.headers['User-Agent'])
#             splash.images_enabled = false
#             assert(splash:go(splash.args.url))
#             splash:wait(5)
#
#             -- Функция для проверки количества товаров
#             local get_count = splash:jsfunc([[
#                 function() {
#                     return document.querySelectorAll('.goods-item').length;
#                 }
#             ]])
#
#             -- Основной цикл загрузки
#             local last_count = 0
#             local attempts = 0
#
#             while attempts < 15 do
#                 -- Прокрутка вниз
#                 splash:runjs("window.scrollTo(0, document.body.scrollHeight)")
#                 splash:wait(3)
#
#                 -- Проверка новых товаров
#                 local current_count = get_count()
#                 if current_count == last_count then
#                     attempts = attempts + 1
#                 else
#                     attempts = 0
#                     last_count = current_count
#                 end
#
#                 -- Дополнительная проверка кнопки "Показать еще"
#                 local btn = splash:select('.items-next-loader__button')
#                 if btn then
#                     btn:click()
#                     splash:wait(3)
#                 end
#             end
#
#             return splash:html()
#         end
#         """
#
#         for url in self.start_urls:
#             yield SplashRequest(
#                 url,
#                 self.parse,
#                 endpoint='execute',
#                 args={
#                     'lua_source': script,
#                     'wait': 5,
#                     'timeout': 90,
#                     'headers': {
#                         'User-Agent': self.custom_settings['USER_AGENT'],
#                         'Referer': 'https://www.google.com/',
#                     },
#                 },
#                 meta={'handle_httpstatus_all': True},
#             )
#
#     def parse(self, response):
#         try:
#             # Проверяем, что ответ содержит HTML
#             if not response.text:
#                 self.logger.error("Пустой ответ от сервера")
#                 return
#
#             # Создаем селектор из HTML
#             selector = scrapy.Selector(text=response.text)
#
#             # Извлекаем все ссылки на товары
#             product_links = selector.css('a.lnk.goods__img-link::attr(href)').getall()
#             self.logger.info(f"Найдено товаров: {len(product_links)}")
#
#             # Сохраняем ссылки в файл для проверки
#             with open('product_links.txt', 'w') as f:
#                 for link in product_links:
#                     f.write(urljoin(response.url, link) + '\n')
#
#             for link in product_links:
#                 yield {
#                     'url': urljoin(response.url, link),
#                     'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
#                 }
#
#         except Exception as e:
#             self.logger.error(f"Ошибка при обработке: {str(e)}")
#             self.logger.debug(f"Содержимое ответа: {response.text[:500]}...")
#
#     def handle_error(self, failure):
#         self.logger.error(f"Ошибка запроса: {repr(failure)}")
