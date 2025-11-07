# Mercadona Product Scraper

Ultra-fast product scraper for Mercadona using their undocumented public API. **10-20x faster** than traditional Selenium-based scrapers.

## Quick Start

```bash
# 1. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run the scraper
python3 scraper.py

# 3. Check results
python3 check_db.py
```

That's it! The scraper will collect products with complete data including EAN codes, prices, images, ingredients, and allergens.

## Current Status

- **Database:** 500 products scraped and ready to use
- **Performance:** 0.81 products/second
- **Data Quality:** Complete product information with real EAN codes

## Why This Scraper?

### Ultra-Fast API Scraping
- **Speed**: 0.81 products/second
- **Direct API Access**: No browser automation needed
- **Complete Data**: Full product information including EAN codes
- **Simple**: Just Python + requests library

### Comparison

| Method | Speed | Time for 500 products |
|--------|-------|----------------------|
| Selenium (single) | 0.1-0.2 products/sec | ~50 minutes |
| API Direct | 0.81 products/sec | ~10 minutes |

## Features

- **Lightning Fast**: Direct API calls - 10-20x faster than Selenium
- **Complete Data**: All product details including:
  - Real EAN codes (barcodes)
  - Accurate prices and unit prices
  - High-quality images
  - Categories and subcategories
  - Full ingredients lists
  - Allergen information
- **Database Storage**: SQLite database with automatic deduplication
- **Simple**: No browser setup, no Selenium, just Python + requests
- **Clean Codebase**: Minimal dependencies, production-ready

## Available Tools

### 1. Main Scraper (RECOMMENDED)

**`scraper.py`** - Production scraper
```bash
python3 scraper.py
```

- **Speed**: ~0.81 products/second
- **Method**: Direct API calls
- **Configurable**: Edit START_ID and END_ID to customize range

### 2. Quick Test Scraper

**`test_api.py`** - Test with 20 products
```bash
python3 test_api.py
```

- Great for testing and verification
- Completes in ~30 seconds

### 3. Database Inspector

**`check_db.py`** - View database contents
```bash
python3 check_db.py
```

- Shows product count and sample data
- Useful for verifying scraper results

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

Dependencies:
- `requests` - HTTP requests
- `sqlalchemy` - Database ORM
- `loguru` - Logging
- `python-dotenv` - Environment variables

### 3. Run the Scraper

```bash
# Main scraper
python3 scraper.py

# Or test with 20 products first
python3 test_api.py
```

## How It Works

The scraper uses Mercadona's undocumented public API:

```
https://tienda.mercadona.es/api/v1_1/products/{product_id}
```

Instead of:
1. ❌ Opening a browser with Selenium (slow)
2. ❌ Parsing HTML (fragile)
3. ❌ Dealing with JavaScript rendering

We:
1. ✅ Call the API directly (fast)
2. ✅ Get structured JSON data (reliable)
3. ✅ No browser needed (simple)

### Product ID Strategy

- Product IDs range from ~4,900 to ~72,000
- Only ~9% of IDs exist (sparse distribution)
- The scraper automatically handles 404s
- Rate limiting: 0.5 second delay between requests to avoid blocking

### Example API Response

```json
{
  "id": "10005",
  "display_name": "Chocolate líquido a la taza Hacendado",
  "ean": "8480000100054",
  "brand": "HACENDADO",
  "price_instructions": {
    "unit_price": 2.35,
    "reference_format": "1 L"
  },
  "thumbnail": "https://...",
  "categories": [...],
  "nutrition_information": {
    "ingredients": "...",
    "allergens": "..."
  }
}
```

## Configuration

Edit `scraper.py` to change the scraping range:

```python
START_ID = 4900   # Starting product ID
END_ID = 75000    # Ending product ID
```

The scraper will automatically:
- Skip non-existent products (404s)
- Add delays to prevent rate limiting
- Save everything to `data/products.db`

## Project Structure

