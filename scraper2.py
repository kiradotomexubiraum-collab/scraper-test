from playwright.sync_api import sync_playwright
import json
import re

url = "https://muffataosupermercado.instabuy.com.br"

products = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url)
    page.wait_for_timeout(7000)

    text = page.inner_text("body")
    lines = text.split("\n")

    current_name = None
    price_found = False

    for line in lines:

        line = line.strip()

        if "R$" in line and current_name and not price_found:

            price_text = re.sub(r"[^0-9,]", "", line)

            if price_text:
                price = float(price_text.replace(",", "."))

                products.append({
                    "store": "Muffatao",
                    "name": current_name,
                    "price": price
                })

                price_found = True

        elif (
            len(line) > 3
            and "R$" not in line
            and "Add" not in line
            and "OFF" not in line
        ):
            current_name = line
            price_found = False


    browser.close()


# append to existing JSON
try:
    with open("products.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except:
    existing = []

existing.extend(products)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)


print("Muffatao products added")
