"""
Mercadona product scraper using sitemap and Selenium

This spider scrapes product information from Mercadona's product pages.
It uses the sitemap to find product URLs and Selenium to render JavaScript.

Usage:
    scrapy crawl mercadona_sitemap
    scrapy crawl mercadona_sitemap -s CLOSESPIDER_ITEMCOUNT=10
"""
import scrapy
from scrapy.spiders import SitemapSpider
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from typing import Generator, Dict, Any
import re
import json
import time


class MercadonaSitemapSpider(SitemapSpider):
    """Spider for scraping Mercadona products via sitemap"""

    name = 'mercadona_sitemap'
    allowed_domains = ['tienda.mercadona.es']
    sitemap_urls = ['https://tienda.mercadona.es/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product_page'),
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 3.0,
        'CONCURRENT_REQUESTS': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'ROBOTSTXT_OBEY': True,
    }

    def __init__(self, *args, **kwargs):
        """Initialize spider with Selenium driver"""
        super().__init__(*args, **kwargs)
        self.driver = None
        logger.info("Initializing Mercadona sitemap spider with Selenium")

    def setup_driver(self):
        """Set up Selenium WebDriver with Chrome"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Set user agent
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium driver initialized")

    def close_driver(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Selenium driver closed")

    def closed(self, reason):
        """Called when the spider is closed"""
        self.close_driver()

    def parse_product_page(self, response):
        """
        Parse a product page using Selenium to render JavaScript

        Args:
            response: Scrapy response object

        Yields:
            Product dictionary
        """
        url = response.url
        logger.info(f"Parsing product page: {url}")

        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Set up driver if not already done
                self.setup_driver()

                # Load the page
                self.driver.get(url)

                # Wait for the page to load (wait for React to render)
                wait = WebDriverWait(self.driver, 15)

                # Wait for multiple elements to ensure page is fully loaded
                try:
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                except:
                    logger.warning(f"Timeout waiting for h1 element on {url}")

                # Give extra time for React to fully hydrate and load all data
                time.sleep(5)

                # Extract product data
                product = self.extract_product_data(url)

                if product and product.get('name'):
                    logger.info(f"Successfully parsed product: {product.get('name')}")
                    yield product
                    break
                else:
                    logger.warning(f"Could not extract product data from {url}")
                    break

            except Exception as e:
                logger.error(f"Error parsing product page {url} (attempt {attempt + 1}/{max_retries}): {e}")
                # If connection error, recreate driver
                if "Connection refused" in str(e) or "session" in str(e).lower():
                    logger.warning("Selenium session lost, recreating driver...")
                    self.close_driver()
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                break

    def extract_product_data(self, url: str) -> Dict[str, Any]:
        """
        Extract product data from the rendered page

        Args:
            url: Product page URL

        Returns:
            Product dictionary
        """
        try:
            product = {
                'url': url,
                'product_id': self.extract_product_id(url),
                'name': '',
                'brand': '',
                'price': 0.0,
                'unit_price': 0.0,
                'unit_measure': '',
                'image_url': '',
                'description': '',
                'category': '',
                'subcategory': '',
                'ean': '',
                'is_available': True,
            }

            # Extract product ID from URL
            product['product_id'] = self.extract_product_id(url)

            # Try to extract data from window.__INITIAL_STATE__ or similar
            try:
                react_data = self.driver.execute_script("""
                    return window.__INITIAL_STATE__ ||
                           window.__NEXT_DATA__ ||
                           window.PRODUCT_DATA ||
                           null;
                """)
                if react_data:
                    logger.info("Found React state data")
                    # Process React state data if available
                    # This would need to be adapted based on actual structure
            except:
                pass

            # Get all text content for analysis
            page_text = self.driver.find_element(By.TAG_NAME, "body").text

            # Try to find product name from h1
            try:
                h1_elements = self.driver.find_elements(By.TAG_NAME, "h1")
                for h1 in h1_elements:
                    text = h1.text.strip()
                    if text and len(text) > 3:  # Filter out empty or very short h1s
                        product['name'] = text
                        logger.debug(f"Found name in h1: {text}")
                        break
            except Exception as e:
                logger.warning(f"Could not find h1: {e}")

            # If no h1, try alternative selectors
            if not product['name']:
                for selector in ['[data-testid="product-title"]', '.product-title', '[class*="title"]']:
                    try:
                        elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if elem.text.strip():
                            product['name'] = elem.text.strip()
                            break
                    except:
                        continue

            # Extract prices using multiple strategies
            price_found = False

            # Strategy 1: Look for price in aria-labels and data attributes
            try:
                price_elements = self.driver.find_elements(By.CSS_SELECTOR,
                    '[aria-label*="precio"], [data-testid*="price"], [class*="price"], [class*="precio"]')
                for elem in price_elements:
                    text = elem.text + " " + elem.get_attribute('aria-label') + " " + elem.get_attribute('data-price')
                    price_match = re.search(r'(\d+[,\.]\d+)\s*€', text)
                    if price_match:
                        price_str = price_match.group(1).replace(',', '.')
                        product['price'] = float(price_str)
                        logger.debug(f"Found price: {product['price']}")
                        price_found = True
                        break
            except:
                pass

            # Strategy 2: Scan all text for price patterns
            if not price_found:
                all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '€')]")
                for elem in all_elements:
                    text = elem.text
                    # Look for standalone prices like "1,23 €" or "1.23€"
                    price_match = re.search(r'(\d+[,\.]\d{2})\s*€', text)
                    if price_match and not any(word in text.lower() for word in ['total', 'descuento', 'ahorro']):
                        price_str = price_match.group(1).replace(',', '.')
                        candidate_price = float(price_str)
                        # Filter out unrealistic prices
                        if 0.01 <= candidate_price <= 1000:
                            product['price'] = candidate_price
                            logger.debug(f"Found price in text: {product['price']}")
                            price_found = True
                            break

            # Extract unit price and measure
            unit_price_match = re.search(r'(\d+[,\.]\d+)\s*€/(kg|l|ud|unidad)', page_text, re.IGNORECASE)
            if unit_price_match:
                product['unit_price'] = float(unit_price_match.group(1).replace(',', '.'))
                product['unit_measure'] = unit_price_match.group(2)

            # Extract images
            try:
                # Look for product images (usually larger images)
                images = self.driver.find_elements(By.TAG_NAME, "img")
                for img in images:
                    src = img.get_attribute('src')
                    alt = img.get_attribute('alt')
                    # Filter out small icons and logos
                    if src and ('prod' in src.lower() or (alt and len(alt) > 10)):
                        if not any(x in src.lower() for x in ['logo', 'icon', 'banner']):
                            product['image_url'] = src
                            logger.debug(f"Found image: {src[:100]}")
                            break
            except Exception as e:
                logger.warning(f"Could not extract images: {e}")

            # Try to extract from JSON-LD structured data
            page_source = self.driver.page_source
            json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page_source, re.DOTALL)

            for json_str in json_ld_matches:
                try:
                    structured_data = json.loads(json_str)
                    if isinstance(structured_data, dict):
                        # Update with structured data if available
                        if structured_data.get('name'):
                            product['name'] = structured_data['name']
                        if structured_data.get('brand'):
                            brand_data = structured_data['brand']
                            if isinstance(brand_data, dict):
                                product['brand'] = brand_data.get('name', '')
                            else:
                                product['brand'] = str(brand_data)
                        if structured_data.get('description'):
                            product['description'] = structured_data['description']

                        # Extract price from offers
                        if 'offers' in structured_data:
                            offers = structured_data['offers']
                            if isinstance(offers, dict):
                                price_val = offers.get('price')
                                if price_val:
                                    try:
                                        product['price'] = float(price_val)
                                    except:
                                        pass

                        # Extract images
                        if structured_data.get('image'):
                            images = structured_data['image']
                            if isinstance(images, list) and len(images) > 0:
                                product['image_url'] = images[0]
                            elif isinstance(images, str):
                                product['image_url'] = images

                        # Extract EAN/GTIN
                        for key in ['gtin13', 'gtin', 'ean']:
                            if structured_data.get(key):
                                product['ean'] = str(structured_data[key])
                                break

                except json.JSONDecodeError:
                    continue

            return product

        except Exception as e:
            logger.error(f"Error extracting product data: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {}

    @staticmethod
    def extract_product_id(url: str) -> str:
        """Extract product ID from URL"""
        match = re.search(r'/product/(\d+)/', url)
        if match:
            return match.group(1)
        return ''
