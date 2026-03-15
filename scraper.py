from playwright.sync_api import sync_playwright
import json
import re

url = "https://irani.delivery/pacaembu/ofertas-clube"
products = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Connecting to Irani...")
    page.goto(url, wait_until="networkidle")

    # FIX 1: Wait for actual content, not just a timer
    # We wait for the product container class (check if '.product-item' is correct)
    try:
        page.wait_for_selector(".product-item, .item-card", timeout=15000)
    except:
        print("Still couldn't find products. The site layout might have changed.")
        browser.close()
        exit()

    # FIX 2: Target the cards individually to avoid mixing up prices
    cards = page.query_selector_all(".product-item, .item-card")
    
    for card in cards:
        card_text = card.inner_text()
        lines = card_text.split("\n")
        
        name = lines[0] # Usually the first line is the name
        
        # Find all prices in this specific card
        prices_found = [line for line in lines if "R$" in line]
        
        if prices_found:
            # If there are two prices, the LAST one is usually the promo/clube price
            price_line = prices_found[-1] 
            
            # Clean price: "R$ 10,90" -> 10.9
            price_numeric = float(re.sub(r"[^0-9,]", "", price_line).replace(",", "."))
            
            products.append({
                "store": "Irani",
                "name": name,
                "price": price_numeric
            })

    browser.close()

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"Success! {len(products)} products saved to products.json")
