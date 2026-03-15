from playwright.sync_api import sync_playwright
import json
import re

url = "https://irani.delivery/pacaembu/ofertas-clube"

products = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(5000)
    text = page.inner_text("body")
    lines = text.split("\n")
    current_name = None
    for line in lines:
        if "R$" in line:
            if current_name:
                price = float(re.sub(r"[^0-9.,]", "", line).replace(",", "."))
                products.append({
                    "store": "Irani",
                    "name": current_name,
                    "price": price
                })
        else:
            if len(line) > 3 and "OFF" not in line and "Add" not in line:
                current_name = line
    browser.close()
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print("Saved products.json")
