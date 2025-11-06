# NeuralList - Context for Claude Sessions

## Project Overview

**NeuralList** is an AI-powered visual shopping assistant mobile app built with Flutter. The app allows users to:
- Take photos of their shopping lists (handwritten or printed)
- AI extracts products from the images
- App matches products with Mercadona inventory
- Shows prices, availability, and product details
- Helps users complete their shopping efficiently

## Repository Structure

```
NeuraList/
├── lib/                  # Flutter app source code
├── ios/                  # iOS native code and configuration
├── android/              # Android native code (to be set up)
├── scraper/              # Python web scraper for Mercadona products
│   ├── spiders/          # Scrapy spiders
│   │   ├── mercadona_api_spider.py        # ⭐ MAIN SPIDER - Ultra-fast API
│   │   ├── mercadona_parallel_spider.py   # Backup: Parallel Selenium
│   │   └── mercadona_sitemap_spider.py    # Old: Single Selenium (slow)
│   ├── models/           # Database models (SQLAlchemy)
│   ├── config/           # Scrapy settings
│   ├── pipelines.py      # Data processing pipeline
│   ├── find_api.py       # Tool to discover API endpoints
│   ├── test_api.py       # Direct API testing script
│   ├── check_db.py       # Database inspection utility
│   └── data/             # SQLite database (gitignored)
└── CONTEXT_FOR_CLAUDE.md # This file
```

## Development Environment

### Setup Status

✅ **Completed:**
- Flutter installed and working
- Xcode 16.3 installed
- iOS development environment configured
- Flutter project created with iOS simulator working
- Python 3.13 virtual environment set up
- Scrapy + Selenium scraper infrastructure
- SQLite database schema
- Git repository connected to GitHub

⏳ **In Progress:**
- Xcode platforms download (running in background)
- Scraping Mercadona product database

❌ **Not Started:**
- Android development setup
- Flutter app implementation
- AI/OCR integration
- Backend API

### Key Commands

```bash
# Flutter
cd ~/Documents/NeuraList
flutter run                      # Run on iOS simulator
flutter doctor                   # Check Flutter setup

# Scraper
cd ~/Documents/NeuraList/scraper
source venv/bin/activate         # Activate Python virtual environment
scrapy crawl mercadona_api -s CLOSESPIDER_ITEMCOUNT=100  # Run API spider
python3 check_db.py              # Check database contents
python3 test_api.py              # Test API directly
```

## 🚀 MAJOR BREAKTHROUGH: Mercadona API Discovery

### The Problem
Original Selenium-based scraper was extremely slow:
- 5-10 seconds per product
- Single-threaded browser automation
- Would take hours to scrape thousands of products

### The Solution
Discovered Mercadona's **undocumented public API**!

**API Endpoint:**
```
https://tienda.mercadona.es/api/v1_1/products/{product_id}
```

**Example:**
```bash
curl "https://tienda.mercadona.es/api/v1_1/products/10005"
```

### API Response Structure

The API returns complete product data in JSON format:

```json
{
  "id": "10005",
  "ean": "8480000100054",
  "brand": "Hacendado",
  "display_name": "Chocolate líquido a la taza Hacendado",
  "price_instructions": {
    "unit_price": "2.35",
    "bulk_price": "2.35",
    "reference_format": "L"
  },
  "categories": [
    {
      "id": 8,
      "name": "Cacao, café e infusiones",
      "categories": [
        {
          "id": 86,
          "name": "Cacao soluble y chocolate a la taza"
        }
      ]
    }
  ],
  "nutrition_information": {
    "allergens": "Contiene leche...",
    "ingredients": "Leche parcialmente desnatada..."
  },
  "photos": [...],
  "details": {
    "description": "...",
    "origin": "Córdoba"
  }
}
```

### Speed Comparison

| Method | Speed per Product | Total for 1000 products |
|--------|------------------|------------------------|
| Selenium (old) | 5-10 seconds | 🐌 1.5-3 hours |
| Parallel Selenium | 2-3 seconds | ⚠️ 30-50 minutes |
| **API Spider** | **0.2 seconds** | ⚡ **3-4 minutes** |

