from playwright.sync_api import sync_playwright
import re
import json

url = "https://superfestval.com.br/ofertas"

products = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url)
    page.wait_for_timeout(6000)

    text = page.inner_text("body")
    lines = text.split("\n")

    current_name = None

    for line in lines:

        if "R$" in line:
            if current_name:

                price = float(
                    re.sub(r"[^0-9.,]", "", line).replace(",", ".")
                )

                products.append({
                    "store": "Festval",
                    "name": current_name,
                    "price": price
                })

        else:
            if len(line) > 3 and "OFF" not in line:
                current_name = line

    browser.close()


# APPEND TO EXISTING JSON
try:
    with open("products.json","r",encoding="utf-8") as f:
        existing = json.load(f)
except:
    existing = []

existing.extend(products)

with open("products.json","w",encoding="utf-8") as f:
    json.dump(existing,f,ensure_ascii=False,indent=2)

print("Festval products added")
