#!/bin/bash
cd "$(dirname "$0")"
rm -f data/products.db
source venv/bin/activate
scrapy crawl mercadona_sitemap -s CLOSESPIDER_ITEMCOUNT=10 -s LOG_FILE=scraper.log -s LOG_LEVEL=INFO
echo "Scraper finished. Checking results..."
python3 check_db.py
