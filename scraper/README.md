# Mercadona Product Scraper

A robust web scraper for collecting product data from Mercadona's online store. Built with Scrapy, it implements rate limiting, retry logic, and respects robots.txt to ensure ethical scraping.

## Features

- **Rate Limiting**: Configurable delays between requests to avoid overwhelming the server
- **Auto-Throttling**: Automatically adjusts request rate based on server response times
- **Retry Logic**: Automatic retry on failed requests with configurable backoff
- **HTTP Caching**: Reduces redundant requests and speeds up development
- **Database Storage**: SQLAlchemy-based storage supporting PostgreSQL and SQLite
- **Structured Data**: Captures product details including:
  - EAN codes
  - Names and brands
  - Prices and unit prices
  - Categories and subcategories
  - Images and thumbnails
  - Ingredients and allergens
  - Nutritional information

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DATABASE_URL=sqlite:///data/products.db  # or PostgreSQL URL
DOWNLOAD_DELAY=2.0
CONCURRENT_REQUESTS=1
```

### 4. Run the Scraper

```bash
# Using default postal code (28001 - Madrid)
scrapy crawl mercadona

# With custom postal code
scrapy crawl mercadona -a postal_code=08001  # Barcelona
```

## Usage

### Basic Scraping

```bash
# Scrape all products for Madrid
scrapy crawl mercadona -a postal_code=28001

# Save output to JSON
scrapy crawl mercadona -o products.json

# Save output to CSV
scrapy crawl mercadona -o products.csv
```

### Testing the Scraper

```bash
# Run with verbose logging
scrapy crawl mercadona -L DEBUG

# Test with limited requests
scrapy crawl mercadona -s CLOSESPIDER_ITEMCOUNT=100
```

## Project Structure

```
scraper/
├── config/
│   └── settings.py          # Scrapy settings
├── models/
│   └── product.py           # Database models
├── spiders/
│   └── mercadona_spider.py  # Main spider
├── utils/                   # Utility functions
├── data/                    # SQLite database location
├── pipelines.py             # Data processing pipelines
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## How It Works

### 1. Postal Code Validation

The scraper starts by validating a Spanish postal code, which Mercadona uses to determine product availability and pricing.

### 2. Category Discovery

It fetches all product categories from Mercadona's API.

### 3. Product Extraction

For each category and subcategory, it extracts:
- Product metadata (name, brand, EAN)
- Pricing information
- Images
- Nutritional data
- Availability status

### 4. Data Storage

Products are stored in a database with automatic deduplication based on EAN codes.

## Best Practices

### Rate Limiting

To avoid being blocked:
- Keep `DOWNLOAD_DELAY` at minimum 2 seconds
- Use `CONCURRENT_REQUESTS=1` for single-threaded scraping
- Enable `AUTOTHROTTLE` to automatically adjust speed

### Ethical Scraping

- Respect `robots.txt` (enabled by default)
- Don't scrape during peak hours
- Cache responses to avoid redundant requests
- Identify your bot with a proper `USER_AGENT`

### Data Quality

- The scraper handles missing fields gracefully
- EAN codes are used as primary keys to prevent duplicates
- Timestamps track when data was collected

## Troubleshooting

### Connection Errors

If you encounter connection errors:
```bash
# Increase delay between requests
DOWNLOAD_DELAY=5.0 scrapy crawl mercadona
```

### Database Errors

For SQLite permission issues:
```bash
mkdir -p data
chmod 755 data
```

For PostgreSQL connection issues, verify your `DATABASE_URL` format:
```
postgresql://username:password@localhost:5432/database_name
```

### IP Blocking

If your IP gets blocked:
1. Wait several hours before trying again
2. Increase `DOWNLOAD_DELAY` to 5+ seconds
3. Consider using rotating proxies (advanced)

## Future Enhancements

- [ ] Image downloading and local storage
- [ ] Price history tracking
- [ ] Support for multiple retailers
- [ ] Proxy rotation for larger scale scraping
- [ ] Selenium integration for JavaScript-heavy pages
- [ ] Product change notifications

## Legal & Ethical Considerations

This scraper is designed for:
- Personal use
- Research purposes
- Building product databases for apps

**Important:**
- Respect Mercadona's Terms of Service
- Don't use scraped data for commercial purposes without permission
- Implement appropriate rate limiting
- Don't overwhelm the server with requests

## Contributing

Contributions are welcome! Areas for improvement:
- Additional data extraction (reviews, related products)
- Better error handling
- Performance optimizations
- Support for more Spanish retailers

## License

This project is part of the NeuralList application.