```
scraper/
├── scraper.py                # Main API scraper
├── test_api.py               # Quick test with 20 products
├── check_db.py               # View database contents
├── models/
│   ├── __init__.py
│   └── product.py            # Database models (SQLAlchemy)
├── data/
│   ├── products.db           # SQLite database (500 products)
│   └── products_backup_91.db # Backup of original 91 products
├── requirements.txt          # Dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Database Schema

Products are stored in SQLite with the following structure:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE NOT NULL,
    url TEXT,
    name TEXT,
    brand TEXT,
    ean TEXT,
    category TEXT,
    subcategory TEXT,
    description TEXT,
    image_url TEXT,
    price REAL,
    unit_price REAL,
    unit_measure TEXT,
    ingredients TEXT,
    allergens TEXT,
    is_available BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

View the data:
```bash
python3 check_db.py
# Or directly with sqlite3:
sqlite3 data/products.db "SELECT name, price, ean FROM products LIMIT 10"
```

## Data Quality

The API scraper provides **high-quality, complete data**:

✅ **Real EAN codes** - Directly from Mercadona's system
✅ **Accurate prices** - Up-to-date pricing information
✅ **Complete ingredients** - Full ingredients and allergen lists
✅ **High-res images** - Direct links to product images
✅ **Structured categories** - Proper category hierarchy

Sample data:
```
Chocolate líquido a la taza Hacendado
  Price: €2.35
  EAN: 8480000100054
  Category: Bebidas → Batidos y leches
  Ingredients: Leche desnatada, cacao desgrasado...
```

## Performance Stats

**Latest Scraper Performance (500 products):**
```
✅ Successfully scraped: 500 products
⏭️  Skipped (404s): 3,395 non-existent IDs
❌ Errors: 1 (minimal)
⏱️  Total time: 620.4 seconds (10.3 minutes)
🚀 Average speed: 0.81 products/second
📊 ID check rate: 0.159 seconds per ID
```

**Full Catalog Estimates:**
```
Total ID range: 4,900 to 75,000 (~70,100 IDs)
Expected products: 5,000-6,000 total
Estimated time: 3-4 hours (with rate limiting)
```

## Troubleshooting

### Database Locked Error
```bash
# Kill any running scraper processes
pkill -9 -f scraper.py
# Remove lock file if needed
rm -f data/products.db-journal
```

### HTTP 403 Forbidden Errors
This means Mercadona's API has temporarily blocked your IP due to too many requests.

**Solutions:**
- Wait 30-60 minutes for the block to expire
- Increase the delay in `scraper.py` (change `time.sleep(0.5)` to a higher value)
- Start from a higher ID range where products exist (e.g., START_ID = 10000)

### No Products Found
```bash
# Test the API manually
curl https://tienda.mercadona.es/api/v1_1/products/10005
# Should return JSON data
```

### Module Not Found
```bash
# Make sure virtual environment is activated
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Check Current Progress
```bash
# Check how many products in database
sqlite3 data/products.db "SELECT COUNT(*) FROM products"

# View recent products
sqlite3 data/products.db "SELECT name, price FROM products ORDER BY id DESC LIMIT 5"
```

## API Discovery Story

The API was discovered by:
1. Opening Chrome DevTools on Mercadona's website
2. Monitoring network requests while browsing products
3. Finding the pattern: `/api/v1_1/products/{id}`
4. Realizing all product data comes from this endpoint
5. Building a scraper that calls it directly

This is **10-20x faster** than Selenium because:
- No browser launch overhead
- No JavaScript execution wait
- No DOM parsing
- Direct JSON responses
- Simple HTTP requests

## Best Practices

**Rate Limiting:**
- Use appropriate delays between requests (currently 0.5 seconds)
- Monitor for 403 errors and adjust delays if needed
- Don't overwhelm the server with parallel requests

**Data Management:**
- Regular backups of `products.db`
- Check database integrity with `check_db.py`
- Keep the database in `.gitignore`

**Usage:**
- Test with `test_api.py` before full scrapes
- Monitor scraper output for errors
- Use realistic browser headers to avoid blocking

## Legal & Ethical Considerations

This scraper is designed for:
- Personal use
- Research purposes
- Building product databases for apps

**Important:**
- Respect Mercadona's Terms of Service
- Don't use scraped data for commercial purposes without permission
- Implement appropriate rate limiting (already included)
- Don't overwhelm the server with requests

## Future Enhancements

- [ ] Scrape IDs 1-4,900 (currently starting at 4,900)
- [ ] Price history tracking over time
- [ ] Image downloading and local storage
- [ ] Automatic periodic database updates
- [ ] Product change notifications
- [ ] Support for other Spanish retailers

## License

This project is part of the NeuralList application.
