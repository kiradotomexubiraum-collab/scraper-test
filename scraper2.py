from playwright.sync_api import sync_playwright
import re
import json

def scrape_festval():
    url = "https://superfestval.com.br/ofertas"
    products = []

    with sync_playwright() as p:
        # We use a real User-Agent so the site doesn't block us as a bot
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Opening Festval... (this may take a few seconds)")
        try:
            # wait_until="networkidle" is key for Festval
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Festval uses 'div.product-card' or 'article' for its items
            # We wait for the price tag specifically, as it's the last thing to load
            page.wait_for_selector(".product-price", timeout=20000)
            
            print("Page loaded! Scrolling to capture all offers...")
            for _ in range(4):
                page.mouse.wheel(0, 1500)
                page.wait_for_timeout(1500)

            # Target the product containers
            # Festval often uses 'div.product-card'
            items = page.query_selector_all(".product-card, .product-item")
            
            for item in items:
                try:
                    name = item.query_selector(".product-name").inner_text().strip()
                    price_raw = item.query_selector(".product-price").inner_text()
                    
                    # Cleans "R$ 10,90" into 10.9
                    price_clean = re.sub(r"[^0-9,]", "", price_raw).replace(",", ".")
                    
                    products.append({
                        "store": "Festval",
                        "name": name,
                        "price": float(price_clean)
                    })
                except:
                    continue

        except Exception as e:
            print(f"Error during scrape: {e}")
        finally:
            browser.close()

    if products:
        save_to_json(products)
    else:
        print("Scraper finished but found 0 products. The site might be blocking the connection or the selectors changed.")

def save_to_json(new_products):
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    # Filter out old Festval data before adding new ones
    data = [p for p in data if p.get("store") != "Festval"]
    data.extend(new_products)

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Success! {len(new_products)} items saved to products.json")

scrape_festval()
