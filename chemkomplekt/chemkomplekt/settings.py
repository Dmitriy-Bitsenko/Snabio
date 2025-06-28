# Scrapy settings for chemkomplekt project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# SPLASH_URL = "http://localhost:8050"

from shutil import which

BOT_NAME = "chemkomplekt"

SPIDER_MODULES = ["chemkomplekt.spiders"]
NEWSPIDER_MODULE = "chemkomplekt.spiders"

from selenium.webdriver.chrome.service import Service

SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_EXECUTABLE_PATH = r'C:\Users\Dmitriy\chromedriver.exe'
#SELENIUM_DRIVER_ARGUMENTS = ['--headless']
SELENIUM_DRIVER_ARGUMENTS=['--no-sandbox', '--disable-dev-shm-usage']
SELENIUM_COMMAND_EXECUTOR = 'http://localhost:4444/wd/hub'
# SELENIUM_DRIVER_SERVICE_ARGS = []
# SELENIUM_DRIVER_SERVICE = Service(SELENIUM_DRIVER_EXECUTABLE_PATH)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "chemkomplekt (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False #True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "chemkomplekt.middlewares.ChemkomplektSpiderMiddleware": 543,
   # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "chemkomplekt.middlewares.ChemkomplektDownloaderMiddleware": 543,
   #'scrapy_splash.SplashCookiesMiddleware': 723,
   #  'scrapy_splash.SplashMiddleware': 725,
   #  'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
   #  'scrapy.downloadermiddlewares.offsite.OffsiteMiddleware': None,
   'scrapy_selenium.SeleniumMiddleware': 800,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "chemkomplekt.pipelines.ChemkomplektPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# settings.py

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}


# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTP_CACHE_STORAGE = 'scrapy_splash.SplashAwareHTTPCacheStorage'

