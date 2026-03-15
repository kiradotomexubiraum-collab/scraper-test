from playwright.sync_api import sync_playwright
import re
import json

def scrape_festval():
    url = "https://superfestval.com.br/ofertas"
    products = []

    with sync_playwright() as p:
        # headless=False helps you see if it's actually scrolling/loading
        browser = p.chromium.launch(headless=True) 
        page = browser.new_page()
        
        print("Opening Festval...")
        page.goto(url, wait_until="networkidle")

        # 1. Wait for the product grid to load
        # Festval usually uses tags like 'article' or classes like '.product-item'
        try:
            page.wait_for_selector(".product-item, .product-card", timeout=10000)
        except:
            print("Timeout: Product elements not found. The site might have changed its layout.")
            browser.close()
            return

        # 2. Scroll to load lazy-loaded items
        for _ in range(3):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)

        # 3. Target the specific elements
        # Note: If this fails, inspect the site and check the current class names
        items = page.query_selector_all(".product-item, .product-card")
        
        for item in items:
            try:
                # Select the name and price inside the card
                name_el = item.query_selector(".product-name, h3, .name")
                price_el = item.query_selector(".product-price, .price, .value")
                
                if name_el and price_el:
                    name = name_el.inner_text().strip()
                    price_raw = price_el.inner_text()
                    
                    # Regex to extract only numbers and decimal
                    price_clean = re.sub(r"[^0-9,]", "", price_raw).replace(",", ".")
                    
                    if price_clean:
                        products.append({
                            "store": "Festval",
                            "name": name,
                            "price": float(price_clean)
                        })
            except Exception as e:
                continue

        browser.close()

    # --- SAVE LOGIC ---
    if products:
        try:
            with open("products.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
        except:
            existing = []

        # Remove old Festval entries so you don't have duplicates
        existing = [p for p in existing if p.get("store") != "Festval"]
        existing.extend(products)

        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        print(f"Success! Added {len(products)} Festval products to JSON.")
    else:
        print("No products found. Check if the website layout changed.")

scrape_festval()
