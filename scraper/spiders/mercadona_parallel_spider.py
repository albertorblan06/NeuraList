"""
Parallel Mercadona spider using concurrent Selenium instances
"""
import scrapy
from scrapy.spiders import SitemapSpider
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
import time

class MercadonaParallelSpider(SitemapSpider):
    """Parallel spider for faster scraping"""

    name = 'mercadona_parallel'
    allowed_domains = ['tienda.mercadona.es']
    sitemap_urls = ['https://tienda.mercadona.es/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product_page'),
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 5,  # Process 5 URLs at once
        'DOWNLOAD_DELAY': 0.5,
        'ROBOTSTXT_OBEY': True,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_pool = []
        self.pool_size = 3  # 3 parallel browsers
        logger.info(f"Initializing parallel spider with {self.pool_size} browsers")

    def setup_driver(self):
        """Create a new Selenium driver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def get_driver(self):
        """Get or create a driver from pool"""
        if len(self.driver_pool) < self.pool_size:
            driver = self.setup_driver()
            self.driver_pool.append(driver)
            return driver
        return self.driver_pool[len(self.driver_pool) % self.pool_size]

    def closed(self, reason):
        """Clean up all drivers"""
        for driver in self.driver_pool:
            try:
                driver.quit()
            except:
                pass

    def parse_product_page(self, response):
        """Parse product using available driver from pool"""
        url = response.url
        logger.info(f"Parsing: {url}")

        try:
            driver = self.get_driver()
            driver.get(url)
            time.sleep(3)  # Reduced wait time

            # Quick extraction
            product = {
                'url': url,
                'product_id': url.split('/product/')[1].split('/')[0] if '/product/' in url else '',
                'name': '',
                'image_url': '',
            }

            # Get name
            try:
                h1 = driver.find_element(By.TAG_NAME, "h1")
                product['name'] = h1.text.strip()
            except:
                pass

            # Get image
            try:
                imgs = driver.find_elements(By.TAG_NAME, "img")
                for img in imgs:
                    src = img.get_attribute('src')
                    if src and 'prod' in src.lower():
                        product['image_url'] = src
                        break
            except:
                pass

            if product['name']:
                logger.info(f"✓ {product['name']}")
                yield product

        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
