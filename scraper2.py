from playwright.sync_api import sync_playwright
import json
import re

url = "https://muffataosupermercado.instabuy.com.br"

products = []

# words we should ignore as product names
ignore_words = [
    "ver todos", "ofertas", "categorias", "adicionar",
    "carrinho", "buscar", "menu"
]

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url)
    page.wait_for_timeout(8000)

    # scroll to load more products
    page.mouse.wheel(0, 50000)
    page.wait_for_timeout(3000)

    text = page.inner_text("body")
    lines = text.split("\n")

    current_name = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # ignore UI text
        if any(word in lower for word in ignore_words):
            continue

        # if price line
        if "R$" in line and current_name:

            price_text = re.sub(r"[^0-9,]", "", line)

            if price_text:
                price = float(price_text.replace(",", "."))

                products.append({
                    "store": "Muffatao",
                    "name": current_name,
                    "price": price
                })

                current_name = None

        else:
            # possible product name
            if (
                len(line) > 6
                and "R$" not in line
                and not line.isupper()
            ):
                current_name = line


    browser.close()


# merge with existing JSON
try:
    with open("products.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except:
    existing = []

existing.extend(products)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print("Muffatão products added")
