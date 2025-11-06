"""
Ultra-fast direct API scraper - NO SITEMAP NEEDED!
Iterates through product IDs and calls API directly
"""
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.product import Product, Base
from loguru import logger
import time

# Setup database
engine = create_engine('sqlite:///data/products.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Start from product ID 10000 and try 5500 IDs to get 500 products
# (some IDs won't exist, that's normal - about 9% hit rate)
START_ID = 10000
END_ID = 15500  # Try 5500 IDs to get ~500 valid products

logger.info(f"🚀 Starting ULTRA-FAST API scraper")
logger.info(f"Trying product IDs from {START_ID} to {END_ID}")

success_count = 0
not_found_count = 0
error_count = 0

start_time = time.time()

for product_id in range(START_ID, END_ID):
    api_url = f"https://tienda.mercadona.es/api/v1_1/products/{product_id}"

    try:
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
                product_id=str(product_id),
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
            existing = session.query(Product).filter_by(product_id=str(product_id)).first()
            if existing:
                session.delete(existing)

            session.add(product)
            session.commit()

            success_count += 1
            if success_count % 10 == 0:
                elapsed = time.time() - start_time
                rate = success_count / elapsed
                logger.info(f"✅ {success_count} products | {rate:.1f} products/sec")

            if success_count % 50 == 0:
                logger.success(f"🎯 Milestone: {success_count} products scraped!")

        elif response.status_code == 404:
            not_found_count += 1
            if not_found_count % 100 == 0:
                logger.debug(f"Skipped {not_found_count} non-existent product IDs")
        else:
            error_count += 1
            logger.warning(f"HTTP {response.status_code} for product {product_id}")

    except requests.exceptions.Timeout:
        error_count += 1
        logger.warning(f"Timeout for product {product_id}")
    except Exception as e:
        error_count += 1
        logger.error(f"Error fetching product {product_id}: {e}")

    # Stop if we've reached 500 products
    if success_count >= 500:
        logger.success(f"🎉 TARGET REACHED! {success_count} products scraped!")
        break

elapsed_time = time.time() - start_time

# Final summary
logger.info(f"\n{'='*60}")
logger.success(f"🎉 SCRAPING COMPLETE!")
logger.info(f"{'='*60}")
logger.info(f"✅ Successfully scraped: {success_count} products")
logger.info(f"⏭️  Skipped (404s): {not_found_count} IDs")
logger.info(f"❌ Errors: {error_count}")
logger.info(f"⏱️  Total time: {elapsed_time:.1f} seconds")
logger.info(f"🚀 Average speed: {success_count/elapsed_time:.2f} products/second")
logger.info(f"{'='*60}\n")

# Show sample products
total = session.query(Product).count()
logger.info(f"Total products in database: {total}")

products = session.query(Product).limit(5).all()
logger.info("\nFirst 5 products:")
for p in products:
    logger.info(f"  • {p.name} - €{p.price} - EAN: {p.ean}")

session.close()
