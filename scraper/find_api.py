from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

print("Loading product page...")
driver.get("https://tienda.mercadona.es/product/10005/chocolate-liquido-taza-hacendado-brick")
time.sleep(5)

print("\nAnalyzing network requests...")
logs = driver.get_log('performance')

api_calls = []
for log in logs:
    message = json.loads(log['message'])
    method = message.get('message', {}).get('method', '')
    
    if 'Network.responseReceived' in method:
        response = message['message']['params']['response']
        url = response.get('url', '')
        
        # Look for API calls
        if '/api/' in url or 'product' in url.lower():
            api_calls.append({
                'url': url,
                'status': response.get('status'),
                'type': response.get('mimeType', '')
            })

print(f"\nFound {len(api_calls)} potential API calls:")
for call in api_calls[:10]:
    print(f"  - {call['url']}")
    print(f"    Status: {call['status']}, Type: {call['type']}")

driver.quit()
