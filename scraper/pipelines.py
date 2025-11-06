"""
Item pipelines for processing scraped data
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
import os
from models.product import Product, Base


class ProductPipeline:
    """Pipeline for storing products in database"""

    def __init__(self):
        self.engine = None
        self.Session = None

    def open_spider(self, spider):
        """Initialize database connection when spider opens"""
        database_url = os.getenv('DATABASE_URL', 'sqlite:///data/products.db')
        logger.info(f"Connecting to database: {database_url}")

        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database connection established")

    def close_spider(self, spider):
        """Close database connection when spider closes"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

    def process_item(self, item, spider):
        """Process and store each scraped item"""
        session = self.Session()

        try:
            # Check if product already exists
            existing_product = session.query(Product).filter_by(
                ean=item.get('ean')
            ).first()

            if existing_product:
                # Update existing product
                for key, value in item.items():
                    setattr(existing_product, key, value)
                logger.info(f"Updated product: {item.get('name')} (EAN: {item.get('ean')})")
            else:
                # Create new product
                product = Product(**item)
                session.add(product)
                logger.info(f"Added new product: {item.get('name')} (EAN: {item.get('ean')})")

            session.commit()
            return item

        except Exception as e:
            session.rollback()
            logger.error(f"Error processing item: {e}")
            raise

        finally:
            session.close()
