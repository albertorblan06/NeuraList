"""
ULTRA-FAST Mercadona API Spider
Uses direct API calls - 10-20x faster than Selenium!
"""
import scrapy
from scrapy.spiders import SitemapSpider
from loguru import logger
import json

class MercadonaAPISpider(SitemapSpider):
    """Lightning-fast API-based spider"""

    name = 'mercadona_api'
    allowed_domains = ['tienda.mercadona.es']
    sitemap_urls = ['https://tienda.mercadona.es/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product_url'),
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 20,  # Process 20 at once!
        'DOWNLOAD_DELAY': 0.1,      # Minimal delay
        'ROBOTSTXT_OBEY': True,
    }

    def parse_product_url(self, response):
        """Extract product ID from URL and call API"""
        url = response.url

        # Extract product ID from URL: /product/10005/name
        try:
            product_id = url.split('/product/')[1].split('/')[0]
        except:
            logger.warning(f"Could not extract ID from {url}")
            return

        # Call the API instead of parsing HTML
        api_url = f"https://tienda.mercadona.es/api/v1_1/products/{product_id}"
        yield scrapy.Request(
            api_url,
            callback=self.parse_api_response,
            meta={'product_id': product_id, 'url': url},
            dont_filter=True
        )

    def parse_api_response(self, response):
        """Parse JSON API response"""
        try:
            data = json.loads(response.text)
            product_id = response.meta['product_id']

            # Extract all the good stuff from JSON
            product = {
                'product_id': product_id,
                'url': response.meta['url'],
                'name': data.get('display_name', ''),
                'brand': data.get('brand', ''),
                'ean': data.get('ean'),
                'category': self._extract_category(data.get('categories', [])),
                'subcategory': self._extract_subcategory(data.get('categories', [])),
                'description': data.get('details', {}).get('description', ''),
                'image_url': data.get('thumbnail', ''),
                'price': float(data.get('price_instructions', {}).get('unit_price', 0) or 0),
                'unit_price': float(data.get('price_instructions', {}).get('bulk_price', 0) or 0),
                'unit_measure': data.get('price_instructions', {}).get('reference_format', ''),
                'ingredients': data.get('nutrition_information', {}).get('ingredients', ''),
                'allergens': data.get('nutrition_information', {}).get('allergens', ''),
                'is_available': data.get('published', True),
            }

            if product['name']:
                logger.info(f"✅ {product['name']} - €{product['price']}")
                yield product
            else:
                logger.warning(f"No name for product {product_id}")

        except Exception as e:
            logger.error(f"Error parsing API response for {response.url}: {e}")

    def _extract_category(self, categories):
        """Extract top-level category"""
        try:
            if categories and len(categories) > 0:
                return categories[0].get('name', '')
        except:
            pass
        return ''

    def _extract_subcategory(self, categories):
        """Extract second-level category"""
        try:
            if categories and len(categories) > 0:
                sub_cats = categories[0].get('categories', [])
                if sub_cats:
                    return sub_cats[0].get('name', '')
        except:
            pass
        return ''
