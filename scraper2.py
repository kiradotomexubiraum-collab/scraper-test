from playwright.sync_api import sync_playwright
import re
import json

def scrape_festval():
    url = "https://superfestval.com.br/ofertas"
    products = []

    with sync_playwright() as p:
        # Using a real-looking browser context
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("Opening Festval... waiting for content...")
        try:
            # Increase timeout and wait for the body to at least exist
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Hard wait for 10 seconds to let their slow JS run
            page.wait_for_timeout(10000)

            # Take a screenshot to see what's happening (check this if it fails!)
            page.screenshot(path="debug.png")

            # NEW STRATEGY: Find all elements that look like a price
            # We look for "R$" followed by numbers
            price_elements = page.locator("text=/R\$.*\d/").all()
            
            print(f"Found {len(price_elements)} potential price tags...")

            for price_el in price_elements:
                try:
                    price_raw = price_el.inner_text()
                    # Find the parent container to get the name
                    # Usually the name is in the same 'div' or 'article'
                    container = price_el.locator("xpath=..")
                    
                    # Search for text nearby that isn't the price
                    name = container.inner_text().split('\n')[0] 
                    
                    price_clean = re.sub(r"[^0-9,]", "", price_raw).replace(",", ".")
                    
                    if float(price_clean) > 0:
                        products.append({
                            "store": "Festval",
                            "name": name.strip(),
                            "price": float(price_clean)
                        })
                except:
                    continue

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

    if products:
        # Deduplicate results
        unique_products = {p['name']: p for p in products}.values()
        save_to_json(list(unique_products))
    else:
        print("Still 0 products. Open 'debug.png' to see if the site is blocked.")

def save_to_json(new_products):
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []
    data = [p for p in data if p.get("store") != "Festval"]
    data.extend(new_products)
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Success! {len(new_products)} items saved.")

scrape_festval()
