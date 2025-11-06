"""
Database models for product storage
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Product(Base):
    """Product model for storing Mercadona products"""

    __tablename__ = 'products'

    # Primary identifiers
    id = Column(Integer, primary_key=True, autoincrement=True)
    ean = Column(String(13), unique=False, nullable=True, index=True)  # Not unique, many products don't have EAN
    product_id = Column(String(50), unique=True, nullable=False, index=True)

    # Basic information
    name = Column(String(255), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    subcategory = Column(String(100))

    # Pricing
    price = Column(Float, nullable=False)
    unit_price = Column(Float)
    unit_measure = Column(String(20))  # e.g., "€/L", "€/kg"

    # Product details
    description = Column(Text)
    ingredients = Column(Text)
    allergens = Column(Text)
    nutritional_info = Column(Text)

    # Images
    image_url = Column(String(500))
    thumbnail_url = Column(String(500))

    # Availability
    is_available = Column(Boolean, default=True)
    stock_status = Column(String(50))

    # Metadata
    url = Column(String(500))
    scrape_date = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Product(ean={self.ean}, name={self.name}, price={self.price})>"
