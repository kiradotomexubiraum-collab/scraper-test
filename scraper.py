from playwright.sync_api import sync_playwright
import json
import re

url = "https://irani.delivery/pacaembu/ofertas-clube"
products = []

with sync_playwright() as p:
    # Use headless=False to debug and see the browser actually working
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Connecting to Irani...")
    page.goto(url, wait_until="networkidle")

    # 1. WAIT: This prevents the 'Saved 0 products' error
    # It waits until at least one product card is visible on the screen
    try:
        page.wait_for_selector(".product-item, .item-card, [class*='product']", timeout=15000)
    except:
        print("Timeout: No products found. Check if the site is blocked or layout changed.")
        browser.close()
        exit()

    # 2. SELECT: Find all product containers
    cards = page.query_selector_all(".product-item, .item-card, [class*='product-card']")
    
    for card in cards:
        try:
            # Get the Name
            name = card.query_selector(".product-name, .name, h3").inner_text().strip()
            
            # 3. FIX PROMO PRICE: We look for the 'new' price specifically
            # Most sites use a specific class for the discounted price
            price_el = card.query_selector(".price-promotion, .sale-price, .special-price, .clube-price")
            
            # If no promo class is found, it's a regular price
            if not price_el:
                price_el = card.query_selector(".price, .regular-price")

            if price_el:
                price_text = price_el.inner_text()
                # Use regex to find the price (e.g., 10,90)
                match = re.search(r"(\d+,\d+)", price_text)
                if match:
                    price_val = float(match.group(1).replace(",", "."))
                    
                    products.append({
                        "store": "Irani",
                        "name": name,
                        "price": price_val
                    })
        except:
            continue

    browser.close()

# 4. SAVE: Writing the final list to your JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"Success! {len(products)} products saved.")
