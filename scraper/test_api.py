"""
Quick test script to scrape a few products using the API directly
"""
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.product import Product, Base
from loguru import logger

# Setup database
engine = create_engine('sqlite:///data/products.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Test with a few known product IDs
test_ids = ['10005', '10010', '10015', '10020', '10025', '10030', '10035', '10040', '10045', '10050',
            '10055', '10060', '10065', '10070', '10075', '10080', '10085', '10090', '10095', '10100']

logger.info(f"Testing API scraping with {len(test_ids)} products...")

success_count = 0
for product_id in test_ids:
    api_url = f"https://tienda.mercadona.es/api/v1_1/products/{product_id}"

    try:
        logger.info(f"Fetching: {api_url}")
        response = requests.get(api_url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Extract categories
            categories = data.get('categories', [])
            category = categories[0].get('name', '') if categories else ''
            subcategory = ''
            if categories and categories[0].get('categories'):
                subcategory = categories[0]['categories'][0].get('name', '')

            # Create product
            product = Product(
                product_id=product_id,
                url=f"https://tienda.mercadona.es/product/{product_id}",
                name=data.get('display_name', ''),
                brand=data.get('brand', ''),
                ean=data.get('ean'),
                category=category,
                subcategory=subcategory,
                description=data.get('details', {}).get('description', ''),
                image_url=data.get('thumbnail', ''),
                price=float(data.get('price_instructions', {}).get('unit_price', 0) or 0),
                unit_price=float(data.get('price_instructions', {}).get('bulk_price', 0) or 0),
                unit_measure=data.get('price_instructions', {}).get('reference_format', ''),
                ingredients=data.get('nutrition_information', {}).get('ingredients', ''),
                allergens=data.get('nutrition_information', {}).get('allergens', ''),
                is_available=data.get('published', True),
            )

            # Check if already exists
            existing = session.query(Product).filter_by(product_id=product_id).first()
            if existing:
                session.delete(existing)

            session.add(product)
            session.commit()

            logger.success(f"✅ {product.name} - €{product.price} - EAN: {product.ean}")
            success_count += 1
        else:
            logger.warning(f"HTTP {response.status_code} for product {product_id}")

    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")

logger.info(f"\n🎉 Successfully scraped {success_count}/{len(test_ids)} products!")

# Show summary
total = session.query(Product).count()
logger.info(f"Total products in database: {total}")

# Show first 5
products = session.query(Product).limit(5).all()
logger.info("\nFirst 5 products:")
for p in products:
    logger.info(f"  - {p.name} (€{p.price}) - EAN: {p.ean}")

session.close()
