"""
Mercadona product scraper spider

This spider scrapes product information from Mercadona's online store.
It implements rate limiting, retry logic, and respects robots.txt.

Usage:
    scrapy crawl mercadona -a postal_code=28001
"""
import scrapy
import json
from loguru import logger
from typing import Generator, Dict, Any
import re


class MercadonaSpider(scrapy.Spider):
    """Spider for scraping Mercadona products"""

    name = 'mercadona'
    allowed_domains = ['tienda.mercadona.es']

    custom_settings = {
        'DOWNLOAD_DELAY': 2.0,
        'CONCURRENT_REQUESTS': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'HTTPCACHE_ENABLED': True,
    }

    def __init__(self, postal_code='28001', *args, **kwargs):
        """
        Initialize spider with postal code for location-based products

        Args:
            postal_code: Spanish postal code (default: 28001 - Madrid)
        """
        super().__init__(*args, **kwargs)
        self.postal_code = postal_code
        self.base_url = 'https://tienda.mercadona.es'
        self.api_url = f'{self.base_url}/api'

        logger.info(f"Initializing Mercadona spider for postal code: {postal_code}")

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """
        Start the scraping process

        Mercadona's website requires:
        1. Setting a postal code
        2. Getting categories
        3. Iterating through products in each category
        """
        # First, we need to set the postal code
        yield scrapy.Request(
            url=f'{self.api_url}/postal-codes/{self.postal_code}',
            callback=self.parse_postal_code,
            errback=self.handle_error,
            dont_filter=True
        )

    def parse_postal_code(self, response):
        """
        Parse postal code response and fetch categories

        The API returns information about available stores for the postal code
        """
        try:
            data = json.loads(response.text)
            logger.info(f"Postal code validated: {data}")

            # Now fetch categories
            yield scrapy.Request(
                url=f'{self.api_url}/categories',
                callback=self.parse_categories,
                errback=self.handle_error
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse postal code response: {e}")

    def parse_categories(self, response):
        """
        Parse categories and subcategories

        Mercadona organizes products in a hierarchical structure:
        Categories > Subcategories > Products
        """
        try:
            data = json.loads(response.text)
            categories = data.get('results', [])

            logger.info(f"Found {len(categories)} categories")

            for category in categories:
                category_id = category.get('id')
                category_name = category.get('name')

                logger.info(f"Processing category: {category_name} (ID: {category_id})")

                # Fetch products for this category
                yield scrapy.Request(
                    url=f'{self.api_url}/categories/{category_id}',
                    callback=self.parse_category_products,
                    meta={
                        'category_id': category_id,
                        'category_name': category_name
                    },
                    errback=self.handle_error
                )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse categories: {e}")

    def parse_category_products(self, response):
        """
        Parse products within a category
        """
        try:
            data = json.loads(response.text)
            category_name = response.meta.get('category_name')

            # Categories may have subcategories
            subcategories = data.get('categories', [])

            if subcategories:
                for subcategory in subcategories:
                    products = subcategory.get('products', [])
                    subcategory_name = subcategory.get('name')

                    logger.info(f"Found {len(products)} products in {category_name} > {subcategory_name}")

                    for product_data in products:
                        yield self.parse_product(product_data, category_name, subcategory_name)
            else:
                # No subcategories, products are directly under category
                products = data.get('products', [])
                logger.info(f"Found {len(products)} products in {category_name}")

                for product_data in products:
                    yield self.parse_product(product_data, category_name, None)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse category products: {e}")

    def parse_product(self, product_data: Dict[str, Any], category: str, subcategory: str) -> Dict[str, Any]:
        """
        Parse individual product data

        Args:
            product_data: Raw product data from API
            category: Category name
            subcategory: Subcategory name (can be None)

        Returns:
            Cleaned product dictionary
        """
        try:
            # Extract product information
            product = {
                'ean': product_data.get('ean', ''),
                'product_id': product_data.get('id', ''),
                'name': product_data.get('display_name', ''),
                'brand': product_data.get('brand', ''),
                'category': category,
                'subcategory': subcategory,
                'price': self.parse_price(product_data.get('price_instructions', {})),
                'unit_price': self.parse_unit_price(product_data.get('price_instructions', {})),
                'unit_measure': product_data.get('price_instructions', {}).get('unit_name', ''),
                'description': product_data.get('details', {}).get('description', ''),
                'ingredients': self.extract_ingredients(product_data.get('details', {})),
                'allergens': self.extract_allergens(product_data.get('details', {})),
                'nutritional_info': json.dumps(product_data.get('details', {}).get('nutrition_information', {})),
                'image_url': self.get_image_url(product_data.get('photos', [])),
                'thumbnail_url': self.get_thumbnail_url(product_data.get('thumbnail', '')),
                'is_available': product_data.get('is_available', True),
                'stock_status': 'in_stock' if product_data.get('is_available') else 'out_of_stock',
                'url': f"{self.base_url}/product/{product_data.get('id', '')}"
            }

            logger.debug(f"Parsed product: {product['name']} (EAN: {product['ean']})")
            return product

        except Exception as e:
            logger.error(f"Error parsing product: {e}")
            return {}

    @staticmethod
    def parse_price(price_instructions: Dict) -> float:
        """Extract main price from price instructions"""
        try:
            return float(price_instructions.get('unit_price', 0.0))
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def parse_unit_price(price_instructions: Dict) -> float:
        """Extract unit price (e.g., price per kg)"""
        try:
            reference_price = price_instructions.get('reference_price', '')
            # Extract numeric value from string like "2.50 €/kg"
            match = re.search(r'(\d+\.?\d*)', reference_price)
            return float(match.group(1)) if match else 0.0
        except (ValueError, TypeError, AttributeError):
            return 0.0

    @staticmethod
    def extract_ingredients(details: Dict) -> str:
        """Extract ingredients from product details"""
        ingredients = details.get('ingredients', '')
        return ingredients if isinstance(ingredients, str) else ''

    @staticmethod
    def extract_allergens(details: Dict) -> str:
        """Extract allergens from product details"""
        allergens = details.get('allergens', [])
        if isinstance(allergens, list):
            return ', '.join(allergens)
        return str(allergens) if allergens else ''

    @staticmethod
    def get_image_url(photos: list) -> str:
        """Get main product image URL"""
        if photos and len(photos) > 0:
            return photos[0].get('zoom', '')
        return ''

    @staticmethod
    def get_thumbnail_url(thumbnail: str) -> str:
        """Get thumbnail image URL"""
        return thumbnail if thumbnail else ''

    def handle_error(self, failure):
        """Handle request errors"""
        logger.error(f"Request failed: {failure.request.url}")
        logger.error(f"Error: {failure.value}")
