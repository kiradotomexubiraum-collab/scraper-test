from playwright.sync_api import sync_playwright
import json

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
                products.append({
                    "store": "Irani",
                    "name": current_name,
                    "price": float(line.replace("R$", "").replace(",", ".").strip())
                })

        else:
            if len(line) > 3 and "OFF" not in line and "Add" not in line:
                current_name = line

    browser.close()

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print("Saved products.json")
