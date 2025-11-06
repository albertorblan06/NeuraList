#!/usr/bin/env python3
"""
Convenience script to run the Mercadona scraper

Usage:
    python run_scraper.py
    python run_scraper.py --postal-code 08001
    python run_scraper.py --output products.json
"""
import sys
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from loguru import logger


def main():
    parser = argparse.ArgumentParser(description='Run Mercadona product scraper')
    parser.add_argument(
        '--postal-code',
        default='28001',
        help='Spanish postal code for product availability (default: 28001 - Madrid)'
    )
    parser.add_argument(
        '--output',
        help='Output file (supports .json, .csv, .xml)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of items to scrape (for testing)'
    )

    args = parser.parse_args()

    # Configure loguru
    logger.remove()
    logger.add(sys.stderr, level=args.log_level)
    logger.add("scraper.log", rotation="10 MB", level=args.log_level)

    logger.info("Starting Mercadona scraper")
    logger.info(f"Postal code: {args.postal_code}")

    # Get Scrapy settings
    settings = get_project_settings()
    settings.set('LOG_LEVEL', args.log_level)

    if args.output:
        settings.set('FEEDS', {
            args.output: {
                'format': args.output.split('.')[-1],
                'overwrite': True,
            }
        })
        logger.info(f"Output will be saved to: {args.output}")

    if args.limit:
        settings.set('CLOSESPIDER_ITEMCOUNT', args.limit)
        logger.info(f"Will scrape maximum {args.limit} items")

    # Create and configure process
    process = CrawlerProcess(settings)

    # Import spider
    from spiders.mercadona_spider import MercadonaSpider

    # Start crawling
    process.crawl(MercadonaSpider, postal_code=args.postal_code)
    process.start()

    logger.info("Scraping completed")


if __name__ == '__main__':
    main()