## Current Database Schema

**Table: `products`**

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| product_id | String(50) | Mercadona product ID (unique) |
| url | String(500) | Product page URL |
| name | String(200) | Product name |
| brand | String(100) | Brand name |
| ean | String(13) | EAN barcode (nullable) |
| category | String(100) | Main category |
| subcategory | String(100) | Subcategory |
| description | Text | Product description |
| image_url | String(500) | Thumbnail image URL |
| price | Float | Unit price in EUR |
| unit_price | Float | Price per reference unit |
| unit_measure | String(50) | Reference unit (L, kg, etc.) |
| ingredients | Text | Ingredients list |
| allergens | Text | Allergen information |
| is_available | Boolean | Product availability |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Git History & Important Commits

### Recent Commits

1. **62c9988** - "Add ultra-fast Mercadona API spider + discovery tools"
   - Added `mercadona_api_spider.py` (MAIN SPIDER)
   - Added `mercadona_parallel_spider.py` (backup)
   - Added `find_api.py` (API discovery tool)
   - Added `test_api.py` (API testing script)

2. **fef4a76** - "Update scraper with product model fixes"
   - Fixed EAN field constraint (made nullable, non-unique)
   - Added retry logic to sitemap spider
   - Many products don't have EAN codes

3. **Earlier commits** - Initial project setup
   - Flutter project initialization
   - Scraper infrastructure
   - Database models
   - Basic Selenium spider

### GitHub Repository

**URL:** `https://github.com/albertorblan06/NeuraList.git`
**Branch:** `main`
**Remote:** `origin`

## How to Use the Scrapers

### Option 1: Ultra-Fast API Spider (RECOMMENDED) ⚡

```bash
cd ~/Documents/NeuraList/scraper
source venv/bin/activate

# Scrape 100 products
scrapy crawl mercadona_api -s CLOSESPIDER_ITEMCOUNT=100

# Scrape 1000 products
scrapy crawl mercadona_api -s CLOSESPIDER_ITEMCOUNT=1000

# Override settings for maximum speed
scrapy crawl mercadona_api \
  -s CLOSESPIDER_ITEMCOUNT=500 \
  -s CONCURRENT_REQUESTS=20 \
  -s CONCURRENT_REQUESTS_PER_DOMAIN=20 \
  -s DOWNLOAD_DELAY=0.1 \
  -s AUTOTHROTTLE_ENABLED=False
```

**How it works:**
1. Fetches sitemap.xml to get all product URLs
2. Extracts product IDs from URLs
3. Makes parallel API calls to get product data
4. Saves to SQLite database

### Option 2: Parallel Selenium Spider (Backup) 🔄

```bash
cd ~/Documents/NeuraList/scraper
source venv/bin/activate

scrapy crawl mercadona_parallel -s CLOSESPIDER_ITEMCOUNT=50
```

**Use when:** API access is blocked or changed

### Option 3: Direct API Testing 🧪

```bash
cd ~/Documents/NeuraList/scraper
source venv/bin/activate

# Test API with 20 hardcoded product IDs
python3 test_api.py

# Quick API test with curl
curl "https://tienda.mercadona.es/api/v1_1/products/10005"
```

## Known Issues & Solutions

### Issue 1: Global Scrapy Settings Too Restrictive

**Problem:** Settings in `config/settings.py` have low concurrency limits:
```python
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
AUTOTHROTTLE_ENABLED = True
```

**Solution:** Override with command-line arguments (shown above)

### Issue 2: EAN Codes Not Always Available

**Problem:** Many Mercadona products don't have EAN codes in API response

**Solution:**
- Made `ean` field nullable in database
- Pipeline converts empty strings to `None`
- Use `product_id` as primary identifier

### Issue 3: Sitemap Parsing Slow

**Problem:** Mercadona's sitemap is very large (thousands of products)

