from playwright.sync_api import sync_playwright
import json
import re

url = "https://irani.delivery/pacaembu/ofertas-clube"
products = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    # Wait for the products to actually load
    page.wait_for_selector(".product-item, [class*='product']", timeout=10000)
    
    # Get all product "cards"
    cards = page.query_selector_all(".product-item, [class*='product-card']")

    for card in cards:
        try:
            name = card.query_selector(".product-name, h3, .name").inner_text().strip()
            
            # Look for the PROMO price first. 
            # If it doesn't exist, fall back to the regular price.
            price_el = card.query_selector(".price-promotion, .special-price, .current-price")
            if not price_el:
                price_el = card.query_selector(".price, .regular-price")
            
            if price_el:
                price_raw = price_el.inner_text()
                price = float(re.sub(r"[^0-9,]", "", price_raw).replace(",", "."))

                products.append({
                    "store": "Irani",
                    "name": name,
                    "price": price
                })
        except:
            continue

    browser.close()

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"Saved {len(products)} products to products.json")
