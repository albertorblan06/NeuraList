#!/usr/bin/env python3
"""
Quick script to analyze Mercadona product page structure
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def analyze_page(url):
    """Analyze a product page and print useful information"""

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"Loading: {url}")
    driver.get(url)

    # Wait for page to load
    time.sleep(5)

    print("\n=== Page Title ===")
    print(driver.title)

    print("\n=== All Text Content ===")
    body = driver.find_element(By.TAG_NAME, "body")
    print(body.text[:2000])  # First 2000 chars

    print("\n=== Looking for specific elements ===")

    # Try to find price elements
    print("\nSearching for price-related elements...")
    try:
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), '€')]")
        for i, elem in enumerate(elements[:10]):
            print(f"Price element {i}: {elem.text} - Tag: {elem.tag_name} - Class: {elem.get_attribute('class')}")
    except:
        print("No price elements found")

    # Try to find images
    print("\nSearching for images...")
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        for i, img in enumerate(images[:5]):
            src = img.get_attribute('src')
            alt = img.get_attribute('alt')
            print(f"Image {i}: {alt} - {src[:100]}")
    except:
        print("No images found")

    # Look for JSON-LD data
    print("\nSearching for structured data...")
    try:
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            content = script.get_attribute('innerHTML')
            if content and 'application/ld+json' in driver.page_source:
                print("Found structured data!")
                # Try to find it in page source
                import re
                matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', driver.page_source, re.DOTALL)
                if matches:
                    for match in matches:
                        try:
                            data = json.loads(match)
                            print(json.dumps(data, indent=2))
                        except:
                            pass
    except:
        print("No structured data found")

    # Save full page source
    print("\n=== Saving page source ===")
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source saved to page_source.html")

    driver.quit()

if __name__ == '__main__':
    url = "https://tienda.mercadona.es/product/10005/chocolate-liquido-taza-hacendado-brick"
    analyze_page(url)