**Solution:**
- Sitemap parsing happens once at start
- Uses Scrapy's built-in sitemap parser (optimized)
- After parsing, requests are concurrent and fast

## Background Processes

When sessions are interrupted, these processes might still be running:

```bash
# Check for running scrapers
ps aux | grep scrapy

# Kill all scrapy processes
pkill -9 -f "scrapy crawl"

# Check for running Python scripts
ps aux | grep python3

# Check background shells (from Claude)
# These are listed in system reminders
```

## Next Steps & Priorities

### Immediate (Scraper)
1. ✅ Commit API spider to GitHub - DONE!
2. ⏳ Run full scrape of Mercadona products (1000-5000 products)
3. Verify data quality in database
4. Export sample products for app development

### Short-term (App Development)
1. Design Flutter app UI/UX
2. Implement camera functionality
3. Integrate OCR/AI for text extraction (Tesseract, Google Vision, or OpenAI)
4. Build product matching algorithm
5. Connect app to product database

### Long-term (Features)
1. Shopping list management
2. Price tracking and history
3. Recipe suggestions based on purchased items
4. Nutrition information display
5. Alternative product recommendations
6. Multi-store support (beyond Mercadona)

## Important Files to Review

When starting a new session, review these files:

1. **scraper/spiders/mercadona_api_spider.py** - Main scraper implementation
2. **scraper/models/product.py** - Database schema
3. **scraper/pipelines.py** - Data processing logic
4. **scraper/config/settings.py** - Global Scrapy configuration
5. **lib/main.dart** - Flutter app entry point (when we start building)

## Dependencies

### Python (scraper/)
- scrapy==2.13.3
- selenium==4.27.2
- sqlalchemy==2.0.39
- loguru==0.7.3
- python-dotenv==1.0.1
- webdriver-manager==4.0.2
- requests (for API testing)

### Flutter
- SDK: 3.29.1
- Dart: 3.8.2
- iOS Deployment Target: 13.0+

## Environment Variables

Create `scraper/.env` file if needed:

```env
# Optional overrides
CONCURRENT_REQUESTS=20
DOWNLOAD_DELAY=0.1
AUTOTHROTTLE_ENABLED=False
DATABASE_URL=sqlite:///data/products.db
USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
```

## Testing the Setup

Quick verification commands:

```bash
# Test Flutter
cd ~/Documents/NeuraList
flutter doctor
flutter test

# Test scraper
cd ~/Documents/NeuraList/scraper
source venv/bin/activate
python3 -c "from spiders.mercadona_api_spider import MercadonaAPISpider; print('✅ Spider loads OK')"

# Test database
sqlite3 scraper/data/products.db "SELECT COUNT(*) FROM products;"

# Test API
curl -s "https://tienda.mercadona.es/api/v1_1/products/10005" | grep -o '"display_name":"[^"]*"'
```

## Tips for Claude in Next Session

1. **Start with context check:**
   - Read this file first
   - Check what's in the database: `cd scraper && source venv/bin/activate && python3 check_db.py`
   - Check git status: `git status`

2. **For scraping:**
   - Use `mercadona_api_spider.py` (it's 50x faster!)
   - Check if any background processes are still running
   - Use command-line setting overrides for max speed

3. **For app development:**
   - Start with simple Flutter UI mockup
   - Focus on camera + list display first
   - AI/OCR integration can come later

4. **For debugging:**
   - Scrapy logs are in `scraper/` directory
   - Database is at `scraper/data/products.db`
   - Check `.scrapy/httpcache` for cached responses

## Contact & Resources

- **GitHub:** https://github.com/albertorblan06/NeuraList
- **Mercadona Website:** https://tienda.mercadona.es
- **Mercadona API:** https://tienda.mercadona.es/api/v1_1/products/{id}
- **Flutter Docs:** https://docs.flutter.dev
- **Scrapy Docs:** https://docs.scrapy.org

---

**Last Updated:** 2025-11-06
**Session:** Claude Code session after API discovery breakthrough
**Status:** ✅ API scraper committed, ready for full product scrape
